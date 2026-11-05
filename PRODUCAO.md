# Padrões de produção

Valem para todo vídeo, salvo pedido contrário no `BRIEF.md`.

## Planejamento

- Antes de construir, escreva a tabela do vídeo em `SPEC.md`: início, fim, o que aparece,
  o que o espectador entende e o que acontece no áudio.
- A tabela cobre o vídeo inteiro, de 0 até o fim, sem buraco.
- Uma ideia por vez. Ação pode ser rápida, reação e leitura ganham mais tempo.
- Antes de planejar, meça cada arquivo de `brutos/` (`bin/hf measure probe` em vídeo, `ffprobe` em imagem e
  áudio) e olhe quadros reais. Riscos como resolução baixa ou áudio mono vão para o `SPEC.md`.
  Nunca deduza o conteúdo pelo nome do arquivo.
- Cada cena tem assunto principal próprio, diferente do da cena anterior. Trocar só o texto sobre o mesmo
  visual não é cena nova.
- O elemento mais marcante do vídeo aparece em 1 ou 2 momentos, de preferência no auge. Nunca serve de base
  para todas as cenas.

## Narrativa

- Prenda a atenção nos 2 primeiros segundos.
- Construa tensão até um momento em que imagem e som atingem o auge juntos.
- Reserve pelo menos 2 s para a composição final.
- Comece e termine em movimento suave, sem entrada ou saída seca em imagem parada.

## Paleta

- Padrão: tema escuro. Fundo `#14170f`, cartão `#1b1f15`, texto `#edeee3`,
  texto apagado `#a7ae98`, destaque `#7bb289`, ouro `#c9a84c`, alerta `#d97e63`.
- Texto sobre o verde usa `#14170f`. Onde o texto é branco fixo, como nos botões do kit do reel,
  o destaque vira `#3f7a53`, o verde escuro da paleta.
- Paleta definida no pedido ou no `BRIEF.md` substitui a padrão.
- Em edição de vídeo real, proponha também a paleta sugerida por `bin/paleta-do-video` e deixe a escolha com quem pediu.
- Cor fica nos gráficos, nunca no rosto.

## Movimento

- Todo movimento tem aceleração e desaceleração. Nada em velocidade constante.
- Use antecipação antes de movimentos importantes e ultrapassagem sutil quando fizer sentido.
- Nas pausas de leitura, só movimento discreto. Sem cena totalmente imóvel.
- Crie profundidade com escala, desfoque e paralaxe.
- Desfoque de movimento só durante o movimento: quadro parado e desfocado é erro.
- Nunca desfoque palavra que precisa ser lida.

## Cortes e transições

- Todo corte tem motivo. Prefira corte por correspondência, máscara, deslocamento rápido ou
  forma que vira a próxima cena.
- Evite dissolução genérica.
- Com música, cortes e movimentos principais caem na batida: defina o BPM no `SPEC.md`.

## Texto e legibilidade

- Texto grande e curto, nunca parágrafo. Mínimo de 30 px em tela de 1080 px de largura.
- Nada some antes de ser lido e entendido por quem assiste pela primeira vez.
- Um assunto dominante por cena e no máximo um elemento de apoio.
- Se a ação já conta a história, não coloque texto.
- Legenda e texto de tela não dizem a mesma coisa ao mesmo tempo. Com o título na tela, a legenda some
  ou acrescenta informação.

## Vídeo vertical

- Cada trecho contínuo tem no máximo cerca de 8 s. Trechos seguidos usam layouts diferentes.
- Capa só no quadro 0, com título criado do gancho se não houver outro.
- Legenda vem dos tempos por palavra da voz final, em blocos de 1 a 3 palavras.
- A cada 2 ou 3 blocos, destaque 1 ou 2 palavras importantes. Nunca dois destaques seguidos
  nem destaque em artigo, preposição ou conjunção.
- Legenda nunca cobre rosto nem conteúdo importante.

## Personagens

- Mantenha proporções, cores e detalhes iguais em todas as cenas.
- Olhos indicam a intenção antes do corpo. Emoção vem de olhos, corpo e postura.
- Personagem com presença clara no quadro, nunca minúsculo em cenário vazio.

## Veracidade

- Só informação verdadeira. O que não dá para confirmar não entra.
- Todo número ou fato citado é conferido em 2 ou mais fontes confiáveis.
- Fala divergente das fontes fica na gravação, sem reforço gráfico, e a divergência vai para o relatório.
- Acontecimento citado aparece com a página real da fonte.
- Interface que exige login pode ser reconstruída de fontes públicas, sempre declarada no relatório.
- Anime a ação mencionada. Não troque a demonstração por um cartão que repete a fala.

## Som

- Música é sintetizada por código (Web Audio com `OfflineAudioContext`, ou NumPy e SciPy),
  salvo arquivo entregue em `brutos/`.
- Efeitos vêm primeiro do kit CC0 local. Sem som certo, busque no Openverse, em inglês. Por último, gere com
  o earshot. Comandos no `AGENTS.md`. Do Openverse só entram CC0 e CC BY.
- O efeito cai em `assets/sfx/` com pico em -3 dBFS: ajuste o volume na composição para a tabela abaixo.
- Crédito de som CC BY, listado em `assets/sfx/CREDITOS.md`, sai junto com o vídeo publicado.
- Um efeito por evento visual relevante. Sem efeito em troca de layout, deslocamento suave ou zoom.
- Som de passagem coincide com o meio do movimento: no máximo 1 por trecho e 3 no vídeo.
- Sem narração, a música fica abaixo dos efeitos para a ação ser ouvida.
- Com narração, a música não tem melodia que dispute com a fala nem automação de volume.
- Voz gerada tem plano em `roteiro/`: ritmo, curva de energia, pausas e palavras de ênfase por trecho.
  "Natural" ou "expressivo" não é direção.
- Gere primeiro o trecho mais difícil da voz e mostre a quem pediu. O resto só depois da aprovação.
  Mudou voz, modelo ou velocidade: nova amostra.

| Faixa | Nível |
| --- | --- |
| Voz | -14 LUFS |
| Música | cerca de 10 LU abaixo da voz, perto de -24 LUFS. Em reel, pelo menos 13 LU abaixo |
| Cliques, impactos, confirmações | pico 10 dB abaixo do pico da voz |
| Passagens | pico 9 dB abaixo |
| Teclas | pico 16 dB abaixo |
| Riser | pico 14 dB abaixo |
| Master | -14 LUFS, pico verdadeiro até -1 dBTP |

Meça voz, música e master com o filtro `ebur128` do FFmpeg. Limitador só se um pico passar do limite.

## Técnica

- Cada quadro depende só do tempo. Aleatoriedade, só com semente fixa.
- Todas as camadas terminam no mesmo ponto: sem quadro branco, imagem sobrando ou silêncio no fim.
- Com voz e música, entregue também as faixas em WAV com a duração completa, para remixar depois.
- Dependência nova é instalada nesta pasta, nunca no sistema.

## Verificação

- Antes do render final, gere prancha de quadros de cada cena e confira pose, continuidade,
  enquadramento, luz e clareza.
- Depois do render, inspecione quadros reais, inclusive os dois lados de cada corte.
- Confira duração, resolução, sincronia de som e imagem, LUFS e pico.
- Achou um defeito: procure o mesmo tipo de defeito no vídeo inteiro antes de corrigir.
- Com outro título, o vídeo serviria para outro assunto? Se sim, a direção está genérica: volte ao `SPEC.md`.
- Corrija e renderize de novo. Entregue só depois de tudo aprovado.

## Relatório

Registre em `REVIEW.md`: decisões tomadas, fatos e fontes, divergências, reconstruções de interface,
efeitos com seus tempos, LUFS e pico de cada faixa e o resultado da verificação.

## Looks disponíveis

Use só quando pedido ou quando o `BRIEF.md` citar.

- **Cartões claros**: fundo quase branco, cartões flutuantes com sombra em
  3 camadas, Poppins, destaque terracota `#D97757`.
- **Editorial quente**: creme `#F0EEE6`, tinta `#1F1E1D`, argila `#D97757`,
  serifa elegante nos títulos.
- **Argila 3D**: stop motion em Three.js, luz quente de luminária com luz fria da lua.
