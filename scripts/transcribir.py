"""Transcribe la voz con Whisper y guarda las palabras con tiempos.
Uso: python3 -I scripts/transcribir.py voz.mp3 palabras.json
Requiere: pip install faster-whisper numpy y ffmpeg."""
import sys, subprocess, json, numpy as np
from faster_whisper import WhisperModel
audio, salida = sys.argv[1], sys.argv[2]
raw = subprocess.run(["ffmpeg","-v","error","-i",audio,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True,check=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
m = WhisperModel("small", device="cpu", compute_type="int8")
segs,_ = m.transcribe(a, language="es", word_timestamps=True)
w = [[x.word.strip(), round(float(x.start),2), round(float(x.end),2)] for s in segs for x in s.words]
json.dump(w, open(salida,"w"), ensure_ascii=False)
print(len(w), "palabras ->", salida)
