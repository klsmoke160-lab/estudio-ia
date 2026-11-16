"""Plano do vídeo MKUltra: fontes, documento, regras por frase e estilo (referência 06: cinema, escuro, uma cor por capítulo)."""
import json, re, subprocess, pathlib
from PIL import Image
MK=pathlib.Path("/home/user/mk"); FULL=MK/"full"
CENAS=json.load(open(MK/"cenas.json")); RAW={k:MK/"raw"/f"{k}.mp4" for k in CENAS}
N={"KO":"1952-08-07_Korea","WP":"1950-12-21_War_or_Peace","RW":"RelaxedW1957","MH":"mental_hospital","TA":"ThirdAve1950","HN":"HearandN1958","AL":"Alcohola1949","DH":"DreamHos1950",
   "AB":"atom_and_biological_science","DI":"Doctorin1946","SU":"Survival1951","NS":"NewspaperSto","GW":"GovernmentWo"}
def C(k,*ts): return [("clip",N[k],t) for t in ts]
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
FOTOS={}
TITULO=("MKULTRA","As sete caixas que a CIA esqueceu de queimar",("doc","caixas"))
T_={"ABERTURA":"vermelho","O MEDO":"petroleo","O QUÍMICO":"petroleo","A REDE":"verde","OS QUE NÃO SABIAM":"azul","FRANK OLSON":"ambar","MONTREAL":"azul","A ORDEM":"vermelho","SETE CAIXAS":"verde","O QUE SABEMOS":"petroleo","FECHO":"vermelho"}
ESTILO=dict(cinema=True,tint=T_,dur_plano=4.6,zoom=0.045,nasce=4.0,brilho=-0.10,cama=-24,golpe=-3)
R=[
("Em janeiro de 1973, o diretor",C("GW",748,754)),("Vinte anos de registros",C("GW",154,700)),("Nomes, pagamentos",C("GW",698)),("A ordem foi cumprida",C("WP",304)),
("Sete caixas tinham sido",C("GW",754)),("E ficaram lá, esquecidas",C("GW",748)),("O que você vai ver",Dc("caixas")),("E a pergunta que essas caixas",C("GW",733,726)),
("No início dos anos 1950",C("KO",30,39)+C("WP",163)),("Alguns elogiavam",C("WP",187)),("A imprensa americana",C("NS",67,871)),("A ideia tomou conta",C("HN",470)+C("WP",350)),
("Dentro da CIA, a conclusão",C("GW",611,621)),("Um documento interno",Dc("restr")),("Conhecer o potencial",Dc("restr")),
("Em 13 de abril de 1953",Dc("aprovado")),("A proposta tinha vindo",C("GW",424,440)),("Para comandar o trabalho",C("AL",124,141)),("Gottlieb não parecia",C("AB",165)),
("E acreditava que existia",C("AL",442,467)),("A droga era nova",C("AL",90,98)),("Uma quantidade invisível",C("AL",155)+C("MH",47)),("Para um serviço secreto",C("RW",637,649)),
("Só faltava descobrir",C("MH",37,132)),
("MKUltra era um guarda-chuva",Dc("sub149")),("Debaixo dele havia",Dc("sub149")),("O dinheiro saía",C("GW",154,262)),("Os papéis recuperados citam",Dc("pesq185")),("E oitenta instituições",Dc("inst80")),
("Quarenta e quatro eram",Dc("univ44")),("Quinze, fundações",Dc("univ44")),("Pense no que essa lista",C("AB",409,437)+C("DH",16)),("Acontecia em salas",C("DH",49,62)+C("AB",473)),
("Havia pesquisa sobre drogas",C("MH",290,299,335)),("Mas voluntário avisado",C("RW",288)),("Queria saber o que acontece",C("MH",47)),
("O Senado americano registrou",C("HN",470)),("LSD dado a pessoas",C("TA",356,576)),("Num bar",C("TA",611)),("Para isso, a CIA montou",Dc("casas")),("Eram chamados de casas",C("TA",282,301)),
("A pessoa era atraída",C("TA",263,136)),("Quem observava não era",C("RW",219)),("As cobaias iam embora",C("TA",123,363)),("Houve quem fosse parar",C("AL",712)),
("Dependentes de heroína",Dc("heroina")),("A recompensa era heroína",Dc("heroina")),("Em um hospital estadual",Dc("psico")),("A avaliação final consta",Dc("sentido")),("Ninguém sabe quantas",C("MH",282)),
("Frank Olson era bacteriologista",C("AB",133,345)),("Em novembro de 1953",C("SU",408)+C("HN",587)),("Depois do jantar",C("AL",426,665)),("Olson voltou para casa",C("RW",58,314)),
("Ele pediu para sair",C("RW",207)),("Em vez disso, foi levado",C("TA",202,530)),("Na madrugada de 28",C("TA",282)),("Tinha quarenta e três",C("SU",24)),("A família ouviu",C("DI",482)),
("Em 1975, uma comissão",C("GW",726,733)),("O nome não aparecia",C("NS",892,806)),("O presidente Gerald Ford",C("HN",470)),("A versão oficial continua",C("TA",301)),("E não há como conferir",C("GW",748)),
("Em Montreal, no Canadá",C("DH",76,81)),("O diretor era Ewen Cameron",C("MH",601,680)),("As pessoas procuravam",C("RW",543,58)),("Ele tinha uma teoria",C("AL",502,525)),
("Os pacientes eram mantidos",C("MH",299,199)),("Recebiam eletrochoques",C("MH",290,335)),("E, enquanto dormiam",C("HN",975,461)),("Entre 1957 e 1964",C("GW",154)),
("Alguns pacientes saíram",C("MH",37)),("Outros desaprenderam",C("MH",206)),("O Canadá só soube",C("MH",886)+C("NS",844)),("Cameron morreu em 1967",C("WP",292)),
("Uma inspeção interna",Dc("antietico")),("Pesquisa sobre manipulação",Dc("antietico")),("O resultado, depois de tantos",C("AL",761,148)),("Sobrava o rastro",C("GW",700,698)),
("Em 1973, o país vivia",C("NS",871,902)+C("HN",470)),("Richard Helms estava de saída",C("GW",431)),("Em janeiro, a ordem foi dada",Dc("destruidos")),("Os registros de MKUltra deviam",Dc("destruidos")),
("Quando o Senado finalmente",C("HN",447)),("Nas palavras de um senador",Dc("ninguem")),("Parecia o fim",C("WP",304)),
("Em 1977, um jornalista",C("NS",328,470)),("Um funcionário da CIA",C("GW",716,707)),("Os arquivos operacionais",C("GW",748)),("Tinham ido para um depósito",Dc("deposito")),("Lá estavam sete caixas",Dc("caixas")),
("Dentro delas, perto de",C("GW",154,754)),("Não eram os relatórios",C("GW",700)),("Mas recibos têm nomes",Dc("pesq185")),("Em 3 de agosto de 1977",C("HN",470,447)),("É por causa de um erro",C("GW",754)),
("Está nos documentos que o programa",Dc("aprovado")),("Está nos documentos que pessoas",Dc("casas")),("Está nos documentos que pelo menos",C("TA",282)),("E está nos documentos que os arquivos",Dc("destruidos")),
("O que não está em documento",C("AL",442)),("Como a maior parte",C("WP",304)),("A fogueira de 1973",C("WP",272,304)),
("No começo deste vídeo",C("GW",748)),("A ordem falhou por sete",Dc("caixas")),("Sidney Gottlieb morreu",C("AL",124)),("Richard Helms morreu",C("GW",440)),("As vítimas, na maior parte",C("MH",282,47)),
("Se aquelas sete caixas",C("GW",754,748)),("Me conta nos comentários",C("GW",726)),("E, para acompanhar",Dc("caixas")),
]
POOL={
"ABERTURA":C("GW",748,754,700)+C("WP",304),
"O MEDO":C("KO",14,30,34,43)+C("WP",142,147,175,178,238,249,282),
"O QUÍMICO":C("AL",124,133,141,148,155)+C("AB",165,186,409,417,455,461)+C("RW",606,642,668),
"A REDE":C("AB",424,437,450,473,483)+C("DH",16,20,39,53,67)+C("GW",116,154,262),
"OS QUE NÃO SABIAM":C("TA",102,123,150,263,282,301,356,363,576,611)+C("AL",426,514,632),
"FRANK OLSON":C("RW",58,73,90,185,207,288,314,332,342)+C("TA",202,282,518,530)+C("SU",24,29),
"MONTREAL":C("MH",37,47,132,145,199,206,282,290,299,335,455,495,734)+C("DH",43,46,71),
"A ORDEM":C("GW",424,431,611,698,700,748)+C("WP",272,304)+C("NS",871,902),
"SETE CAIXAS":C("GW",748,754,733,726,716,707,154)+C("NS",328,470),
"O QUE SABEMOS":C("MH",47,282)+C("GW",748,154)+C("AL",442,502)+C("TA",282,576),
"FECHO":C("GW",748,754,726)+C("MH",47),
}
KEY=[("Em 13 de abril de 1953","13 DE ABRIL DE 1953"),("Para comandar o trabalho","SIDNEY GOTTLIEB"),("Debaixo dele havia","149 SUBPROJETOS"),("Os papéis recuperados citam","185 PESQUISADORES"),
("E oitenta instituições","80 INSTITUIÇÕES"),("Quarenta e quatro eram","44 UNIVERSIDADES"),("Frank Olson era bacteriologista","FRANK OLSON"),("Na madrugada de 28","28 DE NOVEMBRO DE 1953"),
("Em 1975, uma comissão","1975"),("Em Montreal, no Canadá","MONTREAL, CANADÁ"),("O diretor era Ewen Cameron","EWEN CAMERON"),("Em janeiro, a ordem foi dada","JANEIRO DE 1973"),
("Em 1977, um jornalista","1977"),("Em 3 de agosto de 1977","3 DE AGOSTO DE 1977")]
CARDS=[("Destruir tudo.","DESTRUIR TUDO.","vermelho"),("Quase.","QUASE.","branco"),("LSD.","LSD","amarelo"),("Eles tinham ido buscar ajuda.","ELES TINHAM IDO\nBUSCAR AJUDA.","branco")]
LISTA=[]
