# Instalação e configuração

Como montar esta área de trabalho do zero. Tudo fica dentro desta pasta: nada é instalado no sistema, exceto os
pré-requisitos abaixo. Uso do dia a dia está no `AGENTS.md`.

Máquina de referência: Linux x86_64, RTX 4060 Ti 8 GB, driver NVIDIA 580, Node 24, Python 3.12, g++ 13.
macOS e Windows com WSL2 não foram testados, e `bin/instalar-ffmpeg` só existe para Linux x86_64.

## Pré-requisitos

| Item | Para quê | Conferir |
| --- | --- | --- |
| Node 20 ou mais novo | CLI do HyperFrames | `node --version` |
| Python 3.12 com `venv` | ferramentas de mídia | `python3 --version` |
| `git`, `curl`, `xz` | baixar e extrair | `git --version` |
| `cmake` e `g++` | compilar o `whisper-cli` com CUDA | `cmake --version` |
| Driver NVIDIA | só para GPU | `nvidia-smi` |
| Um agente de IA | operar a pasta. Veja [Agentes de IA](#agentes-de-ia) | |

Espaço em disco: cerca de 30 GB. Não é preciso instalar CUDA no sistema nem usar `sudo`.

## Passo a passo

### 0. Clonar

```bash
git clone --recurse-submodules https://github.com/WesleyDev184/HyperCut.git
cd HyperCut
```

- `--recurse-submodules` traz a skill reel, que vem do repositório original dela.
- Os vídeos ficam em `projetos/`, que não vai para o git: cada pessoa cria os seus e faz o próprio backup.

Rode tudo nesta raiz.

### 1. CLI do HyperFrames, FFmpeg e Chrome

```bash
npm install
bin/instalar-ffmpeg
bin/hf browser ensure
```

- `npm install` traz o `hyperframes` na versão fixada em `package.json`.
- `bin/instalar-ffmpeg` baixa o FFmpeg 8.1 com checksum para `.cache/ffmpeg/`. Só existe para Linux x86_64.
- `bin/hf browser ensure` baixa o Chrome de render para `.cache/hyperframes/`.

### 2. Python da pasta

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-venv.txt
```

`requirements-venv.txt` guarda as versões exatas em uso: numpy, OpenCV, MediaPipe, Pillow, `yt-dlp` e `curl_cffi`, que o yt-dlp usa para abrir TikTok.

### 3. Transcrição em GPU

Só com GPU NVIDIA. Sem ela, pule para o passo 5: `bin/hf transcribe` segue em CPU.

```bash
bin/instalar-whisper-gpu    # cerca de 6 GB: faster-whisper, cuBLAS, cuDNN e modelo large-v3
```

Instala em `.cache/whisper-gpu/`. A partir daí, `bin/hf transcribe` roda na GPU sem nenhuma outra configuração.

### 4. `whisper-cli` em GPU, para a skill reel

Só com GPU NVIDIA. Leva cerca de 15 min.

```bash
bin/instalar-whisper-cuda   # cerca de 2,5 GB: toolkit CUDA em pacotes da NVIDIA, com sha256 conferido
```

Instala em `.cache/whisper-cuda/`. `bin/ambiente.sh` passa a preferir esse binário sozinho.

A arquitetura padrão é `89`, da série RTX 40. Para outra placa, use a capacidade de computação dela sem o ponto:

```bash
nvidia-smi --query-gpu=compute_cap --format=csv,noheader    # 8.6 vira 86
WHISPER_CUDA_ARCH=86 bin/instalar-whisper-cuda
```

### 5. Skill reel

```bash
mkdir -p .cache/whisper-cpp .cache/reel
curl -L -o .cache/whisper-cpp/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
curl -L -o .cache/reel/face_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
(cd .cache/reel && npm init -y && npm install -D hyperframes@0.7.109 gsap@3.14.2 playwright@1.64.1)
```

O motor do reel roda o `hyperframes` 0.7.109 de propósito: é a versão com que ele foi aprovado.

Sem o passo 4, a skill precisa de um `whisper-cli` de CPU. Ele vem na primeira transcrição do CLI:

```bash
HF_SEM_GPU=1 bin/hf transcribe <algum-audio-curto>
```

### 6. Efeitos sonoros

```bash
sons/sons instalar
git clone https://github.com/Clipwing/skills .cache/clipwing-skills
git -C .cache/clipwing-skills checkout edbefcb
cp -R .cache/clipwing-skills/skills/real-sfx .claude/skills/real-sfx
```

- `sons/sons instalar` traz o earshot para `.cache/earshot/`, com PyTorch de CPU.
- A skill `real-sfx` não vem neste repositório porque a origem não tem licença de redistribuição. Sem ela, só `sons/sons momentos` deixa de funcionar.

### 7. TikTok, opcional

```bash
.venv/bin/pip install curl_cffi==0.17.0
```

A skill `assistir-video` abre YouTube e Instagram sem isso. O TikTok barra o acesso comum, e com `curl_cffi` o yt-dlp se apresenta como navegador e resolve o desafio do site. Instalar é decisão sua: confira os termos do site e use só em vídeo público. Sem ele, baixe o vídeo e passe o arquivo.

## Agentes de IA

O ambiente acima é igual para todos. Muda só como cada agente acha as regras e as skills, e tudo isso já vem no repositório:

| Arquivo | Para quê |
| --- | --- |
| `AGENTS.md` | regras do projeto, fonte única |
| `CLAUDE.md`, `GEMINI.md` | importam `AGENTS.md` e `PRODUCAO.md` |
| `.github/copilot-instructions.md` | manda o Copilot ler os dois |
| `.claude/skills/` | skills do projeto |
| `.agents/skills` | link para `.claude/skills` |
| `bin/com-ambiente` | carrega o ambiente em qualquer comando |

**Modelo:** serve qualquer um que rode comandos no terminal. Para olhar pranchas e snapshots, ele precisa ler imagem. Sem isso, a revisão visual fica para você.

Falta só instalar as skills do HyperFrames, por um dos caminhos abaixo, e abrir o agente nesta raiz. Comece um chat novo depois de instalar.

### Claude Code

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
claude
```

Lê `CLAUDE.md` e `.claude/skills/`. O hook de `.claude/settings.json` carrega o ambiente. As skills do plugin têm prefixo: `/hyperframes:hyperframes`.

### OpenAI Codex

```bash
bin/instalar-skills
codex
```

Lê `AGENTS.md` e `.agents/skills/`.

### Cursor

```bash
bin/instalar-skills
```

Abra a pasta no Cursor. Ele lê `AGENTS.md` e `.claude/skills/`. Confira as skills em **Customize**. Há relatos de falha ao ler `.claude/skills/`: se elas não aparecerem, crie o link `ln -s ../.claude/skills .cursor/skills`.

### Google Antigravity

```bash
npx skills add heygen-com/hyperframes
```

Rode nesta raiz, escolha **Core Skills** e **Antigravity** e abra a pasta. Ele lê `AGENTS.md` e `.agents/skills/`. As skills do HyperFrames caem em `.claude/skills/` pelo link e ficam fora do git.

### Gemini CLI

```bash
gemini extensions install https://github.com/heygen-com/hyperframes --auto-update
gemini
```

Lê `GEMINI.md` e `.agents/skills/`.

### GitHub Copilot

```bash
copilot plugin marketplace add heygen-com/hyperframes
copilot plugin install hyperframes@hyperframes
copilot
```

Lê `.github/copilot-instructions.md` e `.claude/skills/`. Confira com `/skills list`. No VS Code, procure `@agentPlugins` em Extensões, adicione `heygen-com/hyperframes` como marketplace e instale **hyperframes**.

### Windsurf

```bash
bin/instalar-skills
```

Abra a pasta. Ele lê `AGENTS.md` e `.agents/skills/`. O instalador só alcança o Windsurf se `~/.codeium/windsurf` já existir.

### OpenCode

```bash
bin/instalar-skills
opencode
```

Lê `AGENTS.md`, `.claude/skills/` e `.agents/skills/`.

### Outro agente

Rode `bin/instalar-skills` e peça para ele ler `AGENTS.md` e `PRODUCAO.md` antes de começar. As skills são pastas com `SKILL.md`, que dá para abrir como texto comum.

### Conferir

Peça ao agente: "liste as skills deste projeto e diga qual comando carrega o ambiente". Ele deve citar `assistir-video`, `analisar-post`, `criar-post`, `legendas-da-voz`, `medir-mixagem`, `tratar-bruto`, `reel`, `real-sfx` e `bin/com-ambiente`.

## Como o ambiente é carregado

`bin/hf` e `bin/novo-*` carregam `bin/ambiente.sh` sozinhos. Para qualquer outro comando, use `bin/com-ambiente <comando>`.
No seu terminal, também funciona:

```bash
export HF_ROOT="$PWD"; source bin/ambiente.sh
```

Na Claude Code, o hook `SessionStart` de `.claude/settings.json` já faz isso em cada comando.

| Variável | Valor |
| --- | --- |
| `HYPERFRAMES_FFMPEG_PATH`, `HYPERFRAMES_FFPROBE_PATH` | FFmpeg de `.cache/ffmpeg/`, ou o do npm como reserva |
| `HYPERFRAMES_CACHE_DIR` | `.cache/hyperframes` |
| `HYPERFRAMES_SKIP_SKILLS` | `1`: o `init` não mexe nas skills. `bin/instalar-skills` desliga isso |
| `REEL_SKILL`, `WHISPER_MODEL`, `FACE_MODEL`, `VSL_PYTHON`, `VSL_NODE_MODULES`, `CHROME` | skill reel |
| `PATH`, `LD_LIBRARY_PATH` | FFmpeg, `.venv` e `whisper-cli`, com o de CUDA na frente quando existe |
| `HF_SEM_GPU` | não vem definida. Com `1`, `bin/hf transcribe` usa CPU |

## Como a GPU é usada

| Quem chama | Caminho | Motor | Modelo | Medido |
| --- | --- | --- | --- | --- |
| `bin/hf transcribe`, `assistir-video`, `legendas-da-voz` | `bin/hf` → `bin/transcrever-gpu` | faster-whisper, float16 | `large-v3` | 9:08 de áudio em 55 s; em CPU, mais de 20 min |
| skill reel | `whisper-cli` no `PATH` | whisper.cpp com CUDA | `large-v3-turbo` | 1 min de áudio em 3,5 s; em CPU, 31,7 s |

- `bin/hf transcribe` usa `large-v3` seja qual for o `--model` pedido e grava `transcript.json` em `-d` ou na pasta atual.
- O CLI é chamado direto em três casos: importar `.json`, `.srt` ou `.vtt`, pedir outro `--engine` ou passar opção desconhecida.
- Se a GPU falhar, o comando avisa e cai no CPU, sem parar o trabalho.
- `tratar-bruto` procura `whisper-cli` no `PATH` e por isso herda a GPU.

## Verificação

```bash
bin/hf --version                                     # versão do package.json
bin/hf doctor                                        # ambiente do HyperFrames
"$HYPERFRAMES_FFMPEG_PATH" -version | head -1        # n8.1
which whisper-cli                                    # .cache/whisper-cuda/build/bin/whisper-cli
python3 "$REEL_SKILL/corte/scripts/0-checar.py"      # "Tudo pronto."
sons/sons kit --tipo whoosh                          # lista sons
```

Prova da GPU, com um áudio curto qualquer:

```bash
bin/hf transcribe audio.wav -d /tmp/teste --language pt --json     # "engine": "faster-whisper-cuda"
whisper-cli -m "$WHISPER_MODEL" -f audio-16k.wav -l pt -nt 2>&1 | grep ggml_cuda_init
```

## Problemas conhecidos

| Sintoma | Causa | Saída |
| --- | --- | --- |
| `whisper-cli` em CUDA leva o mesmo tempo do CPU | `LD_LIBRARY_PATH` carregou as bibliotecas de CPU primeiro | Confira `ggml_cuda_init` na saída sem `-np`. `bin/ambiente.sh` já põe as de CUDA na frente; abra sessão nova depois de instalar |
| `open() got an unexpected keyword argument 'metadata_errors'` | PyAV novo quebra o `decode_audio` do faster-whisper | Já contornado: `bin/transcrever_gpu.py` lê o áudio com FFmpeg |
| `cannot find -lcudadevrt` no `cmake` | `nvcc.profile` procura `lib64` | Já resolvido no instalador com um link `lib64` |
| `undefined reference ... libcudart.so.12` | link final sem o caminho do toolkit | Já resolvido no instalador com `-rpath-link` |
| Transcrição repete frases ou inventa texto | Modelo preso no contexto do trecho anterior | Já resolvido na GPU: `condition_on_previous_text=False` e VAD. No CPU o defeito continua |
| `transcript.json` apareceu em `brutos/` | O CLI em CPU grava ao lado do áudio | Mova para `roteiro/`. Na GPU, ele fica em `-d` ou na pasta atual |
| `bin/hf render --gpu` não muda nada | O CLI 0.9.9 mostra "encoder GPU", mas passa `libx264` ao FFmpeg, mesmo com `--workers 1`. Saída idêntica byte a byte | Não use `--gpu`. O FFmpeg tem `h264_nvenc` e funciona direto; falta o CLI usar. Testar de novo ao atualizar o HyperFrames |
| Memória da GPU esgotada | `large-v3` em float16 pede cerca de 4 GB | Feche o que usa a placa. Em último caso, `HF_SEM_GPU=1` |

## Atualizar

- **HyperFrames:** só com pedido, junto com as skills do agente, e conferindo os projetos existentes.
- **Python:** depois de mudar `.venv/`, rode `.venv/bin/pip freeze | grep -v curl_cffi > requirements-venv.txt`.
- **Versões da GPU:** ficam fixadas em `bin/instalar-whisper-gpu` e `bin/instalar-whisper-cuda`.

## O que foi testado do zero

Instaladores rodados em pasta limpa em 2026-11-05: `bin/instalar-whisper-gpu` e `bin/instalar-whisper-cuda`.
Os dois produziram binário e modelo que acharam a GPU. Nesse teste, a fonte do whisper.cpp já existia em `.cache/`: o clone
automático para máquina sem ela não foi exercitado. Os passos 1, 2, 5 e 6 foram escritos do que existe nesta máquina e não
foram refeitos em máquina limpa.

Configuração por agente, em 2026-11-05:

- **OpenCode 1.14.48:** testado aqui. Achou as 6 skills pelos dois caminhos, sem duplicar.
- **`bin/instalar-skills`:** testado com pasta pessoal falsa. Chegou a Claude Code, Cursor, Gemini CLI, OpenCode e `~/.agents/skills`.
- **Claude Code:** em uso nesta máquina.
- **Codex, Cursor, Antigravity, Gemini CLI, Copilot e Windsurf:** escritos da documentação de cada um, sem teste. Se algo divergir, abra uma issue.
