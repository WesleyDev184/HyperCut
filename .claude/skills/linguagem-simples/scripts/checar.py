#!/usr/bin/env python3
"""Aponta palavra difícil e frase longa no texto que vai para o público.

Uso: python3 checar.py <arquivo-ou-pasta> [...]
     python3 checar.py --teste
Lê o texto visível de .html (lâminas) e .md (legenda, roteiro). Ignora títulos markdown (#), hashtags e
a seção "Texto alternativo" (é para leitor de tela, não para o feed). Termos e trocas ficam em ../termos.tsv.
Sai com 1 quando acha algo, para dar para usar em script.
"""
import html
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MAX_PALAVRAS_LAMINA = 16
MAX_PALAVRAS_LEGENDA = 22


def carregar_termos(tsv: Path):
    termos = []
    for linha in tsv.read_text(encoding="utf-8").splitlines():
        if not linha.strip() or linha.startswith("#"):
            continue
        partes = linha.split("\t")
        padrao, troca = partes[0], partes[1] if len(partes) > 1 else ""
        termos.append((re.compile(rf"(?<![\wÀ-ÿ])(?:{padrao})(?![\wÀ-ÿ])", re.I), troca))
    return termos


def texto_html(src: str) -> list[str]:
    src = re.sub(r"<(script|style|title)\b.*?</\1>", " ", src, flags=re.S | re.I)
    # cada bloco vira uma linha: p, h1-h3, li, span de rótulo
    src = re.sub(r"</?(p|h[1-6]|li|header|footer|div)\b[^>]*>", "\n", src, flags=re.I)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", src))
    return [re.sub(r"\s+", " ", l).strip() for l in txt.splitlines() if l.strip()]


def texto_md(src: str) -> list[str]:
    linhas, pular = [], False
    for l in src.splitlines():
        if l.startswith("#"):
            pular = "texto alternativo" in l.lower() or "alt text" in l.lower()
            continue
        if pular or not l.strip() or l.strip().startswith(("#", "Fonte:")):
            continue
        linhas.append(l.strip())
    return linhas


def checar_linhas(nome: str, linhas: list[str], termos, max_palavras: int) -> list[str]:
    achados = []
    for l in linhas:
        for rx, troca in termos:
            m = rx.search(l)
            if m:
                achados.append(f"{nome}: '{m.group(0)}' → troque por {troca}  | {l[:90]}")
        for frase in re.split(r"(?<=[.!?:;])\s+", l):
            n = len(frase.split())
            if n > max_palavras:
                achados.append(f"{nome}: frase com {n} palavras (até {max_palavras}) | {frase[:90]}")
    return achados


def checar_arquivo(p: Path, termos) -> list[str]:
    src = p.read_text(encoding="utf-8")
    if p.suffix == ".html":
        return checar_linhas(p.name, texto_html(src), termos, MAX_PALAVRAS_LAMINA)
    return checar_linhas(p.name, texto_md(src), termos, MAX_PALAVRAS_LEGENDA)


def arquivos(alvos: list[str]):
    for a in alvos:
        p = Path(a)
        if p.is_dir():
            yield from sorted(x for x in p.rglob("*") if x.suffix in (".html", ".md") and "renders" not in x.parts
                              and x.name not in ("SPEC.md", "REVIEW.md", "BRIEF.md", "DESIGN.md", "index.html"))
        elif p.is_file():
            yield p


def teste():
    termos = carregar_termos(AQUI.parent / "termos.tsv")
    a = checar_linhas("x", ["a resposta está nas próximas lâminas"], termos, 16)
    assert any("lâminas" in s for s in a), a
    a = checar_linhas("x", ["Todo animal que transitar, antes da primeira movimentação."], termos, 16)
    assert len([s for s in a if "troque" in s]) == 2, a
    assert checar_linhas("x", ["Boi sem número oficial não sai da fazenda."], termos, 16) == []
    assert not checar_linhas("x", ["Integrado"], termos, 16) or True  # só confere que não quebra
    assert texto_md("## Legenda\nFonte: Portaria 1.331/2025") == []
    assert checar_linhas("x", ["Plano Nacional de Identificação Individual de Bovinos"], termos, 16) == []
    assert texto_md("## Legenda\nUsar a lâmina\n## Texto alternativo (Alt Text)\n- slide-01: lâmina") == ["Usar a lâmina"]
    assert texto_html("<p>Olá <b>gado</b></p><script>lâmina()</script>") == ["Olá gado"]
    longa = " ".join(["palavra"] * 25) + "."
    assert any("25 palavras" in s for s in checar_linhas("x", [longa], termos, 22))
    print("ok")


def main():
    if sys.argv[1:] == ["--teste"]:
        return teste()
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    termos = carregar_termos(AQUI.parent / "termos.tsv")
    total = []
    for p in arquivos(sys.argv[1:]):
        for s in checar_arquivo(p, termos):
            print(f"{os.path.relpath(p.parent)}/{s}")
            total.append(s)
    print(f"\n{len(total)} ponto(s) para revisar." if total else "Nenhum termo difícil nem frase longa.")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
