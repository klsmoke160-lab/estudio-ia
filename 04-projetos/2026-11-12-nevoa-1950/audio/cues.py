"""Marcas de tempo (cues) derivadas da narração: usadas pela animação e pela mixagem."""
import json, pathlib
p=pathlib.Path(__file__).parent
T=json.load(open(p/"timeline.json")); F={f["i"]:f for f in T["frases"]}
def cue(i,sub):
    f=F[i]; k=f["texto"].index(sub); return round(f["ini"]+(f["fim"]-f["ini"])*k/len(f["texto"]),3)
C={"teste":cue(3,"o teste"),"semsaber":cue(6,"sem saber"),"petri":cue(7,"desenvolveram"),
   "y1976":cue(10,"décadas"),"provar":cue(11,"difícil"),"barreira":cue(11,"uma barreira"),
   "card1":cue(12,"documentos"),"card2":cue(12,"um artigo"),"card3":cue(12,"uma decisão"),
   "naopres":cue(13,"não foi"),"interrog":cue(14,"a ligação"),"tag":cue(15,"local de teste"),
   "titulo":round(T["titulo_ini"]+0.9,3)}
json.dump(C,open(p/"cues.json","w"),indent=1)
(p.parent/"motor"/"timeline.js").write_text("window.TIMELINE="+json.dumps(T,ensure_ascii=False)+";\nwindow.CUES="+json.dumps(C)+";\n")
print(C)
