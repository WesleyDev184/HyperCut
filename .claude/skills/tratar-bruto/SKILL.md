---
name: tratar-bruto
description: Trata gravação própria de `brutos/` antes de virar asset: limpa voz (ruído, chiado, sibilância), estabiliza imagem tremida, converte HDR de celular para SDR, corrige cor básica, borra região fixa e confere um arquivo contra a spec de Reels, Shorts, TikTok ou YouTube. Use quando a gravação tiver problema técnico, mesmo sem citar a skill: "a voz tá com chiado", "tem ruído no áudio", "o vídeo tá tremido", "gravei em HDR no iPhone", "a cor ficou lavada", "borra essa parte", "esse arquivo passa no Reels?". Não use para editar ou cortar (`/reel`), para medir a mixagem final (`medir-mixagem`) nem em arquivo de terceiro.
---

# Tratar bruto

São ferramentas locais, sem rede. Vieram de `kajisho5/ffmpeg-skill`, com correções de segurança: veja `ORIGEM.md`.

Use só com material da pessoa. O código protege pouco contra arquivo feito para atacar, e os metadados de um arquivo de terceiro chegariam a você como texto. Referência de fora passa por `assistir-video`.

A mídia anda num sentido só: leia de `brutos/` e grave em `assets/`. Coloque o comando em `tools/` do projeto para o preparo poder ser refeito. Nunca sobrescreva um bruto.

Rode da pasta do projeto e sempre com `--json-brief`, que deixa de fora os metadados do arquivo:

```bash
S=../../.claude/skills/tratar-bruto/scripts
../../bin/com-ambiente ../../.venv/bin/python $S/audio.py brutos/fala.mp4 --voice light -o assets/audio/fala.wav --json-brief
```

## Voz

| Caso | Comando |
| --- | --- |
| Boa gravação, só nivelar | `audio.py <arq> --voice light -o <saida>` |
| Ruído de fundo e sibilância | `audio.py <arq> --voice medium -o <saida>` |
| Celular ou notebook | `audio.py <arq> --voice strong -o <saida>` |
| Só ruído | `audio.py <arq> --denoise -o <saida>` |

Comece pelo mais leve, porque limpeza forte deixa a voz metálica. Saída `.wav` extrai o áudio. Medição não diz se ficou bom: mostre à pessoa para ouvir.

Não use `--music` nem `--duck`: o `PRODUCAO.md` pede música sem automação de volume. A mixagem final é da composição, conferida com `medir-mixagem`.

## Imagem

| Caso | Comando |
| --- | --- |
| Tremido | `stabilize.py <arq> --shakiness 5 --smoothing 15 --zoom 3 -o <saida>` |
| HDR de celular | `color.py <arq> --to-sdr -o <saida>` |
| Exposição ou saturação | `color.py <arq> --correct --exposure 0.2 --saturation 1.05 -o <saida>` |

Em vídeo real, a cor fica no gráfico, nunca no rosto. Compare antes e depois com `bin/hf snapshot` ou `bin/hf measure frames`.

## Borrar

```bash
redact.py <arq> --x 820 --y 140 --width 240 --height 120 --mode pixelate --block-size 24 -o <saida>
```

Serve para esconder algo pequeno e fixo, como uma placa ou um canto da tela. **Não serve para dado sensível:** o retângulo não acompanha movimento, borrão de texto pode ser recuperado, e legendas e metadados do arquivo continuam nele. Em demonstração do sistema, use dados fictícios desde a gravação.

## Conferir spec

```bash
check.py <arq> --platform reels --content --json-brief
```

Plataformas: `reels`, `shorts`, `tiktok`, `youtube`, entre outras. `--content` procura trecho preto, congelado, mudo e quadro solto. Saída 1 significa que algum item reprovou. Loudness de entrega segue o `PRODUCAO.md`, mesmo onde a plataforma aceita outro valor.

## Ao ler a saída

- As dicas citam ferramentas que não vieram para cá (`export.py`, `fit.py`, `loudness.py`, `look.py`, `_contract.py`). Não procure esses arquivos nem rode `python3 scripts/_contract.py`: resolva com `bin/hf` ou com o fluxo do projeto.
- Não cole comandos impressos pelas ferramentas. As aspas delas valem só para bash e quebram em outro shell, como o fish.
- Sem FFmpeg 6.1 ou mais novo, elas param com saída 127. Peça à pessoa para rodar `bin/instalar-ffmpeg`.
