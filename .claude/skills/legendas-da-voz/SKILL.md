---
name: legendas-da-voz
description: Gera compositions/legendas.html de um vídeo desta pasta a partir da voz final, em blocos de 1 a 3 palavras com destaques, seguindo as regras do PRODUCAO.md. Use sempre que precisar pôr, refazer ou ressincronizar legenda em vídeo narrado de projetos/, mesmo sem citar a skill: "põe legenda", "legenda palavra por palavra", "a legenda atrasou", "troquei a voz, refaz a legenda", "acerta os destaques da legenda", "tira a legenda do final". Não use em projetos reel-*, em que a legenda vem do motor da skill reel, nem para arquivo SRT ou VTT, que sai de `bin/hf transcribe --to srt`.
---

# Legendas da voz

A legenda vem dos tempos da voz final. Roteiro e transcrição têm papéis diferentes: o texto da tela vem do roteiro, com a grafia certa, e a transcrição só dá os tempos. O whisper escreve "Eveja", "velho" no lugar de "Véio" e "R$320", mas casa letra a letra com o roteiro mesmo assim.

## 1. Transcrever a voz final

Use a faixa montada, a mesma que toca no vídeo, já acelerada se for o caso, sem trilha nem efeitos. O nome está no `<audio>` da voz em `index.html`:

```bash
bin/com-ambiente .venv/bin/python .claude/skills/legendas-da-voz/scripts/legendas.py <projeto> --transcrever assets/audio/voz.wav
```

O script corta a voz nos silêncios e transcreve cada trecho. Não troque isso por `bin/hf transcribe` no arquivo inteiro: em voz com pausas longas, o whisper errou até 4 s, mesmo com `large-v3`, e os erros não aparecem na taxa de casamento. O padrão `--modelo small` já dá conta, porque o tempo vem do trecho e o texto vem do roteiro.

Mudou a voz ou a velocidade? Repita este passo. `roteiro/transcript.json` feito por outro caminho pode trazer tempos da voz sem aceleração, e o script avisa quando a voz mudou depois da transcrição.

## 2. Escrever os blocos

Edite `roteiro/legendas.txt`. Se o arquivo não existir, comece por um rascunho:

```bash
bin/com-ambiente .venv/bin/python .claude/skills/legendas-da-voz/scripts/legendas.py <projeto> --rascunho
```

O rascunho quebra por pausa e pontuação, mas traz os erros do whisper e escolhe destaques pelo tamanho da palavra. Reescreva com a grafia do roteiro e destaque o que importa para a mensagem. Se o projeto tiver o texto da narração em `roteiro/`, confira com ele.

```text
quanto *custa*
cada cabeça?
*R$ 320* | trezentos e vinte reais
~meusite.com.br
```

- Uma linha é um bloco, de 1 a 3 palavras.
- `*palavra*` sai em destaque. A cada 2 ou 3 blocos visíveis, 1 ou 2 palavras importantes. Nunca em blocos seguidos nem em artigo, preposição ou conjunção. Quando ritmo e importância brigarem, fique com a importância: bloco demais sem destaque é só aviso.
- ` | ` traz o que a voz diz quando difere da tela. O script tenta as duas formas e fica com a que casa.
- `~` no começo mantém o tempo, mas o bloco não aparece. Use onde a tela já diz o mesmo, inclusive em rótulo pequeno, porque legenda e texto de tela não dizem a mesma coisa ao mesmo tempo.

Para achar essas repetições, gere uma vez e veja os quadros do passo 4. É mais rápido que ler as cenas, e os tempos escritos nelas podem não ser os reais em vídeo acelerado.

## 3. Gerar

```bash
bin/com-ambiente .venv/bin/python .claude/skills/legendas-da-voz/scripts/legendas.py <projeto>
```

Com `REPROVA`, nada é gravado. As regras de vídeo vertical reprovam em `portrait` e só avisam nos outros formatos.

| Saída | O que fazer |
| --- | --- |
| Menos de 60% casou | A voz é outra, ou a transcrição veio traduzida. Refaça o passo 1 |
| Bloco casou pouco | O tempo foi estimado pelos vizinhos. Confira esse bloco primeiro |
| Bloco fica pouco tempo na tela | Junte com o vizinho, se couber em 3 palavras |
| `index.html` não monta a legenda | Acrescente a linha que o aviso traz |
| Arquivo não veio deste script | Veja o que ele tem de próprio, passe para `roteiro/legendas.css` e use `--sobrescrever` |

## Aparência

Padrão: Public Sans 800, 62 px em vertical e 48 px nos outros formatos, cores da paleta escura, na altura aprovada nos vídeos anteriores. Tudo que for do projeto, como `.lg b { color: #e3c47c; }`, vai em `roteiro/legendas.css`, que entra no fim do estilo e sobrevive a cada geração. Não edite `compositions/legendas.html`: a próxima geração apaga a mudança.

## 4. Conferir

1. Rode `../../bin/hf check --json` no projeto. `content_overlap` com `#lgs...` significa legenda sobre texto: mude a posição em `roteiro/legendas.css`, ou confirme que o que está embaixo é só decoração. `timeline_track_too_dense` na legenda é esperado.
2. Rode `snapshot` com um quadro por cena, mais os blocos com aviso. Olhe se a legenda cobre rosto ou conteúdo e se repete o que a tela diz. O `check` não pega nenhum dos dois.
3. Passe à pessoa no `preview`. O tempo por palavra do whisper varia cerca de 0,1 s, e até 0,5 s em alguns blocos. Sincronia se confere vendo e ouvindo: quadro parado não prova.

Registre no `REVIEW.md` a origem da voz e os blocos com tempo estimado. Se `tools/` tiver um gerador antigo de legenda, avise: rodá-lo apaga a legenda nova.
