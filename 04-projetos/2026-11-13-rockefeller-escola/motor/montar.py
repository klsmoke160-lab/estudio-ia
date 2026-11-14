"""Monta o documentário "Rockefeller e a escola obrigatória".
Dois tipos de plano: DOCUMENTO (página real, câmera que se aproxima e marca-texto no trecho) e FILME (arquivo em domínio público, tratado).
Uso: python3 montar.py edl | python3 montar.py render [índices...]"""
import json, re, subprocess, sys, pathlib, itertools, os, unicodedata, concurrent.futures as cf
P=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(P/"motor")); sys.path.insert(0,"/home/user/escola")
import achar, doc
E=pathlib.Path("/home/user/escola"); FULL=E/"full"; CENAS=json.load(open(E/"cenas.json"))
RAW={k:(E/"raw"/f"{k}.mp4") for k in CENAS}
for k in ("Tubercul1955","atom_and_biological_science","bacteria_friend_and_foe"): RAW[k]=pathlib.Path("/home/user/footage/raw")/f"{k}.mp4"
OUT=P/"render"/"doc"; SEG=OUT/"segs"; SEG.mkdir(parents=True,exist_ok=True); TXT=OUT/"txt"; TXT.mkdir(exist_ok=True)
ANTON=P/"motor"/"font1.ttf"; ELITE=P/"motor"/"font2.ttf"; SERIF=P/"motor"/"serif.ttf"; SANS=P/"motor"/"sans.ttf"; FPS=24
NOVO=os.environ.get("NOVO")=="1"
T=json.load(open(P/"audio"/("timeline_novo.json" if NOVO else "timeline_completa.json"))); F=T["frases"]; TOTAL=T["total"]
N={"SUB":"HERE_IS_GERMANY","ASL":"AndSoTheyLive","CML":"Children1940","SR":"SchoolRules","HQ":"HowQuiet1953","TX":"HowTexti1948",
   "NY1":"What_Happened_1901","NY5":"loc-film-00694373-bargain-day-14th-street-new-york","SUBW":"new-york-subway-1905-directed-by-g.-w.-bitzer","FISH":"nyc_ghetto_fish_market_1903",
   "TB":"Tubercul1955","AB":"atom_and_biological_science","BF":"bacteria_friend_and_foe"}
def C(k,*ts): return [("clip",N[k],t) for t in ts]
# ---- documentos: (arquivo, id do livro, trecho inicial, trecho final, rótulo da fonte) ou foco relativo (fx,fy,fw) ----
G="countryschooloft00gates"; B="generaleducation00geneiala"; M="reportofeducatio00mannuoft"
FG="F. T. Gates, The Country School of To-Morrow (1913), p. 6"; FB="The General Education Board: An Account of Its Activities (1915)"; FM="Horace Mann, Report of an Educational Tour (1846)"
D={
"gates_capa":("gates_000.jpg",None,(0.5,0.30,0.95),"General Education Board, Occasional Papers No. 1 (1913)"),
"gates_sonho":("gates_006.jpg",(G,"In our dream","molding hand"),None,FG),
"gates_nao":("gates_006.jpg",(G,"We shall not try","of science"),None,FG),
"gates_oferta":("gates_006.jpg",(G,"Nor will we cherish","ample supply"),None,FG),
"gates_genio":("gates_006.jpg",(G,"if by chance a child","not be blighted"),None,FG),
"gates_visao":("gates_006.jpg",None,(0.5,0.20,0.80),FG),
"gates_treinar":("gates_006.jpg",(G,"to train these people as we find them","just where they are"),None,FG),
"geb_titulo":("geb_008.jpg",None,(0.5,0.22,0.95),FB),
"rock":("geb_007.jpg",None,(0.5,0.36,0.80),"John D. Rockefeller — retrato publicado em "+FB),
"rock_ass":("geb_007.jpg",None,(0.5,0.62,0.62),"Assinatura de John D. Rockefeller — "+FB),
"geb_1902":("geb_036.jpg",(B,"Mr. Rockefeller in 1902 gave","General Education Board"),None,FB+", p. 15"),
"geb_1905":("geb_036.jpg",(B,"1905, and amounting to $10,000,000","de-"),None,FB+", p. 15"),
"geb_sistema":("geb_036.jpg",(B,"to promote a","United States"),None,FB+", p. 15"),
"geb_1907":("geb_037.jpg",(B,"In February, 1907, a further gift of $32,000,000","made"),None,FB+", p. 16"),
"mapa1":("geb_069.jpg",None,(0.5,0.5,1.15),"Mapa — "+FB),"mapa2":("geb_073.jpg",None,(0.5,0.45,1.0),"Mapa — "+FB),"mapa3":("geb_179.jpg",None,(0.5,0.5,1.15),"Mapa — "+FB),
"mapa4":("geb_086.jpg",None,(0.5,0.45,0.95),"Mapa — "+FB),"mapa5":("geb_181.jpg",None,(0.5,0.5,1.15),"Mapa — "+FB),"mapa6":("geb_071.jpg",None,(0.5,0.5,1.1),"Mapa — "+FB),
"esc1":("geb_144.jpg",None,(0.5,0.34,0.92),"Escola financiada pelo conselho — "+FB),"esc1b":("geb_144.jpg",None,(0.5,0.72,0.92),"Escola financiada pelo conselho — "+FB),
"esc2":("geb_150.jpg",None,(0.5,0.34,0.92),"Escola financiada pelo conselho — "+FB),"esc2b":("geb_150.jpg",None,(0.5,0.72,0.92),"Escola financiada pelo conselho — "+FB),
"esc3":("geb_156.jpg",None,(0.5,0.34,0.92),"Escola financiada pelo conselho — "+FB),"esc4":("geb_160.jpg",None,(0.5,0.34,0.92),"Escola financiada pelo conselho — "+FB),
"esc5":("geb_166.jpg",None,(0.5,0.34,0.92),"Escola financiada pelo conselho — "+FB),"esc5b":("geb_166.jpg",None,(0.5,0.72,0.92),"Escola financiada pelo conselho — "+FB),
"faz1":("geb_052.jpg",None,(0.5,0.42,0.95),"Fazenda de demonstração — "+FB),"faz2":("geb_058.jpg",None,(0.5,0.42,0.95),"Fazenda de demonstração — "+FB),
"faz3":("geb_098.jpg",None,(0.5,0.34,0.92),"Casa de um agente do conselho — "+FB),"faz4":("geb_102.jpg",None,(0.5,0.30,0.92),"Reunião de campo — "+FB),"faz5":("geb_118.jpg",None,(0.5,0.45,0.95),"Clube de moças — "+FB),
"mann":("mann_007.jpg",None,(0.5,0.40,0.80),"Horace Mann — retrato em Life of Horace Mann (1865)"),
"tour_titulo":("tour_004.jpg",None,(0.5,0.30,0.95),FM),
"tour_prussia":("tour_017.jpg",(M,"Among the nations of Europe","distinguished reputation for the"),None,FM),
"tour_males":("tour_019.jpg",(M,"In the first place, the evils imputed","denied to possess"),None,FM),
"tour_intima":("tour_200.jpg",(M,"school inspector, who cites the delinquent parent","to be served"),None,FM),
"tour_obrig":("tour_200.jpg",(M,"respecting this compulsory attend-","of the children"),None,FM),
"flex":("flex_006.jpg",None,(0.5,0.30,0.95),"A. Flexner, Medical Education in the United States and Canada (1910)"),
}
def Dc(*ks): return [("doc",k) for k in ks]
# ---- regras por frase (trecho do texto -> planos, na ordem) ----
R=[
("Em 1913, um homem de confiança",C("NY1",6)+Dc("gates_capa")),
("Em uma das páginas",Dc("gates_visao")),
("No nosso sonho, temos recursos",Dc("gates_sonho")),
("E continuou.",Dc("gates_nao")),
("Essa página não é uma invenção",Dc("gates_visao")+C("HQ",409)),
("É a partir dela que nasce",C("HQ",204,393)+C("SR",245)),
("A frase é real.",Dc("gates_sonho")),
("Para responder, precisamos abrir",Dc("geb_titulo","tour_titulo")),
("O autor do texto se chamava",Dc("gates_capa")),
("Gates era um pastor batista",Dc("rock")+C("NY5",24)),
("Era ele quem decidia",Dc("rock_ass")),
("O texto se chama",Dc("gates_capa")),
("Foi o primeiro de uma série",Dc("geb_titulo")),
("Não era um memorando secreto",Dc("gates_visao")),
("A resposta está no relatório",Dc("geb_titulo")),
("Em 1902, Rockefeller deu",Dc("geb_1902")),
("O alvo declarado",Dc("mapa2")),
("Em 1905, vieram mais dez",Dc("geb_1905")),
("Dessa vez, para promover",Dc("geb_sistema")),
("Em 1907, outros trinta",Dc("geb_1907")),
("São valores que, na época",Dc("rock")),
("Com esse dinheiro, o conselho pagou",Dc("esc1","esc2","faz1")),
("Os mapas do relatório",Dc("mapa1")),
("Cada ponto é um lugar",Dc("mapa3")),
("Então a influência existiu",Dc("esc3","esc4")),
("Um grupo pequeno, que ninguém elegeu",Dc("rock_ass")+C("HQ",550)),
("Um visitante americano descreveu",Dc("tour_titulo")),
("Se a criança faltava",Dc("tour_intima")),
("O inspetor convocava",Dc("tour_intima")),
("E a intimação era entregue",C("SUB",1126)),
("Esse visitante não escreveu",Dc("tour_obrig")),
("O nome dele era Horace Mann",Dc("mann")),
("Mann era secretário",Dc("mann")+C("HQ",110)),
("E voltou convencido",Dc("tour_prussia")),
("Ele sabia das críticas",Dc("tour_males")),
("A resposta dele foi simples",Dc("tour_males")),
("O relatório circulou",Dc("tour_titulo")),
("Guarde a primeira data",Dc("rock")),
("O conselho dele só seria criado",Dc("geb_titulo")),
("Mas nada disso explica a frase",Dc("gates_sonho")),
("A proposta dele era outra escola",Dc("faz2","faz5")),
("É nesse ponto que aparece a frase",Dc("gates_sonho")),
("Ele mesmo a chama de sonho",Dc("gates_visao")),
("E, logo depois da lista",Dc("gates_oferta")),
("Há ainda uma linha",Dc("gates_genio")),
("Gates escreve que, se por acaso",Dc("gates_genio")),
("Na segunda, é um homem muito rico",Dc("gates_treinar")),
("As duas leituras cabem",Dc("gates_visao")),
("O que o texto não contém",Dc("gates_capa")),
("E uma visão de mundo com dinheiro",Dc("mapa5")),
("Em 1910, a Fundação Carnegie",Dc("flex")),
("O autor era um educador",Dc("flex")),
("Nos anos seguintes, o conselho de Rockefeller despejou",Dc("mapa3")+C("AB",158)),
("Bastava escolher quem recebia",Dc("rock_ass")),
("Financiou campanhas contra",Dc("faz4","faz3")),
("Foi ele quem juntou as duas pontas",C("SUB",1201)+Dc("gates_sonho")),
("A Prússia, de um lado",C("SUB",525)),
("Gates e Rockefeller, do outro",Dc("rock")),
("Na internet, a teoria quase sempre",Dc("rock")),
("Eu não quero uma nação de pensadores",C("SUBW",80)),
("Quero uma nação de trabalhadores",C("TX",189)),
("O problema é que ninguém consegue",C("SUBW",120)),
("A frase verdadeira, a de Gates",Dc("gates_sonho")),
("É verdade que o modelo de escola",C("SUB",525,1201)),
("É verdade que ele foi copiado",Dc("tour_prussia")),
("É verdade que homens muito ricos",Dc("geb_1907","gates_nao")),
("Mas não é verdade que Rockefeller inventou",Dc("tour_intima")),
("No começo deste vídeo, havia uma frase",Dc("gates_sonho")),
("Ela não prova uma conspiração",Dc("gates_capa","rock_ass")),
]
POOL={
"ABERTURA":C("HQ",31,204)+C("NY1",14),
"O HOMEM POR TRÁS DA FRASE":C("NY1",10,22)+C("NY5",30,44)+C("FISH",34),
"O DINHEIRO":Dc("esc5","mapa4","esc1b","mapa6","esc2b","esc5b"),
"ANTES DE ROCKEFELLER":C("SUB",525,826,901,976,1126,1201,1277)+C("HQ",409,550),
"O HOMEM QUE TROUXE A IDEIA":C("HQ",31,63,126,204,330)+C("FISH",40,57,70)+C("NY5",36,50)+C("TX",189)+C("CML",483),
"AS CRIANÇAS DAS FÁBRICAS":C("TX",113,189,302,415,490,792,1019,1396)+C("ASL",472,509,1199)+C("CML",38,348,753),
"O QUE O SONHO DIZIA":C("ASL",36,254,290,399,472,618,763,1018,1345)+C("CML",77,174,251,483,541,580,657),
"A MEDICINA":C("TB",353,454,529,441)+C("AB",488,502,172,416)+C("BF",25,576),
"E NO BRASIL":C("AB",43,201,431,517)+C("TB",113,100,567)+C("BF",38,269)+Dc("mapa6","faz1"),
"O PROFESSOR QUE PEDIU DEMISSÃO":C("SR",92,215,245,276,306,398,475,490,536,582)+C("HQ",251,393,456,503),
"A FRASE QUE NINGUÉM ENCONTRA":C("SUBW",75,100,140,170)+C("NY5",24)+C("FISH",50),
"O QUE OS DOCUMENTOS SUSTENTAM":C("HQ",204,550)+C("SR",276)+C("NY1",18)+C("ASL",290),
"FECHO":C("HQ",393,409,267,503)+C("SR",582,475)+C("CML",560,638,753)+C("ASL",1345,399),
}
KEY=[("Em 1913, um homem","1913"),("O autor do texto se chamava","FREDERICK T. GATES"),("Em 1902, Rockefeller deu","1902 — 1 MILHÃO DE DÓLARES"),("Em 1905, vieram","1905 — 10 MILHÕES"),
("Em 1907, outros","1907 — 32 MILHÕES"),("Em 1763, o rei","PRÚSSIA, 1763"),("O nome dele era Horace Mann","HORACE MANN"),("Em 1843, viajou","1843"),
("Em 1852, Massachusetts","MASSACHUSETTS, 1852"),("O último foi o Mississippi","MISSISSIPPI, 1918"),("Em 1900, cerca de uma em cada seis","1900: UMA EM CADA SEIS CRIANÇAS TRABALHAVA"),
("Em 1910, a Fundação Carnegie","RELATÓRIO FLEXNER, 1910"),("A partir de 1916","BRASIL, 1916"),("só entrou na Constituição","CONSTITUIÇÃO DE 1934"),
("John Taylor Gatto deu aula","JOHN TAYLOR GATTO"),("Em 1991, no auge","1991"),("Eu não quero uma nação de pensadores","CITAÇÃO SEM FONTE CONHECIDA"),
("Mas não é verdade que Rockefeller inventou","A ESCOLA OBRIGATÓRIA É MAIS ANTIGA"),("E a pergunta que fica","QUEM ESTÁ ESCOLHENDO HOJE?")]
QUOTE=[("No nosso sonho, temos recursos","\u201cperfeita docilidade\u201d"),("Não tentaremos fazer dessas pessoas","\u201cfilósofos\u201d"),("desenhada por milionários","\u201ctrabalhadores obedientes\u201d"),
("A Prússia queria súditos","\u201cobedecer\u201d"),("entregue em casa por um policial","\u201cum policial\u201d"),("Ele estava encantado","\u201cencantado\u201d"),
("Ele mesmo a chama de sonho","\u201csonho\u201d"),("desses, nós já temos oferta de sobra","\u201coferta de sobra\u201d"),("uma criança de gênio","\u201cgênio\u201d"),
("Bastava escolher quem recebia","\u201co cheque\u201d"),("a obedecer ao sinal","\u201cobedecer ao sinal\u201d"),("Quero uma nação de trabalhadores","\u201cnação de trabalhadores\u201d"),
("alguém fabrica um mais simples","\u201cfabricada\u201d"),("Alguém escolheu","\u201calguém escolheu\u201d")]
VERM={"ANTES DE ROCKEFELLER","A FRASE QUE NINGUÉM ENCONTRA"}
TITULO=("PERFEITA DOCILIDADE","Rockefeller, a Prússia e a escola obrigatória")
RUINS={("HERE_IS_GERMANY",826),("HERE_IS_GERMANY",1277),("HowTexti1948",113),("HowTexti1948",302),("HowTexti1948",415),("HowTexti1948",1396),
("Children1940",38),("Children1940",580),("AndSoTheyLive",36),("AndSoTheyLive",509),("AndSoTheyLive",1018)}
for _k in POOL: POOL[_k]=[x for x in POOL[_k] if not (x[0]=="clip" and (x[1],x[2]) in RUINS)]
def _norm(x): return re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",x.lower()).encode("ascii","ignore").decode())
import math
VELHOS=("Tubercul1955","atom_and_biological_science","bacteria_friend_and_foe")
def snap(film,t):
    """os tempos vieram truncados das folhas de contato: volta ao instante exato da miniatura"""
    step=CENAS[film][-1]/(48 if film in VELHOS else 40); return min(CENAS[film][-1]-0.5,math.ceil(t/step-1e-6)*step+0.05)
def shot_src(film,t,need):
    t=snap(film,t); c=CENAS[film]; a=max(x for x in c if x<=t); b=min(x for x in c if x>t); a+=0.25; b-=0.25; L=b-a
    if L>=need: s=min(max(t-need/2,a),b-need); return s,need,1.0
    if L>=need/1.7: return a,L,need/L
    return max(0,t-need/2),need,1.0
def build():
    cyc={k:itertools.cycle(v) for k,v in POOL.items()}; shots=[]; ov=[]; cap=None
    for n,f in enumerate(F):
        txt=f["texto"]; ini=0.0 if n==0 else f["ini"]-0.12; nxt=F[n+1]["ini"]-0.12 if n+1<len(F) else TOTAL; end=f.get("titulo_ini",nxt)
        if f["cap"]!=cap:
            cap=f["cap"]
            if cap!="ABERTURA": ov.append(dict(tipo="cap",txt=cap,a=f["ini"]-1.75,b=f["ini"]+0.25))
        for k,word in KEY:
            if k in txt:
                ka=f["ini"]+0.25
                if f.get("t"):
                    ix=len(_norm(txt.split(k)[0]).split()); ka=f["t"][min(ix,len(f["t"])-1)]-0.25
                ov.append(dict(tipo="key",txt=word,a=max(0,ka),b=min(max(f["fim"]+0.4,ka+2.5),ka+4.5)))
        for k,word in QUOTE:
            if k in txt:
                qa=f["ini"]+0.2
                if f.get("t"):
                    ix=len(_norm(txt.split(k)[0]).split()); qa=f["t"][min(ix,len(f["t"])-1)]-0.1
                ov.append(dict(tipo="quote",txt=word,a=qa,b=min(qa+2.4,end-0.05)))
        # legenda: pedaços de até 7 palavras, tempo proporcional ao tamanho
        pal=txt.split(); ch=[" ".join(pal[i:i+7]) for i in range(0,len(pal),7)]; tot=sum(len(c) for c in ch); t0=f["ini"]
        for c in ch:
            dd=(f["fim"]-f["ini"])*len(c)/tot; ov.append(dict(tipo="leg",txt=c,a=t0,b=t0+dd)); t0+=dd
        rule=next((r for s,r in R if s in txt),None); D_=end-ini
        if rule: plan=list(rule)
        else: plan=[next(cyc[cap]) for _ in range(max(1,round(D_/3.0)))]
        # documento com marca-texto precisa de tempo: no mínimo 3,2 s por plano
        while len(plan)>1 and D_/len(plan)<(2.6 if any(x[0]=="doc" for x in plan) else 1.9): plan.pop()
        for j,sp in enumerate(plan):
            a=ini+D_*j/len(plan); b=ini+D_*(j+1)/len(plan)
            if sp[0]=="doc": shots.append(dict(tipo="doc",k=sp[1],a=a,b=b,i=f["i"],cap=cap))
            else: shots.append(dict(tipo="clip",film=sp[1],t=sp[2],a=a,b=b,i=f["i"],cap=cap,zin=len(shots)%2==0))
        if "titulo_ini" in f:
            shots.append(dict(tipo="doc",k="gates_capa",a=f["titulo_ini"],b=nxt,i=f["i"],cap=cap,titulo=True)); ov.append(dict(tipo="titulo",txt=TITULO[0],sub=TITULO[1],a=f["titulo_ini"]+0.4,b=nxt-1.95))
    for s in shots: s["fa"]=round(s["a"]*FPS); s["fb"]=round(s["b"]*FPS)
    shots=[s for s in shots if s["fb"]>s["fa"]]
    # funde planos de documento iguais e consecutivos sem marca-texto diferente? não: cada frase reinicia a câmera de propósito
    caps_=[o for o in ov if o["tipo"]=="cap"]
    for o in ov:
        if o["tipo"]=="key":
            for c in caps_:
                if o["a"]<c["b"] and o["b"]>c["a"]: o["a"]=c["b"]+0.05; o["b"]=max(o["b"],o["a"]+2.5)
    ov.append(dict(tipo="aviso",txt="FILMES DE ARQUIVO ILUSTRATIVOS · DOCUMENTOS ORIGINAIS",a=1.0,b=8.0))
    return shots,ov
def esc(p): return str(p).replace(":","\\:")
def tf(txt):
    f=TXT/f"o{abs(hash(txt))%10**9}.txt"; f.write_text(txt); return esc(f)
def overlays(s,ov):
    a0=s["fa"]/FPS; b0=s["fb"]/FPS; fl=[]
    for o in ov:
        if o["b"]<=a0 or o["a"]>=b0: continue
        a=o["a"]-a0; b=o["b"]-a0
        al=f"if(lt(t\\,{a:.3f})\\,0\\,if(lt(t\\,{a+0.12:.3f})\\,(t-{a:.3f})/0.12\\,if(lt(t\\,{b-0.35:.3f})\\,1\\,max(0\\,({b:.3f}-t)/0.35))))"
        en=f"enable='between(t,{a:.3f},{b:.3f})'"
        if o["tipo"]=="cap":
            fl+= [f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.66:t=fill:{en}",
                  f"drawtext=fontfile={esc(ANTON)}:textfile={tf(o['txt'])}:fontsize={150 if len(o['txt'])<22 else 104}:fontcolor=0xECE6D6:x=(w-text_w)/2:y=(h-text_h)/2-10:alpha='{al}':shadowcolor=black@0.8:shadowx=4:shadowy=5",
                  f"drawbox=x=(iw-520)/2:y=ih/2+110:w=520:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.12:.3f},{b-0.2:.3f})'"]
        elif o["tipo"]=="titulo":
            fl+= [f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.72:t=fill:{en}",
                  f"drawtext=fontfile={esc(ANTON)}:textfile={tf(o['txt'])}:fontsize=190:fontcolor=0xECE6D6:x=(w-text_w)/2:y=(h-text_h)/2-60:alpha='{al}':shadowcolor=black@0.8:shadowx=5:shadowy=6",
                  f"drawbox=x=(iw-760)/2:y=ih/2+80:w=760:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.3:.3f},{b-0.2:.3f})'",
                  f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['sub'])}:fontsize=40:fontcolor=0xD8D2C2:x=(w-text_w)/2:y=h/2+130:alpha='{al}'"]
        elif o["tipo"]=="quote":
            fl+= [f"drawbox=x=0:y=0:w=iw:h=ih:color=0x2a0000@0.55:t=fill:{en}",
                  f"drawtext=fontfile={esc(SERIF)}:textfile={tf(o['txt'])}:fontsize=104:fontcolor=0xF4E04D:x=(w-text_w)/2:y=(h-text_h)/2-20:alpha='{al}':shadowcolor=black@0.9:shadowx=4:shadowy=4"]
        elif o["tipo"]=="leg":
            if any(x["tipo"] in("cap","titulo","quote") and x["a"]<o["b"] and x["b"]>o["a"] for x in ov): continue
            fl.append(f"drawtext=fontfile={esc(SANS)}:textfile={tf(o['txt'])}:fontsize=40:fontcolor=0xF4E04D:x=(w-text_w)/2:y=h-150:borderw=3:bordercolor=black@0.85:{en}")
        elif o["tipo"]=="key":
            fs=150 if len(o["txt"])<16 else (112 if len(o["txt"])<24 else (80 if len(o["txt"])<34 else 60))
            # estilo da referência 04: texto grande e branco no alto, sem faixa, com sombra suave e traço vermelho que cresce
            sl=f"if(lt(t\\,{a:.3f})\\,0\\,min(1\\,(t-{a:.3f})/0.35))"
            fl+= [f"drawtext=fontfile={esc(ANTON)}:textfile={tf(o['txt'])}:fontsize={fs}:fontcolor=white:x=110-40*(1-{sl}):y=96:alpha='{al}':shadowcolor=black@0.75:shadowx=0:shadowy=6:borderw=2:bordercolor=black@0.35",
                  f"drawbox=x=114:y=96+{fs}*1.36:w=150:h=7:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.15:.3f},{b-0.3:.3f})'"]
        else:
            fl.append(f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['txt'])}:fontsize=28:fontcolor=0xD8D2C2:x=w-text_w-70:y=70:alpha='{al}':shadowcolor=black@0.9:shadowx=2:shadowy=2")
    return fl
COLOR={"SchoolRules","HowTexti1948","bacteria_friend_and_foe"}
def grade(s,n):
    if s.get("cap") in VERM and n%3!=0:
        return ["hue=s=0","eq=contrast=1.45:brightness=-0.06","colorchannelmixer=rr=1.25:rg=0:rb=0:gr=0.18:gg=0.12:gb=0:br=0.10:bg=0:bb=0.08"]
    if s["film"] in COLOR:
        return ["eq=contrast=1.28:brightness=-0.05:saturation=1.75:gamma=0.92","colorbalance=rs=-0.06:gs=0.04:bs=-0.10:rm=0.05:gm=0.06:bm=-0.12:rh=0.06:gh=0.04:bh=-0.08"]
    pal=n%4
    if pal==1: return ["hue=s=0","eq=contrast=1.35:brightness=-0.05","colorchannelmixer=rr=0.95:gr=0.85:br=0.35:rg=0.05:gg=0.15:bg=0.05:rb=0:gb=0:bb=0.15","eq=saturation=1.4"]
    if pal==3: return ["hue=s=0","eq=contrast=1.35:brightness=-0.06","colorchannelmixer=rr=0.55:gr=0.85:br=0.70:rg=0.05:gg=0.15:bg=0.20:rb=0:gb=0:bb=0.10","eq=saturation=1.3"]
    return ["hue=s=0","eq=contrast=1.32:brightness=-0.05:gamma=0.9","colorchannelmixer=rr=1.0:gr=0.80:br=0.45:rg=0.0:gg=0.12:bg=0.05:rb=0:gb=0:bb=0.12","eq=saturation=1.5"]
def render_one(args):
    n,s,ov,last=args; out=SEG/f"s{n:04d}.mp4"; d=(s["fb"]-s["fa"])/FPS; nf=s["fb"]-s["fa"]; extra=overlays(s,ov)
    if n==0: extra.append("fade=t=in:st=0:d=1.2")
    if last: extra.append(f"fade=t=out:st={max(0,d-1.2):.3f}:d=1.2")
    if s["tipo"]=="doc":
        arq,hl,foco,fonte=D[s["k"]]; boxes=None; fc=None
        if hl:
            r=achar.find(*hl)
            if r: boxes=r[2]
        from PIL import Image
        pw,ph=Image.open(FULL/arq).size
        if foco: fc=(foco[0]*pw,foco[1]*ph,foco[2]*pw*1.38)
        # rótulo da fonte (some quando há palavra-chave na mesma faixa)
        tem_key=any(o["tipo"] in("key","cap","titulo") and o["a"]<s["b"] and o["b"]>s["a"] for o in ov)
        if not tem_key and not s.get("titulo"):
            extra=[f"drawtext=fontfile={esc(ELITE)}:textfile={tf(fonte)}:fontsize=30:fontcolor=0xD8D2C2@0.92:x=80:y=60:shadowcolor=black@0.9:shadowx=2:shadowy=2:alpha='min(1\\,t/0.5)'"]+extra
        doc.render_doc(str(FULL/arq),str(out),d,boxes=boxes,t_marca=min(d*0.34,2.6) if boxes else None,foco=fc,extra_vf=extra,marca_dur=0.5)
        return n,0,""
    ss,L,slow=shot_src(s["film"],s["t"],d)
    _of=OUT/"offsets.json"
    if _of.exists(): ss=max(0.0,ss+json.load(open(_of)).get(str(n),0.0))
    z=f"(1+0.07*t/{d:.3f})" if s["zin"] else f"(1.07-0.07*t/{d:.3f})"
    vf=[f"setpts=(PTS-STARTPTS)*{slow:.4f}",f"fps={FPS}","hqdn3d=3:3:6:6",
        f"scale=w='2*trunc(960*{z})':h='2*trunc(720*{z})':eval=frame:flags=lanczos","crop=1920:1080:(iw-1920)/2:(ih-1080)*0.42",
        *grade(s,n),"unsharp=5:5:0.7","vignette=angle=PI/3.3","noise=alls=10:allf=t+u"]+extra+["format=yuv420p"]
    cmd=["ffmpeg","-loglevel","error","-y","-ss",f"{ss:.3f}","-t",f"{L+0.2:.3f}","-i",str(RAW[s["film"]]),"-an","-vf",",".join(vf),"-frames:v",str(nf),"-r",str(FPS),
         "-c:v","libx264","-preset","veryfast","-crf","24","-video_track_timescale","12288",str(out)]
    r=subprocess.run(cmd,capture_output=True,text=True); return n,r.returncode,r.stderr[-300:]
if __name__=="__main__":
    shots,ov=build(); json.dump({"shots":shots,"overlays":ov,"total":TOTAL},open(OUT/"edl.json","w"),ensure_ascii=False,indent=1)
    from collections import Counter
    usadas=set(s for s,_ in R if any(s in f["texto"] for f in F)); print("regras sem frase:",[s for s,_ in R if s not in usadas])
    print(len(shots),"planos;",round(TOTAL/60,2),"min;",Counter(s["tipo"] for s in shots),"| doc curtos (<3 s):",sum(1 for s in shots if s["tipo"]=="doc" and s["b"]-s["a"]<3))
    if sys.argv[1:]==["edl"]: sys.exit()
    sel=[int(x) for x in sys.argv[2:]] if len(sys.argv)>2 else range(len(shots))
    jobs=[(n,shots[n],ov,n==len(shots)-1) for n in sel]
    with cf.ProcessPoolExecutor(max_workers=4) as ex:
        for n,rc,err in ex.map(render_one,jobs):
            if rc: print("ERRO",n,err,flush=True)
            elif n%25==0: print("ok",n,flush=True)
    print("FIM")
