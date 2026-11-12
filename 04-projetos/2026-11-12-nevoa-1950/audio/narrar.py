"""Narração provisória (voz sintética Piper pt_BR-faber) frase a frase + linha do tempo."""
import json, subprocess, wave, sys, pathlib
PIPER="/home/user/tts/.venv/bin/piper"; MODEL="/home/user/tts/pt_BR-faber-medium.onnx"
out=pathlib.Path(__file__).parent
FRASES=[ # (texto falado, pausa depois)
("Em setembro de 1950, os Estados Unidos fizeram uma pergunta sobre São Francisco:",0.35),
("seria possível expor uma cidade a bactérias lançadas do mar?",0.9),
("Para descobrir, realizaram o teste.",1.1),
("Navios da Marinha liberaram microrganismos perto da costa.",0.5),
("Em terra, equipamentos recolheram amostras para acompanhar a dispersão.",0.6),
("Os moradores continuaram a vida, sem saber que o ar da cidade fazia parte de um experimento militar.",1.0),
("Naquele mesmo período, pacientes de um hospital de São Francisco desenvolveram infecções por uma das bactérias usadas no teste.",0.8),
("Um deles morreu.",1.2),
("O nome dele era Edward Nevin.",1.4),
("A família só descobriria o experimento décadas depois.",0.7),
("E, quando tentou levar o governo à Justiça, encontrou uma pergunta difícil de provar, e uma barreira que não tinha nada a ver com microscópios.",0.9),
("Essa história deixou documentos militares, um artigo médico, e uma decisão de tribunal.",0.7),
("Mas existe uma peça que não foi preservada.",0.8),
("Uma peça que poderia ajudar a esclarecer a ligação entre o navio e o hospital.",1.0),
("Para entender por que ela importa, precisamos voltar ao momento em que uma cidade passou a ser tratada como local de teste.",1.0),
]
INTRO=2.0; TITULO=6.0
t=INTRO; tl=[]; parts=[]
for i,(txt,pausa) in enumerate(FRASES,1):
    f=out/"frases"/f"f{i:02d}.wav"
    subprocess.run([PIPER,"-m",MODEL,"-f",str(f),"--length-scale","1.08","--sentence-silence","0.05"],input=txt.encode(),check=True,capture_output=True)
    w=wave.open(str(f)); d=w.getnframes()/w.getframerate(); sr=w.getframerate(); w.close()
    tl.append({"i":i,"texto":txt,"ini":round(t,3),"fim":round(t+d,3),"pausa":pausa})
    parts.append((f,d,pausa)); t+=d+pausa
total=t+TITULO
json.dump({"intro":INTRO,"titulo_ini":round(t,3),"total":round(total,3),"frases":tl},open(out/"timeline.json","w"),ensure_ascii=False,indent=1)
# concatena com silêncios
lst=out/"frases"/"lista.txt"
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i",f"anullsrc=r={sr}:cl=mono","-t",str(INTRO),str(out/"frases"/"sil_intro.wav")],check=True)
lines=[f"file 'sil_intro.wav'"]
for k,(f,d,p) in enumerate(parts,1):
    s=out/"frases"/f"sil{k:02d}.wav"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i",f"anullsrc=r={sr}:cl=mono","-t",str(p),str(s)],check=True)
    lines+= [f"file '{f.name}'",f"file '{s.name}'"]
lst.write_text("\n".join(lines))
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",str(lst),"-c","copy",str(out/"narracao_provisoria.wav")],check=True)
print("total",round(total,2),"s; título em",round(t,2))
for x in tl: print(x["i"],x["ini"],x["fim"])
