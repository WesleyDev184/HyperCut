---
name: linguagem-simples
description: Use when writing or revising any text that goes to the public in this workspace (post or carousel slides, Instagram caption, story, video on-screen text, voice script) or when someone says a text is hard, formal, "rebuscado", full of jargon or technical words: "linguagem difícil", "o povo não entende", "simplifica o texto", "termo complexo", "fala como o produtor fala". Especially when the facts come from laws, decrees, government plans or technical papers (PNIB, GTA, brucelose, MAPA, Embrapa).
---

# Linguagem simples

Texto para o público fala como quem explica no curral, não como a portaria. A fonte oficial dá o fato; a palavra do post é a do dia a dia.
Base: Lei 15.263/2025 (Política Nacional de Linguagem Simples), art. 5º: ordem direta, frase curta, uma ideia por parágrafo,
palavra comum, termo técnico trocado ou explicado, nome completo antes da sigla, voz ativa, verbo no lugar de substantivo,
o mais importante primeiro, e teste com o público.

## Como cada frase sai

Toda frase de lâmina, story, legenda ou tela tem estas partes, nesta ordem:

1. **Quem faz ou quem é afetado:** "o gado", "você", "as bezerras".
2. **Um verbo de ação comum:** "sai", "comprove", "vacine", "declare". Nunca o substantivo do verbo ("comprovação", "movimentação", "obrigatoriedade").
3. **O quê e quando, com o número intacto:** data, idade, prazo e quantidade exatamente como na fonte.

Palavra oficial só entra quando a pessoa vai precisar dela para agir: nome do documento (GTA), do sistema onde declara (SIDAGO),
da agência (Adapec), da vacina. Na primeira vez, venha explicada: "PNIB, o plano do governo que dá um número para cada animal".

## Simplificar sem mudar o fato

A troca de palavra não pode mudar quem, o quê, quando nem o grau da regra. Depois de reescrever, compare cada frase com a fonte:

| Na fonte | Errado (mudou o fato) | Certo |
| --- | --- | --- |
| Etapa 3 (2027 a 2029) começa pelos vacinados | "Em 2027 todo boi precisa de brinco" | "Em 2027, o brinco oficial começa pelos vacinados contra brucelose" |
| 1º/01/2033: proibido movimentar não identificado | "Boi sem brinco não anda mais" (hoje) | "A partir de 2033, boi sem número oficial não sai da fazenda" |
| Trânsito proibido, exceto abate imediato | "O gado não pode sair" | "O gado não sai da fazenda, só direto para o abate" |
| Prazo nacional de comprovação | "O prazo é 10/01" | "O prazo nacional é 10/01. Seu estado pode ter outro" |

Dramatizar ("o cerco fecha", "acabou a farra") tende a exagerar a regra. Use o fato concreto: a data e o que acontece.

## Passos

1. Escreva o texto pela receita acima.
2. Rode o checador nos arquivos do post:
   `python3 .claude/skills/linguagem-simples/scripts/checar.py projetos/<projeto>/posts/<slug>` (ou a pasta `slides/` e o `legenda.md`).
   Ele lê o texto visível das lâminas e a legenda, aponta os termos de `termos.tsv` com a troca sugerida e as frases longas
   (mais de 16 palavras na lâmina, 22 na legenda). O texto alternativo e a linha "Fonte:" ficam de fora. Rótulo de formato ("slide-01:") num rascunho não conta: só o texto do público.
3. Para cada ponto: troque, ou mantenha só se a coluna "quando manter" de `termos.tsv` cobrir o caso.
4. Teste do curral: leia em voz alta. Se você não diria assim para o vaqueiro, reescreva.
5. Compare de novo com a fonte (tabela acima). Rode o checador até sobrar só o que tem motivo para ficar.
6. Termo difícil novo que apareceu e não está em `termos.tsv`? Acrescente a linha (termo, troca, quando manter).

## Trocas mais comuns

| Difícil | Comum |
| --- | --- |
| lâmina, slide, carrossel (no texto do público) | post, "arraste para o lado" |
| transitar, movimentação | sair da fazenda, viajar |
| comprovação | comprovar a vacina |
| identificação individual | brinco com número próprio |
| Base Central de Dados | cadastro do governo |
| obrigatoriedade | vale para todos, tem que |
| isento | fica de fora |
| integração dos sistemas | os sistemas se ligam |
| finalidade sanitária | para cuidar da saúde do rebanho |
| ilustrativo | só um exemplo |
| idade-padrão | idade usada para comparar |
| pico de temperatura | hora mais quente |
| RFID | chip eletrônico |
| portaria/decreto nº X | regra do Ministério / do estado (número só como fonte, na legenda) |

## Erros comuns

- **Palavra de bastidor no texto do público:** "lâmina", "CTA", "engajamento", "conteúdo". Quem lê vê um post e fotos.
- **Copiar a frase da fonte:** a ficha diz "órgãos estaduais integram seus sistemas"; o post diz "os estados ligam os sistemas ao do governo federal".
- **Sigla solta:** MAPA, PNIB, PNCEBT sem o nome na primeira vez. Nome completo uma vez, depois a sigla ou "o plano".
- **Número da norma no meio da lâmina:** "Portaria SDA/MAPA 1.331/2025" vira "regra do Ministério da Agricultura, de 2025". O número fica numa linha "Fonte: ..." no fim da legenda, antes das hashtags.
- **Termo sem troca segura:** se a palavra comum muda o sentido ("protocolos privados" → "programa privado"), tire a informação ou explique com a fonte. Nunca chute um sinônimo.
- **Simplificar e generalizar:** "alguns" virou "todos", "a partir de 2033" virou "agora". Sempre volte à fonte.
