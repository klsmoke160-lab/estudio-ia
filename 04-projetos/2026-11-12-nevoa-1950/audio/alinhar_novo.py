"""Alinha o roteiro com a narração nova (áudio B): descobre quando cada frase começa e termina,
abre um intervalo para o título depois da abertura e grava timeline_novo.json + narracao_video.wav."""
import json, re, subprocess, pathlib, unicodedata, difflib
from faster_whisper import WhisperModel
p=pathlib.Path(__file__).parent; N=p.parent/"narracao"; SRC=N/"narracao_final_B.wav"
norm=lambda s:re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",s.lower()).encode("ascii","ignore").decode())
cache=p/"palavras_B.json"
if cache.exists(): aw=json.load(open(cache))
else:
    m=WhisperModel("small",compute_type="int8")
    segs,_=m.transcribe(str(SRC),language="pt",word_timestamps=True,condition_on_previous_text=False)
    aw=[dict(w=w.word,a=w.start,b=w.end) for s in segs for w in s.words]; json.dump(aw,open(cache,"w"))
T=json.load(open(p/"timeline_completa.json")); F=T["frases"]
# fichas do roteiro e do áudio
S=[];own=[]
for k,f in enumerate(F):
    for t in norm(f["texto"]).split(): S.append(t); own.append(k)
A=[];at=[]
for w in aw:
    for t in norm(w["w"]).split(): A.append(t); at.append((w["a"],w["b"]))
sm=difflib.SequenceMatcher(None,S,A,autojunk=False)
ta=[None]*len(S); tb=[None]*len(S); casadas=0
for blk in sm.get_matching_blocks():
    for d in range(blk.size): ta[blk.a+d]=at[blk.b+d][0]; tb[blk.a+d]=at[blk.b+d][1]; casadas+=1
print("palavras do roteiro casadas com o áudio:",casadas,"de",len(S),f"({100*casadas/len(S):.1f}%)")
ini=[None]*len(F); fim=[None]*len(F)
for i,k in enumerate(own):
    if ta[i] is not None:
        if ini[k] is None: ini[k]=ta[i]
        fim[k]=tb[i]
# preenche frases sem nenhuma palavra casada por interpolação
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(SRC)],capture_output=True,text=True).stdout)
for k in range(len(F)):
    if ini[k] is None:
        a=next((fim[j] for j in range(k-1,-1,-1) if fim[j] is not None),0.0); b=next((ini[j] for j in range(k+1,len(F)) if ini[j] is not None),dur)
        ini[k]=a+0.1; fim[k]=max(ini[k]+0.3,b-0.1)
for k in range(1,len(F)):
    if ini[k]<fim[k-1]: ini[k]=fim[k-1]+0.02
    if fim[k]<=ini[k]: fim[k]=ini[k]+0.3
# tempo de cada palavra do roteiro (interpola as que não casaram)
pos={}
for i,k in enumerate(own): pos.setdefault(k,[]).append(i)
tw=[]
for k in range(len(F)):
    idx=pos.get(k,[]); a=[ta[i] for i in idx]
    if not idx: tw.append([]); continue
    for j in range(len(a)):
        if a[j] is None:
            l=next((a[x] for x in range(j-1,-1,-1) if a[x] is not None),ini[k]); r=next((a[x] for x in range(j+1,len(a)) if a[x] is not None),fim[k])
            a[j]=(l+r)/2
    tw.append(a)
ult=next(k for k,f in enumerate(F) if "titulo_ini" in f)
GAP=4.6; corte=(fim[ult]+ini[ult+1])/2
out=[]
for k,f in enumerate(F):
    d=GAP if k>ult else 0.0
    g=dict(i=f["i"],texto=f["texto"],cap=f["cap"],ini=round(ini[k]+d,3),fim=round(fim[k]+d,3))
    g["t"]=[round(x+d,3) for x in tw[k]]
    if "titulo_ini" in f: g["titulo_ini"]=round(fim[k]+1.0,3)
    out.append(g)
total=dur+GAP+2.0
json.dump({"total":round(total,3),"frases":out},open(p/"timeline_novo.json","w"),ensure_ascii=False,indent=1)
# áudio do vídeo: narração B com o intervalo do título
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(SRC),"-filter_complex",
 f"[0:a]atrim=0:{corte:.3f},asetpts=N/SR/TB[a];[0:a]atrim={corte:.3f},asetpts=N/SR/TB[b];aevalsrc=0:d={GAP}:s=48000:c=mono[s];[a][s][b]concat=n=3:v=0:a=1[o]",
 "-map","[o]","-ar","48000","-c:a","pcm_s16le",str(N/"narracao_video.wav")],check=True)
print("frases",len(out),"| título em",out[ult]["titulo_ini"],"s | total",round(total/60,2),"min | corte",round(corte,2))
for k in (0,ult,ult+1,len(F)-1): print(k,out[k]["ini"],out[k]["fim"],out[k]["texto"][:60])
