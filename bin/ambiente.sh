# Ambiente desta pasta. Fonte unica para bin/hf, bin/com-ambiente e o hook da Claude Code.
# Uso: HF_ROOT=<raiz> source bin/ambiente.sh
HF_ROOT="${HF_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64) hf_alvo=linux/x64 ;;
  Linux-aarch64) hf_alvo=linux/arm64 ;;
  Darwin-arm64) hf_alvo=darwin/arm64 ;;
  Darwin-x86_64) hf_alvo=darwin/x64 ;;
esac
hf_ffmpeg="$HF_ROOT/node_modules/ffmpeg-static"
hf_ffprobe="$HF_ROOT/node_modules/ffprobe-static/bin/$hf_alvo"
hf_whisper="$HF_ROOT/.cache/hyperframes/whisper/whisper.cpp/build/bin"
# bin/instalar-ffmpeg traz a versao com as correcoes de seguranca; sem ela, fica a do npm.
if [ -x "$HF_ROOT/.cache/ffmpeg/atual/ffmpeg" ]; then
  hf_ffmpeg="$HF_ROOT/.cache/ffmpeg/atual"
  hf_ffprobe="$HF_ROOT/.cache/ffmpeg/atual"
fi

# bin/instalar-whisper-cuda traz o whisper-cli em GPU, usado pela skill reel; sem ele, fica o de CPU.
hf_whisper_lib="$hf_whisper"
if [ -x "$HF_ROOT/.cache/whisper-cuda/build/bin/whisper-cli" ]; then
  hf_whisper="$HF_ROOT/.cache/whisper-cuda/build/bin"
  hf_whisper_lib="$hf_whisper:$HF_ROOT/.cache/whisper-cuda/toolkit/lib"
fi

# HyperFrames
export HYPERFRAMES_FFMPEG_PATH="$hf_ffmpeg/ffmpeg"
export HYPERFRAMES_FFPROBE_PATH="$hf_ffprobe/ffprobe"
export HYPERFRAMES_CACHE_DIR="$HF_ROOT/.cache/hyperframes"
# O init nao mexe nas skills: elas vem do plugin do agente ou de bin/instalar-skills.
export HYPERFRAMES_SKIP_SKILLS=1

# Skill reel (.claude/skills/reel)
export REEL_SKILL="$HF_ROOT/.claude/skills/reel"
export WHISPER_MODEL="$HF_ROOT/.cache/whisper-cpp/ggml-large-v3-turbo.bin"
export VSL_PYTHON="$HF_ROOT/.venv/bin/python"
export VSL_NODE_MODULES="$HF_ROOT/.cache/reel/node_modules"
export FACE_MODEL="$HF_ROOT/.cache/reel/face_landmarker.task"
export CHROME="$(ls -d "$HF_ROOT"/.cache/hyperframes/chrome/chrome-headless-shell/*/*/chrome-headless-shell 2>/dev/null | tail -1)"

export LD_LIBRARY_PATH="$hf_whisper_lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="$hf_ffmpeg:$hf_ffprobe:$hf_whisper:$HF_ROOT/.venv/bin:$PATH"
unset hf_alvo hf_ffmpeg hf_ffprobe hf_whisper hf_whisper_lib
