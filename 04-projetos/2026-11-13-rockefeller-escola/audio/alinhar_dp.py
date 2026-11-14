"""Alinha o roteiro com uma narração gravada (DarkPlanner): acha onde cada frase começa e termina,
limpa o chiado, remonta com as pausas do projeto e grava timeline_novo.json + narracao/narracao_video.wav.
Uso: uv run python 04-projetos/2026-11-13-rockefeller-escola/audio/alinhar_dp.py <audio.mp3>
Depois: NOVO=1 python3 motor/montar.py ... | NOVO=1 python3 audio/mixar.py"""
import json, re, subprocess, pathlib, unicodedata, difflib, sys
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
p=pathlib.Path(__file__).parent; N=p.parent/"narracao"; SRC=pathlib.Path(sys.argv[1]); SR=44100; INTRO=1.5
W=p/"dp"; W.mkdir(exist_ok=True)
norm=lambda s:re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",s.lower()).encode("ascii","ignore").decode())
bruto=W/"bruto.wav"; limpo=W/"limpo.wav"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(SRC),"-ac","1","-ar",str(SR),"-c:a","pcm_s16le",str(bruto)],check=True)
# limpeza leve: graves, chiado, sibilância
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(bruto),"-af","highpass=f=80,afftdn=nr=10:nf=-48:tn=1,deesser=i=0.45:m=0.5:f=0.5,equalizer=f=6500:t=q:w=1.2:g=-3,lowpass=f=11000","-c:a","pcm_s16le",str(limpo)],check=True)
cache=W/"palavras.json"
if cache.exists(): aw=json.load(open(cache))
else:
    m=WhisperModel("small",compute_type="int8")
    segs,_=m.transcribe(str(bruto),language="pt",word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
    aw=[dict(w=w.word,a=w.start,b=w.end) for s in segs for w in s.words]; json.dump(aw,open(cache,"w"))
F=json.load(open(p/"timeline_completa.json"))["frases"]       # só o texto, o capítulo e as pausas vêm daqui
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
print(f"palavras do roteiro casadas com o áudio: {casadas} de {len(S)} ({100*casadas/len(S):.1f}%) | palavras ouvidas: {len(A)}")
ini=[None]*len(F); fim=[None]*len(F); cas=[0]*len(F); tot=[0]*len(F)
for i,k in enumerate(own):
    tot[k]+=1
    if ta[i] is not None:
        cas[k]+=1
        if ini[k] is None: ini[k]=ta[i]
        fim[k]=tb[i]
dur=sf.info(str(limpo)).duration
fracas=[k for k in range(len(F)) if cas[k]<0.6*tot[k]]
print("frases com menos de 60% das palavras reconhecidas:",len(fracas))
for k in fracas[:25]: print("  ",k,f"{cas[k]}/{tot[k]}",F[k]["texto"][:80])
for k in range(len(F)):
    if ini[k] is None:
        a=next((fim[j] for j in range(k-1,-1,-1) if fim[j] is not None),0.0); b=next((ini[j] for j in range(k+1,len(F)) if ini[j] is not None),dur)
        ini[k]=a+0.1; fim[k]=max(ini[k]+0.3,b-0.1)
for k in range(1,len(F)):
    if ini[k]<fim[k-1]: ini[k]=fim[k-1]+0.02
    if fim[k]<=ini[k]: fim[k]=ini[k]+0.3
pos={}
for i,k in enumerate(own): pos.setdefault(k,[]).append(i)
tw=[]
for k in range(len(F)):
    a=[ta[i] for i in pos[k]]
    for j in range(len(a)):
        if a[j] is None:
            l=next((a[x] for x in range(j-1,-1,-1) if a[x] is not None),ini[k]); r=next((a[x] for x in range(j+1,len(a)) if a[x] is not None),fim[k])
            a[j]=(l+r)/2
    tw.append(a)
te=[[tb[i] for i in pos[k]] for k in range(len(F))]
# Correções do roteiro feitas por corte (conferência de fatos de 2026-11-14), sem regravar:
# prefixo da frase -> (palavras a tirar | "TUDO" | None, texto que fica, pausa extra depois de um corte no fim)
CORTES={
 "Descreve crianças doentes":("e escolas que ensinavam latim a filhos de lavradores que mal tinham o que comer","Descreve crianças doentes, tomadas por vermes.",0.35),
 "São valores que, na época":("TUDO",None,0),
 "E quem mais resistia à lei":("não eram as famílias com medo de doutrinação","E quem mais resistia à lei",0.0),
 "Eram donos de fábricas":(None,"eram donos de fábricas, que perdiam mão de obra barata, e pais muito pobres, que perdiam um salário.",0),
 "poucos alunos, tempo integral":("poucos alunos","tempo integral e pesquisa.",0),
 "Uma que ensinasse a plantar":("e a consertar","Uma que ensinasse a plantar melhor, a cuidar da saúde, a cozinhar.",0.35),
}
def corte_de(f):
    return next((v for kk,v in CORTES.items() if f["texto"].startswith(kk)),None)
y,_=sf.read(str(limpo),dtype="float32"); y=y.reshape(-1)
partes=[np.zeros(int(INTRO*SR),dtype=np.float32)]; t=INTRO; out=[]
for k,f in enumerate(F):
    # ritmo natural da voz: as frases do mesmo capítulo ficam coladas, com a pausa original entre elas.
    # Só as pontas de capítulo e do título são aparadas e recebem a pausa do projeto (1,9 s e 6 s).
    cr=corte_de(f)
    if cr and cr[0]=="TUDO": continue
    ant=(fim[k-1]+ini[k])/2 if k>0 else 0.0; prox=(fim[k]+ini[k+1])/2 if k+1<len(F) else dur
    ponta=f["pausa"]>1 or k==len(F)-1; apos=k>0 and F[k-1]["pausa"]>1
    a=max(ini[k]-0.08,ant) if (k==0 or apos) else ant
    b=min(fim[k]+0.16,prox) if ponta else prox
    texto=f["texto"]; tws=list(tw[k]); ik=ini[k]; fk=fim[k]; extra=0.0; trechos=[(a,b)]
    if cr and cr[0]:
        toks=norm(f["texto"]).split(); sub=norm(cr[0]).split()
        i0=next(x for x in range(len(toks)) if toks[x:x+len(sub)]==sub); i1=i0+len(sub)-1
        if i1==len(toks)-1:          # corte até o fim da frase: fica [a, c0] + pausa extra
            c0=(te[k][i0-1]+tw[k][i0])/2 if te[k][i0-1] is not None else tw[k][i0]-0.05
            trechos=[(a,c0)]; fk=c0; tws=tws[:i0]; extra=cr[2]
        elif i0==0:                  # corte no começo da frase: começa na primeira palavra que fica
            c1=(te[k][i1]+tw[k][i1+1])/2 if te[k][i1] is not None else tw[k][i1+1]-0.04
            trechos=[(c1,b)]; ik=tw[k][i1+1]; tws=tws[i1+1:]
        else:                        # corte no meio da frase
            c0=(te[k][i0-1]+tw[k][i0])/2 if te[k][i0-1] is not None else tw[k][i0]-0.05
            c1=(te[k][i1]+tw[k][i1+1])/2 if te[k][i1] is not None else tw[k][i1+1]-0.04
            trechos=[(a,c0),(c1,b)]; tws=tws[:i0]+tws[i1+1:]
        texto=cr[1]; assert len(norm(texto).split())==len(tws),(texto,len(tws))
    elif cr: texto=cr[1]
    def mapear(x):
        acc=0.0
        for x0,x1 in trechos:
            if x<=x1+1e-6: return t+acc+max(0.0,x-x0)
            acc+=x1-x0
        return t+acc
    fd=int(0.012*SR); pedacos=[]
    for n,(x0,x1) in enumerate(trechos):
        s=y[int(x0*SR):int(x1*SR)].copy()
        if n>0 or k==0 or apos or (cr and cr[0] and x0>a): s[:fd]*=np.linspace(0,1,fd)
        if n<len(trechos)-1 or ponta or extra>0: s[-fd:]*=np.linspace(1,0,fd)
        pedacos.append(s)
    seg=np.concatenate(pedacos)
    g=dict(i=f["i"],texto=texto,cap=f["cap"])
    g["ini"]=round(mapear(ik),3); g["fim"]=round(mapear(fk),3); g["t"]=[round(mapear(x),3) for x in tws]
    pausa=(f["pausa"] if f["pausa"]>1 else 0.0)+extra
    if f["pausa"]>5: g["titulo_ini"]=round(g["fim"]+1.0,3)
    g["pausa"]=pausa; partes+=[seg,np.zeros(int(pausa*SR),dtype=np.float32)]; t+=len(seg)/SR+pausa; out.append(g)
total=t+2.0; partes.append(np.zeros(int(2.0*SR),dtype=np.float32))
bruta=W/"montada.wav"; sf.write(str(bruta),np.concatenate(partes),SR)
N.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(bruta),"-af","loudnorm=I=-16:TP=-1.5:LRA=8","-ar","48000","-c:a","pcm_s16le",str(N/"narracao_video.wav")],check=True)
json.dump({"intro":INTRO,"total":round(total,3),"voz":"DarkPlanner","frases":out},open(p/"timeline_novo.json","w"),ensure_ascii=False,indent=1)
fala=sum(g["fim"]-g["ini"] for g in out)
print(f"frases {len(out)} | áudio original {dur/60:.2f} min | vídeo {total/60:.2f} min | fala líquida {fala/60:.2f} min")
for k in (0,13,14,len(out)-1): print(k,out[k]["ini"],out[k]["fim"],out[k]["texto"][:70])
