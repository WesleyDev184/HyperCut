# Padrões de produção

Valem para todo vídeo, post e carrossel, salvo pedido contrário no `BRIEF.md`.

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
- Títulos, cartões e textos que já pousaram ficam cravados em coordenadas inteiras: nunca aplique flutuação lenta (`x`/`y`), micro-escala (`scale`) ou rotação lenta sobre elementos com texto ou borda fina, pois isso gera tremor de subpixel quadro a quadro. O movimento contínuo fica no fundo, em barras internas, traçados SVG ou cursores.
- Nunca aplique zoom lento (`scale`) sobre imagem estática (`<img>`), pois a reamostragem quadro a quadro treme. Em tela cheia, use deslocamento lateral leve (`x`) com sobra nas bordas ou pré-renderize o zoom em vídeo.
- Quando um elemento permanece na mesma posição entre dois cortes seguidos (como o primeiro painel de um layout duplo), mantenha-o imóvel e anime apenas a entrada do elemento novo.
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
- Ao derivar versão 9:16 de um projeto 16:9 (ou vice-versa), reaproveite o mesmo mapa de tempos e cortes e troque apenas o layout geométrico: lado a lado vira empilhado e grades horizontais viram verticais, respeitando as zonas seguras (topo `>= 130 px`, base `>= 185 px`). Nunca adapte cortando as laterais do 16:9.

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
- Som de passagem coincide com o meio do movimento: no máximo 1 por trecho/bloco (até 3 em vídeos curtos de até 90 s; em vídeos longos divididos em capítulos, no máximo 1 por capítulo).
- Sem narração, a música fica abaixo dos efeitos para a ação ser ouvida.
- Com narração, a música não tem melodia que dispute com a fala nem automação de volume; na síntese, concentre fundamentais e harmônicos abaixo de `600 Hz`, deixando a faixa de inteligibilidade da voz (`800–3000 Hz`) livre.
- Voz gerada tem plano em `roteiro/`: ritmo, curva de energia, pausas e palavras de ênfase por trecho.
  "Natural" ou "expressivo" não é direção.
- Em voz gerada (TTS), escreva URLs, siglas e termos compostos de forma fonética no script de locução (`"cria gestão ponto com"`), mantendo a grafia oficial nos textos de tela e nas legendas.
- Gere primeiro o trecho mais difícil da voz e mostre a quem pediu. O resto só depois da aprovação.
  Mudou voz, modelo ou velocidade: nova amostra.
- Quando uma gravação única for dividida em blocos ou episódios, normalize o áudio inteiro em duas passadas (`loudnorm` linear) antes de fatiar. Para cortar entre blocos, use o timestamp do Whisper só como referência e corte no meio do silêncio real medido com `silencedetect`.

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
- Selos, cabeçalhos e marcas fixas de canto encerram seu `data-duration` no exato corte em que entra a cena de placar, resumo ou cartão final (CTA), sem sobrepor o fechamento.
- Todo `.gif` ou clipe de `brutos/` é convertido em `tools/` para `.mp4` mudo (`30 fps`, `yuv420p`) em `assets/vid/`. Na composição, tags `<video>` ficam sempre no nível raiz (`#root`) com `data-start` e `data-duration` próprios, nunca aninhadas dentro de outra cena temporizada.
- Em scripts de preparo (`tools/`), remova faixas pretas de capturas (`letterbox`) e limite a ampliação de imagens a no máximo `3,2x` do tamanho original (com Lanczos). Imagem pequena fica menor no painel em vez de estourar borrada.
- Com voz e música, entregue também as faixas em WAV com a duração completa, para remixar depois.
- **Saída de render (`renders/<prefixo>-<slug>/`):** cada conteúdo renderizado fica na sua própria pasta dentro de `renders/` com o prefixo correspondente ao formato (`video-<slug>/`, `reel-<slug>/`, `post-<slug>/` ou `carrossel-<slug>/`), contendo o arquivo renderizado e a `legenda.md` daquela publicação (com `## Título`, `## Rede principal`, `## Legenda` e `## Texto alternativo (Alt Text)`).
- **Re-renderização na mesma pasta:** novas renderizações ou ajustes sobre o mesmo conteúdo **mantêm e sobrescrevem os arquivos na mesma pasta `renders/<prefixo>-<slug>/`**, nunca criando outra pasta (`-v2`, `-novo`, `-copia`) para a mesma peça.
- Dependência nova é instalada nesta pasta, nunca no sistema.

## Verificação

- Antes do render final, gere prancha de quadros de cada cena e confira pose, continuidade,
  enquadramento, luz, clareza e posicionamento: revise se os componentes permanecem estáveis sem
  tremor entre quadros e se nenhuma linha, borda ou cursor atravessa textos.
- Depois do render, inspecione quadros reais, inclusive os dois lados de cada corte.
- Confira duração, resolução, sincronia de som e imagem, LUFS e pico.
- Achou um defeito: procure o mesmo tipo de defeito no vídeo inteiro antes de corrigir.
- Com outro título, o vídeo serviria para outro assunto? Se sim, a direção está genérica: volte ao `SPEC.md`.
- Corrija e renderize de novo. Entregue só depois de tudo aprovado.

## Relatório

Registre em `REVIEW.md`: decisões tomadas, fatos e fontes, divergências, reconstruções de interface,
efeitos com seus tempos, LUFS e pico de cada faixa (em vídeo), métricas de lâminas e legenda (em post/carrossel) e o resultado da verificação.

## Posts e carrosséis

Valem para projetos `post-*` (imagem única ou carrossel em HTML renderizado para PNG e PDF). Paleta, veracidade e preparo de mídia seguem as mesmas regras acima.

### Formatos e dimensões por rede

Todas as lâminas de um carrossel têm **exatamente a mesma dimensão em pixels** (a Lâmina 1 trava a proporção da postagem inteira nas plataformas).

| Formato (`bin/novo-post`) | Resolução | Proporção | Onde usar | Limite de lâminas |
| --- | --- | --- | --- | --- |
| `retrato` (padrão) | `1080 × 1350 px` | `4:5` | Instagram Feed, LinkedIn (PDF), Threads, Facebook | Até 20 no Instagram/Threads; até 300 pág. no LinkedIn (ideal: 5 a 10) |
| `grade` | `1080 × 1440 px` | `3:4` | Instagram quando a capa precisa casar sem corte com a grade 3:4 do perfil | Até 20 no Instagram (ideal: 5 a 10) |
| `quadrado` | `1080 × 1080 px` | `1:1` | Multiplataforma universal, Instagram, LinkedIn, X, Pinterest | Até 20 no Instagram; até 10 em anúncios |
| `vertical` | `1080 × 1920 px` | `9:16` | TikTok (Modo Foto), Stories, capa de Reels | Até 35 no TikTok (ideal: 5 a 12) |
| `paisagem` | `1600 × 900 px` | `16:9` | X (Twitter), LinkedIn imagem única horizontal | Até 4 imagens em grade no X |
| `pin` | `1000 × 1500 px` | `2:3` | Pinterest (Pin estático ou carrossel) | 2 a 5 lâminas no Pinterest |

### Zonas seguras e grade do perfil

- **Margens gerais (`4:5`, `3:4`, `1:1`, `2:3`):** mantenha textos, logos e elementos de leitura a pelo menos **`60 px` das bordas laterais** e **`80 px` do topo e da base**. Fundos, texturas e elementos marcados com `.sangria` (corte contínuo entre lâminas vizinhas) vão até a borda.
- **Conflito Feed `4:5` vs. Grade `3:4` do Instagram (Lâmina 1):** a grade do perfil do Instagram exibe miniaturas em `3:4`. Quando o carrossel é `4:5` (`1080 × 1350 px`), o perfil corta as laterais (mantendo os `1012 px` centrais) ou, em pré-visualizações quadradas/compactas, corta até `135 px` do topo e da base. Na **Lâmina 1**, mantenha o título principal, o rosto e o gancho na caixa central segura (`x` entre `80` e `1000 px`, `y` entre `135` e `1215 px`).
- **Formato vertical (`9:16`, `1080 × 1920 px`):** respeite **`>= 130 px` no topo**, **`>= 185 px` na base** e **`>= 60 px` na lateral direita** (onde ficam os botões de curtir, comentar e compartilhar do TikTok/Reels/Stories).

### Estrutura narrativa do carrossel

Planeje cada lâmina em `SPEC.md` antes de escrever o HTML. O ponto ótimo de retenção fica entre **5 e 10 lâminas** (abaixo de 4 entrega pouco valor; acima de 10 exige ritmo muito rápido para evitar fadiga de deslize):

1. **Lâmina 1 — Gancho (Capa / Outdoor):** concentra 80% do resultado. Deve abrir uma lacuna de curiosidade, mostrar um contraste claro ("o erro vs. o acerto"), uma promessa específica ou um dado real verificado. Frase principal curta (**máximo de 8 a 10 palavras**), mais uma pista visual de continuidade (numeração `01/05`, seta ou elemento visual sangrando na borda direita).
2. **Lâmina 2 — Segunda capa e contexto:** no Instagram, quando a pessoa passa pela Lâmina 1 sem deslizar, o algoritmo costuma reentregar o post mais tarde começando pela **Lâmina 2**. Ela deve fazer sentido sozinha: valide a dor, mostre por que o jeito comum falha ou apresente a premissa central.
3. **Lâminas centrais (3 até N−2) — Desenvolvimento:** uma única ideia por lâmina. Use progressão lógica (passo a passo numerado, antes/depois, mito/verdade, anatomia de um caso). Nunca jogue um bloco de texto corrido: divida em **1 título de ação + 1 argumento curto ou visual demonstrativo**.
4. **Penúltima lâmina (N−1) — Resumo salvável:** sintetize o método em um checklist, tabela rápida ou mapa mental que funcione como cola de consulta. É a lâmina desenhada para gerar **salvamentos** (*saves*).
5. **Última lâmina (N) — Chamada para ação (CTA):** uma única instrução clara e de baixo atrito (salvar o post, enviar para alguém que passa pelo problema, comentar uma palavra-chave ou acessar o link da bio/comentários).

### Tipografia, contraste e continuidade visual

- **Regra de duas fontes:** no máximo **2 famílias tipográficas** por post (uma de impacto para títulos/números e uma limpa para corpo; uma 3ª monoespaçada é permitida apenas para código, métricas ou rótulos técnicos).
- **Tamanhos mínimos em tela de `1080 px` de largura:**
  - Título da capa (Lâmina 1): **`>= 64 px`**
  - Títulos das lâminas internas: **`>= 48 px`**
  - Texto de corpo e itens de lista: **`>= 34 px`** (nunca abaixo de `30 px`)
  - Rótulos secundários, cabeçalho, rodapé e numeração: **`>= 22 px`**
- **Densidade e alinhamento:** no máximo **45 a 55 palavras por lâmina** e linhas de **6 a 8 palavras**. Alinhe blocos de texto de corpo sempre **à esquerda** (texto longo centralizado dificulta a leitura no celular).
- **Contraste e respiro:** relação de contraste mínima de **`4,5:1`** (WCAG AA) entre texto de corpo e fundo, e **`3:1`** em títulos grandes. Mantenha pelo menos **35% da lâmina livre** (espaço negativo).
- **Âncoras fixas e sangria contínua:** cabeçalho (marca/tema), rodapé (arroba/fonte) e indicador de progresso (`02/05`) ficam cravados na **mesma coordenada inteira** em todas as lâminas internas. Na última lâmina (CTA), desligue indicadores de "arraste para o lado". Quando usar sangria contínua (um gráfico ou cartão que atravessa da borda direita da lâmina $N$ para a borda esquerda da lâmina $N+1$), confira na prancha se o encaixe vertical bate no pixel exato.

## Legendas de postagem

Todo vídeo, reel, post ou carrossel traz o texto da publicação em `roteiro/legenda.md` (ou `roteiro/legenda-<slug>.md` quando o projeto tiver múltiplas peças) e entrega uma cópia pronta junto com o arquivo renderizado em `renders/<prefixo>-<slug>/legenda.md`. Assim como no vídeo a legenda de tela não repete o título, na postagem **a legenda da rede nunca copia texto por texto o que já está escrito nas lâminas ou na locução**: a peça visual mostra *o quê*; a legenda entrega *o porquê*, o contexto, o bastidor ou o exemplo prático.

### 0. Título da publicação (`## Título`)

Toda publicação (vídeo, reel, post único ou carrossel) tem obrigatoriamente um **título próprio** na seção `## Título` do `legenda.md`, pronto para plataformas que exigem título separado (YouTube, YouTube Shorts, LinkedIn, Pinterest) e para identificação da peça:

- **Extensão:** até **100 caracteres** (limite técnico do YouTube e do Pinterest), com alvo recomendado entre **40 e 70 caracteres** para aparecer inteiro sem corte em celulares e sugestões.
- **Construção:** inclua a palavra-chave principal do assunto e a promessa, pergunta ou contraste direto. O título não pode repetir palavra por palavra a 1ª linha da seção `## Legenda`.

### 1. Gancho antes do botão "...mais" (Primeiras 2 linhas)

As plataformas truncam a legenda no feed antes do clique em *"mais"* / *"ver mais"*:

- **Limite do corte visível:** até **120 caracteres** na primeira linha (o corte ocorre perto de `125` caracteres no Instagram, `140 a 210` no LinkedIn e `100` no TikTok).
- **Proibido na abertura:** saudações vazias (*"Olá, pessoal!"*, *"Bom dia, rede!"*, *"No post de hoje vamos falar sobre..."*), fileira de emojis no início ou repetição literal da frase da Lâmina 1.
- **Fórmula da 1ª linha:** comece com uma tese contraintuitiva, um número concreto verificado, o custo real de um erro comum ou uma pergunta direta que obrigue o clique em *"mais"*.
- **2ª linha (ponte):** após uma quebra de linha, entregue em 1 frase o que a pessoa ganha lendo as lâminas ou o texto abaixo.

### 2. Corpo do texto e escaneabilidade

- **Parágrafos curtos:** máximo de **1 a 3 linhas por parágrafo** (até **45 palavras** por bloco), sempre separados por uma linha em branco. Blocos maciços de texto são reprovados na verificação.
- **Marcadores:** sempre que listar 3 ou mais pontos na legenda, use lista com marcadores (`-` ou `•`) ou numeração (`1.`, `2.`, `3.`), com uma ideia por linha.
- **Tom por plataforma:**
  - **Instagram e Threads:** direto, conversacional e prático, como quem explica para uma pessoa só (*"você"*).
  - **LinkedIn:** analítico, voltado a decisões reais, bastidores técnicos, números medidos e aprendizados de mercado.
  - **TikTok (Modo Foto):** enxuto, complementar ao visual e rico nos termos exatos que o público digita na busca.

### 3. Extensão alvo e limites por rede

| Rede | Extensão recomendada (carrossel / vídeo denso) | Extensão recomendada (post / short direto) | Limite técnico da plataforma |
| --- | --- | --- | --- |
| **YouTube / Shorts** | Título até `70` chars (máx. `100`) + descrição de `600 a 2.000` caracteres com capítulos | Título até `70` chars + descrição de `150 a 500` caracteres | `100` (título) / `5.000` (descrição) |
| **Instagram** | `400 a 1.200` caracteres (70 a 200 palavras) | `150 a 400` caracteres | `2.200` caracteres |
| **LinkedIn** | `800 a 1.800` caracteres (130 a 300 palavras) | `400 a 900` caracteres | `3.000` caracteres |
| **TikTok (Modo Foto)** | `150 a 600` caracteres | `80 a 250` caracteres | `4.000` caracteres |
| **Threads** | `200 a 450` caracteres por nota | `100 a 300` caracteres | `500` caracteres |
| **X (Twitter)** | Fio numerado (`1/N`), até `260` caracteres por post | Até `240` caracteres | `280` caracteres (conta padrão) |
| **Pinterest** | Título até `100` caracteres (foco nos `50` iniciais) + descrição de `150 a 400` caracteres | `100 a 250` caracteres | `100` (título) / `500` (descrição) |

### 4. Chamada para ação (CTA) na legenda

Feche o corpo da legenda com **uma única chamada para ação**, alinhada ao objetivo do `BRIEF.md` e à última lâmina:

- **Para salvamento (retenção e autoridade):** *"Salve este post para consultar antes de [ação específica]."*
- **Para compartilhamento (alcance orgânico):** *"Mande para a pessoa do seu time que cuida de [assunto]."*
- **Para comentários (conversa ou automação):** faça uma pergunta fechada de escolha fácil (*"Qual dos passos (1, 2 ou 3) trava mais aí hoje?"*) ou peça uma palavra-chave específica.
- Nunca empilhe múltiplos pedidos no mesmo fechamento (*"curta, comente, salve e ative o sininho"*).

### 5. SEO social, hashtags e texto alternativo (Alt Text)

Os algoritmos de recomendação indexam o texto da legenda, o OCR das lâminas e o texto alternativo como motor de busca:

- **Palavras-chave naturais:** inclua os 2 ou 3 termos principais de busca do tema de forma natural nas **2 primeiras linhas da legenda** e no **título da Lâmina 1**.
- **Hashtags:** use de **3 a 5 hashtags** específicas do assunto e do nicho, posicionadas na última linha da legenda após uma linha em branco. Nunca coloque hashtags no meio de frases, nunca passe de 5 hashtags e nunca use tags genéricas de spam (`#fyp`, `#foryou`, `#viral`, `#instagood`, `#like4like`).
- **Texto alternativo (`Alt Text`):** obrigatório em `roteiro/legenda.md` para **cada lâmina do post/carrossel** (1 frase objetiva de até **125 caracteres por lâmina**, descrevendo o visual e transcrevendo a ideia central para leitores de tela e indexação de busca).

## Looks disponíveis

Use só quando pedido ou quando o `BRIEF.md` citar.

- **Cartões claros**: fundo quase branco, cartões flutuantes com sombra em
  3 camadas, Poppins, destaque terracota `#D97757`.
- **Editorial quente**: creme `#F0EEE6`, tinta `#1F1E1D`, argila `#D97757`,
  serifa elegante nos títulos.
- **Argila 3D**: stop motion em Three.js, luz quente de luminária com luz fria da lua.
