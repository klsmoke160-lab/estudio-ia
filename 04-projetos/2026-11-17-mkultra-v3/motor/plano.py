"""Plano do MKUltra v3 (roteiro do dono, 17/11): fontes, documento, regras por frase e estilo (referência 06: cinema, escuro, uma cor por capítulo)."""
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
# ---------- documentos do depoimento de 1977 (mesmo motor da v2) ----------
doc("destruidos",6,"The records of all these","Richard Helms."); doc("heroina",6,"heroin addicts were enticed","reward -- heroin.")
doc("caixas",9,"seven boxes of documents","Project MKULTRA"); doc("deposito",10,"Retired Records Center in 1970","Budget and")
doc("sub149",11,"there are 149 MKULTRA","subprojects"); doc("pesq185",14,"names of 185","researchers and assistants"); doc("inst80",14,"The names of 80 institutions","80 institutions")
doc("univ44",14,"44 colleges or universities","3 penal institutions."); doc("casas",15,"safehouses in San Francisco","New York City")
doc("aprovado",99,"MKULTRA was approved","April 13, 1953"); doc("oitomil",26,"closer to 8,000","pages.")
doc("altosbaixos",6,"covert drug tests on unwitting citizens","native Americans and")
# ---------- documentos novos (PDF com camada de texto; caixas em pontos -> 220 dpi) ----------
V3=MK/"v3docs"; import html as _h
_CACHE={}
def _pal_pdf(pdf):
    if pdf in _CACHE: return _CACHE[pdf]
    t=open(V3/(pdf+".bbox.html"),encoding="utf-8",errors="replace").read(); pags=[]
    for pg in re.findall(r"<page[^>]*>(.*?)</page>",t,re.S):
        pags.append([(_h.unescape(w),float(a),float(b),float(c),float(d)) for a,b,c,d,w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',pg)])
    _CACHE[pdf]=pags; return pags
def docx(key,pdf,ini,fim,fonte,pagina=None):
    pags=_pal_pdf(pdf); a=[norm(x) for x in ini.split()]; b=[norm(x) for x in fim.split()]
    for n,ws in enumerate(pags):
        if pagina is not None and n!=pagina: continue
        nn=[norm(w[0]) for w in ws]
        i=next((i for i in range(len(nn)-len(a)+1) if nn[i:i+len(a)]==a),None)
        if i is None: continue
        j=next((j for j in range(i,len(nn)-len(b)+1) if nn[j:j+len(b)]==b),None)
        if j is None: continue
        png=V3/f"{pdf}_p{n+1:03d}.png"
        if not png.exists(): subprocess.run(["pdftoppm","-r","220","-f",str(n+1),"-l",str(n+1),"-png","-singlefile",str(V3/(pdf+".pdf")),str(png)[:-4]],check=True)
        linhas={}
        for w,x0,y0,x1,y1 in ws[i:j+len(b)]:
            k=round(y0/6); L=linhas.get(k,[1e9,1e9,0,0]); linhas[k]=[min(L[0],x0),min(L[1],y0),max(L[2],x1),max(L[3],y1)]
        D[key]=(png,[[v*ESC for v in linhas[k]] for k in sorted(linhas)],None,fonte); return
    FALTAM.append(key)
IG="Relatório de inspeção da CIA sobre o MKULTRA, 26 de julho de 1963 (National Security Archive)"
docx("ig_niveis","ig1963","individuals at all social","and foreign",IG)
docx("ig_registros","ig1963","Present practice is to maintain","test programe.",IG)
docx("ig_minimo","ig1963","philosophy","minimum documentation",IG)
FORD="Casa Branca, nota do secretário de imprensa, 21 de julho de 1975 (Ford Library)"
docx("ford","ford_nota","The President met with","Frank Olson's death in November 1953.",FORD)
COOP="Parecer de George Cooper ao governo do Canadá, 1986, p. 95"
docx("cooper_anos","cooper","Total funding apparently","1957 to 1962.",COOP)
docx("cooper_limite","cooper","it is impossible to reach","actually played",COOP)
# ---------- fotos (as do Wikimedia chegam pelo celular do dono, em fotos3) ----------
F2=MK/"fotos2"; F3=MK/"fotos3"
_F={"dulles_id":(F2,0.45,"Crachá de Allen W. Dulles · CIA (domínio público)"),"gottlieb":(F2,0.30,"Sidney Gottlieb · governo dos EUA (domínio público)"),
    "olson":(F3,0.30,"Frank Olson (1910–1953)"),"cameron":(F3,0.30,"D. Ewen Cameron · Canadian Medical Association Journal"),
    "allan":(F3,0.5,"Allan Memorial Institute, Montreal · Wikimedia Commons (CC BY-SA 2.5 CA)"),"white":(F3,0.3,"George Hunter White (domínio público)"),
    "turner":(F3,0.4,"Carter e Stansfield Turner, fevereiro de 1977 · CIA (domínio público)")}
FOTOS={}
for k,(d,fy,fonte) in _F.items():
    for ext in (".jpg",".png",".jpeg"):
        f=d/(k+ext)
        if f.exists() and f.stat().st_size>30000: FOTOS[k]=(str(f),fy,fonte)
def P_(k,*alt): return [("foto",k)] if k in FOTOS else list(alt)
LS=lambda *t:C("LS",*t); BS=lambda *t:C("BS",*t); LW=lambda *t:C("LW",*t); HE=lambda *t:C("HE",*t); VS=lambda *t:C("VS",*t)
BW=lambda *t:C("BW",*t); HY=lambda *t:C("HY",*t); SF=lambda *t:C("SF",*t); GV=lambda *t:C("GV",*t); NX=lambda *t:C("NX",*t)
X=lambda k,*t:C(k,*t)
FICHAS=X("px6549976",8); ARQ=X("mx48574",6); GAVETA=X("px6550137",4); GOTA=X("mx110",8); TINTA=X("mx203",12); FOGO=X("px9667286",150)
TROPA=X("tropas",60) if (MK/"raw2/tropas.mp4").exists() else LS(1588)
AR={k:16/9 for k in C2 if k.startswith(("px","mx"))}; AR["LW"]=16/9; AR["SF"]=2.2; AR["tropas"]=16/9
PRE={"SF":"crop=634:288:6:96","mx41439":"eq=gamma=1.6:brightness=0.04"}
TITULO=("MKULTRA","As sete caixas que a CIA não destruiu",("doc","caixas"))
T_={"ABERTURA":"vermelho","O MEDO":"petroleo","O QUÍMICO":"petroleo","A REDE":"verde","OS QUE NÃO SABIAM":"azul","FRANK OLSON":"ambar","MONTREAL":"azul",
    "OS INSPETORES":"verde","SETE CAIXAS":"verde","O QUE SABEMOS":"petroleo","FECHO":"vermelho"}
ESTILO=dict(cinema=True,tint=T_,dur_plano=4.0,zoom=0.045,nasce=4.0,brilho=-0.10,cama=-24,golpe=-3)
AVISO="REGISTROS DE ARQUIVO E IMAGENS ILUSTRATIVAS · DOCUMENTOS ORIGINAIS"
R=[
# ABERTURA: sem fogo como "registro" (o método de destruição não está documentado)
("Em 1973, dentro da CIA",GAVETA),("Os arquivos de um programa secreto",FICHAS),("Grande parte dos registros desapareceu",ARQ),("Mas havia um problema",ARQ),
("sete caixas de documentos financeiros",Dc("caixas")),("Estavam guardadas num centro de arquivos",Dc("deposito")),("Permaneceram ali enquanto",VS(137)),
("Dois anos depois, um funcionário",X("mx10395",5)+FICHAS),("Encontrou as caixas",Dc("caixas")),("Lá não estava a história completa",ARQ),
("Eram aprovações de despesas",FICHAS),("Papéis que pareciam menos importantes",GAVETA),("Só que os papéis traziam nomes",Dc("pesq185")),
("O programa já tinha sido revelado",VS(27)),("As caixas mostrariam quanto maior",Dc("sub149")),("O seu nome era MKUltra",Dc("aprovado")),
("E a pergunta que abre esta história",ARQ),("quando alguém destrói os registros",Dc("destruidos")),
# O MEDO
("Volte ao começo dos anos 1950",LW(30)),("A Guerra Fria já dividia o mundo",LW(401)),("Na Coreia, militares americanos",LW(92)),
("Relatos de declarações favoráveis",BS(108,180)),("e se o adversário tivesse descoberto",BS(396)),("Lavagem cerebral era a expressão",X("px29906414",15)),
("Mas a palavra sugeria uma precisão",BS(468)),("Prisão, medo, coerção",LW(463)+BS(540)),("Ainda assim, a possibilidade",LW(216)),
("A CIA queria entender drogas",P_("dulles_id",*LW(216))),("Era pesquisa para antecipar",LS(888)),("E também para descobrir",LS(296)),
("O receio virou justificativa",ARQ),("A justificativa abriu a porta",LS(135)),("E os testes avançaram",LS(350)),
# O QUÍMICO
("Em abril de 1953, sob a direção de Allen Dulles",P_("dulles_id")+Dc("aprovado")),("Richard Helms estava entre os dirigentes",HE(587)),
("A figura central na execução",P_("gottlieb",*LS(888))),("É fácil transformar Gottlieb",P_("gottlieb",*LS(888))),("Mas há algo mais inquietante",FICHAS),
("ele era um funcionário com recursos",LS(780,834)),("Uma das substâncias que mais interessavam",LS(1319)),("Doses minúsculas podiam alterar",GOTA+TINTA),
("Isso despertou uma hipótese tentadora",LS(404)),("seria possível induzir uma confissão",LS(565,619)),("O problema é que uma hipótese",LS(1372)),
("Os efeitos variavam",LS(1534)),("A CIA precisava observar pessoas",LS(942)),("Uma parte dos testes envolveu voluntários informados",LS(996)),
("Outra atingiu pessoas que não sabiam",X("mx41439",5)),("Essa distinção muda toda a história",LS(1641)),
# A REDE
("MKUltra não era uma única sala",LS(296)),("Sob o nome do programa, foram identificados",Dc("sub149")),("Parte do financiamento passou por intermediários",FICHAS),
("Quando Stansfield Turner prestou depoimento",P_("turner",*VS(27))+Dc("pesq185","inst80")),("Entre elas, quarenta e quatro",Dc("univ44")),
("Havia ainda fundações",Dc("univ44")),("Esses números não significam",LS(780)),("Significam que o programa tinha uma rede ampla",ARQ),
("Os temas iam de drogas e hipnose",HY(16,140)),("Para a agência, financiar pesquisas",LS(834)),("Mas um laboratório convencional",X("px29241126",4)),
("Uma pessoa que sabe que recebeu",LS(1049)+X("mx41439",5)),("Foi assim que a CIA justificou",ARQ),("os chamados testes com sujeitos",Dc("altosbaixos")),
# OS QUE NÃO SABIAM
("Em meados dos anos 1950, a agência passou",SF(993,1047)),("O relatório interno de inspeção",Dc("ig_niveis")),("O agente George Hunter White",P_("white",*SF(1101))),
("Casas seguras foram usadas",Dc("casas")),("Ali, alguém podia ser convidado",GOTA+X("mx41439",8)),("Alguns dos envolvidos eram pessoas vulneráveis",X("px31042229",5)),
("O Senado ouviu que dependentes",Dc("heroina")),("E ouviu algo mais",VS(192)),("os agentes envolvidos nas casas seguras",LS(780)),
("Não havia um acompanhamento médico",X("px29241126",3)),("Não havia consentimento",X("px9431644",4)),("Não havia sequer uma contagem",ARQ),
("Em um memorando sobre o financiamento",FICHAS+X("mx10395",3)),("O documento que sobreviveu fala sobre despesas",FICHAS),("E, ao falar sobre despesas",SF(1154)),
("Esse é o aspecto mais perturbador",GAVETA),("Às vezes, o vestígio de uma vítima",X("px9431644",8)),
# FRANK OLSON
("Uma pessoa ligada aos testes tem nome",P_("olson",*BW(85))),("Frank Olson era um cientista civil",BW(109,85)),("Em novembro de 1953, participou",X("mx20464",10)),
("Durante o encontro, funcionários da CIA",LS(942)),("Olson recebeu a substância",GOTA),("Nos dias seguintes",X("px31042229",8)),
("Foi levado a Nova York",GV(757,683)),("Na madrugada de 28 de novembro",X("mx22336",5)),("A explicação dada à família omitiu",X("px9431644",3)),
("A esposa e os filhos só souberam",VS(302,357)),("Em julho de 1975, o presidente Gerald Ford",Dc("ford")),("Em 1976, assinou a lei",Dc("ford")),
("A versão oficial classificou",X("px31042229",3)),("A família contestou essa conclusão",P_("olson",*X("px9431644",5))),("É preciso preservar essa diferença",ARQ),
("O LSD administrado sem conhecimento",LS(942)),("Uma teoria definitiva",X("mx22336",8)),("O rosto de Olson torna concreto",P_("olson",*FICHAS)),
# MONTREAL
("A rede alcançou o Canadá",X("mx20464",3)),("Em Montreal, pacientes chegavam",P_("allan",*X("px29241126",2))),("O diretor do instituto, Ewen Cameron",P_("cameron",*X("px29241126",5))),
("Cameron acreditava que poderia desfazer",X("mx46738",6)),("Os seus procedimentos incluíram",HY(109,421)+X("mx14451",10)),("Pessoas que procuravam ajuda",X("mx20464",16)),
("Parte dessa pesquisa recebeu dinheiro",FICHAS),("Um parecer oficial canadense",Dc("cooper_anos")),("O financiamento é documentado",Dc("cooper_anos")),
("Já o grau exato em que a CIA",Dc("cooper_limite")),("Essa precisão importa",HY(140)),("Uma delas, Val Orlikow",X("mx48357",5)),
("O seu depoimento, gravado anos depois",X("mx4135",6)),("o que acontece depois que um paciente",X("px29241126",7)),
# OS INSPETORES
("Em 1963, um inspetor da própria CIA",Dc("ig_niveis")),("O relatório registrou falhas",Dc("ig_minimo")),("Também descreveu uma prática desconcertante",ARQ),
("a agência evitava criar registros",Dc("ig_registros")),("O projeto MKUltra foi encerrado",FICHAS),("Pesquisas relacionadas prosseguiram",TROPA),
("Quanto ao objetivo mais ambicioso",LS(1426,1534)),("O LSD era imprevisível",TINTA),("O dano causado aos sujeitos",LS(1641)),
("É aqui que a história começa a voltar",ARQ),("Se os testes já eram difíceis",GAVETA),
# SETE CAIXAS
("Em 1973, Richard Helms deixava",HE(509)),("Segundo a documentação examinada",Dc("destruidos")),("Em 1975, a investigação do Senado",VS(247)+VS(412)),
("As sete caixas descobertas em 1977",Dc("caixas")),("Os papéis financeiros haviam sido enviados",Dc("deposito")),("Na audiência de 3 de agosto de 1977",P_("turner",*VS(27))),
("O total poderia estar mais perto de oito mil",Dc("oitomil")),("Ele deixou claro que eram sobretudo",FICHAS),("Não um relato completo",ARQ),
("Mesmo assim, as caixas forneceram nomes",Dc("sub149")),("Aquilo que não bastava",Dc("inst80")),("Imagine o contrário",GAVETA),("Se esses registros tivessem recebido",ARQ),
# O QUE SABEMOS
("Com o tempo, o MKUltra passou",X("mx4111",4)),("Assassinos programados",X("mx4135",8)),("Nenhuma dessas alegações",X("mx48357",5)),
("O que os documentos sustentam",Dc("aprovado")),("Um programa secreto financiado",Dc("aprovado")),("Testes com drogas em pessoas",Dc("altosbaixos")),
("Pesquisas intermediadas",Dc("inst80")),("Ocultação de fatos à família",Dc("ford")),("E destruição deliberada",Dc("destruidos")),
("Não temos uma lista completa",ARQ),("Não conhecemos o conteúdo",GAVETA),("Também não há prova",LS(1534)),
("É possível reconhecer duas coisas",FICHAS),("Há limites para o que sabemos",ARQ),("E há fatos suficientes",Dc("caixas")),
# FECHO
("A história começou com uma ordem",Dc("destruidos")),("Terminou com sete caixas",Dc("caixas")),("Elas não devolveram o passado",LS(1641)),
("Não responderam a todas as perguntas",P_("olson",*X("px31042229",5))),("Nem explicaram por inteiro",P_("allan",*X("px29241126",3))),
("Mas deixaram uma pista",FICHAS),("Quando os relatórios desaparecem",Dc("pesq185")),("Se as caixas tivessem sido guardadas",ARQ),
("Escreva nos comentários",GAVETA),("E, para acompanhar outras investigações",Dc("caixas")),
]
POOL={c:ARQ+FICHAS+GAVETA for c in T_}
KEY=[("Em abril de 1953","ABRIL DE 1953"),("A figura central na execução","SIDNEY GOTTLIEB"),("Sob o nome do programa, foram","149 SUBPROJETOS"),
     ("Quando Stansfield Turner","185 PESQUISADORES · 80 INSTITUIÇÕES"),("O agente George Hunter White","GEORGE HUNTER WHITE"),("Frank Olson era um cientista","FRANK OLSON"),
     ("Na madrugada de 28 de novembro","28 DE NOVEMBRO DE 1953"),("Em julho de 1975","JULHO DE 1975"),("O diretor do instituto, Ewen Cameron","EWEN CAMERON"),
     ("Um parecer oficial canadense","1957–1962"),("Em 1963, um inspetor","1963"),("O total poderia estar mais perto","~8.000 PÁGINAS")]
CARDS=[("Encontrou as caixas.","SETE CAIXAS.","branco"),("Não havia consentimento.","SEM CONSENTIMENTO.","vermelho"),("Essa distinção muda toda a história.","QUEM NÃO SABIA.","amarelo")]
LISTA=[]
# trilha de verdade (Mixkit, licença gratuita para vídeo monetizado) no lugar do zumbido sintético: (arquivo, capítulo onde começa, ganho dB)
_M=pathlib.Path("/home/user/estudio-ia/05-biblioteca/musica/mixkit")
ESTILO["trilha"]=[(_M/"echoes-andrew-ev.mp3","ABERTURA",-15),(_M/"tapis-eugenio-mininni.mp3","OS QUE NÃO SABIAM",-19),
                  (_M/"piano-horror-francisco-alvear.mp3","FRANK OLSON",-17),(_M/"echoes-andrew-ev.mp3","OS INSPETORES",-15)]
ESTILO["lufs"]=-16.0   # voz da DarkPlanner já vem em -16: sem limitar picos (limitador forte deixava a voz "dobrada")
