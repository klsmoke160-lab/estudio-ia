"""Arruma o áudio gerado na DarkPlanner: acha o fim de cada frase, insere pausas (maiores entre capítulos),
tira o pico e normaliza o volume. Uso: uv run python narracao/arrumar_audio.py"""
import json, re, subprocess, pathlib, unicodedata, difflib
from faster_whisper import WhisperModel
p=pathlib.Path(__file__).parent; SRC=p/"darkplanner"/"original.mp3"; W=p/"darkplanner"/"work"; W.mkdir(exist_ok=True)
roteiro=(p.parent/"roteiro-completo.txt").read_text()
norm=lambda s:re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",s.lower()).encode("ascii","ignore").decode())
# primeira frase de cada capítulo (menos o primeiro)
caps=[]; novo=True
for l in roteiro.split("\n"):
    l=l.strip()
    if l.startswith("#"): novo=True; continue
    if l and novo: caps.append(" ".join(norm(re.split(r"(?<=[.?!:])\s",l)[0]).split()[:5])); novo=False
caps=caps[1:]
m=WhisperModel("small",compute_type="int8")
segs,_=m.transcribe(str(SRC),language="pt",word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
words=[w for s in segs for w in s.words]
# frases: termina em palavra com . ? ! :
sent=[];cur=[]
for w in words:
    cur.append(w)
    if re.search(r"[.?!:]$",w.word.strip()): sent.append(cur);cur=[]
if cur: sent.append(cur)
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(SRC)],capture_output=True,text=True).stdout)
firsts=[" ".join(norm(" ".join(w.word for w in x)).split()[:5]) for x in sent]
capidx=set(); pos=0
for c in caps:
    best=max(range(pos,len(sent)),key=lambda j:difflib.SequenceMatcher(None,firsts[j],c).ratio())
    capidx.add(best-1); pos=best  # pausa vai depois da frase anterior
cuts=[0.0]; pauses=[]
for i,s in enumerate(sent[:-1]):
    nxt=sent[i+1]; gap_a=s[-1].end; gap_b=nxt[0].start; mid=(gap_a+gap_b)/2
    txt=" ".join(w.word for w in s); n=len(txt.split())
    first=" ".join(norm(" ".join(w.word for w in nxt)).split()[:5])
    if i in capidx: extra=1.9; tipo="capitulo"
    elif n<=6: extra=0.55; tipo="curta"
    elif txt.strip().endswith("?"): extra=0.5; tipo="pergunta"
    elif txt.strip().endswith(":"): extra=0.3; tipo="dois-pontos"
    else: extra=0.28; tipo="frase"
    cuts.append(mid); pauses.append((mid,extra,tipo))
cuts.append(dur)
lst=[];k=0
for i in range(len(cuts)-1):
    a,b=cuts[i],cuts[i+1]; f=W/f"p{i:04d}.wav"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",f"{a:.3f}","-to",f"{b:.3f}","-i",str(SRC),"-ac","1","-ar","44100","-c:a","pcm_s16le",str(f)],check=True)
    lst.append(f"file '{f.name}'")
    if i<len(pauses):
        s=W/f"s{i:04d}.wav"; d=max(0.0,pauses[i][1])
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",f"{d:.3f}","-c:a","pcm_s16le",str(s)],check=True); lst.append(f"file '{s.name}'")
(W/"lista.txt").write_text("\n".join(lst))
junto=W/"junto.wav"
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",str(W/"lista.txt"),"-c:a","pcm_s16le",str(junto)],check=True)
# limpeza de graves, compressão leve e volume padrão de YouTube (-16 LUFS, pico -1.5 dB)
filtro="highpass=f=70,acompressor=threshold=-22dB:ratio=2:attack=15:release=250:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=8"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(junto),"-af",filtro,"-ar","48000","-c:a","pcm_s16le",str(p/"narracao_arrumada.wav")],check=True)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(p/"narracao_arrumada.wav"),"-c:a","libmp3lame","-b:a","192k",str(p/"narracao_arrumada.mp3")],check=True)
from collections import Counter
print("frases",len(sent),"| capítulos achados",sum(1 for _,_,t in pauses if t=="capitulo"),"de",len(caps),"|",Counter(t for _,_,t in pauses))
print("duração original",round(dur/60,2),"min → nova",round((dur+sum(e for _,e,_ in pauses))/60,2),"min")
json.dump([{"corte":round(a,3),"extra":e,"tipo":t} for a,e,t in pauses],open(p/"darkplanner"/"pausas.json","w"))
