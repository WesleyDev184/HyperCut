# Origem

Código de `kajisho5/ffmpeg-skill`, commit `1ce2c186bf1dba96132d87274eee46df4f537e0e`, licença MIT (`LICENSE-ffmpeg-skill`).
Copiados só 18 arquivos: `audio`, `check`, `color`, `redact`, `stabilize`, `_platforms` e `_common/`. Sem MCP, instalador, testes nem `.claude/`.

Revisados em 2026-11-04, lendo o código inteiro. Nada malicioso, ofuscado ou de rede.

## Correções locais

| Arquivo | Mudança | Motivo |
| --- | --- | --- |
| `_common/runner.py` | `_audit_default` retorna `None` | Log ao lado da saída seguia symlink plantado e acrescentava texto em outro arquivo |
| `_common/runner.py` | `_check_output_path` recusa symlink | Symlink quebrado na saída fazia o FFmpeg escrever em outro lugar |
| `check.py`, `_common/probe.py` | Usa a última ocorrência do resultado | Metadados forjados falsificavam loudness e pico |
| `check.py` | `shell_quote` no comando sugerido | Nome de arquivo entrava sem aspas |

Testado com arquivo gerado: título forjado, saída por symlink e log plantado. As 5 ferramentas rodaram no FFmpeg 6.1.1.

## Riscos que ficam

Valem para arquivo de terceiro, e por isso a skill é só para material próprio.

- `black`, `freeze` e silêncio em `--content` ainda leem o log do FFmpeg e podem ser forjados.
- Lock plantado como FIFO pode travar a ferramenta.
- Nome de arquivo com sintaxe de protocolo do FFmpeg pode passar pelas barreiras.
- Comandos impressos usam aspas de bash, não de fish.

Ao atualizar, repita a revisão e as correções. Não troque por `npm install` nem copie o repositório inteiro.
