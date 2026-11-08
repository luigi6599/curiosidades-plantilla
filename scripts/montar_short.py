"""Monta un Short a partir de proyecto.json. Uso: python3 -I scripts/montar_short.py proyecto.json
proyecto.json:
{
 "clips_dir": "clips",            # escena01.mp4, escena02.mp4 ...
 "audio": "voz.mp3",
 "palabras": "palabras.json",     # salida de transcribir.py
 "salida": "short.mp4",
 "correcciones": [{"t":37.66,"texto":"no"}],   # opcional: sustituye la palabra que empieza cerca de t (s) por el texto del guion
 "escenas": [ {"n":1, "src_fin":3.1, "dur":3.1}, ... ]   # src_fin: segundos útiles del clip; dur: duración en el vídeo
}
Requiere ffmpeg con libass y minterpolate; fuente Inter Black instalada."""
import json, subprocess, sys, os, tempfile
P = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
tmp = tempfile.mkdtemp(); fps = 30; segs = []
for i, e in enumerate(P["escenas"]):
    n, se, d = e["n"], e["src_fin"], e["dur"]
    z0, z1 = (1.0, 1.09) if i % 2 == 0 else (1.09, 1.0)
    z = f"({z0}+({z1}-{z0})*t/{d})"
    vf = f"trim=0:{se},setpts=PTS-STARTPTS"
    if abs(se-d) > 0.01: vf += f",setpts={d/se:.5f}*PTS"
    vf += (f",minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if d > se*1.2 else f",fps={fps}")
    vf += (f",scale=w='trunc(1080*{z}/2)*2':h='trunc(1920*{z}/2)*2':eval=frame:flags=lanczos,crop=1080:1920,"
           f"format=yuv420p,fade=t=in:st=0:n=3:color=white,trim=0:{d},setpts=PTS-STARTPTS")
    out = os.path.join(tmp, f"seg{n:02d}.mp4"); segs.append(out)
    subprocess.run(["ffmpeg","-v","error","-y","-i",os.path.join(rel(P["clips_dir"]),f"escena{n:02d}.mp4"),
                    "-an","-vf",vf,"-r",str(fps),"-c:v","libx264","-preset","veryfast","-crf","10",out],check=True)
lst = os.path.join(tmp,"list.txt"); open(lst,"w").write("".join(f"file '{s}'\n" for s in segs))
vid = os.path.join(tmp,"video.mp4")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy",vid],check=True)
words = json.load(open(rel(P["palabras"]))); corr = P.get("correcciones", [])
def t(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
ass = ["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 2","","[V4+ Styles]",
"Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
"Style: Sub,Inter Black,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,10,0,2,60,60,330,1","",
"[Events]","Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
for i,(w,s,e) in enumerate(words):
    for c in corr:
        if abs(c['t']-s) < 0.05: w = c['texto']
    nxt = words[i+1][1] if i+1 < len(words) else e+0.2
    end = max(min(nxt, e+0.35) if nxt-e < 0.35 else e+0.15, s+0.12)
    ass.append(f"Dialogue: 0,{t(s)},{t(end)},Sub,,0,0,0,,{{\\fscx125\\fscy125\\t(0,90,\\fscx100\\fscy100)}}{w.strip('.,;:!').upper()}")
sub = os.path.join(tmp,"subs.ass"); open(sub,"w").write("\n".join(ass))
total = sum(e["dur"] for e in P["escenas"])
subprocess.run(["ffmpeg","-v","error","-y","-i",vid,"-i",rel(P["audio"]),"-filter_complex",
  f"[0:v]ass={sub}[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]","-map","[v]","-map","[a]","-t",f"{total-0.07:.2f}",
  "-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p","-r",str(fps),"-c:a","aac","-b:a","192k",
  "-movflags","+faststart",rel(P["salida"])],check=True)
print("Listo:", rel(P["salida"]))
