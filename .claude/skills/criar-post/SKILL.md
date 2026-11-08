---
name: criar-post
description: Cria posts estáticos e carrosséis para Instagram, LinkedIn, TikTok (Modo Foto), Threads, X e Pinterest em HTML renderizado para PNG e PDF, além da legenda completa com gancho, CTA, hashtags e texto alternativo, seguindo as regras do PRODUCAO.md. Use sempre que pedirem para criar post, carrossel, arte de feed, documento PDF de LinkedIn ou legenda de postagem, mesmo sem citar a skill: "cria um carrossel", "faz um post pro Instagram", "monta um carrossel de 7 slides", "faz um carrossel pro LinkedIn", "escreve a legenda desse post". Não use para vídeos ou reels (`bin/novo-video` ou `reel`) nem para analisar post de terceiro (`analisar-post`).
---

# Criar post ou carrossel

Cria projetos `projetos/post-<nome>/` em HTML e CSS, valida tipografia, contraste, margens, zonas seguras e legenda (com título) no Chrome de render da pasta, e entrega tudo agrupado na pasta única `renders/<prefixo>-<slug>/` (`renders/post-<slug>/` para 1 lâmina ou `renders/carrossel-<slug>/` para 2+ lâminas), contendo as lâminas PNG, `prancha.png`, `carrossel-<slug>.pdf` e `legenda.md`. Novas renderizações do mesmo conteúdo atualizam essa mesma pasta, sem criar outra.

## 1. Criar o projeto

Da raiz do HyperCut:

```bash
bin/novo-post <nome-em-kebab-case> [formato] [laminas]
```

| Formato | Resolução | Quando escolher |
| --- | --- | --- |
| `retrato` (padrão) | `1080 × 1350 px` (`4:5`) | Instagram Feed, LinkedIn PDF, Threads, Facebook |
| `grade` | `1080 × 1440 px` (`3:4`) | Instagram quando a capa não pode sofrer nenhum corte na grade 3:4 do perfil |
| `quadrado` | `1080 × 1080 px` (`1:1`) | Post multiplataforma universal |
| `vertical` | `1080 × 1920 px` (`9:16`) | TikTok Modo Foto, Stories, capa de Reels |
| `paisagem` | `1600 × 900 px` (`16:9`) | X (Twitter), LinkedIn imagem única horizontal |
| `pin` | `1000 × 1500 px` (`2:3`) | Pinterest |

Quantidade ideal de lâminas em carrossel: **5 a 10 lâminas** (ou `1` para post estático único).

## 2. Planejar antes de construir

1. Preencha `BRIEF.md` (objetivo, rede principal, formato, promessa e CTA). Se faltar definição essencial que mude o post, pergunte antes.
2. Se houver post de referência, rode a skill `analisar-post` e registre a direção em `referencias/<slug>/ficha.md`.
3. Se houver fotos ou capturas em `brutos/`, trate em `tools/` e grave em `assets/img/` (removendo faixas pretas e respeitando o limite de ampliação de `3,2x` do `PRODUCAO.md`). Nunca aponte as lâminas para `brutos/` ou `referencias/`.
4. Escreva a tabela completa em `SPEC.md`:
   - **Lâmina 01 (Capa / Gancho):** frase curta de impacto (até 8–10 palavras), palavra-chave principal do tema e pista visual de deslize. Na proporção `4:5` (`1080x1350`), mantenha título e elementos vitais entre `y = 135 px` e `y = 1215 px` para não cortar na grade `3:4` do perfil.
   - **Lâmina 02 (Segunda capa / Contexto):** precisa fazer sentido sozinha caso o algoritmo reentregue o carrossel começando por ela.
   - **Lâminas centrais:** uma ideia por lâmina, no máximo 45–55 palavras, corpo alinhado à esquerda (`>= 34 px`) e títulos `>= 48 px`.
   - **Penúltima lâmina:** resumo salvável (checklist, quadro comparativo ou síntese).
   - **Última lâmina (CTA):** chamada única e direta, sem indicador de "deslize".

## 3. Construir lâminas e legenda

1. Edite `slides/base.css` (se o projeto pedir outra paleta do `DESIGN.md` ou looks `.tema-claro` / `.tema-editorial`) e cada `slides/slide-XX.html`.
2. Escreva `roteiro/legenda.md` seguindo o `PRODUCAO.md`:
   - **Título (`## Título`):** obrigatório para toda publicação (até **100 caracteres**, ideal entre **40 e 70 caracteres** para não cortar no YouTube, Shorts, LinkedIn e Pinterest), trazendo a palavra-chave principal e a promessa ou pergunta direta.
   - **Gancho (1ª linha de `## Legenda`):** até **120 caracteres** (antes do botão *"...mais"*), sem saudação vazia e **sem repetir literalmente o título da Lâmina 01 nem o `## Título`**.
   - **Corpo:** complementar às lâminas (o *porquê*, bastidor ou exemplo), em parágrafos curtos de **1 a 3 linhas** separados por linha em branco.
   - **CTA:** uma única ação clara no fechamento.
   - **Hashtags:** **3 a 5 hashtags** específicas do nicho na última linha (nunca tags genéricas como `#fyp` ou `#instagood`).
   - **Texto alternativo (`Alt Text`):** uma linha `- slide-XX: ...` para cada lâmina (até 125 caracteres), descrevendo o visual e a mensagem central.

## 4. Conferir, renderizar e revisar

```bash
bin/render-post post-<nome> --checar     # valida DOM, fontes, contraste, margens, título e legenda
bin/render-post post-<nome>              # grava na pasta única renders/<prefixo>-<slug>/ (PNGs, prancha.png, PDF e legenda.md)
```

1. Corrija qualquer `ERRO` apontado por `bin/render-post`.
2. Abra e **olhe `renders/<prefixo>-<slug>/prancha.png`** (que inclui todas as lâminas lado a lado e a simulação da Capa recortada na Grade `3:4` do perfil). Confira se não há texto cortado, linha atravessando letras ou desalinhamento entre cabeçalhos e rodapés.
3. Em novas renderizações ou ajustes sobre o mesmo conteúdo, rode `bin/render-post` novamente sem mudar o `--slug`: ele manterá tudo na mesma pasta `renders/<prefixo>-<slug>/`, sem criar outra.
4. Preencha `REVIEW.md` com as decisões, fontes verificadas e o resultado da checagem, e apresente a prancha e a legenda à pessoa.
