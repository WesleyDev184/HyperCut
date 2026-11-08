#!/usr/bin/env python3
"""Mede voz, trilha, efeitos e master de um video e compara com o PRODUCAO.md.

Uso, com o Python da pasta:
  .venv/bin/python .claude/skills/medir-mixagem/scripts/medir.py <projeto> [opcoes]

Opcoes:
  --video renders/x.mp4         arquivo a medir (padrao: renders/<projeto>.mp4 ou o mais novo)
  --faixa voz=caminho[@volume]  faixa manual, repetivel (voz, trilha, efeitos). Substitui a timeline
  --atualizar-review            grava a tabela em "## Audio medido" do REVIEW.md
  --json                        saida em JSON

Saida: 0 aprovado, 1 reprovado, 2 erro de uso ou de ferramenta. So mede: nunca altera audio.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[4]
SR = 48000
ALVO_MASTER, TOL_MASTER = -14.0, 0.3
TETO_DBTP = -1.0
ALVO_VOZ, TOL_VOZ = -14.0, 1.0  # a voz pode subir para o master fechar em -14: quem manda e o master
GAP_TRILHA, GAP_TRILHA_REEL = 9.0, 13.0  # tabela: cerca de 10 LU; em reel, pelo menos 13
PICO_EFEITO_MIN = 9.0  # passagem e a classe mais forte da tabela
TOL_EFEITO = 1.0
TOL_SOMA = 0.5
TOL_DURACAO = 0.05
SILENCIO_FIM_DB, SILENCIO_FIM_S = -50, 0.5
SILENCIO = -69.0

RE_VOZ = re.compile(r"voz|narra|voice|locu", re.I)
RE_TRILHA = re.compile(r"trilha|music|bgm", re.I)
CLASSES_EFEITO = [
    (re.compile(r"riser", re.I), 14),
    (re.compile(r"tecla|keystroke|typing", re.I), 16),
    (re.compile(r"passagem|whoosh|swish", re.I), 9),
]
ROTULOS = {"voz": "Voz", "trilha": "Trilha", "efeitos": "Efeitos"}


def ferramenta(var, relativo):
    return os.environ.get(var) or str(RAIZ / relativo)


FFMPEG = ferramenta("HYPERFRAMES_FFMPEG_PATH", "node_modules/ffmpeg-static/ffmpeg")
FFPROBE = ferramenta("HYPERFRAMES_FFPROBE_PATH", "node_modules/ffprobe-static/bin/linux/x64/ffprobe")


def erro(msg):
    print(f"erro: {msg}", file=sys.stderr)
    sys.exit(2)


def num(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",").replace("-", "\u2212")


def sonda(caminho):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=codec_type,channels",
                        "-of", "json", str(caminho)], capture_output=True, text=True)
    if r.returncode:
        erro(f"ffprobe falhou em {caminho}: {r.stderr.strip()}")
    d = json.loads(r.stdout)
    audio = [s for s in d.get("streams", []) if s.get("codec_type") == "audio"]
    return {"duracao": float(d["format"].get("duration", 0)), "canais": audio[0].get("channels", 0) if audio else 0}


def loudness(caminho):
    """LUFS integrado e pico verdadeiro pelo ebur128, como pede o PRODUCAO.md."""
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(caminho), "-map", "a:0",
                        "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"], capture_output=True, text=True)
    resumo = r.stderr.rsplit("Summary:", 1)[-1]
    i = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", resumo)
    p = re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", resumo)
    if not i or not p:
        erro(f"ebur128 sem resultado em {caminho}: {r.stderr[-300:]}")
    return {"lufs": max(float(i.group(1)), -70.0), "pico": max(float(p.group(1)), -120.0)}


def silencio_no_fim(caminho, duracao):
    r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(caminho), "-map", "a:0", "-af",
                        f"silencedetect=noise={SILENCIO_FIM_DB}dB:d={SILENCIO_FIM_S}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    inicios = re.findall(r"silence_start: ([\d.]+)", r)
    fins = re.findall(r"silence_end: ([\d.]+)", r)
    if not inicios:
        return 0.0
    inicio = float(inicios[-1])
    # Sem silence_end, ou com ele colado no fim, o silencio chega ao ultimo quadro.
    if len(fins) < len(inicios) or float(fins[-1]) >= duracao - 0.05:
        return duracao - inicio
    return 0.0


def amostras(caminho):
    r = subprocess.run([FFMPEG, "-v", "error", "-i", str(caminho), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                       capture_output=True)
    if r.returncode:
        erro(f"nao li {caminho}: {r.stderr.decode()[-300:]}")
    return np.abs(np.frombuffer(r.stdout, "<f4")).reshape(-1, 2).max(1)


def db(x):
    return 20 * np.log10(max(float(x), 1e-6))


def classe(texto):
    if RE_VOZ.search(texto):
        return "voz"
    if RE_TRILHA.search(texto):
        return "trilha"
    return "efeitos"


def clipes_da_timeline(projeto):
    r = subprocess.run([str(RAIZ / "bin/hf"), "timeline", "--json"], cwd=projeto, capture_output=True, text=True)
    if r.returncode:
        return None, []
    linha = r.stdout[r.stdout.find("{"):]
    t = json.loads(linha)["timeline"]
    clipes = []
    for trilho in t["tracks"]:
        for row in trilho.get("rows", []):
            if row.get("kind") != "audio":
                continue
            clipes.append({
                "id": row.get("id") or row["src"], "classe": classe(f"{row.get('id')} {row['src']}"),
                "arquivo": projeto / row["src"], "inicio": float(row.get("absStart") or 0),
                "duracao": float(row.get("duration") or 0), "midia": float(row.get("mediaStart") or 0),
                "volume": 1.0 if row.get("volume") is None else float(row["volume"]),
                "velocidade": float(row.get("playbackRate") or 1),
            })
    return float(t["duration"]), clipes


def clipes_manuais(pares, projeto, total):
    clipes = []
    for par in pares:
        m = re.fullmatch(r"(voz|trilha|efeitos)=(.+?)(?:@([\d.]+))?", par)
        if not m:
            erro(f"--faixa invalida: {par}. Use voz=caminho[@volume]")
        arquivo = Path(m[2]) if Path(m[2]).is_absolute() else projeto / m[2]
        if not arquivo.exists():
            erro(f"faixa nao existe: {arquivo}")
        clipes.append({"id": m[1], "classe": m[1], "arquivo": arquivo, "inicio": 0.0, "duracao": total, "midia": 0.0,
                       "volume": float(m[3] or 1), "velocidade": 1.0})
    return clipes


def monta_faixa(clipes, total, saida):
    """Recria a faixa como o render a toca. Mono vai aos dois canais a 0 dB, igual ao render."""
    args, filtros, rotulos = [], [], []
    for n, c in enumerate(clipes):
        args += ["-i", str(c["arquivo"])]
        canais = sonda(c["arquivo"])["canais"]
        cadeia = [f"atrim=start={c['midia']}:duration={c['duracao'] * c['velocidade']}", "asetpts=PTS-STARTPTS"]
        if c["velocidade"] != 1:
            cadeia.append(f"atempo={c['velocidade']}")
        cadeia += ["pan=stereo|c0=c0|c1=c0" if canais == 1 else "aformat=channel_layouts=stereo",
                   f"aresample={SR}", f"volume={c['volume']}", f"adelay={int(c['inicio'] * 1000)}:all=1"]
        filtros.append(f"[{n}:a]{','.join(cadeia)}[a{n}]")
        rotulos.append(f"[a{n}]")
    junta = f"{''.join(rotulos)}amix=inputs={len(rotulos)}:normalize=0:duration=longest" if len(rotulos) > 1 \
        else f"{rotulos[0]}anull"
    filtros.append(f"{junta},apad=whole_dur={total},atrim=0:{total}[o]")
    subprocess.run([FFMPEG, "-v", "error", "-y", *args, "-filter_complex", ";".join(filtros), "-map", "[o]",
                    "-c:a", "pcm_f32le", str(saida)], check=True)


def soma_faixas(caminhos, saida):
    args = [x for c in caminhos for x in ("-i", str(c))]
    subprocess.run([FFMPEG, "-v", "error", "-y", *args, "-filter_complex",
                    f"amix=inputs={len(caminhos)}:normalize=0:duration=longest", "-c:a", "pcm_f32le", str(saida)], check=True)


def eventos_de_efeito(projeto, clipes):
    """Eventos com o nivel esperado: de roteiro/efeitos.json ou dos clipes soltos."""
    soltos = [c for c in clipes if c["classe"] == "efeitos"]
    if len(soltos) > 1:
        saida = []
        for c in soltos:
            esperado = next((d for r, d in CLASSES_EFEITO if r.search(f"{c['id']} {c['arquivo'].name}")), 10)
            saida.append({"t": c["inicio"], "fim": c["inicio"] + c["duracao"], "nome": c["id"], "esperado": esperado})
        return saida
    lista = projeto / "roteiro/efeitos.json"
    if not lista.exists():
        return []
    saida = []
    for e in json.loads(lista.read_text()):
        t = e.get("tempo", e.get("t"))
        nivel = e.get("abaixo_da_voz_db", e.get("nivel_db"))
        if t is None or nivel is None:
            continue
        saida.append({"t": float(t), "fim": float(t) + float(e.get("duracao", 0.3)), "nome": e.get("som") or e.get("efeito", "?"), "esperado": abs(nivel)})
    return saida


def grupos_de_eventos(eventos):
    """Junta eventos cujas janelas se sobrepoem: o pico deles e medido junto."""
    grupos = []
    for e in sorted(eventos, key=lambda x: x["t"]):
        if grupos and e["t"] - 0.08 < grupos[-1]["fim"]:
            grupos[-1]["eventos"].append(e)
            grupos[-1]["fim"] = max(grupos[-1]["fim"], e["fim"])
        else:
            grupos.append({"t": e["t"], "fim": e["fim"], "eventos": [e]})
    return grupos


def confere_eventos(eventos, efeitos, pico_voz):
    """Cada evento segue a tabela sozinho. Empilhados somam: passar do mais forte e aviso, passar da soma e reprova."""
    acima, empilhados = [], []
    for g in grupos_de_eventos(eventos):
        trecho = efeitos[max(int((g["t"] - 0.08) * SR), 0):int(g["fim"] * SR)]
        if not len(trecho):
            continue
        medido = pico_voz - db(trecho.max())
        esperados = [e["esperado"] for e in g["eventos"]]
        soma = -db(sum(10 ** (-x / 20) for x in esperados))
        item = {"t": g["t"], "nomes": ", ".join(sorted({e["nome"] for e in g["eventos"]})),
                "medido": round(medido, 1), "limite": round(soma, 1)}
        if medido < soma - TOL_EFEITO:
            acima.append(item)
        elif len(esperados) > 1 and medido < min(esperados) - TOL_EFEITO:
            empilhados.append(item)
    return acima, empilhados


def dentro_de_evento(eventos, t):
    return any(e["t"] - 0.08 <= t <= e["fim"] for e in eventos)


def escolhe_video(projeto, pedido):
    if pedido:
        v = Path(pedido) if Path(pedido).is_absolute() else projeto / pedido
        if not v.exists():
            erro(f"video nao existe: {v}")
        return v
    for padrao in (
        projeto / "renders" / f"video-{projeto.name}" / f"video-{projeto.name}.mp4",
        projeto / "renders" / f"{projeto.name}.mp4",
    ):
        if padrao.exists():
            return padrao
    achados = [p for d in ("renders", "entrega", "render") if (projeto / d).is_dir() for p in (projeto / d).rglob("*.mp4")]
    if not achados:
        erro(f"nenhum MP4 em {projeto}. Renderize antes: a medicao vale para o arquivo final")
    return max(achados, key=lambda p: p.stat().st_mtime)


def medir(projeto, video, manuais):
    achados = []

    def nota(nivel, texto):
        achados.append({"nivel": nivel, "texto": texto})

    sv = sonda(video)
    if not sv["canais"]:
        nota("reprova", "O vídeo não tem áudio.")
        return {"video": video.name, "faixas": {}, "master": None, "achados": achados}
    master = loudness(video)
    reel = projeto.name.startswith("reel-")

    duracao, clipes = clipes_da_timeline(projeto)
    total = duracao or sv["duracao"]
    if manuais:
        clipes = clipes_manuais(manuais, projeto, total)
    faltando = [c for c in clipes if not c["arquivo"].exists()]
    if faltando:
        erro("arquivo da timeline nao existe: " + ", ".join(str(c["arquivo"]) for c in faltando))

    if duracao and abs(sv["duracao"] - duracao) > TOL_DURACAO:
        nota("reprova", f"Duração do vídeo {num(sv['duracao'], 2)} s difere do data-duration raiz {num(duracao, 2)} s.")
    if not clipes:
        nota("aviso", "Sem faixas para medir: só o master foi conferido. Passe --faixa se o projeto não usa a timeline.")

    faixas = {}
    with tempfile.TemporaryDirectory() as tmp:
        caminhos = {}
        for nome in ROTULOS:
            grupo = [c for c in clipes if c["classe"] == nome]
            if not grupo:
                continue
            caminhos[nome] = Path(tmp) / f"{nome}.wav"
            monta_faixa(grupo, total, caminhos[nome])
            faixas[nome] = loudness(caminhos[nome])
            faixas[nome]["clipes"] = len(grupo)
        mono = sorted({c["arquivo"].name for c in clipes if sonda(c["arquivo"])["canais"] == 1})
        if mono:
            nota("aviso", f"Mono: {', '.join(mono)}. Medido nos dois canais a 0 dB, como o render toca. "
                          "Mistura de teste com aformat engana em 3 dB: gere estéreo.")
        velhas = sorted({c["arquivo"].name for c in clipes if c["arquivo"].stat().st_mtime > video.stat().st_mtime})

        if len(caminhos) >= 1:
            soma = Path(tmp) / "soma.wav"
            if len(caminhos) > 1:
                soma_faixas(list(caminhos.values()), soma)
            else:
                soma = next(iter(caminhos.values()))
            estimado = loudness(soma)["lufs"]
            if abs(estimado - master["lufs"]) > TOL_SOMA:
                # Data de arquivo nao sobrevive a copia: so serve de pista quando a soma ja divergiu.
                pista = f" Mais novos que o vídeo: {', '.join(velhas)}." if velhas else ""
                nota("aviso", f"Soma das faixas dá {num(estimado)} LUFS e o vídeo {num(master['lufs'])}: "
                              f"o render não toca estas faixas, ou há áudio fora da timeline.{pista}")

        voz, trilha, efeitos = (faixas.get(k) for k in ("voz", "trilha", "efeitos"))
        if efeitos and "voz" in caminhos:
            onda = amostras(caminhos["efeitos"])
            pico_voz = db(amostras(caminhos["voz"]).max())
            efeitos["abaixo_da_voz"] = round(pico_voz - db(onda.max()), 1)
            eventos = eventos_de_efeito(projeto, clipes)
            acima, empilhados = confere_eventos(eventos, onda, pico_voz)
            for e in acima:
                nota("reprova", f"Efeito em {num(e['t'], 2)} s ({e['nomes']}): {num(e['medido'])} dB abaixo do pico "
                                f"da voz. Limite declarado: {num(e['limite'])} dB.")
            for e in empilhados:
                nota("aviso", f"Efeitos empilhados em {num(e['t'], 2)} s ({e['nomes']}): juntos ficam {num(e['medido'])} dB "
                              "abaixo do pico da voz. Cada um segue a tabela, mas a soma pesa: confira no ouvido.")
            t_pico = int(onda.argmax()) / SR
            if efeitos["abaixo_da_voz"] < PICO_EFEITO_MIN - TOL_EFEITO and not dentro_de_evento(eventos, t_pico):
                nota("reprova", f"Pico dos efeitos em {num(t_pico, 2)} s está {num(efeitos['abaixo_da_voz'])} dB abaixo do "
                                f"pico da voz, fora dos eventos declarados. Mínimo da tabela: {PICO_EFEITO_MIN:.0f} dB.")
            faixas["efeitos"]["eventos"] = len(eventos)

    fim_mudo = silencio_no_fim(video, sv["duracao"])
    if fim_mudo:
        nota("aviso", f"Silêncio nos últimos {num(fim_mudo, 2)} s do vídeo. O PRODUCAO.md pede todas as camadas até o fim.")
    if abs(master["lufs"] - ALVO_MASTER) > TOL_MASTER:
        nota("reprova", f"Master em {num(master['lufs'])} LUFS. Alvo: {num(ALVO_MASTER)} (±{num(TOL_MASTER)}).")
    if master["pico"] > TETO_DBTP:
        nota("reprova", f"Pico do master em {num(master['pico'])} dBTP. Teto: {num(TETO_DBTP)}.")
    if voz and voz["lufs"] > SILENCIO and abs(voz["lufs"] - ALVO_VOZ) > TOL_VOZ:
        nota("aviso", f"Voz em {num(voz['lufs'])} LUFS, longe dos {num(ALVO_VOZ)} da tabela.")
    if voz and trilha:
        gap = voz["lufs"] - trilha["lufs"]
        trilha["abaixo_da_voz"] = round(gap, 1)
        minimo = GAP_TRILHA_REEL if reel else GAP_TRILHA
        if gap < minimo:
            nota("reprova", f"Trilha só {num(gap)} LU abaixo da voz. Mínimo: {minimo:.0f} LU.")
    if trilha and efeitos and not voz and trilha["pico"] >= efeitos["pico"]:
        nota("aviso", "Sem narração, a trilha deveria ficar abaixo dos efeitos e está igual ou acima.")

    if voz and trilha:
        pasta = projeto / "renders/faixas"
        wavs = list(pasta.glob("*.wav")) if pasta.exists() else []
        if not wavs:
            nota("aviso", "Com voz e música, falta entregar as faixas em renders/faixas/.")
        for w in wavs:
            if abs(sonda(w)["duracao"] - sv["duracao"]) > TOL_DURACAO:
                nota("aviso", f"Faixa {w.name} não tem a duração completa do vídeo.")

    return {"video": str(video.relative_to(projeto)) if video.is_relative_to(projeto) else str(video),
            "duracao": round(sv["duracao"], 3), "faixas": faixas, "master": master, "achados": achados}


def tabela(res):
    linhas = ["| Faixa | LUFS | Pico |", "| --- | --- | --- |"]
    for nome, rotulo in ROTULOS.items():
        f = res["faixas"].get(nome)
        if f:
            linhas.append(f"| {rotulo} | {num(f['lufs'])} | {num(f['pico'])} dB |")
    m = res["master"]
    linhas.append(f"| Master | {num(m['lufs'])} | {num(m['pico'])} dBTP |")
    return "\n".join(linhas)


def atualiza_review(projeto, res):
    arquivo = projeto / "REVIEW.md"
    if not arquivo.exists():
        print("aviso: projeto sem REVIEW.md, nada gravado", file=sys.stderr)
        return
    texto = arquivo.read_text()
    bloco = tabela(res)
    m = re.search(r"^## Áudio medido.*$", texto, re.M)
    if m:
        prox = re.search(r"^## ", texto[m.end():], re.M)
        fim = m.end() + prox.start() if prox else len(texto)
        secao = texto[m.end():fim]
        velha = re.search(r"(^\|.*\|[ \t]*\n?)+", secao, re.M)
        if velha:
            rotulo = re.search(r"^\| (Master[^|]*?) +\|", velha.group(0), re.M)
            if rotulo:
                bloco = bloco.replace("| Master |", f"| {rotulo.group(1)} |")
            nova = secao[:velha.start()] + bloco + "\n" + secao[velha.end():]
        else:
            nova = "\n" + bloco + "\n" + secao
        texto = texto[:m.end()] + nova + texto[fim:]
    else:
        novo = f"## Áudio medido (arquivo final)\n{bloco}\n\nMedido, não ouvido.\n\n"
        v = re.search(r"^## Verificação", texto, re.M)
        texto = texto[:v.start()] + novo + texto[v.start():] if v else texto.rstrip() + "\n\n" + novo
    arquivo.write_text(texto)
    print(f"tabela gravada em {arquivo}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Mede a mixagem de um video contra o PRODUCAO.md")
    ap.add_argument("projeto")
    ap.add_argument("--video")
    ap.add_argument("--faixa", action="append", default=[])
    ap.add_argument("--atualizar-review", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    projeto = Path(a.projeto) if Path(a.projeto).is_dir() else RAIZ / "projetos" / a.projeto
    projeto = projeto.resolve()
    if not projeto.is_dir():
        erro(f"projeto nao existe: {a.projeto}")

    res = medir(projeto, escolhe_video(projeto, a.video), a.faixa)
    reprovou = any(x["nivel"] == "reprova" for x in res["achados"])
    res["veredito"] = "reprovado" if reprovou else "aprovado"

    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"{res['video']}: {res['veredito']}\n")
        if res["master"]:
            print(tabela(res))
        for x in res["achados"]:
            print(f"\n{x['nivel'].upper()}: {x['texto']}", end="")
        print("\n\nMedido, não ouvido.")
    if a.atualizar_review and res["master"]:
        atualiza_review(projeto, res)
    sys.exit(1 if reprovou else 0)


if __name__ == "__main__":
    main()
