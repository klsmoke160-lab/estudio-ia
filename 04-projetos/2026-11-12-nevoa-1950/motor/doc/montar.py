"""Monta o documentário inteiro: um trecho de filme de arquivo (domínio público) por frase,
tratado (P&B, contraste, vinheta, grão, zoom lento), com títulos de capítulo e palavras-chave.
Uso: python3 montar.py edl   (só a lista de planos)  |  python3 montar.py render"""
import json, re, subprocess, sys, pathlib, itertools, concurrent.futures as cf
P=pathlib.Path(__file__).resolve().parents[2]; RAW=pathlib.Path("/home/user/footage/raw"); CENAS=json.load(open("/home/user/footage/cenas.json"))
import os
COR=os.environ.get("COR")=="1"
OUT=P/"render"/"doc"; SEG=OUT/(("segs_cor" if COR else "segs")+("_novo" if os.environ.get("NOVO")=="1" else "")); SEG.mkdir(parents=True,exist_ok=True); TXT=OUT/"txt"; TXT.mkdir(exist_ok=True)
FR=P/"render"/"frames"; ANTON=P/"motor"/"font1.ttf"; ELITE=P/"motor"/"font2.ttf"
FPS=24
NOVO=os.environ.get("NOVO")=="1"
TEMPO=1.0 if NOVO else 1.10
T=json.load(open(P/"audio"/("timeline_novo.json" if NOVO else "timeline_completa.json"))); F=T["frases"]
for f in F:
    for k in ("ini","fim","titulo_ini"):
        if k in f: f[k]=f[k]/TEMPO
TOTAL=T["total"]/TEMPO
# ---- biblioteca: filme -> tempos (s) de planos escolhidos nas folhas de contato ----
LIB={
"naval":{"Operatio1946":[166,302,333,348],"Operatio1946_2":[145,163,235,290,326,344,688,725,743,761,779]},
"mil":{"Operatio1946":[272,287,318],"Operatio1946_2":[253,362,398,417,435,453,471],"mental_hospital":[499]},
"city":{"Bridging1937":[62,83,104,480,584,856,876,897,939],"Powersof1947":[524]},
"lab":{"bacteria_friend_and_foe":[25,38,51,64,269,333,371,384,422,461,474,576,589],
       "atom_and_biological_science":[43,129,158,172,201,316,344,416,431,445,474,517,589,660],"Tubercul1955":[100,189,214,239]},
"hosp":{"Tubercul1955":[113,151,353,403,416,428,441,454,466,479,491,504,517,529,542,567,580],"atom_and_biological_science":[488,502],"mental_hospital":[723]},
"people":{"Survival1951":[153,186,295,317,372],"Tubercul1955":[277,365,378,88],"mental_hospital":[49,798,898],"BoyinCou1940":[274],"Doctorin1946":[375,399,422,446]},
"court":{"BoyinCou1940":[339,352,378,391,417,561,574,587,600],"mental_hospital":[499],"Powersof1947":[380,393,432,445]},
"docs":{"NewspaperSto":[61,247,288,308,329,370,411,432,473,494,576,597,617,679,700,720,741,803,844,865,906,926],
        "Powersof1947":[380,393,419,432,445],"mental_hospital":[624,649,574],"Doctorin1946":[587]},
}
LIB["gov"]={"BoyinCou1940":[391,339,352,587],"mental_hospital":[649,674,499],"Powersof1947":[406,380],"NewspaperSto":[329],"Operatio1946":[287]}
REG=[("court",r"tribunal|justiça|juiz|\bação\b|processo|recurso|\blei\b|jurídic|imunidade|responsabiliza"),
("hosp",r"hospital|pacient|infec|médic|cirurgia|endocardite|prontuário|doença|adoec|morreu|\bmorte\b|saúde|debilitad"),
("lab",r"bactéria|microrganismo|serratia|cepa|bacillus|simulante|organismo|amostra|cultura|pigmento|espécie"),
("naval",r"navio|marinha|\bcosta\b|\bmar\b|sea-spray|vento|liberad|pulveriz|liberação"),
("docs",r"document|artigo|jornal|reportagem|registro|relatório|publicaram|newsday|carta|dados|informaç"),
("gov",r"senado|audiência|subcomitê|nixon|política|governo|institucion|reconheceu"),
("mil",r"militar|exército|adversário|guerra|ataque|defesa|armas|operação|experimento|teste"),
("city",r"cidade|são francisco|paisagem|neblina|ponte|mapa|lojas"),
("people",r"morador|população|pessoas|família|crianças|vida|você|parente")]
CAPDEF={"ABERTURA":"city","A LÓGICA MILITAR":"mil","A BACTÉRIA":"lab","OPERAÇÃO SEA-SPRAY":"naval","O HOSPITAL":"hosp","A PEÇA QUE FALTA":"lab",
"A REVELAÇÃO":"docs","O TRIBUNAL":"court","DUAS INVESTIGAÇÕES":"people","1969":"gov","FECHO":"city"}
# ---- encartes gráficos (quadros já renderizados da abertura v1): (primeiro quadro, nº de quadros) ----
INS={"mapq":(192,92),"mappts":(450,100),"name":(945,72),"missing":(1450,70),"link":(1522,126),"title":(1828,143),"petri":(792,96),"time":(1020,88)}
def ins_for(i,txt):
    if i==2: return "mapq"
    if i==5 or "ponto marcado no mapa" in txt or "ponto daquele mapa" in txt: return "mappts"
    if i==9: return "name"
    if i==13 or "não foram preservadas" in txt: return "missing"
    if i==14 or "ligação entre um navio e um hospital" in txt: return "link"
    if "pigmento vermelho" in txt: return "petri"
    if "vinte e seis anos" in txt: return "time"
    return None
KEY=[("Operação Sea-Spray.","OPERAÇÃO SEA-SPRAY"),("foi a Serratia marcescens","SERRATIA MARCESCENS"),("Bacillus globigii","BACILLUS GLOBIGII"),
("Em outubro de 1951","OUTUBRO DE 1951"),("se estendeu de setembro","SETEMBRO DE 1950 A FEVEREIRO DE 1951"),("Em novembro de 1976","NOVEMBRO DE 1976"),
("Em 1977","1977 — SENADO AMERICANO"),("Em janeiro de 1983","JANEIRO DE 1983"),("vinte e cinco de novembro","25 DE NOVEMBRO DE 1969"),
("Em setembro de 1950, os","SETEMBRO DE 1950"),("Para descobrir","REALIZARAM O TESTE"),("sem saber que o ar","SEM SABER"),
("O experimento aconteceu.","O EXPERIMENTO ACONTECEU"),("não foi demonstrada","A LIGAÇÃO NÃO FOI DEMONSTRADA"),("as últimas a saber","E SE ELAS FOREM AS ÚLTIMAS A SABER?")]
import math
def snap(film,t):
    """Os tempos da biblioteca vieram truncados das folhas de contato (48 quadros por filme): volta ao tempo exato da miniatura."""
    step=CENAS[film][-1]/48; return math.ceil(t/step-1e-6)*step+0.05
def shot_src(film,t,need):
    t=snap(film,t); c=CENAS[film]; a=max(x for x in c if x<=t); b=min(x for x in c if x>t)
    a+=0.25; b-=0.25; L=b-a
    if L>=need: s=min(max(t-need/2,a),b-need); return s,need,1.0
    if L>=need/1.7: return a,L,need/L           # câmera lenta leve
    return max(0,t-need/2),need,1.0             # plano curto demais: aceita o corte interno
def build():
    cyc={k:itertools.cycle([(f,t) for f,ts in v.items() for t in ts]) for k,v in LIB.items()}
    # intercala filmes dentro de cada categoria para variar
    for k,v in LIB.items():
        lst=[(f,t) for f,ts in v.items() for t in ts]; lst.sort(key=lambda x:(v[x[0]].index(x[1]),x[0])); cyc[k]=itertools.cycle(lst)
    used={}; shots=[]; ov=[]; cap=None; last=None
    for n,f in enumerate(F):
        i=f["i"]; txt=f["texto"]; ini=0.0 if n==0 else f["ini"]-0.12
        nxt=F[n+1]["ini"]-0.12 if n+1<len(F) else TOTAL
        end=f.get("titulo_ini",nxt)
        if f["cap"]!=cap:
            cap=f["cap"]
            if cap!="ABERTURA": ov.append(dict(tipo="cap",txt=cap,a=f["ini"]-1.45,b=f["ini"]+1.9))
        for k,word in KEY:
            if k in txt: ov.append(dict(tipo="key",txt=word,a=f["ini"]+0.25,b=min(f["fim"]+0.5,f["ini"]+5.5)))
        g=ins_for(i,txt)
        if g: shots.append(dict(tipo="ins",g=g,a=ini,b=end,i=i))
        else:
            low=txt.lower(); cat=next((c for c,r in REG if re.search(r,low)),CAPDEF[cap])
            if cat==last and cat in("mil","docs") and re.search(REG[-1][1],low): cat="people"
            last=cat; D=end-ini; k=max(1,round(D/4.7))
            for j in range(k):
                a=ini+D*j/k; b=ini+D*(j+1)/k; film,t=next(cyc[cat]); u=used.get((film,t),0); used[(film,t)]=u+1
                shots.append(dict(tipo="clip",film=film,t=t,a=a,b=b,i=i,cap=cap,cat=cat,flip=u%2==1,zin=len(shots)%2==0))
        if "titulo_ini" in f: shots.append(dict(tipo="ins",g="title",a=f["titulo_ini"],b=nxt,i=i))
    # duração em quadros exatos
    for s in shots: s["fa"]=round(s["a"]*FPS); s["fb"]=round(s["b"]*FPS)
    shots=[s for s in shots if s["fb"]>s["fa"]]
    ov.append(dict(tipo="aviso",txt="IMAGENS DE ARQUIVO ILUSTRATIVAS",a=1.0,b=9.0))
    return shots,ov
def esc(p): return str(p).replace(":","\\:")
def overlays(s,ov):
    a0=s["fa"]/FPS; b0=s["fb"]/FPS; fl=[]
    for k,o in enumerate(ov):
        if o["b"]<=a0 or o["a"]>=b0: continue
        a=o["a"]-a0; b=o["b"]-a0; tf=TXT/f"o{abs(hash(o['txt']))%10**8}.txt"; tf.write_text(o["txt"])
        al=f"if(lt(t\\,{a:.3f})\\,0\\,if(lt(t\\,{a+0.12:.3f})\\,(t-{a:.3f})/0.12\\,if(lt(t\\,{b-0.35:.3f})\\,1\\,max(0\\,({b:.3f}-t)/0.35))))"
        if o["tipo"]=="cap":
            fl.append(f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.62:t=fill:enable='between(t,{a:.3f},{b:.3f})'")
            fl.append(f"drawtext=fontfile={esc(ANTON)}:textfile={esc(tf)}:fontsize=170:fontcolor=0xECE6D6:x=(w-text_w)/2:y=(h-text_h)/2-10:alpha='{al}':shadowcolor=black@0.8:shadowx=4:shadowy=5")
            fl.append(f"drawbox=x=(iw-520)/2:y=ih/2+110:w=520:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.12:.3f},{b-0.2:.3f})'")
        elif o["tipo"]=="key":
            fs=96 if len(o["txt"])<24 else 68
            fl.append(f"drawbox=x=0:y=ih-300:w=iw:h=220:color=black@0.5:t=fill:enable='between(t,{a:.3f},{b:.3f})'")
            fl.append(f"drawbox=x=120:y=ih-268:w=8:h=150:color=0xE2333B@0.95:t=fill:enable='between(t,{a:.3f},{b:.3f})'")
            fl.append(f"drawtext=fontfile={esc(ANTON)}:textfile={esc(tf)}:fontsize={fs}:fontcolor=0xECE6D6:x=160:y=h-300+(220-text_h)/2:alpha='{al}':shadowcolor=black@0.8:shadowx=3:shadowy=4")
        else:
            fl.append(f"drawtext=fontfile={esc(ELITE)}:textfile={esc(tf)}:fontsize=30:fontcolor=0xD8D2C2:x=w-text_w-70:y=h-80:alpha='{al}':shadowcolor=black@0.9:shadowx=2:shadowy=2")
    return fl
TOM={"ABERTURA":"colorbalance=rm=-0.038:bm=0.114:bs=0.095","A LÓGICA MILITAR":"colorbalance=rm=-0.057:bm=0.133:bs=0.114:bh=0.057",
"A BACTÉRIA":"colorbalance=rm=0.095:gm=-0.038:bm=-0.076","OPERAÇÃO SEA-SPRAY":"colorbalance=rm=-0.057:bm=0.152:bs=0.133",
"O HOSPITAL":"colorbalance=rm=0.114:gm=0.019:bm=-0.095:rs=0.057","A PEÇA QUE FALTA":"colorbalance=rm=0.095:bm=-0.095:rs=0.038",
"A REVELAÇÃO":"colorbalance=rm=0.076:gm=0.019:bm=-0.076","O TRIBUNAL":"colorbalance=rm=0.095:gm=0.019:bm=-0.095:rs=0.057",
"DUAS INVESTIGAÇÕES":"colorbalance=rm=-0.038:bm=0.095","1969":"colorbalance=rm=0.057:bm=-0.038","FECHO":"colorbalance=rm=-0.038:bm=0.114:bs=0.095"}
def grade(s):
    if not COR:
        return ["hue=s=0","eq=contrast=1.22:brightness=-0.075:gamma=0.90","colorbalance=rs=-0.03:bs=0.05:rm=-0.015:bm=0.025"]
    if s["film"]=="bacteria_friend_and_foe":   # cor original do filme, só mais escura e dessaturada
        return ["eq=contrast=1.15:brightness=-0.09:gamma=0.92:saturation=0.78","colorbalance=rs=0.03:rm=0.02:bm=-0.03"]
    # preto e branco com tom leve por capítulo e realce de vermelho nas sombras
    return ["hue=s=0","eq=contrast=1.22:brightness=-0.075:gamma=0.90",TOM.get(s.get("cap"),"colorbalance=rm=0.02"),"colorbalance=rs=0.06:rh=0.03","eq=saturation=1.0"]
def render_one(args):
    n,s,ov,last=args; out=SEG/f"s{n:04d}.mp4"; d=(s["fb"]-s["fa"])/FPS; nf=s["fb"]-s["fa"]
    if s["tipo"]=="ins":
        st,cnt=INS[s["g"]]; src=cnt/FPS
        vf=[f"setpts=PTS*{d/src:.5f}",f"fps={FPS}"]
        inp=["-framerate",str(FPS),"-start_number",str(st),"-i",str(FR/"f%05d.jpg")]; pre=["-frames:v",str(cnt)]
        cmd=["ffmpeg","-loglevel","error","-y",*inp]
        vf=[f"trim=end_frame={cnt}",f"setpts=(PTS-STARTPTS)*{d/src:.5f}",f"fps={FPS}"]
    else:
        ss,L,slow=shot_src(s["film"],s["t"],d)
        cmd=["ffmpeg","-loglevel","error","-y","-ss",f"{ss:.3f}","-t",f"{L+0.2:.3f}","-i",str(RAW/(s["film"]+".mp4"))]
        z=f"(1+0.055*t/{d:.3f})" if s["zin"] else f"(1.055-0.055*t/{d:.3f})"
        vf=[f"setpts=(PTS-STARTPTS)*{slow:.4f}",f"fps={FPS}","hqdn3d=3:3:6:6"]+(["hflip"] if s["flip"] else [])+[
            f"scale=w='2*trunc(960*{z})':h='2*trunc(720*{z})':eval=frame:flags=lanczos","crop=1920:1080:(iw-1920)/2:(ih-1080)*0.42",
            *grade(s),"unsharp=5:5:0.7",
            "vignette=angle=PI/3.9","noise=alls=9:allf=t+u"]
    vf+=overlays(s,ov)
    if n==0: vf.append("fade=t=in:st=0:d=1.5")
    if last: vf.append(f"fade=t=out:st={max(0,d-1.2):.3f}:d=1.2")
    vf.append("format=yuv420p")
    cmd+=["-an","-vf",",".join(vf),"-frames:v",str(nf),"-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","24","-video_track_timescale","12288",str(out)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    return n,r.returncode,r.stderr[-300:]
if __name__=="__main__":
    shots,ov=build(); json.dump({"shots":shots,"overlays":ov,"total":TOTAL},open(OUT/"edl.json","w"),ensure_ascii=False,indent=1)
    from collections import Counter
    print(len(shots),"planos;",round(TOTAL/60,2),"min;",Counter(s.get("cat",s.get("g")) for s in shots))
    if sys.argv[1:]==["edl"]: sys.exit()
    sel=[int(x) for x in sys.argv[2:]] if len(sys.argv)>2 else range(len(shots))
    jobs=[(n,shots[n],ov,n==len(shots)-1) for n in sel]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for n,rc,err in ex.map(render_one,jobs):
            if rc: print("ERRO",n,err,flush=True)
            elif n%25==0: print("ok",n,flush=True)
    print("FIM")
