"""Arruma um áudio gerado na DarkPlanner: acha o fim de cada frase e o começo de cada capítulo,
insere pausas (1,9 s entre capítulos, mais respiro depois de frases curtas), tira o chiado e normaliza o volume.
Uso: uv run python narracao/arrumar_audio.py <entrada.mp3> <nome-saida> [--so-conferir]"""
import json, re, subprocess, pathlib, unicodedata, difflib, sys
from faster_whisper import WhisperModel
p=pathlib.Path(__file__).parent; SRC=pathlib.Path(sys.argv[1]); NOME=sys.argv[2]; SO=("--so-conferir" in sys.argv)
W=p/"darkplanner"/f"work-{NOME}"; W.mkdir(exist_ok=True)
norm=lambda s:" ".join(re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",s.lower()).encode("ascii","ignore").decode()).split())
# primeira frase de cada capítulo (menos o primeiro)
caps=[]; novo=True
for l in (p.parent/"roteiro-completo.txt").read_text().split("\n"):
    l=l.strip()
    if l.startswith("#"): novo=True; continue
    if l and novo: caps.append(norm(re.split(r"(?<=[.?!:])\s",l)[0])); novo=False
caps=caps[1:]
cache=W/"palavras.json"
if cache.exists(): words=json.load(open(cache))
else:
    m=WhisperModel("small",compute_type="int8")
    segs,_=m.transcribe(str(SRC),language="pt",word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
    words=[dict(w=w.word,a=w.start,b=w.end) for s in segs for w in s.words]; json.dump(words,open(cache,"w"))
sent=[];cur=[]
for w in words:
    cur.append(w)
    if re.search(r"[.?!:]$",w["w"].strip()): sent.append(cur);cur=[]
if cur: sent.append(cur)
txt=[norm(" ".join(x["w"] for x in s)) for s in sent]
capidx={}; pos=1
for c in caps:
    cand=range(pos,len(sent))
    best=max(cand,key=lambda j:difflib.SequenceMatcher(None,txt[j][:len(c)+20],c).ratio()-(0.0001*(j-pos)))
    capidx[best-1]=(best,round(difflib.SequenceMatcher(None,txt[best][:len(c)+20],c).ratio(),2)); pos=best+1
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(SRC)],capture_output=True,text=True).stdout)
print("Capítulos achados (minuto | pontuação | começa com):")
for k,(j,r) in sorted(capidx.items()): print(f"  {sent[j][0]['a']/60:5.2f} | {r} | {' '.join(x['w'] for x in sent[j])[:70]}")
if SO or len(capidx)!=len(caps): print("capítulos:",len(capidx),"de",len(caps)); sys.exit()
cuts=[0.0]; pauses=[]
for i,s in enumerate(sent[:-1]):
    nxt=sent[i+1]; mid=(s[-1]["b"]+nxt[0]["a"])/2; t=" ".join(x["w"] for x in s).strip(); n=len(t.split())
    if i in capidx: e,tp=1.9,"capitulo"
    elif n<=6: e,tp=0.5,"curta"
    elif t.endswith("?"): e,tp=0.4,"pergunta"
    else: e,tp=0.0,"frase"
    cuts.append(mid); pauses.append((mid,e,tp))
cuts.append(dur); lst=[]
for i in range(len(cuts)-1):
    f=W/f"p{i:04d}.wav"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",f"{cuts[i]:.3f}","-to",f"{cuts[i+1]:.3f}","-i",str(SRC),"-ac","1","-ar","44100","-c:a","pcm_s16le",str(f)],check=True); lst.append(f"file '{f.name}'")
    if i<len(pauses) and pauses[i][1]>0:
        s_=W/f"s{i:04d}.wav"; subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",f"{pauses[i][1]:.3f}","-c:a","pcm_s16le",str(s_)],check=True); lst.append(f"file '{s_.name}'")
(W/"lista.txt").write_text("\n".join(lst)); junto=W/"junto.wav"
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",str(W/"lista.txt"),"-c:a","pcm_s16le",str(junto)],check=True)
FORTE=("--forte" in sys.argv)
filtro=("highpass=f=80,afftdn=nr=16:nf=-45:tn=1,deesser=i=0.7:m=0.6:f=0.5,equalizer=f=6000:t=q:w=1.0:g=-5,equalizer=f=9000:t=q:w=1.0:g=-4,lowpass=f=9500,loudnorm=I=-16:TP=-1.5:LRA=8") if FORTE else "highpass=f=80,afftdn=nr=10:nf=-48:tn=1,deesser=i=0.45:m=0.5:f=0.5,equalizer=f=6500:t=q:w=1.2:g=-3,lowpass=f=11000,loudnorm=I=-16:TP=-1.5:LRA=8"
out=p/f"{NOME}.wav"; subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(junto),"-af",filtro,"-ar","48000","-c:a","pcm_s16le",str(out)],check=True)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(out),"-c:a","libmp3lame","-b:a","192k",str(p/f"{NOME}.mp3")],check=True)
json.dump([{"corte":round(a,3),"extra":e,"tipo":t} for a,e,t in pauses],open(p/"darkplanner"/f"pausas-{NOME}.json","w"))
print("pronto:",round((dur+sum(e for _,e,_ in pauses))/60,2),"min")
