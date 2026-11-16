"""Plano do vídeo MKUltra: fontes, documento, regras por frase e estilo (referência 06: cinema, escuro, uma cor por capítulo)."""
import json, re, subprocess, pathlib
from PIL import Image
MK=pathlib.Path("/home/user/mk"); FULL=MK/"full"
CENAS=json.load(open(MK/"cenas.json")); RAW={k:MK/"raw"/f"{k}.mp4" for k in CENAS}
C2=json.load(open(MK/"cenas2.json")); CENAS.update(C2); RAW.update({k:MK/"raw2"/f"{k}.mp4" for k in C2})
N={"KO":"1952-08-07_Korea","WP":"1950-12-21_War_or_Peace","RW":"RelaxedW1957","MH":"mental_hospital","TA":"ThirdAve1950","HN":"HearandN1958","AL":"Alcohola1949","DH":"DreamHos1950",
   "AB":"atom_and_biological_science","DI":"Doctorin1946","SU":"Survival1951","NS":"NewspaperSto","GW":"GovernmentWo"}
def C(k,*ts): return [("clip",N.get(k,k),t) for t in ts]
def Dc(*ks): return [("doc",k) for k in ks]
FONTE="Senado dos EUA, audiência sobre o Projeto MKULTRA, 3 de agosto de 1977 (transcrição)"
PAL=json.load(open(MK/"docs/palavras.json")); norm=lambda s:re.sub(r"[^a-z0-9]","",s.lower()); ESC=220/72
def _pag(n):
    f=FULL/f"p{n:03d}.png"
    if not f.exists(): subprocess.run(["pdftoppm","-r","220","-f",str(n+1),"-l",str(n+1),"-png","-singlefile",str(MK/"docs/audiencia1977.pdf"),str(f)[:-4]],check=True)
    return f
D={}; FALTAM=[]
def doc(key,n,ini,fim):
    W,H,ws=PAL[n]; nn=[norm(w[0]) for w in ws]; a=[norm(x) for x in ini.split()]; b=[norm(x) for x in fim.split()]
    i=next((i for i in range(len(nn)-len(a)+1) if nn[i:i+len(a)]==a),None); j=next((j for j in range(i or 0,len(nn)-len(b)+1) if nn[j:j+len(b)]==b),None) if i is not None else None
    if j is None: FALTAM.append(key); D[key]=(_pag(n),None,(0.5,0.35,0.9),FONTE); return
    sel=ws[i:j+len(b)]; linhas={}
    for w,x0,y0,x1,y1 in sel:
        k=round(y0/4); L=linhas.get(k,[1e9,1e9,0,0]); linhas[k]=[min(L[0],x0),min(L[1],y0),max(L[2],x1),max(L[3],y1)]
    D[key]=(_pag(n),[[v*ESC for v in linhas[k]] for k in sorted(linhas)],None,FONTE)
doc("destruidos",6,"The records of all these","Richard Helms."); doc("heroina",6,"heroin addicts were enticed","reward -- heroin."); doc("sentido",6,"these tests made little","scientific sense.")
doc("ninguem",7,"no single individual","remembered the details"); doc("caixas",9,"seven boxes of documents","Project MKULTRA"); doc("deposito",10,"Retired Records Center","outside of Washington")
doc("sub149",11,"there are 149 MKULTRA","subprojects"); doc("pesq185",14,"names of 185","researchers and assistants"); doc("inst80",14,"The names of 80 institutions","80 institutions")
doc("univ44",14,"44 colleges or universities","3 penal institutions."); doc("casas",15,"safehouses in San Francisco","New York City"); doc("psico",15,"criminal sexual psychopaths","State hospital")
doc("aprovado",99,"MKULTRA was approved","April 13, 1953"); doc("restr",99,"a foe who might not","as we are."); doc("antietico",99,"Research in the manipulation","professionally unethical")
# ---------- v2: registros reais e acervos com direito conferido (pesquisa/plano-visual.md) ----------
F2=MK/"fotos2"
_F={"dulles_id":(0.45,"Crachá de Allen W. Dulles · CIA (domínio público)"),"gottlieb":(0.30,"Sidney Gottlieb · governo dos EUA (domínio público)"),
    "helms_tumulo":(0.5,"Túmulo de Richard Helms, Arlington (domínio público)"),"lenexa":(0.5,"Depósito federal de registros · NARA (domínio público)"),
    "cavernas":(0.5,"Depósito federal de registros · NARA (domínio público)"),"ravenscrag":(0.45,"Ravenscrag, Montreal, década de 1870 · J. G. Parks (CC0)"),
    "allan_hoje":(0.5,"Allan Memorial Institute · Thomas1313 (CC BY-SA 3.0)"),"ford_relatorio":(0.4,"Ford recebe o relatório da Comissão Rockefeller, 1975 · Ford Library"),
    "turner_carter":(0.35,"Carter e Stansfield Turner, 1977 · CIA (domínio público)"),"dulles":(0.3,"Allen W. Dulles · governo dos EUA (domínio público)")}
FOTOS={}
for k,(fy,fonte) in _F.items():
    for ext in (".jpg",".png"):
        f=F2/(k+ext)
        if f.exists() and f.stat().st_size>50000: FOTOS[k]=(str(f),fy,fonte)
def P_(k,*alt):
    "foto se ela baixou; senão a alternativa"
    return [("foto",k)] if k in FOTOS else list(alt)
LS=lambda *t:C("LS",*t)   # LSD-25 e MER-17, 1955, cor (coleção de filmes da CIA no NARA)
BS=lambda *t:C("BS",*t); LW=lambda *t:C("LW",*t); HE=lambda *t:C("HE",*t); VS=lambda *t:C("VS",*t)
BW=lambda *t:C("BW",*t); HY=lambda *t:C("HY",*t); SF=lambda *t:C("SF",*t); GV=lambda *t:C("GV",*t); NX=lambda *t:C("NX",*t)
X=lambda k,*t:C(k,*t)
FOGO=X("px9667286",150); FOGO2=X("mx36234",8); FICHAS=X("px6549976",8); GOTA=X("mx110",8); TINTA=X("mx203",12); ARQ=X("mx48574",6)
AR={k:16/9 for k in C2 if k.startswith(("px","mx"))}; AR["LW"]=16/9; AR["SF"]=2.2
PRE={"SF":"crop=634:288:6:96","mx41439":"eq=gamma=1.6:brightness=0.04"}
R=[
("Em janeiro de 1973, o diretor",FOGO),("Vinte anos de registros",FICHAS),("Nomes, pagamentos",FICHAS+ARQ),("A ordem foi cumprida",FOGO2),
("Sete caixas tinham sido",P_("lenexa",*ARQ)),("E ficaram lá, esquecidas",X("px6550137",4)),("O que você vai ver",Dc("caixas")),("E a pergunta que essas caixas",ARQ),
("No início dos anos 1950",LW(92)+BS(108)),("Alguns elogiavam",BS(396)),("A imprensa americana",X("px29906414",15)),("A ideia tomou conta",LW(216)+P_("dulles",*LW(401))),
("Dentro da CIA, a conclusão",P_("dulles_id",*LW(463))),("Um documento interno",Dc("restr")),("Conhecer o potencial",Dc("restr")),
("Em 13 de abril de 1953",Dc("aprovado")),("A proposta tinha vindo",HE(587)),("Para comandar o trabalho",P_("gottlieb",*LS(888))),("Gottlieb não parecia",P_("gottlieb",*LS(888))),
("E acreditava que existia",LS(135)),("A droga era nova",GOTA),("Uma quantidade invisível",TINTA+LS(404)),("Para um serviço secreto",LS(565,619)),
("Só faltava descobrir",LS(1319)),
("MKUltra era um guarda-chuva",Dc("sub149")),("Debaixo dele havia",Dc("sub149")),("O dinheiro saía",FICHAS),("Os papéis recuperados citam",Dc("pesq185")),("E oitenta instituições",Dc("inst80")),
("Quarenta e quatro eram",Dc("univ44")),("Quinze, fundações",Dc("univ44")),("Pense no que essa lista",LS(780,834)),("Acontecia em salas",LS(296)+X("px29241126",4)),
("Havia pesquisa sobre drogas",HY(16,140)+X("px29241126",6)),("Parte dos voluntários",LS(996,1049)),("Mas voluntário avisado",LS(1103)),("Queria saber o que acontece",LS(1534)),
("Os documentos usam",ARQ),("O Senado americano registrou",VS(137)),("LSD dado a pessoas",GOTA),("Num bar",X("mx41439",5)),("Para isso, a CIA montou",Dc("casas")),("Eram chamados de casas",SF(1047,1101)),
("A pessoa era atraída",SF(993)+X("px9431644",5)),("Quem observava não era",LS(780)),("As cobaias iam embora",X("px31042229",5)+LS(1641)),("Houve quem fosse parar",X("px29241126",3)),
("Dependentes de heroína",Dc("heroina")),("A recompensa era heroína",Dc("heroina")+X("mx33734",3)),("Em um hospital estadual",Dc("psico")),("A avaliação final consta",Dc("sentido")),("Ninguém sabe quantas",ARQ),
("Frank Olson era bacteriologista",BW(109,85)),("Em novembro de 1953",X("mx20464",10)),("Depois do jantar",LS(942)),("Olson voltou para casa",GV(794)),
("Ele pediu para sair",X("px31042229",8)),("Em vez disso, foi levado",GV(757,683)),("Na madrugada de 28",X("mx22336",5)),("Tinha quarenta e três",X("px31042229",3)),("A família ouviu",X("px9431644",8)),
("Em 1975, uma comissão",P_("ford_relatorio",*VS(27))),("O nome não aparecia",VS(192,302)),("O presidente Gerald Ford",P_("ford_relatorio",*VS(27))),("A versão oficial continua",X("px9431644",3)),("E não há como conferir",FOGO2),
("Em Montreal, no Canadá",P_("ravenscrag",*X("mx20464",3))),("O diretor era Ewen Cameron",P_("allan_hoje",*X("px29241126",3))),("As pessoas procuravam",X("px29241126",2)),("Ele tinha uma teoria",X("mx46738",6)),
("Os pacientes eram mantidos",HY(109,421)),("Recebiam eletrochoques",X("px29241126",7)),("E, enquanto dormiam",X("mx14451",10)+X("mx46738",12)),("Entre 1957 e 1964",FICHAS),
("Alguns pacientes saíram",X("mx20464",16)),("Outros desaprenderam",HY(140)),("O Canadá só soube",X("mx48357",5)+X("mx4135",6)),("Cameron morreu em 1967",X("mx20464",5)),
("Uma inspeção interna",Dc("antietico")),("Pesquisa sobre manipulação",Dc("antietico")),("O resultado, depois de tantos",LS(1372,1426)),("Sobrava o rastro",FICHAS),
("Em 1973, o país vivia",NX(50,110)),("Richard Helms estava de saída",HE(509)),("Em janeiro, a ordem foi dada",Dc("destruidos")),("Os registros de MKUltra deviam",Dc("destruidos")+FOGO),
("Quando o Senado finalmente",VS(247)),("Nas palavras de um senador",Dc("ninguem")),("Parecia o fim",X("px6550137",8)),
("Em 1977, um jornalista",X("mx10395",5)),("Um funcionário da CIA",FICHAS),("Os arquivos operacionais",FOGO2),("Tinham ido para um depósito",Dc("deposito")),("Lá estavam sete caixas",P_("cavernas",*Dc("caixas"))),
("Dentro delas, perto de",ARQ),("Não eram os relatórios",FICHAS),("Mas recibos têm nomes",Dc("pesq185")),("Em 3 de agosto de 1977",P_("turner_carter",*VS(27))),("É por causa de um erro",X("px6550137",3)),
("Está nos documentos que o programa",Dc("aprovado")),("Está nos documentos que pessoas",Dc("casas")),("Está nos documentos que pelo menos",X("mx22336",8)),("E está nos documentos que os arquivos",Dc("destruidos")),
("O que não está em documento",X("mx4111",4)),("Como a maior parte",FOGO2),("A fogueira de 1973",X("px4684207",8)),
("No começo deste vídeo",FOGO),("A ordem falhou por sete",Dc("caixas")),("Sidney Gottlieb morreu",P_("gottlieb",*LS(888))),("Richard Helms morreu",P_("helms_tumulo",*HE(509))),("As vítimas, na maior parte",X("mx20464",12)),
("Se aquelas sete caixas",P_("lenexa",*ARQ)),("Me conta nos comentários",FOGO),("E, para acompanhar",Dc("caixas")),
]
POOL={
"ABERTURA":FOGO+FICHAS+ARQ,
"O MEDO":BS(36,180,324,468)+LW(92,216,401),
"O QUÍMICO":LS(135,350,404,457,511,565)+GOTA,
"A REDE":LS(296,780,834,888)+FICHAS+X("px29241126",5),
"OS QUE NÃO SABIAM":SF(993,1047,1101,1154)+X("px9431644",4)+X("mx41439",6)+GOTA,
"FRANK OLSON":X("mx20464",4,12)+GV(683,757,794)+X("px31042229",6),
"MONTREAL":HY(47,234,421)+X("px29241126",4)+X("mx46738",4)+X("mx14451",6),
"A ORDEM":NX(70,150)+FOGO+FOGO2+X("px10802584",10)+VS(357),
"SETE CAIXAS":ARQ+FICHAS+X("px6550137",5)+X("mx10395",3),
"O QUE SABEMOS":X("mx4111",3)+X("mx4135",8)+FICHAS+LS(1534),
"FECHO":FOGO+FOGO2+ARQ,
}
KEY=[("Em 13 de abril de 1953","13 DE ABRIL DE 1953"),("Para comandar o trabalho","SIDNEY GOTTLIEB"),("Debaixo dele havia","149 SUBPROJETOS"),("Os papéis recuperados citam","185 PESQUISADORES"),
("E oitenta instituições","80 INSTITUIÇÕES"),("Quarenta e quatro eram","44 UNIVERSIDADES"),("Frank Olson era bacteriologista","FRANK OLSON"),("Na madrugada de 28","28 DE NOVEMBRO DE 1953"),
("Em 1975, uma comissão","1975"),("Em Montreal, no Canadá","MONTREAL, CANADÁ"),("O diretor era Ewen Cameron","EWEN CAMERON"),("Em janeiro, a ordem foi dada","JANEIRO DE 1973"),
("Em 1977, um jornalista","1977"),("Em 3 de agosto de 1977","3 DE AGOSTO DE 1977")]
CARDS=[("Destruir tudo.","DESTRUIR TUDO.","vermelho"),("Quase.","QUASE.","branco"),("LSD.","LSD","amarelo"),("Eles tinham ido buscar ajuda.","ELES TINHAM IDO\nBUSCAR AJUDA.","branco")]
LISTA=[]
TITULO=("MKULTRA","As sete caixas que a CIA esqueceu de queimar",("doc","caixas"))
T_={"ABERTURA":"vermelho","O MEDO":"petroleo","O QUÍMICO":"petroleo","A REDE":"verde","OS QUE NÃO SABIAM":"azul","FRANK OLSON":"ambar","MONTREAL":"azul","A ORDEM":"vermelho","SETE CAIXAS":"verde","O QUE SABEMOS":"petroleo","FECHO":"vermelho"}
ESTILO=dict(cinema=True,tint=T_,dur_plano=4.0,zoom=0.045,nasce=4.0,brilho=-0.10,cama=-24,golpe=-3)
AVISO="REGISTROS DE ARQUIVO E IMAGENS ILUSTRATIVAS · DOCUMENTOS ORIGINAIS"
