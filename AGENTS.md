# HyperCut: área de trabalho de vídeos, posts e carrosséis

Pasta única para produzir vídeos com HyperFrames (HTML renderizado para MP4) e posts ou carrosséis para redes sociais (HTML renderizado para PNG e PDF), com qualquer agente de IA.
Todo projeto é feito aqui, e o ambiente inteiro mora aqui: CLI, FFmpeg, FFprobe, Chrome, whisper, TTS,
Python e as skills do projeto. Cada vídeo, reel ou post é um projeto isolado em `projetos/`.
As regras abaixo valem para todos eles.

Este arquivo é a fonte única das regras. `CLAUDE.md` e `GEMINI.md` só importam este arquivo e o `PRODUCAO.md`.
**Leia o `PRODUCAO.md` antes de trabalhar em qualquer vídeo, post ou carrossel:** ele traz os padrões de produção e de legendas.

## Escopo

- Vídeo, post ou carrossel novo nasce aqui, nunca em outra pasta.
- Aqui ficam só projetos de mídia e as ferramentas que eles compartilham.
- Trabalhe dentro do projeto pedido. Não altere outro projeto sem pedido explícito.
- Mudanças em `bin/`, `package.json` ou neste arquivo só com pedido explícito.

- **Padrão repetitivo:** quando a mesma sequência de passos, o mesmo script ou a mesma correção se repetir
  entre projetos ou na sessão e valer virar skill, crie-a em `.claude/skills/<nome>/SKILL.md`, a pasta que todos
  os agentes enxergam. Antes, confira se uma skill do HyperFrames ou uma daqui já cobre o caso.
  Avise quem pediu do que criou. Skills existentes continuam sem mudança, salvo pedido.

## Estrutura

```
HyperCut/
├── AGENTS.md          regras gerais (este arquivo)
├── CLAUDE.md          importa AGENTS.md e PRODUCAO.md para a Claude Code
├── GEMINI.md          importa AGENTS.md e PRODUCAO.md para o Gemini CLI
├── PRODUCAO.md        padrões de produção
├── README.md          apresentação do projeto
├── INSTALACAO.md      instalação do zero, configuração por agente, GPU e problemas conhecidos
├── TERCEIROS.md       licenças do que vem de terceiros
├── CONTRIBUTING.md    como contribuir
├── SECURITY.md        como relatar falha de segurança
├── CODE_OF_CONDUCT.md código de conduta
├── requirements-venv.txt  versões exatas de `.venv/`
├── package.json       versão fixa do hyperframes; FFmpeg e FFprobe do npm só como reserva
├── .github/           modelos de issue e de pull request
├── .claude/           skills do projeto e hook que carrega o ambiente na Claude Code
├── .agents/skills     link para `.claude/skills`, para os demais agentes
├── .cache/            Chrome, whisper, TTS, fontes, histórico, dependências da skill reel e earshot
├── .venv/             Python com numpy, OpenCV e MediaPipe
├── bin/
│   ├── ambiente.sh    variáveis do ambiente: fonte única
│   ├── com-ambiente   roda qualquer comando com esse ambiente
│   ├── hf             wrapper do CLI: use sempre este
│   ├── instalar-skills  skills do HyperFrames nos agentes da máquina
│   ├── instalar-ffmpeg  FFmpeg e FFprobe fixados em `.cache/ffmpeg/`, com checksum
│   ├── instalar-whisper-gpu  transcrição em GPU NVIDIA em `.cache/whisper-gpu/`
│   ├── instalar-whisper-cuda  `whisper-cli` em GPU para a skill reel, em `.cache/whisper-cuda/`
│   ├── transcrever-gpu  motor de `hf transcribe` na GPU
│   ├── novo-video     cria projeto padronizado de vídeo
│   ├── novo-reel      cria projeto de vídeo real
│   ├── novo-post      cria projeto de post ou carrossel (`projetos/post-<nome>/`)
│   ├── render-video   valida título/legenda e renderiza MP4 + `legenda.md` em `renders/<prefixo>-<slug>/`
│   ├── render-post    valida e renderiza lâminas HTML e `legenda.md` em `renders/<prefixo>-<slug>/`
│   └── paleta-do-video  sugere paleta a partir de um vídeo
├── modelo/            estrutura copiada para cada vídeo novo
├── modelo-post/       estrutura copiada para cada post ou carrossel novo
├── paletas/           paletas prontas para reel (`escura.json`)
├── sons/              `sons/sons`: acha onde pôr som, usa o kit CC0, busca no Openverse e gera com earshot
└── projetos/          um vídeo, reel ou post por pasta, fora do git
```

### Estrutura de um projeto

```
projetos/<nome>/
├── BRIEF.md           pedido: objetivo, público, formato, tom
├── referencias/       inspiração: vídeos, prints, links. Nunca entra no vídeo
├── roteiro/           narração, textos da tela, transcrições
├── brutos/            mídia original como foi recebida. Nunca editar
├── tools/             scripts de preparo: brutos/ → assets/
├── assets/            só o que o vídeo usa, já tratado
│   ├── img/  vid/  audio/  sfx/  fonts/
├── index.html         composição principal
├── compositions/      uma cena por arquivo
├── renders/           uma subpasta por peça (`video-<slug>/`, `reel-<slug>/`) com o MP4 e `legenda.md`
├── SPEC.md            direção em números (skill, filmes acima de ~15 s)
├── REVIEW.md          revisão final (skill)
├── DESIGN.md          paleta do vídeo: nasce com a paleta escura
├── AGENTS.md, CLAUDE.md  gerados pelo init: regras do framework
└── .hyperframes/      histórico do projeto: nunca apagar
```

- A mídia anda num sentido só: `brutos/` → `tools/` → `assets/` → composição.
- Composições só apontam para `assets/`, nunca para `brutos/` ou `referencias/`.
- Pasta extra em `assets/` é livre quando o vídeo pedir (`assets/sprites/`, `assets/medalhoes/`).
- Pasta nova de trabalho na raiz do projeto entra também no `.hyperframesignore`.
- Mudar a estrutura padrão é mudar `modelo/` (ou `modelo-post/`) e esta seção juntos. Projetos existentes não mudam.

### Estrutura de um post ou carrossel (`projetos/post-<nome>/`)

```
projetos/post-<nome>/
├── BRIEF.md           pedido: objetivo, rede principal, formato, lâminas, CTA
├── referencias/       inspiração: posts, carrosséis e relatórios de `analisar-post`
├── roteiro/
│   └── legenda.md     título (`## Título`), legenda, hashtags (3 a 5) e texto alternativo por lâmina
├── brutos/            fotos e capturas originais como recebidas. Nunca editar
├── tools/             scripts de preparo: brutos/ → assets/
├── assets/            só o que entra nas lâminas, já tratado (`img/`, `fonts/`)
├── slides/            uma lâmina HTML por arquivo (`slide-01.html`...) e `base.css`
├── index.html         mesa de luz: pré-visualização lado a lado, zonas seguras e corte 3:4
├── renders/           uma subpasta por peça (`post-<slug>/` ou `carrossel-<slug>/`) com PNGs, PDF, `prancha.png` e `legenda.md`
├── SPEC.md            mapa lâmina a lâmina e direção da legenda
├── REVIEW.md          revisão final
└── DESIGN.md          paleta do post: nasce com a paleta escura
```

## Comandos

Abra o agente nesta raiz. Em máquina nova, siga o `INSTALACAO.md`.

**Ambiente:** `bin/hf` e `bin/novo-*` carregam tudo sozinhos. Para qualquer outro comando que use FFmpeg, whisper
ou o Python da pasta, inclusive scripts de skill e `sons/sons`, use `bin/com-ambiente <comando>`.
Na Claude Code isso é opcional: o hook de `.claude/settings.json` já carrega `bin/ambiente.sh`.

```bash
bin/novo-video <nome> [landscape|portrait|square]   # padrão: landscape
bin/novo-post <nome> [retrato|grade|quadrado|vertical|paisagem|pin] [laminas]   # padrão: retrato (1080x1350), 5 lâminas

# dentro de projetos/<nome>/ (vídeo)
../../bin/hf check --json
../../bin/hf snapshot --at 1,3,5
../../bin/hf preview --background
../../bin/render-video . --quality looks

# para projetos/post-<nome>/ (post ou carrossel)
bin/render-post post-<nome> --checar
bin/render-post post-<nome>
```

- Use `bin/hf` no lugar de `npx hyperframes`, inclusive nos exemplos das skills e do `CLAUDE.md`
  gerado no projeto. `npx` dentro de um projeto baixaria outra versão, fora deste ambiente.
- `bin/hf transcribe` roda na GPU com `large-v3`, seja qual for o `--model`, e grava `transcript.json` em `-d`
  ou na pasta atual. Sem GPU ou com `HF_SEM_GPU=1`, cai no CPU. A skill reel usa o `whisper-cli` em GPU.
- `npm run dev`, `check`, `render` e `publish` funcionam: `bin/novo-video` aponta os scripts para `bin/hf`.
- Crie projetos só com `bin/novo-video`, nunca copiando outro projeto.

## GPU

Todo processamento pesado tenta primeiro a GPU, pelos caminhos abaixo, com queda para CPU se ela falhar. Detalhes no `INSTALACAO.md`.

- **Transcrição:** `bin/hf transcribe` e `whisper-cli` já usam a GPU.
- **Vídeo em script próprio:** FFmpeg com `-c:v h264_nvenc -preset p7 -tune hq -rc constqp -qp 15`, voltando a `libx264` se falhar.
  Não use `-cq`: ele satura e perde cerca de 4 dB para `libx264 -crf 18`. O arquivo fica cerca de 60% maior.
- **Render do HyperFrames:** segue em CPU. `--gpu` não tem efeito na versão 0.9.9.
- Cheque o encoder real antes de dizer que rodou na GPU: aviso do CLI não prova.

## Padrões

- **Nome:** kebab-case, igual para pasta e MP4 (`lancamento-produto`).
- **Idioma:** textos do vídeo, specs e comentários em pt-BR, salvo pedido contrário.
- **Formato:** `landscape` para 1920x1080, `portrait` para 1080x1920 (Reels, Shorts, TikTok),
  `square` para 1080x1080.
- **Mídia:** todo arquivo usado fica em `assets/` do projeto, sem caminho para fora dele.
  Arquivos em minúsculas e kebab-case (`trono-armadura.jpg`).
- **Renders:** `draft` ao iterar, `looks` para revisar, `delivery` no final. Cada peça renderizada sai em uma pasta própria dentro de `renders/` com o prefixo correspondente (`renders/video-<slug>/`, `renders/reel-<slug>/`, `renders/post-<slug>/`, `renders/carrossel-<slug>/`), contendo o arquivo renderizado e a `legenda.md` daquela publicação (com `## Título` obrigatório, compatível com YouTube/Shorts/LinkedIn/Pinterest). Novas renderizações do mesmo conteúdo atualizam e mantêm a mesma pasta, sem criar outra.
- **Commits e pull requests:** nunca citam agente, modelo ou ferramenta de IA como autor ou coautor. Sem `Co-Authored-By`
  e sem rodapé de ferramenta. Isso vale sobre qualquer padrão do agente.
- **Versão:** uma só para todos os projetos, fixada no `package.json` da raiz. Atualizar só com
  pedido, junto com as skills do HyperFrames, e conferir os projetos existentes depois.

## Skills do projeto

Ficam em `.claude/skills/`, e `.agents/skills` aponta para lá. Além de `reel` e `real-sfx`:

- `medir-mixagem`: mede faixas e master no MP4 final e preenche a tabela do `REVIEW.md`.
- `legendas-da-voz`: gera `compositions/legendas.html` da voz final.
- `assistir-video`: analisa vídeo de referência por link ou arquivo, tudo local.
- `analisar-post`: analisa post ou carrossel de referência por link, imagem ou pasta local, gerando prancha, paleta e relatório.
- `criar-post`: planeja, constrói e renderiza posts e carrosséis (PNG e PDF) e escreve a legenda da postagem.
- `tratar-bruto`: limpa voz, estabiliza e confere spec, só em material próprio.

O agente precisa ler imagem para olhar pranchas e snapshots. Sem isso, a análise fica só nos metadados: avise quem pediu.

## Efeitos sonoros

Tudo pela raiz, com `sons/sons`. O som cai em `assets/sfx/` com pico em -3 dBFS e crédito em `CREDITOS.md`.

```bash
sons/sons momentos <projeto> [--video renders/x.mp4]   # 1. onde colocar: grava em roteiro/
sons/sons kit --tipo whoosh                            # 2. som gravado local, CC0, sem rede
sons/sons pegar <arquivo-do-kit> <nome> <projeto>
sons/sons buscar "whoosh" --cc0                        # 3. som gravado, busca em inglês
sons/sons baixar <id> <nome> <projeto>
sons/sons banco --tipo whoosh                          # 4. sem som certo: 252 sons em código
sons/sons gerar <id-do-banco> <nome> <projeto> --dur 0.8 --apex 0.32
sons/sons forjar <receita> <nome> <projeto> --alvo "a small bubble pop"   # 5. som novo
```

- `forjar` só varia as receitas do earshot (`.cache/earshot/venv/bin/earshot forge --list`). Som de animal ou
  objeto específico fora delas não sai daí.
- O crítico do `forjar` é o próprio earshot: `PASS` não prova que soa bem. Mostre a quem pediu para ouvir.
- `momentos` entrega rascunho. Tempos que a skill não entende ficam de fora e o comando avisa: confira no render.

**Skill `real-sfx`:** use só para análise de posição (`from_hyperframes`, `find_moments`, `suggest_cues`, `beats`,
`critique`), rodando com `.cache/earshot/venv/bin/python`. Ela fica em `.claude/skills/real-sfx`, no commit
`edbefcb` de Clipwing/skills, sem edição, baixada pelo `INSTALACAO.md`. Aqui estas regras valem sobre as dela:

- Som gerado por código é permitido, apesar do "never synthesized" dela.
- A densidade segue o `PRODUCAO.md`. `texture.py` e `bed.py` só com pedido.
- O som entra na composição como `<audio>`. O MP4 de `mix.py` não é a entrega.
- `look.py` não foi testado com o FFmpeg 8.1, que tem `drawtext`. Use `bin/hf snapshot`.

## Vídeo real: skill reel

Gravação de alguém falando para a câmera usa a skill `reel` (`.claude/skills/reel`), que corta e edita
em 9:16. Não serve para vídeo longo de YouTube nem para vídeo sem pessoa falando.

```bash
bin/novo-reel <nome> [video-bruto]    # cria projetos/reel-<nome>/
```

- O projeto segue a estrutura da skill: `corte/`, `motor/`, `render/`, `qa/`, `entrega/`, `assets/`.
  O bruto fica em `brutos/`, e a skill trabalha em `projetos/reel-<nome>/`, não ao lado do vídeo.
- `S` da skill é `$REEL_SKILL`, nunca um caminho fixo na pasta pessoal.
- Dentro de `motor/`, use `npx hyperframes` como a skill manda. O motor roda a versão 0.7.109 com que
  foi aprovado, não `bin/hf`.
- O fluxo da skill substitui as etapas abaixo. `PRODUCAO.md` continua valendo onde não contrariar o motor.
- 30 fps, punch-in, layouts, fontes e legenda ficam como na skill, salvo pedido.
- **Paleta:** `pele-resolvida.json` do projeto define as cores, e isso vale sobre o "não crie uma" da skill.
  Antes de montar, proponha a paleta escura ou a sugerida por `bin/paleta-do-video`. Sem resposta, fica a escura.
- **Música:** trilha sintetizada por código em `motor/assets/`, ligada no `vsl.json` com
  `"music": {"file": "musica.wav", "volume": 0.12}`. Fica pelo menos 13 LU abaixo da voz, sem automação.
  Só fica sem trilha se o `BRIEF.md` pedir.
- **Tomadas:** quem grava repete a frase até ficar satisfeito, então fica a ÚLTIMA tomada completa de cada frase.
  Use uma anterior só se a última tiver defeito audível, e registre a troca. Isso vale sobre a regra
  de "melhor tomada" da skill.
- **Contato visual:** mostre a câmera só enquanto a pessoa olha para a lente. Fora disso, use cena sem câmera.
- `modelo/kit/` e `corte/scripts/` da skill não se alteram. Mudança na skill só com pedido.

## Fluxo de trabalho

Antes de qualquer composição:

1. Crie o projeto com `bin/novo-video`.
2. Preencha `BRIEF.md`. Se faltar campo que muda o vídeo, pergunte antes de seguir.
3. Reúna o material: `referencias/`, `roteiro/` e `brutos/`.
4. Prepare a mídia com scripts em `tools/`, gerando `assets/`.

Depois, com o HyperFrames:

5. Carregue a skill `hyperframes` antes de criar ou editar composição.
6. Procure na skill `hyperframes-registry` antes de construir um visual do zero.
7. Rode `check --json` e corrija todos os erros.
8. Rode `snapshot` nos trechos alterados e olhe os frames.
9. Abra o `preview` e espere aprovação. Check verde não é motivo para renderizar.
10. Depois do render, confira com `ffprobe` se a duração bate com o `data-duration` raiz.

Em posts e carrosséis (`skill criar-post`):

1. Crie o projeto com `bin/novo-post <nome> [formato] [laminas]`.
2. Preencha `BRIEF.md` e planeje cada lâmina e a legenda em `SPEC.md`.
3. Se houver referência, rode `analisar-post` e escreva `referencias/<slug>/ficha.md`.
4. Edite `slides/slide-XX.html` e escreva o título (`## Título`) e a legenda completa (gancho, corpo escaneável, CTA, 3 a 5 hashtags e texto alternativo por lâmina) em `roteiro/legenda.md`.
5. Rode `bin/render-post post-<nome> --checar`, corrija todos os erros, renderize com `bin/render-post post-<nome>`, inspecione `renders/<prefixo>-<nome>/prancha.png` e registre em `REVIEW.md`.

Na Claude Code, as skills do plugin têm prefixo: `/hyperframes:hyperframes`, `/hyperframes:hyperframes-registry`.
