#!/usr/bin/env python3
"""Transcricao na GPU com a mesma interface de `hyperframes transcribe`.

Chamado por bin/hf. Saida 3 quer dizer "este caso nao e comigo": bin/hf segue para o CLI em CPU.
Entrega transcript.json em lista de {text, start, end, id}, igual ao do CLI.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

NAO_E_COMIGO = 3
MODELO = "large-v3"

p = argparse.ArgumentParser(add_help=False)
p.add_argument("entrada", nargs="?")
p.add_argument("-d", "--dir")
p.add_argument("-m", "--model")
p.add_argument("-l", "--language")
p.add_argument("-e", "--engine")
p.add_argument("-o", "--output")
p.add_argument("--to")
p.add_argument("--json", action="store_true")
p.add_argument("--no-runtime-install", action="store_true")
p.add_argument("--runtime-install", action="store_true")
p.add_argument("--optional", action="store_true")
p.add_argument("--timeout")
a, resto = p.parse_known_args()

# Importar transcricao pronta, pedir outro motor ou opcao desconhecida: fica com o CLI.
if (resto or not a.entrada or a.engine not in (None, "auto", "whisper")
        or Path(a.entrada).suffix.lower() in {".json", ".srt", ".vtt"}):
    sys.exit(NAO_E_COMIGO)

try:
    import numpy as np
    from faster_whisper import WhisperModel
    t0 = time.time()
    modelo = WhisperModel(MODELO, device="cuda", compute_type="float16")
except Exception as erro:
    print(f"aviso: GPU indisponivel ({str(erro)[:120]})", file=sys.stderr)
    sys.exit(NAO_E_COMIGO)

# Sem PyAV: o av atual quebra o decode_audio do faster-whisper.
ffmpeg = os.environ.get("HYPERFRAMES_FFMPEG_PATH", "ffmpeg")
pcm = subprocess.run([ffmpeg, "-v", "error", "-i", a.entrada, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)

idioma = a.language or ("en" if (a.model or "").endswith(".en") else None)
# Sem contexto do trecho anterior: com ele, o modelo repete frases e inventa texto em fala longa.
segmentos, info = modelo.transcribe(audio, language=idioma, word_timestamps=True, beam_size=5,
                                    condition_on_previous_text=False, vad_filter=True,
                                    vad_parameters=dict(min_silence_duration_ms=300))
palavras = []
for seg in segmentos:
    for w in seg.words or []:
        palavras.append({"text": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2),
                         "id": f"w{len(palavras)}"})

pasta = Path(a.dir or ".").resolve()
pasta.mkdir(parents=True, exist_ok=True)
saida = pasta / "transcript.json"
saida.write_text(json.dumps(palavras, ensure_ascii=False, indent=2), encoding="utf-8")

if a.to:
    cmd = [str(Path(__file__).resolve().parents[1] / "node_modules/.bin/hyperframes"), "transcribe", str(saida), "--to", a.to]
    subprocess.run(cmd + (["-o", a.output] if a.output else []), check=True, stdout=subprocess.DEVNULL)

if a.json:
    print(json.dumps({"ok": True, "engine": "faster-whisper-cuda", "model": MODELO, "detectedLanguage": info.language,
                      "wordCount": len(palavras), "durationSeconds": round(info.duration, 2), "speechOnsetSeconds": None,
                      "transcriptPath": str(saida)}))
else:
    print(f"GPU: {len(palavras)} palavras, {info.duration:.0f} s de audio em {time.time() - t0:.0f} s -> {saida}")
