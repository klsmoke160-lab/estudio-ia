"""Plano do vídeo Operação Northwoods: fontes, documento, regras por frase e estilo (referência 05)."""
import json, os, sys, zipfile, io, pathlib
os.environ["DOCS_OCR"]="/home/user/nw/docs"
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[3]/"scripts/video"))
import achar_ocr as achar
from PIL import Image, ImageFilter
NW=pathlib.Path("/home/user/nw"); FULL=NW/"full"
CENAS=json.load(open(NW/"cenas.json")); RAW={k:NW/"raw"/f"{k}.mp4" for k in CENAS}
N={"CI":"1961-04-19_Cuba_Invaded","CT":"1959-01-05_Castro_Triumphs","HR":"1959-07-27_Havana_Rally","UB":"1961-01-05_US_Breaks_Relations_With_Cuba","CC":"1962-10-25_The_Cuban_Crisis",
   "CE":"1962-10-29_Crisis_Eases","KT":"1962-07-23_Kennedy_on_Telstar","RT":"1962-10-22_The_Red_Threat","NN":"1960-11-17_Nuclear_Navy","VN":"1965-02-08_Showdown_in_Vietnam",
   "M6":"612Magic1958","PT":"PlaneTal1965","MI":"miami_the_magic_city","GW":"GovernmentWo","MW":"Maine_wreck_1898","MB":"Maine_burial_1898"}
def C(k,*ts): return [("clip",N[k],t) for t in ts]
def Dc(*ks): return [("doc",k) for k in ks]
def Ft(*ks): return [("foto",k) for k in ks]
FONTE="Estado-Maior Conjunto dos EUA, memorando de 13 de março de 1962 (liberado em 1997)"
_z=None
def _pag(n):
    global _z
    f=FULL/f"p{n:03d}.jpg"
    if not f.exists():
        _z=_z or zipfile.ZipFile(NW/"docs/Northwoods_jp2.zip"); nm=sorted(x for x in _z.namelist() if x.endswith(".jp2"))[n]
        im=Image.open(io.BytesIO(_z.read(nm))).convert("RGB"); im=im.resize((im.width*5//2,im.height*5//2),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,80,2)); im.save(f,quality=92)
    return f
D={}; FALTAM=[]
def doc(key,ini,fim,start=120):
    r=achar.find("Northwoods",ini,fim,start)
    if not r: FALTAM.append((key,ini,fim)); D[key]=(_pag(128),None,(0.5,0.30,0.95),FONTE); return
    n,(W,H),bx,_=r; f=_pag(n); k=Image.open(f).size[0]/W
    D[key]=(f,[[b[0]*k,b[1]*k,b[2]*k,b[3]*k] for b in bx],None,FONTE)
def pagina(key,n,foco): D[key]=(_pag(n),None,foco,FONTE)
pagina("capa",128,(0.5,0.30,0.95)); pagina("ficha",2,(0.5,0.45,0.95)); pagina("lista_pg",137,(0.5,0.62,0.9))
doc("navio","We could blow up a US ship","blame Cuba."); doc("assunto","Subject: Justification","Cuba (TS)"); doc("pedido","brief but precise","intervention in Cuba.")
doc("boatload","We could sink a boatload","or simulated)."); doc("bombas","Exploding a few plastic","chosen spots"); doc("estudantes","The passengers could be","on a holiday")
doc("objetivo","to place the United States","government of Cuba"); doc("imagem","to develop an","Western Hemisphere."); doc("meses","Time is an","next few months.")
doc("incidentes","A series of well coordinated","hostile Cuban forces."); doc("funerais","Conduct funerals","for mock"); doc("terror","We could develop a Communist","even in Washington.")
doc("ferir","We could foster attempts","widely publicized."); doc("maine","incident could be arranged","several forms:"); doc("tripulacao","follow up with an air/sea","non-existent")
doc("indignacao","Casualty lists in US","national indignation."); doc("airliner","shot down a chartered","civil airliner"); doc("duplicata","would be painted and numbered","exact duplicate")
doc("aliases","all boarded under","prepared aliases."); doc("drone","would be converted","to a drone."); doc("mayday","distress frequency","by Cuban MIG"); doc("vender","instead of the US","the incident.")
doc("f86","An F-86 properly painted","Cuban MIG,"); doc("tresmeses","reasonable copies of the MIG","three months."); doc("jumped","had been jumped by MIGs","going down."); doc("verdade","would have a true story","they knew.")
doc("nato","This paper NOT be forwarded","NATO activities.",start=0)
FOTOS={"d_aviao":(str(FULL/"diag_aviao.png"),0.5,"Esquema feito a partir do item 8 do memorando"),"d_cacas":(str(FULL/"diag_cacas.png"),0.5,"Esquema feito a partir do item 9 do memorando"),
       "painel":(str(FULL/"painel.png"),0.5,None)}
TITULO=("OPERAÇÃO NORTHWOODS","O plano de 1962 para fabricar uma guerra",("doc","capa"))
ESTILO=dict(cinema=False,dur_plano=2.6,zoom=0.06,cama=-27,golpe=-5)
R=[
("Poderíamos explodir um navio americano na Baía de Guantánamo e culpar Cuba.",Dc("navio")),
("Essa frase não saiu de um filme",C("CC",59)),("Nem de um fórum",C("CC",63)),
("Ela está em um memorando de 13 de março",Dc("capa")),("Quem assina é o general",C("VN",85)),
("O mesmo papel sugere afundar",Dc("boatload")),("Espalhar bombas em Miami",Dc("bombas")),("E simular a derrubada",Dc("estudantes")),
("Tudo para ser colocado na conta",C("HR",20)),("O documento é verdadeiro",Dc("capa")),("Você vai ver as páginas",Dc("lista_pg")),
("Se o plano existiu",C("KT",36)+Dc("navio")),
("Em abril de 1961",C("CI",6,22,90)),("O objetivo era derrubar",C("HR",13)),("Durou três dias",C("CI",104)),("A invasão foi esmagada",C("CI",94,116)),
("E o mundo inteiro soube",C("CI",49)),("Foi a maior humilhação",C("KT",22)),("O presidente não desistiu",C("KT",68)),
("No comando das operações",C("GW",424,431)),("Os Estados Unidos não podiam",C("CC",249,25)),("Faltava o motivo",C("GW",698)),
("O pedido está citado",Dc("pedido")),("Uma descrição breve",Dc("pedido")),("À frente dele estava",C("VN",60)),("A resposta ficou pronta",Dc("capa")),("O assunto, escrito",Dc("assunto")),
("Justificativa para intervenção",Dc("assunto")),("E o que vem depois",Dc("lista_pg")),
("O resultado desejado",Dc("objetivo")),("E criar, no mundo",Dc("imagem")),("O documento tem pressa",Dc("meses")),("Diz que o tempo",Dc("meses")),
("A lista começa em Guantánamo",C("CC",49,54)),("O plano era fabricar",Dc("incidentes")),("E há um item que é difícil",Dc("funerais")),("Realizar funerais",Dc("funerais")),
("O texto propõe desenvolver",Dc("terror")),("Explodir algumas bombas",Dc("bombas")),("O documento fala em afundar",Dc("boatload")),("E, entre parênteses",Dc("boatload")),
("Fala também em promover",Dc("ferir")),
("Um dos itens tem um título",Dc("maine")),("Em 1898, o navio de guerra",C("MW",20,35)),("Morreram mais de",C("MB",30,60)),("A causa da explosão",C("MW",48)),
("Em poucos meses",C("MB",90)),("O memorando diz, com todas",Dc("navio")),("Poderíamos explodir um navio americano na Baía de Guantánamo e culpar Cuba.",Dc("navio")),
("Ou explodir uma embarcação",Dc("tripulacao")),("As listas de vítimas",Dc("indignacao")),
("O item mais detalhado",C("M6",272,281)),("A proposta era fazer",Dc("airliner")),("Os passageiros, sugere",Dc("estudantes")+C("M6",382)),("O truque funcionaria",Ft("d_aviao")),
("Numa base aérea da Flórida",Dc("duplicata")),("Na hora marcada",Dc("aliases")+C("M6",288)),("O avião verdadeiro",Dc("drone")),("Os dois se encontrariam",Ft("d_aviao")),
("O avião com os passageiros",Ft("d_aviao")),("Sobre Cuba, o drone",Dc("mayday")),("Mayday.",C("PT",713)),("A transmissão seria cortada",C("M6",45)),("O documento explica a vantagem",Dc("vender")),
("O texto chega a calcular",Dc("f86")),("Um caça americano, pintado",Dc("f86")+C("VN",142)),("Cópias razoáveis",Dc("tresmeses")),("Outro item descreve",C("VN",151,134)),
("Quatro ou cinco aviões",Ft("d_cacas")),("Perto da ilha, esse piloto",Dc("jumped")),("Em vez de cair",Ft("d_cacas")),("No mesmo instante, um submarino",C("NN",47)+Ft("d_cacas")),
("O documento faz questão",Dc("verdade")),("Os outros pilotos voltariam",Dc("verdade")),
("A última página traz",Dc("nato")),("O papel não deveria ser enviado",Dc("nato")),("Três dias depois, em 16 de março",C("VN",235)+C("KT",27)),("A resposta do presidente",C("KT",36)),
("Ele disse que não estava discutindo",C("RT",23)),("Nenhum navio foi explodido",C("CC",59)),("Nenhum avião decolou",C("PT",731)),("Nenhuma bomba foi plantada",C("MI",502)),
("Sete meses depois da reunião",C("RT",110)+C("CC",164)),("Durante treze dias",C("CC",174,231)),("É impossível saber",C("CC",54,141)),
("O papel ficou guardado",C("GW",748,754)),("Uma comissão independente",C("GW",733,707)),("Em novembro de 1997",Dc("ficha")),("Quase ninguém notou",C("GW",726)),
("Quatro meses depois, aviões",C("M6",45)),
("Em agosto de 1964",C("VN",122,129)),("Dois dias depois, a Marinha",C("VN",85)),("O presidente Lyndon Johnson",C("VN",235,245)),("Décadas depois, um estudo",C("GW",154,116)),
("A primeira parte é fato",Dc("capa")),("Quem diz que governos",Dc("navio")),("O documento mostra um plano proposto",Ft("painel")),("Ele não mostra um plano executado",Ft("painel")),
("Mostra também o momento",C("KT",36)),("O memorando só sobreviveu",Dc("ficha")),("Se as propostas tivessem",C("GW",748)),
("A frase era real",Dc("navio")),("Porque um homem, numa sala",C("KT",36)),("Havia só a decisão",C("RT",183)),("Um plano que fica escrito",Dc("capa")),("A pergunta que fica é sobre os papéis",C("GW",754,748)),
("Me conta nos comentários",C("GW",726)),("E, para acompanhar",Dc("capa")),
]
POOL={
"ABERTURA":C("CC",59,63)+Dc("capa"),
"CUBA, 1961":C("CT",11,21,41,82,101)+C("HR",6,17,23)+C("UB",5,8,16,24)+C("CI",14,29,85,121,125)+C("KT",22,68),
"A ENCOMENDA":C("GW",47,138,150,389,393,611,626,635)+C("VN",60,85),
"O OBJETIVO":Dc("objetivo","imagem","meses")+C("GW",611,621,116),
"A LISTA":C("CC",49,54,63,67,70,73)+C("MI",34,510,574)+C("CT",95,107,113),
"LEMBREM-SE DO MAINE":C("MW",20,35,48)+C("MB",30,60,90,120)+C("CC",59),
"O AVIÃO":C("M6",221,272,281,288,301,326,342,361,412,463,479,532)+C("PT",4,9,640,671,713,747,812,903,916),
"OS CAÇAS FALSOS":C("VN",112,122,134,142,151)+C("CC",141,156)+C("NN",63,74,81)+C("PT",903,916,932),
"TRÊS DIAS DEPOIS":C("KT",22,27,36,68)+C("VN",235,237)+C("GW",424,440),
"O GENERAL":C("VN",60,85,173)+C("CC",224,228,235,238,243)+C("CE",5,11,19,29)+C("RT",23,110),
"TRINTA E CINCO ANOS NUMA CAIXA":C("GW",748,754,733,726,700,698,707,154)+Dc("ficha"),
"DOIS ANOS DEPOIS":C("VN",112,122,129,134,60,85,173,182,204),
"O QUE O DOCUMENTO PROVA":Dc("capa","navio","lista_pg","ficha")+C("GW",748,726)+C("KT",36),
"FECHO":C("KT",36,68)+C("GW",754,748,726)+Dc("capa"),
}
KEY=[("Em abril de 1961","BAÍA DOS PORCOS, 1961"),("Operação Mangusto","OPERAÇÃO MANGUSTO"),("Edward Lansdale","EDWARD LANSDALE"),("À frente dele estava","LYMAN LEMNITZER"),
("A resposta ficou pronta","13 DE MARÇO DE 1962"),("Em 1898, o navio","HAVANA, 1898"),("Robert McNamara","ROBERT McNAMARA"),("Três dias depois, em 16 de março","16 DE MARÇO DE 1962"),
("Sete meses depois da reunião","OUTUBRO DE 1962"),("Em novembro de 1997","NOVEMBRO DE 1997"),("Foi só em 2001","2001"),("Em agosto de 1964","GOLFO DE TONKIN, 1964")]
CARDS=[("Pretextos.","PRETEXTOS.","amarelo"),("Northwoods.","NORTHWOODS","branco"),("Real ou simulado.","REAL OU SIMULADO.","amarelo"),("Útil.","ÚTIL.","vermelho")]
LISTA=[("Espalhar boatos","Boatos por rádio clandestina"),("Colocar cubanos aliados","Ataque encenado à base"),("Provocar tumultos","Tumultos no portão"),("Incendiar munição","Munição incendiada"),
("Sabotar um navio","Navio sabotado no porto"),("Realizar funerais","Funerais para vítimas falsas"),("campanha de terror comunista","Terror em Miami e em Washington"),("Explodir algumas bombas","Bombas de plástico"),
("afundar um barco cheio","Barco de refugiados afundado"),("promover atentados","Atentados contra refugiados")]
