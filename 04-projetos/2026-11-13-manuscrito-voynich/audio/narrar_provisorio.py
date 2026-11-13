"""Narração provisória do roteiro inteiro (Piper pt_BR-cadu) frase a frase + linha do tempo."""
import json, re, subprocess, wave, pathlib
PIPER="/home/user/tts/.venv/bin/piper"; MODEL="/home/user/tts/pt_BR-cadu-medium.onnx"
p=pathlib.Path(__file__).parent; out=p/"completo"; out.mkdir(exist_ok=True)
PRON=[("Wilfrid Voynich","Uílfrid Vóinitch"),("Voynich","Vóinitch"),("Villa Mondragone","Vila Mondragône"),("Johannes Marcus Marci","Iohánes Márcus Mártsi"),("Marci","Mártsi"),
("Athanasius Kircher","Atanásius Quírquer"),("Kircher","Quírquer"),("Roger Bacon","Rôdjer Bêicon"),("Bacon","Bêicon"),("Jacobus Horcicky de Tepenecz","Iácobus Hôrtchitsqui de Tépenets"),
("Horcicky","Hôrtchitsqui"),("Tepenecz","Tépenets"),("Georg Baresch","Guêorg Bárech"),("Baresch","Bárech"),("William Newbold","Uíliam Niúbold"),("Newbold","Niúbold"),("John Manly","Djón Mênli"),
("William Friedman","Uíliam Frídman"),("Friedman","Frídman"),("Prescott Currier","Préscot Cârrier"),("Lisa Fagin Davis","Lisa Fêiguin Dêivis"),("Gordon Rugg","Górdon Râg"),("Hans Kraus","Háns Cráus"),
("Kraus","Cráus"),("Yale","Iêil"),("Beinecke","Báineque")]
INTRO=1.5; TITULO=5.0; ABERTURA_FIM=None
frases=[]; cap=None
for par in (p.parent/"roteiro-completo.txt").read_text().split("\n"):
    par=par.strip()
    if not par: continue
    if par.startswith("#"):
        cap=par[1:].strip(); 
        if frases: frases[-1]["pausa"]=1.9
        continue
    ss=re.split(r'(?<=[.?!:])\s+',par)
    for k,s in enumerate(ss):
        frases.append({"texto":s,"cap":cap,"pausa":0.36 if k<len(ss)-1 else 0.75})
t=INTRO; sr=22050; lines=[]
def sil(name,d):
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i",f"anullsrc=r={sr}:cl=mono","-t",f"{d:.3f}","-c:a","pcm_s16le",str(out/name)],check=True)
sil("s_intro.wav",INTRO); lines.append("file 's_intro.wav'")
for i,f in enumerate(frases,1):
    fala=f["texto"]
    for a,b in PRON: fala=fala.replace(a,b)
    w=out/f"f{i:03d}.wav"
    subprocess.run([PIPER,"-m",MODEL,"-f",str(w),"--length-scale","1.0","--sentence-silence","0.05"],input=fala.encode(),check=True,capture_output=True)
    ww=wave.open(str(w)); d=ww.getnframes()/ww.getframerate(); sr=ww.getframerate(); ww.close()
    f.update(i=i,ini=round(t,3),fim=round(t+d,3))
    pausa=f["pausa"]
    if f["cap"]=="ABERTURA" and (i==len(frases) or frases[i]["cap"]!="ABERTURA"): pausa=1.0+TITULO; f["titulo_ini"]=round(t+d+1.0,3)
    f["pausa"]=pausa; sil(f"s{i:03d}.wav",pausa); lines+= [f"file 'f{i:03d}.wav'",f"file 's{i:03d}.wav'"]; t+=d+pausa
total=t+2.0
(out/"lista.txt").write_text("\n".join(lines))
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",str(out/"lista.txt"),"-c:a","pcm_s16le",str(p/"narracao_completa.wav")],check=True)
json.dump({"intro":INTRO,"total":round(total,3),"frases":frases},open(p/"timeline_completa.json","w"),ensure_ascii=False,indent=1)
print(len(frases),"frases; total",round(total/60,2),"min")
