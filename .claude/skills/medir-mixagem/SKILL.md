---
name: medir-mixagem
description: Mede voz, trilha, efeitos e master de um vídeo desta pasta com ebur128, compara com a tabela de níveis do PRODUCAO.md e gera a tabela de áudio do REVIEW.md. Use sempre depois de renderizar um vídeo com som e sempre que pedirem para medir, conferir ou fechar o áudio, mesmo sem citar a skill: "mede a mixagem", "tá em quantos LUFS", "o áudio tá alto/baixo", "a trilha tá abafando a voz", "confere os efeitos", "preenche a tabela de áudio do REVIEW", "bateu -14?". Não serve para escolher onde pôr efeito (`sons/sons momentos`) nem para gerar ou buscar som (`sons/sons`).
---

# Medir mixagem

O número que vale é o do MP4 entregue. Mistura de teste já errou por 3 dB em um vídeo real, então a medição parte do render e das faixas como o render as toca.

## Rodar

Da raiz da pasta, depois do render:

```bash
bin/com-ambiente .venv/bin/python .claude/skills/medir-mixagem/scripts/medir.py <projeto>
```

O script acha o MP4, lê as faixas em `hf timeline` com início e volume reais, mede tudo e imprime a tabela. Ele só mede: nunca altera áudio. Saída 0 é aprovado, 1 é reprovado, 2 é erro.

| Opção | Quando usar |
| --- | --- |
| `--video renders/x.mp4` | O MP4 certo não é `renders/<projeto>.mp4` |
| `--faixa voz=caminho[@volume]` | Projeto sem timeline. Repita para `voz`, `trilha` e `efeitos` |
| `--atualizar-review` | Grava a tabela na seção "Áudio medido" do `REVIEW.md`, sem mexer no texto ao redor |
| `--json` | Precisa dos valores para outro passo |

A classe da faixa vem do id e do arquivo: `voz`, `narra` ou `locu` é voz; `trilha`, `music` ou `bgm` é trilha; o resto é efeito. Confira a tabela se um nome fugir disso.

## O que ele reprova

| Item | Limite |
| --- | --- |
| Master | −14 LUFS (±0,3), pico até −1 dBTP |
| Trilha | Pelo menos 9 LU abaixo da voz, 13 em projeto `reel-*` |
| Efeito | Pico no nível declarado em `roteiro/efeitos.json`, com 1 dB de folga. Sem lista, 9 dB abaixo do pico da voz |
| Duração | Igual ao `data-duration` raiz |

Voz longe de −14 é só aviso, porque quem fecha é o master: com trilha, a voz costuma ficar perto de −13 para o master dar −14.

A tabela mostra pico verdadeiro, como a entrega pede. Os limites de efeito comparam pico de amostra, porque é assim que as montagens de efeitos ajustam o nível. Por isso a distância na tabela pode diferir 1 ou 2 dB da citada no aviso.

Cada evento de `roteiro/efeitos.json` é conferido em 0,3 s a partir do tempo. Em evento longo com o pico no fim, como riser, declare `"duracao"` em segundos, senão o pico fica fora da conferência.

## Corrigir

Corrija a faixa e renderize de novo. Mexer só no MP4 deixa `assets/` e `renders/faixas/` diferentes do vídeo.

- **Master fora do alvo:** a diferença em dB vai para a faixa de voz, ou para todas se a proporção já estiver certa. Em `data-volume`, o valor é linear: `10^(dB/20)`.
- **Pico acima de −1 dBTP:** primeiro baixe o ganho. Limitador só se um pico isolado continuar passando, como manda o `PRODUCAO.md`.
- **Trilha perto da voz:** baixe a trilha. Automação de volume não é opção, pela mesma regra.
- **Efeito acima do declarado:** ajuste o volume do evento e rode a montagem de efeitos do projeto.
- **Soma das faixas diferente do vídeo:** o render está velho, a timeline não mostra tudo o que toca, ou há som em um `<video>`. Renderize de novo antes de confiar na tabela.
- **Faixa mono:** gere estéreo com `pan=stereo|c0=c0|c1=c0`. O script mede como o render toca, mas outras misturas erram em 3 dB.
- **Silêncio no fim:** encurte o vídeo ou leve trilha ou som de fechamento até o último quadro. A escolha é da pessoa.
- **Efeitos empilhados:** não é erro. Dois eventos no mesmo instante somam, mesmo com cada um no nível certo. Aponte o tempo à pessoa para ouvir.

Depois de cada correção, meça de novo o MP4 novo.

## Entregar

- Use `--atualizar-review` na medição final, sem medir antes de novo se nada mudou. Desvio aceito, como voz acima da tabela, fica explicado na seção do `REVIEW.md`. Aviso ainda sem decisão fica na resposta à pessoa.
- Diga sempre que foi medido, não ouvido. Nível certo não prova que a mistura soa bem.
- Passe avisos adiante com o tempo de cada um. Não os esconda porque o veredito foi aprovado.

## Em reel

`verificar.py` e `audio-final-vsl.sh` da skill `reel` cuidam do master. Use esta skill para conferir a trilha e preencher a tabela:

```bash
bin/com-ambiente .venv/bin/python .claude/skills/medir-mixagem/scripts/medir.py reel-<nome> --video entrega/<arquivo>.mp4 \
  --faixa voz=motor/assets/clean.mp4 --faixa trilha=motor/assets/musica.wav@0.12
```

Sem todas as faixas, o aviso de soma diferente é esperado.
