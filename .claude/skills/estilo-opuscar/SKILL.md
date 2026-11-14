---
name: estilo-opuscar
description: Aplica qualquer um dos 99 estilos do catálogo visual em .cache/lemo-opuscar/ dentro do fluxo nativo do HyperCut/HyperFrames. Use sempre que pedirem um vídeo em um estilo visual específico (ex.: swiss-motion, midcentury-toon, blueprint, risograph, teardown, ukiyoe, watercolor, chalkboard, paper-lantern, pixel art, aquarela, xilogravura, desenho técnico, colagem) ou pedirem sugestão de estilo visual para um vídeo novo em projetos/ ("que estilo combina com esse tema?", "sugere um estilo de vídeo"), mesmo sem citar Lemo-Opuscar.
---

# Estilo Opuscar no HyperCut

Esta skill une a **direção de arte dos 99 estilos do Lemo-Opuscar** ao **fluxo nativo do HyperCut** (`bin/novo-video`, `bin/hf`, `PRODUCAO.md`, `bin/render-video`, `renders/video-<slug>/legenda.md`).

> **Regra de motor:** não use `core/render/video.mjs`, `core/render/mux.sh`, `playwright-core` nem `core/tts/` do Lemo-Opuscar. Todo vídeo nasce e renderiza em `projetos/<nome>/` com `bin/hf` e `bin/render-video`.

## 1. Localizar a biblioteca e o estilo

A biblioteca fica em `.cache/lemo-opuscar/`. Se não existir, instale com:

```bash
bin/instalar-opuscar
```

Para listar ou buscar estilos:

- Índice completo: `.cache/lemo-opuscar/styles/README.md`
- Prompt do estilo: `.cache/lemo-opuscar/styles/<slug>/STYLE.md`
- Guia geral de direção: `.cache/lemo-opuscar/DIRECTOR.md`

**Checagens obrigatórias antes de propor o estilo:**

1. Verifique no `styles/README.md` (ou `style.json`) se o estilo é marcado com `✦` (`image-generation`). Se for, avise quem pediu que o estilo exige imagens geradas externamente antes de começar.
2. Leia `.cache/lemo-opuscar/styles/<slug>/STYLE.md` inteiro e respeite suas restrições de licença (`LICENSE`: docs `CC BY-NC 4.0` com permissão para produzir vídeos próprios/clientes; código de `core/` é `MIT`).

## 2. Criar e configurar o projeto no HyperCut

1. Crie o projeto normalmente na raiz:
   ```bash
   bin/novo-video <nome> [landscape|portrait|square]
   ```
2. Copie o `STYLE.md` escolhido para dentro do projeto, como referência (nunca para `assets/`):
   ```bash
   cp .cache/lemo-opuscar/styles/<slug>/STYLE.md projetos/<nome>/referencias/estilo.md
   ```
3. Preencha `projetos/<nome>/BRIEF.md` citando `referencias/estilo.md` e declare em `projetos/<nome>/DESIGN.md` a paleta e as fontes do estilo (substituindo a paleta escura padrão, conforme autorizado pelo `PRODUCAO.md`).
4. Escreva o planejamento cena a cena em `projetos/<nome>/SPEC.md` aplicando a gramática de câmera, transições e ritmo do `STYLE.md` + `DIRECTOR.md`.

## 3. Traduzir o estilo para o HyperFrames

Siga sempre `AGENTS.md` e `PRODUCAO.md` do projeto:

- **Cenas em `compositions/`:** uma cena por arquivo (`compositions/cena-01.html`...), conectadas no `index.html` com `data-composition-src`, `data-composition-id`, `data-start`, `data-duration` e `class="clip"`.
- **Desenho em código (`<canvas>`, SVG ou Three.js):**
  - Para manter o render 100% determinístico e compatível com `bin/hf`, dirija o desenho de cada cena por um estado `{ t: 0 }` ligado a uma timeline GSAP `{ paused: true }`:
    ```js
    const state = { t: 0 };
    const tl = gsap.timeline({ paused: true });
    tl.to(state, { t: DUR, duration: DUR, ease: "none", onUpdate: () => draw(state.t) }, 0);
    window.__timelines["cena-01"] = tl;
    ```
  - Estilos com estética *stop-motion* / *on twos* (ex.: `midcentury-toon`, `rubber-hose`, `crayon-book`) quantizam o jitter/poses para 12 fps (`Math.floor(t * 12)`), enquanto textos HTML permanecem cravados em coordenadas inteiras (sem tremor de subpixel).
- **Módulos MIT reutilizáveis de `.cache/lemo-opuscar/core/`:**
  - Quando útil, copie apenas o arquivo necessário para `projetos/<nome>/compositions/` (ex.: `core/lib.js` para ruído/easing determinístico, `core/three/post.js` para DoF/GTAO em Three.js, `core/post/crt.js` para pass WebGL2 CRT/VHS), sem criar dependência de caminho fora do projeto.
- **Zonas seguras e legibilidade (`PRODUCAO.md`):**
  - Em `portrait` (`1080×1920`), mantenha textos e cartões dentro de `topo >= 130 px`, `base >= 185 px` e `laterais >= 60 px`, com texto legível `>= 28–30 px`.
  - Use `ease` em `transform` (`x`, `y`, `scale`, `scaleX`) e `clipPath`, evitando animar `left`/`top`/`width`/`height` no GSAP.

## 4. Áudio, verificação e entrega

- **Música:** sintetize em `projetos/<nome>/tools/gerar_musica.py` gerando `assets/audio/musica.wav` no gênero pedido pelo `STYLE.md`. Se precisar de instrumentos reais CC0 ou cordas físicas, os módulos MIT `.cache/lemo-opuscar/core/audio/sampler.py` e `pluck.py` podem ser usados dentro do script em `tools/`.
- **Efeitos sonoros:** use `sons/sons kit` / `sons/sons buscar` / `sons/sons gerar` normalmente para `assets/sfx/` e insira como `<audio id="..." data-start="..." data-duration="...">` no `#root`.
- **Legenda de postagem:** preencha `projetos/<nome>/roteiro/legenda.md` com `## Título`, `## Rede principal`, `## Legenda` e `## Texto alternativo (Alt Text)`.
- **Fluxo de verificação obrigatório:**
  1. `../../bin/hf check --json` (0 erros)
  2. `../../bin/hf snapshot --at ...` e inspecionar os quadros reais
  3. `../../bin/hf preview --background` para aprovação antes da entrega final
  4. `../../bin/render-video . --quality looks` (ou `delivery`)
  5. Conferir duração com `ffprobe`, medir LUFS/pico com `medir-mixagem` (`-14 LUFS`, pico `<= -1 dBTP`) e registrar tudo em `REVIEW.md`.
