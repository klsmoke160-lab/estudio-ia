"""Mixagem do documentário inteiro: narração (acelerada 10%) + cama grave + efeitos nos títulos e palavras-chave."""
import json, subprocess, pathlib, os
NOVO=os.environ.get("NOVO")=="1"
p=pathlib.Path(__file__).parent; SFX=p.parents[2]/"05-biblioteca"/"som"/"sfx"
E=json.load(open(p.parent/"render"/"doc"/"edl.json")); tot=E["total"]; EV=[(0.4,"riser/riser-1",-14)]
for o in E["overlays"]:
    if o["tipo"]=="cap": EV+=[(o["a"]-0.25,"whoosh-grande/whoosh-grande-1",-15),(o["a"]+0.1,"impacto/impacto-2",-9)]
    if o["tipo"]=="key": EV+=[(o["a"],"carimbo/carimbo-1",-12)]
for s in E["shots"]:
    if s["tipo"]=="ins":
        if s["g"]=="title": EV+=[(s["a"]-1.0,"riser/riser-2",-10),(s["a"]+0.9,"impacto/impacto-1",-4)]
        elif s["g"] in("name","missing","link"): EV+=[(s["a"],"impacto/impacto-3",-12)]
        else: EV+=[(s["a"],"whoosh/whoosh-2",-16)]
json.dump([{"t":round(t,3),"sfx":f,"db":g} for t,f,g in EV],open(p/("eventos_doc_novo.json" if NOVO else "eventos_doc.json"),"w"),indent=1)
inp=["-i",str(p.parent/"narracao"/"narracao_video.wav") if NOVO else str(p/"narracao_completa.wav")]
fl=[(f"[0:a]aresample=48000,apad=whole_dur={tot}[n]" if NOVO else f"[0:a]atempo=1.10,aresample=48000,highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur={tot}[n]"),
 f"sine=f=55:r=48000:d={tot},volume=-26dB[b1];sine=f=82.5:r=48000:d={tot},tremolo=f=0.13:d=0.7,volume=-30dB[b2];anoisesrc=r=48000:c=brown:d={tot},lowpass=f=260,tremolo=f=0.11:d=0.6,volume=-28dB[b3]",
 f"[b1][b2][b3]amix=inputs=3:normalize=0,afade=t=in:d=2,afade=t=out:st={tot-1.5}:d=1.5[bed]"]; mix=["[n]","[bed]"]
for k,(t,f,g) in enumerate(EV,1):
    inp+=["-i",str(SFX/(f+".wav"))]; fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=mono,volume={g}dB,adelay={max(0,int(t*1000))}[e{k}]"); mix.append(f"[e{k}]")
fl.append("".join(mix)+f"amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.84,atrim=0:{tot}[out]")
(p/"mix_doc.filter").write_text(";".join(fl))
subprocess.run(["ffmpeg","-loglevel","error","-y",*inp,"-filter_complex_script",str(p/"mix_doc.filter"),"-map","[out]","-ar","48000",str(p/("mix_doc_novo.wav" if NOVO else "mix_doc.wav"))],check=True)
print("mix ok",round(tot,1),len(EV),"eventos")
