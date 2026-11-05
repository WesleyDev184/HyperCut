#!/usr/bin/env python3
"""Gera compositions/legendas.html a partir de roteiro/legendas.txt e da transcricao da voz final.

Uso, com o Python da pasta:
  .venv/bin/python .claude/skills/legendas-da-voz/scripts/legendas.py <projeto> [opcoes]

Opcoes:
  --transcrever VOZ     transcreve a voz final por trecho de fala e grava roteiro/transcript.json
  --modelo small        modelo do whisper para --transcrever
  --rascunho            cria roteiro/legendas.txt a partir da transcricao (nunca sobrescreve)
  --transcricao ARQ     padrao: roteiro/transcript.json
  --sobrescrever        troca um legendas.html que nao foi gerado por este script

Saida: 0 gerado, 1 regra reprovada (nada gravado), 2 erro de uso.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from difflib import SequenceMatcher
from html import escape
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
MARCA = "<!-- gerado por legendas-da-voz -->"
MIN_BLOCO, CAUDA, CAUDA_FIM, PISCA, INICIO_MIN = 0.45, 0.12, 0.3, 0.15, 0.1
PAUSA = 0.15  # pausa que quebra bloco no rascunho
MIN_TRECHO = 3  # trecho menor que isso casa por acaso
COBERTURA_MIN, COBERTURA_BLOCO = 0.6, 0.5
SILENCIO_DB, SILENCIO_MIN, MARGEM_ILHA = -35, 0.35, 0.1
FFMPEG = os.environ.get("HYPERFRAMES_FFMPEG_PATH") or str(RAIZ / "node_modules/ffmpeg-static/ffmpeg")
FUNDO, TEXTO, DESTAQUE = "#14170f", "#edeee3", "#7bb289"
FONTE = "assets/fonts/public-sans.woff2"
CABECALHO = """# Um bloco por linha, de 1 a 3 palavras. *palavra* sai em destaque.
# Depois de " | " vai o que a voz diz, quando difere da tela: *R$ 320* | trezentos e vinte reais
# Linha com ~ no começo conta o tempo, mas não aparece: use onde o título já está na tela.
"""
# Artigos, preposicoes e conjuncoes: nunca recebem destaque (PRODUCAO.md).
FRACAS = set("""o a os as um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas
para pra pro com sem sob sobre ate entre ao aos num numa e ou mas que se porque como quando nem pois""".split())


def erro(msg):
    print(f"erro: {msg}", file=sys.stderr)
    sys.exit(2)


def normal(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in t if not unicodedata.combining(c)))


def impressao(arquivo):
    return hashlib.md5(Path(arquivo).read_bytes()).hexdigest()


def ilhas_de_fala(voz):
    """Trechos entre silencios. O whisper chuta tempo em pausa longa: em um video real errou ate 4 s no arquivo inteiro."""
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(voz), "-af",
                        f"silencedetect=noise={SILENCIO_DB}dB:d={SILENCIO_MIN}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    h, m, seg = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r).groups()
    duracao = int(h) * 3600 + int(m) * 60 + float(seg)
    inicios = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    ilhas, pos = [], 0.0
    for a, b in zip(inicios, fins + [duracao]):
        if a > pos:
            ilhas.append((pos, a))
        pos = b
    if pos < duracao:
        ilhas.append((pos, duracao))
    return ilhas, duracao


def transcreve(projeto, voz, modelo):
    ilhas, duracao = ilhas_de_fala(voz)
    if not ilhas:
        erro(f"nenhuma fala em {voz}")
    palavras = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (a, b) in enumerate(ilhas):
            a2, b2 = max(a - MARGEM_ILHA, 0), min(b + MARGEM_ILHA, duracao)
            trecho = f"{tmp}/ilha{i}.wav"
            subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(a2), "-to", str(b2), "-i", str(voz),
                            "-ac", "1", "-ar", "16000", trecho], check=True)
            q = subprocess.run([str(RAIZ / "bin/hf"), "transcribe", trecho, "-d", tmp, "--model", modelo, "--language", "pt",
                                "--no-runtime-install", "--json"], capture_output=True, text=True)
            if q.returncode:
                erro(f"transcricao falhou no trecho {a:.2f}-{b:.2f}: {q.stderr[-300:]}")
            caminho = json.loads(q.stdout[q.stdout.rfind('{"ok"'):])["transcriptPath"]
            for w in json.loads(Path(caminho).read_text()):
                palavras.append({"text": w["text"], "start": round(w["start"] + a2, 3), "end": round(w["end"] + a2, 3)})
    saida = projeto / "roteiro/transcript.json"
    saida.write_text(json.dumps({"voz": str(voz.relative_to(projeto)) if voz.is_relative_to(projeto) else str(voz),
                                 "md5": impressao(voz), "ilhas": [[round(a, 3), round(b, 3)] for a, b in ilhas], "words": palavras},
                                ensure_ascii=False, indent=1))
    print(f"{len(palavras)} palavras em {len(ilhas)} trechos de fala: roteiro/transcript.json")
    print(" ".join(w["text"] for w in palavras))


def prende_nas_ilhas(blocos, ilhas):
    """Bloco estimado por interpolacao pode cair no silencio: traz de volta para a fala."""
    for b in blocos:
        if not any(a - MARGEM_ILHA <= b["inicio"] <= z + MARGEM_ILHA for a, z in ilhas):
            b["inicio"] = next((a for a, _ in ilhas if a > b["inicio"]), b["inicio"])
        if not any(a - MARGEM_ILHA <= b["fim"] <= z + MARGEM_ILHA for a, z in ilhas):
            b["fim"] = next((z for _, z in reversed(ilhas) if z < b["fim"]), b["fim"])
        b["fim"] = max(b["fim"], b["inicio"])


def le_transcricao(arquivo):
    if not arquivo.exists():
        erro(f"sem transcricao em {arquivo}. Transcreva a voz final: veja a skill")
    d = json.loads(arquivo.read_text())
    palavras = d if isinstance(d, list) else d.get("words", [])
    palavras = [w for w in palavras if normal(w.get("text", ""))]
    if not palavras:
        erro(f"transcricao sem palavras: {arquivo}")
    return palavras, ({} if isinstance(d, list) else d)


def le_blocos(arquivo):
    blocos = []
    for n, linha in enumerate(arquivo.read_text().splitlines(), 1):
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        oculto = linha.startswith("~")
        tela, _, falado = linha.lstrip("~ ").partition(" | ")
        tela = tela.strip()
        blocos.append({"linha": n, "tela": tela, "falado": falado.strip() or tela.replace("*", ""), "oculto": oculto})
    if not blocos:
        erro(f"nenhum bloco em {arquivo}")
    return blocos


def alinha(blocos, palavras):
    """Casa letra a letra: aguenta palavra juntada ou separada pelo reconhecedor e numero por extenso."""
    letras, ini, fim = [], [], []
    for w in palavras:
        n = normal(w["text"])
        d = (w["end"] - w["start"]) / len(n)
        for k, c in enumerate(n):
            letras.append(c)
            ini.append(w["start"] + d * k)
            fim.append(w["start"] + d * (k + 1))
    ini, fim = np.array(ini), np.array(fim)
    alvo = "".join(letras)

    texto, faixas = "", []
    for b in blocos:
        n = normal(b["falado"])
        faixas.append((len(texto), len(texto) + len(n)))
        texto += n

    casou = np.zeros(len(texto), bool)
    t_ini, t_fim = np.zeros(len(texto)), np.zeros(len(texto))
    for m in SequenceMatcher(None, texto, alvo, autojunk=False).get_matching_blocks():
        if m.size >= MIN_TRECHO:
            casou[m.a:m.a + m.size] = True
            t_ini[m.a:m.a + m.size] = ini[m.b:m.b + m.size]
            t_fim[m.a:m.a + m.size] = fim[m.b:m.b + m.size]
    if not casou.any():
        return 0.0
    eixo, xp = np.arange(len(texto)), np.flatnonzero(casou)
    t_ini = np.interp(eixo, xp, t_ini[xp])
    t_fim = np.interp(eixo, xp, t_fim[xp])
    for b, (a, z) in zip(blocos, faixas):
        if a == z:
            erro(f"linha {b['linha']}: bloco sem letras faladas: {b['tela']}")
        b["inicio"], b["fim"] = float(t_ini[a]), float(t_fim[z - 1])
        b["cobertura"] = float(casou[a:z].mean())
    return float(casou.mean())


def ajusta(visiveis, total):
    """Um bloco por vez, sem piscar entre blocos colados."""
    for i, b in enumerate(visiveis):
        b["inicio"] = max(b["inicio"], INICIO_MIN)
        prox = visiveis[i + 1]["inicio"] if i + 1 < len(visiveis) else None
        b["fim"] = max(b["fim"] + CAUDA, b["inicio"] + MIN_BLOCO)
        if prox is None:
            b["fim"] = min(b["fim"] + CAUDA_FIM, total)
        elif prox - b["fim"] < PISCA:
            b["fim"] = prox


def palavras_tela(tela):
    return tela.replace("*", "").split()


def confere(visiveis, vertical):
    """Regras do PRODUCAO.md. As da secao de video vertical sao aviso nos outros formatos."""
    reprovas, avisos = [], []
    regra = reprovas if vertical else avisos
    ultimo = None
    for i, b in enumerate(visiveis):
        n = len(palavras_tela(b["tela"]))
        if n > 3:
            regra.append(f"linha {b['linha']}: {n} palavras em \"{b['tela']}\". Máximo: 3.")
        marcados = re.findall(r"\*(.+?)\*", b["tela"])
        if not marcados:
            continue
        ditas = [p for m in marcados for p in m.split()]
        if len(ditas) > 2:
            regra.append(f"linha {b['linha']}: {len(ditas)} palavras em destaque. Máximo: 2.")
        for p in ditas:
            if normal(p) in FRACAS:
                regra.append(f"linha {b['linha']}: destaque em palavra fraca: {p}.")
        if ultimo is not None:
            if i - ultimo == 1:
                regra.append(f"linha {b['linha']}: destaque em blocos seguidos.")
            elif i - ultimo > 3:
                avisos.append(f"linha {b['linha']}: {i - ultimo - 1} blocos sem destaque antes deste.")
        ultimo = i
    for b in visiveis:
        if b["cobertura"] < COBERTURA_BLOCO:
            avisos.append(f"linha {b['linha']}: \"{b['tela']}\" casou só {b['cobertura']:.0%} com a voz. "
                          "Tempo estimado: confira no snapshot. Se a fala difere da tela, use \" | \".")
    for b in visiveis:
        if b["fim"] - b["inicio"] < 0.3:
            avisos.append(f"linha {b['linha']}: \"{b['tela']}\" fica só {b['fim'] - b['inicio']:.2f} s na tela.")
    return reprovas, avisos


def rascunho(palavras):
    """Agrupa por pausa, pontuacao e limite de 3 palavras, sem terminar bloco em palavra fraca."""
    grupos, atual = [], []
    for i, w in enumerate(palavras):
        atual.append(w)
        fim_frase = re.search(r"[.,;:!?…]$", w["text"])
        pausa = i + 1 < len(palavras) and palavras[i + 1]["start"] - w["end"] >= PAUSA
        if fim_frase or pausa or len(atual) == 3:
            sobra = []
            while not (fim_frase or pausa) and len(atual) > 1 and normal(atual[-1]["text"]) in FRACAS:
                sobra.insert(0, atual.pop())
            grupos.append(atual)
            atual = sobra
    if atual:
        grupos.append(atual)

    linhas, desde = [], 3
    for g in grupos:
        textos = [re.sub(r"[.,;:!?…]+$", "", w["text"]) for w in g]
        fortes = [t for t in textos if normal(t) not in FRACAS and len(normal(t)) >= 4]
        desde += 1
        if fortes and desde >= 3:
            alvo = max(fortes, key=len)
            textos[textos.index(alvo)] = f"*{alvo}*"
            desde = 0
        linhas.append(" ".join(textos))
    return linhas


def html(visiveis, largura, altura, total, css_extra, fonte):
    vertical = altura > largura
    tamanho = 62 if vertical else 48
    lugar = "top: 1400px" if vertical else "bottom: 56px"
    clipes, passos = [], []
    for i, b in enumerate(visiveis):
        txt = re.sub(r"\*(.+?)\*", r"<b>\1</b>", escape(b["tela"]))
        clipes.append(f'    <div id="lg{i}" class="clip lg" data-start="{b["inicio"]:.2f}" '
                      f'data-duration="{b["fim"] - b["inicio"]:.2f}" data-track-index="{i % 2}">'
                      f'<span id="lgs{i}">{txt}</span></div>')
        passos.append(f'      tl.fromTo("#lgs{i}", {{ scale: 0.9 }}, '
                      f'{{ scale: 1, duration: 0.12, ease: "back.out(2)" }}, {b["inicio"]:.2f});')
    face = f'@font-face {{ font-family: "Public Sans"; src: url("{FONTE}") format("woff2"); font-weight: 100 900; }}' if fonte else ""
    quebra = "\n"
    return f"""{MARCA}
<template>
  <div id="root" data-composition-id="legendas" data-start="0" data-duration="{total}" data-width="{largura}" data-height="{altura}">
    <style>
      {face}
      #root {{ position: relative; width: {largura}px; height: {altura}px; overflow: hidden; pointer-events: none; }}
      .lg {{ position: absolute; left: 0; right: 0; {lugar}; text-align: center; overflow: visible; }}
      .lg span {{ display: inline-block; padding: 12px 30px 14px; border-radius: 14px; background: {FUNDO}; color: {TEXTO};
        font: 800 {tamanho}px/1.15 "Public Sans", sans-serif; }}
      .lg b {{ color: {DESTAQUE}; font-weight: 800; }}
{css_extra}    </style>
{quebra.join(clipes)}
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{quebra.join(passos)}
      window.__timelines["legendas"] = tl;
    </script>
  </div>
</template>
"""


def main():
    ap = argparse.ArgumentParser(description="Gera legendas da voz final")
    ap.add_argument("projeto")
    ap.add_argument("--transcrever")
    ap.add_argument("--modelo", default="small")
    ap.add_argument("--rascunho", action="store_true")
    ap.add_argument("--transcricao", default="roteiro/transcript.json")
    ap.add_argument("--sobrescrever", action="store_true")
    a = ap.parse_args()

    projeto = Path(a.projeto) if Path(a.projeto).is_dir() else RAIZ / "projetos" / a.projeto
    projeto = projeto.resolve()
    if not projeto.is_dir():
        erro(f"projeto nao existe: {a.projeto}")
    if a.transcrever:
        voz = Path(a.transcrever) if Path(a.transcrever).is_absolute() else projeto / a.transcrever
        if not voz.exists():
            erro(f"voz nao existe: {voz}")
        transcreve(projeto, voz, a.modelo)
        return
    palavras, dados = le_transcricao(projeto / a.transcricao)
    ilhas = dados.get("ilhas", [])
    arquivo = projeto / "roteiro/legendas.txt"

    if a.rascunho:
        if arquivo.exists():
            erro(f"{arquivo} ja existe e pode ter revisao manual. Apague antes se quiser refazer")
        linhas = rascunho(palavras)
        arquivo.write_text(CABECALHO + "\n".join(linhas) + "\n")
        print(f"{len(linhas)} blocos em roteiro/legendas.txt. Corrija a grafia pelo roteiro antes de gerar.")
        return
    if not arquivo.exists():
        erro("sem roteiro/legendas.txt. Rode com --rascunho ou escreva o arquivo")

    r = subprocess.run([str(RAIZ / "bin/hf"), "info", "--json"], cwd=projeto, capture_output=True, text=True)
    if r.returncode:
        erro(f"hf info falhou: {r.stderr[-300:]}")
    info = json.loads(r.stdout[r.stdout.find("{"):])
    largura, altura, total = info["width"], info["height"], info["duration"]

    blocos = le_blocos(arquivo)
    cobertura = alinha(blocos, palavras)
    # O whisper escreve numero em digitos: quem casa mal pelo texto falado tenta o texto da tela.
    trocados = [b for b in blocos if b["cobertura"] < COBERTURA_BLOCO and normal(b["tela"]) != normal(b["falado"])]
    if trocados:
        guardados = [b["falado"] for b in trocados]
        for b in trocados:
            b["falado"] = b["tela"].replace("*", "")
        nova = alinha(blocos, palavras)
        if nova > cobertura:
            cobertura = nova
        else:
            for b, f in zip(trocados, guardados):
                b["falado"] = f
            alinha(blocos, palavras)
    if cobertura < COBERTURA_MIN:
        print(f"REPROVA: só {cobertura:.0%} do texto casou com a transcrição. Voz errada, ou o modelo traduziu: "
              "transcreva com --model small --language pt ou maior. Nada gravado.")
        sys.exit(1)
    prende_nas_ilhas(blocos, ilhas)
    visiveis = [b for b in blocos if not b["oculto"]]
    ajusta(visiveis, total)
    reprovas, avisos = confere(visiveis, altura > largura)
    voz = projeto / dados.get("voz", "")
    if dados.get("md5") and voz.is_file() and impressao(voz) != dados["md5"]:
        avisos.append(f"{dados['voz']} mudou depois da transcrição: os tempos são da voz antiga. Refaça --transcrever.")
    if not ilhas:
        avisos.append("Transcrição sem trechos de fala: em voz com pausas longas os tempos erram. Use --transcrever.")

    fonte = (projeto / FONTE).exists()
    if not fonte:
        avisos.append(f"Sem {FONTE}: a legenda vai usar a fonte padrão do sistema.")
    host = projeto / "index.html"
    if host.exists() and "compositions/legendas.html" not in host.read_text():
        avisos.append("index.html ainda não monta a legenda. Acrescente: "
                      f'<div id="legendas" class="clip" data-composition-id="legendas" data-composition-src="compositions/legendas.html" '
                      f'data-start="0" data-duration="{total}" data-track-index="11" data-track-kind="captions" '
                      f'data-width="{largura}" data-height="{altura}" style="z-index:11"></div>')

    saida = projeto / "compositions/legendas.html"
    print(f"{len(visiveis)} blocos na tela, {len(blocos) - len(visiveis)} ocultos, {cobertura:.0%} do texto casou com a voz")
    for x in reprovas:
        print(f"REPROVA: {x}")
    for x in avisos:
        print(f"AVISO: {x}")
    if reprovas:
        print("Nada gravado.")
        sys.exit(1)
    if saida.exists() and MARCA not in saida.read_text() and not a.sobrescrever:
        erro(f"{saida} nao veio deste script. Confira o que ele tem de proprio e use --sobrescrever")
    extra = projeto / "roteiro/legendas.css"
    css = extra.read_text() if extra.exists() else ""
    saida.parent.mkdir(exist_ok=True)
    saida.write_text(html(visiveis, largura, altura, total, css, fonte))
    print(f"gravado: {saida.relative_to(projeto)}")


if __name__ == "__main__":
    main()
