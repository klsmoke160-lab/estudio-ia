"""Trata uma narração gravada (DarkPlanner) para um projeto do estúdio:
alinha com roteiro-completo.txt, confere o texto, dá timbre mais natural e redistribui as pausas sem cortar fala.
Só alonga pausas (nunca encurta) e sempre no meio do silêncio entre duas frases.
Uso: uv run python scripts/som/tratar_narracao.py <pasta_do_projeto> <audio> [--linha 0.45] [--curta 0.8] [--capitulo 1.9] [--titulo 5.0] [--so-conferir]
Saídas: narracao/narracao_tratada.wav e .mp3, audio/timeline_novo.json, narracao/conferencia.json"""
import sys, json, re, subprocess, pathlib, unicodedata, difflib, statistics as st
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
P=pathlib.Path(sys.argv[1]); SRC=pathlib.Path(sys.argv[2]); A=sys.argv[3:]
opt=lambda k,d: float(A[A.index(k)+1]) if k in A else d
LINHA,CURTA,CAP,TIT=opt("--linha",0.45),opt("--curta",0.8),opt("--capitulo",1.9),opt("--titulo",5.0); SO="--so-conferir" in A
N=P/"narracao"; N.mkdir(exist_ok=True); (P/"audio").mkdir(exist_ok=True); SR=48000
norm=lambda s:re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",s.lower()).encode("ascii","ignore").decode())
# frases do roteiro: cada linha é um parágrafo; cada frase guarda capítulo e se fecha a linha / o capítulo
F=[]; cap=None
for l in (P/"roteiro-completo.txt").read_text().split("\n"):
    l=l.strip()
    if not l: continue
    if l.startswith("#"):
        cap=l[1:].strip()
        if F: F[-1]["fim_cap"]=True
        continue
    ss=re.split(r"(?<=[.?!:])\s+",l)
    for k,s in enumerate(ss): F.append(dict(texto=s,cap=cap,fim_linha=k==len(ss)-1,fim_cap=False))
bruto=N/"_bruto.wav"; subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(SRC),"-ac","1","-ar",str(SR),"-c:a","pcm_s16le",str(bruto)],check=True)
cache=N/"_palavras.json"
if cache.exists(): aw=json.load(open(cache))
else:
    m=WhisperModel("small",compute_type="int8")
    segs,_=m.transcribe(str(bruto),language="pt",word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
    aw=[dict(w=w.word,a=w.start,b=w.end) for s in segs for w in s.words]; json.dump(aw,open(cache,"w"))
S=[];own=[]
for k,f in enumerate(F):
    for t in norm(f["texto"]).split(): S.append(t); own.append(k)
Aw=[];at=[]
for w in aw:
    for t in norm(w["w"]).split(): Aw.append(t); at.append((w["a"],w["b"]))
sm=difflib.SequenceMatcher(None,S,Aw,autojunk=False); ta=[None]*len(S); tb=[None]*len(S)
for b in sm.get_matching_blocks():
    for d in range(b.size): ta[b.a+d],tb[b.a+d]=at[b.b+d]
cas=sum(x is not None for x in ta); print(f"texto: {cas} de {len(S)} palavras do roteiro reconhecidas no áudio ({100*cas/len(S):.1f}%)")
ini=[None]*len(F); fim=[None]*len(F); c=[0]*len(F); n=[0]*len(F); pos={}
for i,k in enumerate(own):
    n[k]+=1; pos.setdefault(k,[]).append(i)
    if ta[i] is not None:
        c[k]+=1
        if ini[k] is None: ini[k]=ta[i]
        fim[k]=tb[i]
dur=sf.info(str(bruto)).duration
fracas=[dict(i=k,ok=f"{c[k]}/{n[k]}",texto=F[k]["texto"],ouvido=" ".join(w["w"].strip() for w in aw if ini[k] is not None and ini[k]-0.3<=w["a"]<=fim[k]+0.3)) for k in range(len(F)) if c[k]<0.7*n[k]]
print("frases com menos de 70% reconhecido:",len(fracas))
for x in fracas[:30]: print("  ",x["ok"],"|",x["texto"][:70],"| ouvido:",x["ouvido"][:70])
for k in range(len(F)):
    if ini[k] is None:
        a=next((fim[j] for j in range(k-1,-1,-1) if fim[j] is not None),0.0); b=next((ini[j] for j in range(k+1,len(F)) if ini[j] is not None),dur)
        ini[k]=a+0.05; fim[k]=max(ini[k]+0.2,b-0.05)
for k in range(1,len(F)):
    if ini[k]<fim[k-1]: ini[k]=fim[k-1]+0.01
    if fim[k]<=ini[k]: fim[k]=ini[k]+0.2
gaps=[ini[k+1]-fim[k] for k in range(len(F)-1)]
print(f"pausas originais entre frases: mediana {st.median(gaps):.2f} s | p10 {np.percentile(gaps,10):.2f} | p90 {np.percentile(gaps,90):.2f} | duração {dur/60:.2f} min")
json.dump(dict(reconhecido_pct=round(100*cas/len(S),1),fracas=fracas,pausa_mediana=round(st.median(gaps),2)),open(N/"conferencia.json","w"),ensure_ascii=False,indent=1)
if SO: sys.exit()
# timbre: só tira o grave inaudível. O dono ouviu a voz "dobrada" com de-esser e equalização (17/11) e limpa no original: não mexer no timbre da DarkPlanner
limpo=N/"_limpo.wav"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(bruto),"-af",
 "highpass=f=60","-c:a","pcm_s16le",str(limpo)],check=True)
y,_=sf.read(str(limpo),dtype="float32"); y=y.reshape(-1)
# silêncio "vivo": ruído de sala muito baixo, para a pausa não soar como corte digital
rng=np.random.default_rng(3)
def sala(seg): return (rng.normal(0,1,int(seg*SR)).astype(np.float32))*10**(-72/20)
curta=lambda k: len(F[k]["texto"].split())<=4
INTRO=1.5; partes=[sala(INTRO)]; t=INTRO; out=[]; corte_ant=0.0; ult_abertura=max(k for k,f in enumerate(F) if f["cap"]==F[0]["cap"])
for k,f in enumerate(F):
    prox=(fim[k]+ini[k+1])/2 if k+1<len(F) else dur
    seg=y[int(corte_ant*SR):int(prox*SR)].copy(); gap=(ini[k+1]-fim[k]) if k+1<len(F) else 0
    alvo=0.0
    if k+1<len(F):
        if k==ult_abertura: alvo=1.0+TIT
        elif f["fim_cap"]: alvo=CAP
        elif curta(k) or curta(k+1): alvo=CURTA
        elif f["fim_linha"]: alvo=LINHA
    extra=max(0.0,alvo-gap) if gap>=0.10 or f["fim_cap"] or k==ult_abertura else 0.0
    fd=int(0.01*SR)
    if extra>0 and len(seg)>2*fd: seg[-fd:]*=np.linspace(1,0,fd)
    g=dict(i=k+1,texto=f["texto"],cap=f["cap"],ini=round(t+(ini[k]-corte_ant),3),fim=round(t+(fim[k]-corte_ant),3),pausa=round(extra,3))
    idx=pos.get(k,[]); a=[ta[i] for i in idx]
    for j in range(len(a)):
        if a[j] is None:
            l=next((a[x] for x in range(j-1,-1,-1) if a[x] is not None),ini[k]); r=next((a[x] for x in range(j+1,len(a)) if a[x] is not None),fim[k]); a[j]=(l+r)/2
    g["t"]=[round(t+(x-corte_ant),3) for x in a]
    if k==ult_abertura: g["titulo_ini"]=round(g["fim"]+1.0,3)
    partes.append(seg); t+=len(seg)/SR
    if extra>0:
        s=sala(extra); partes.append(s); t+=len(s)/SR
        if k+1<len(F):
            pass
    out.append(g); corte_ant=prox
    if extra>0 and k+1<len(F):  # entrada suave do trecho seguinte
        pass
partes.append(sala(2.0)); total=t+2.0
junto=N/"_junto.wav"; sf.write(str(junto),np.concatenate(partes),SR)
final=N/"narracao_tratada.wav"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(junto),"-af","loudnorm=I=-16:TP=-1.5:LRA=9","-ar",str(SR),"-c:a","pcm_s16le",str(final)],check=True)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(final),"-c:a","libmp3lame","-b:a","192k",str(N/"narracao_tratada.mp3")],check=True)
json.dump(dict(intro=INTRO,total=round(total,3),voz="DarkPlanner (tratada)",frases=out),open(P/"audio"/"timeline_novo.json","w"),ensure_ascii=False,indent=1)
for x in (bruto,limpo,junto): x.unlink()
g2=[out[k+1]["ini"]-out[k]["fim"] for k in range(len(out)-1)]
print(f"pronto: {total/60:.2f} min | pausas agora: mediana {st.median(g2):.2f} s | alongadas: {sum(o['pausa']>0 for o in out)} de {len(out)}")
