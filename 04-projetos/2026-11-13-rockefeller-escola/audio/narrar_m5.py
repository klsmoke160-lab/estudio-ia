"""Narração com a voz M5 do Supertonic-3 (motor do VoiceStudio, licença OpenRAIL-M), frase a frase, com linha do tempo.
Rodar com: /home/user/supertonic/.venv/bin/python audio/narrar_m5.py"""
import json, re, subprocess, pathlib, sys
sys.path.insert(0,"/home/user/supertonic")
import numpy as np, soundfile as sf
from supertonic import TTS
from preparar import preparar
p=pathlib.Path(__file__).parent; out=p/"m5"; out.mkdir(exist_ok=True)
VOZ="M5"; INTRO=1.5; TITULO=5.0; SR=44100
tts=TTS(model="supertonic-3"); st=tts.get_voice_style(VOZ)
frases=[]; cap=None
for par in (p.parent/"roteiro-completo.txt").read_text().split("\n"):
    par=par.strip()
    if not par: continue
    if par.startswith("#"):
        cap=par[1:].strip()
        if frases: frases[-1]["pausa"]=1.9
        continue
    ss=re.split(r'(?<=[.?!:])\s+',par)
    for k,s in enumerate(ss): frases.append({"texto":s,"cap":cap,"pausa":0.42 if k<len(ss)-1 else 0.8})
partes=[np.zeros(int(INTRO*SR))]; t=INTRO
for i,f in enumerate(frases,1):
    w,_=tts.synthesize(preparar(f["texto"]),st,lang="pt",total_steps=12,speed=1.0,silence_duration=0.2)
    w=np.asarray(w,dtype=np.float32).reshape(-1)
    # tira silêncio das pontas
    a=np.abs(w); nz=np.where(a>0.01*a.max())[0]; w=w[max(0,nz[0]-int(0.03*SR)):nz[-1]+int(0.08*SR)] if len(nz) else w
    d=len(w)/SR; f.update(i=i,ini=round(t,3),fim=round(t+d,3))
    # tempo aproximado de cada palavra, proporcional às letras
    pal=f["texto"].split(); tot=sum(len(x)+1 for x in pal); acc=0; f["t"]=[]
    for x in pal: f["t"].append(round(t+d*acc/tot,3)); acc+=len(x)+1
    pausa=f["pausa"]
    if f["cap"]=="ABERTURA" and (i==len(frases) or frases[i]["cap"]!="ABERTURA"): pausa=1.0+TITULO; f["titulo_ini"]=round(t+d+1.0,3)
    f["pausa"]=pausa; partes+= [w,np.zeros(int(pausa*SR))]; t+=d+pausa
    if i%20==0: print(i,"/",len(frases),flush=True)
total=t+2.0; partes.append(np.zeros(int(2.0*SR)))
sf.write(out/"bruta.wav",np.concatenate(partes),SR)
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(out/"bruta.wav"),"-af","highpass=f=70,equalizer=f=180:t=q:w=1.0:g=1.5,deesser=i=0.35,loudnorm=I=-16:TP=-1.5:LRA=8","-ar","48000",str(p/"narracao_completa.wav")],check=True)
json.dump({"intro":INTRO,"total":round(total,3),"voz":f"supertonic-3 {VOZ}","frases":frases},open(p/"timeline_completa.json","w"),ensure_ascii=False,indent=1)
print(len(frases),"frases;",round(total/60,2),"min")
