"""Mixagem: narração + cama grave (sintetizada) + efeitos da biblioteca nos cues."""
import json, subprocess, pathlib
p=pathlib.Path(__file__).parent; SFX=p.parents[2]/"05-biblioteca"/"som"/"sfx"
T=json.load(open(p/"timeline.json")); C=json.load(open(p/"cues.json")); F={f["i"]:f for f in T["frases"]}; tot=T["total"]
EV=[ # (tempo, arquivo, ganho dB)
(0.9,"riser/riser-1",-12),(F[1]["ini"]-.05,"impacto/impacto-2",-9),(F[2]["ini"]-.1,"whoosh/whoosh-1",-14),
(F[3]["ini"]-.12,"glitch/glitch-1",-13),(C["teste"],"impacto/impacto-1",-5),(C["teste"],"carimbo/carimbo-1",-9),
(F[4]["ini"]-.3,"whoosh-grande/whoosh-grande-1",-13),(F[5]["ini"]-.15,"whoosh/whoosh-2",-15),
(F[6]["ini"]-.15,"glitch/glitch-2",-14),(C["semsaber"],"carimbo/carimbo-2",-8),(C["semsaber"],"impacto/impacto-3",-12),
(F[7]["ini"]-.2,"glitch/glitch-3",-14),(C["petri"]-.2,"whoosh/whoosh-3",-15),
(F[9]["ini"]-.25,"impacto/impacto-3",-9),(F[10]["ini"]-.2,"relogio/relogio-1",-12),(C["y1976"]+.45,"carimbo/carimbo-1",-9),
(F[11]["ini"]-.25,"whoosh-grande/whoosh-grande-2",-14),(C["provar"],"carimbo/carimbo-2",-10),(C["barreira"],"impacto/impacto-2",-6),
(C["card1"],"papel/papel-1",-9),(C["card2"],"papel/papel-2",-9),(C["card3"],"papel/papel-3",-9),
(F[13]["ini"]-.15,"whoosh/whoosh-4",-15),(C["naopres"],"carimbo/carimbo-1",-6),(F[14]["ini"]-.2,"whoosh/whoosh-1",-15),
(C["interrog"]+.5,"impacto/impacto-3",-10),(F[15]["ini"]-.2,"whoosh-grande/whoosh-grande-3",-14),(C["tag"],"digitacao/digitacao-1",-14),
(C["titulo"]-1.85,"riser/riser-2",-9),(C["titulo"],"impacto/impacto-1",-3),(C["titulo"]+.9,"digitacao/digitacao-2",-15)]
json.dump([{"t":round(t,3),"sfx":f,"db":g} for t,f,g in EV],open(p/"eventos.json","w"),indent=1)
inp=["-i",str(p/"narracao_provisoria.wav")]; fl=["[0:a]aresample=48000,highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur=%s[n]"%tot]; mix=["[n]"]
# cama: dois graves + ruído filtrado, com respiração lenta
fl.append(f"sine=f=55:r=48000:d={tot},volume=-25dB[b1];sine=f=82.5:r=48000:d={tot},tremolo=f=0.13:d=0.7,volume=-29dB[b2];anoisesrc=r=48000:c=brown:d={tot},lowpass=f=260,tremolo=f=0.11:d=0.6,volume=-27dB[b3]")
fl.append(f"[b1][b2][b3]amix=inputs=3:normalize=0,afade=t=in:d=2,afade=t=out:st={tot-1.2}:d=1.2[bed]"); mix.append("[bed]")
# monitor cardíaco: dois bipes e o tom contínuo
f8=F[8]["ini"]
fl.append(f"sine=f=880:r=48000:d=0.09,adelay={int((f8+.05)*1000)},volume=-20dB[bp1];sine=f=880:r=48000:d=0.09,adelay={int((f8+.28)*1000)},volume=-20dB[bp2];sine=f=880:r=48000:d=1.5,afade=t=out:st=0.9:d=0.6,adelay={int((f8+.6)*1000)},volume=-24dB[bp3]"); mix+=["[bp1]","[bp2]","[bp3]"]
for k,(t,f,g) in enumerate(EV,1):
    inp+=["-i",str(SFX/(f+".wav"))]; fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=mono,volume={g}dB,adelay={max(0,int(t*1000))}[e{k}]"); mix.append(f"[e{k}]")
fl.append("".join(mix)+f"amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.89,atrim=0:{tot}[out]")
subprocess.run(["ffmpeg","-loglevel","error","-y",*inp,"-filter_complex",";".join(fl),"-map","[out]","-ar","48000",str(p/"mix.wav")],check=True)
print("mix ok",tot)
