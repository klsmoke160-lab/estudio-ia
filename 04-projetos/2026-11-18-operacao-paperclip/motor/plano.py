"""Plano da Operação Paperclip: fontes, documentos (transcrições oficiais), fotos da NASA e regras por frase.
Ordem de abertura pedida pelo dono (lista do ChatGPT): decolagem da Apollo 11 → Rudolph → corte seco para o escuro da montanha."""
import json, pathlib
PC = pathlib.Path("/home/user/mk/pc"); RAWD = PC / "raw"; NA = PC / "nasa"; DOC = PC / "docs"
CENAS = json.load(open(PC / "cenas3.json")); RAW = {k: RAWD / f"{k}.mp4" for k in CENAS}
def C(k, *ts): return [("clip", k, t) for t in ts]
def Dc(*ks): return [("doc", k) for k in ks]
def Fo(*ks): return [("foto", k) for k in ks]

# ---------- documentos: transcrições oficiais com marca-texto (gerar_docs.py) ----------
_DJ = json.load(open(DOC / "docs.json"))
FONTES = {"memo": "Memorando de Acheson a Truman, 30/08/1946 (FRUS 1946, vol. V)", "jioa": "Arquivo Nacional dos EUA, registros da JIOA (RG 330)",
          "nara": "Arquivo Nacional dos EUA, dossiês de cientistas (RG 330)", "smith": "Smithsonian, National Air and Space Museum (Neufeld, 2020)"}
D = {}
def doc(chave, pagina, *trechos, foco=None):
    arq, cx = _DJ[pagina]; boxes = sum([cx[t] for t in trechos], [])
    D[chave] = (arq, boxes, foco, FONTES[pagina])
doc("memo_curto", "memo", "for short-term exploitation"); doc("memo_perda", "memo", "may be lost to us unless steps are taken quickly")
doc("memo_800", "memo", "between 800 and 1000 specialists"); doc("memo_familias", "memo", "bringing members of specialists' families")
doc("memo_exclui", "memo", "excluding from the program persons with Nazi or militaristic records"); doc("memo_status", "memo", "granted regular status under the immigration laws")
doc("memo_truman", "memo", "Approved 9/3/46 Harry S Truman")
doc("jioa_nomes", "jioa", "initially code-named Overcast", "subsequently code-named Paperclip"); doc("jioa_dossie", "jioa", "compiling dossiers")
doc("jioa_brit", "jioa", "liaison to British intelligence officers"); doc("jioa_1962", "jioa", "The JIOA was disbanded in 1962.")
doc("nara_1500", "nara", "over 1,500 German and other foreign scientists"); doc("nara_rickhey", "nara", "Georg Rickhey", "tried (and acquitted) for war crimes")
doc("nara_schreiber", "nara", "Walter Schreiber", "fled the United States to Argentina in 1952"); doc("nara_rudolph", "nara", "Arthur Rudolph", "left the United States in 1984")
doc("nara_braun", "nara", "one for rocket scientist Wernher von Braun. It was never transferred to NARA.")
doc("smith_mortos", "smith", "20,000 to 25,000 detainees died", "out of 60,000 sent there"); doc("smith_10mil", "smith", "A minimum of 10,000 deaths")
doc("smith_dobro", "smith", "more than twice as many Allied prisoners died")

# ---------- fotos ----------
FOTOS = {
 "apollo": (str(NA / "apollo11_lancamento.jpg"), 0.35, "Apollo 11, 16 de julho de 1969 · NASA"),
 "apollo2": (str(NA / "apollo11_lancamento2.jpg"), 0.35, "Apollo 11, 16 de julho de 1969 · NASA"),
 "grupo1959": (str(NA / "grupo_1959_rudolph.jpg"), 0.30, "Huntsville, 1959: Arthur Rudolph e von Braun estão no grupo · NASA"),
 "rendicao": (str(NA / "rendicao_1945.jpg"), 0.30, "Von Braun se rende ao Exército dos EUA, maio de 1945 · NASA"),
 "fortbliss": (str(NA / "fortbliss_equipe.jpg"), 0.40, "A equipe alemã em Fort Bliss, Texas · NASA"),
 "v2ws": (str(NA / "v2_whitesands_1946.jpg"), 0.35, "V-2 em White Sands, Novo México, 1946 · NASA"),
 "v2estatico": (str(NA / "v2_teste_estatico_1947.jpg"), 0.30, "V-2 em teste estático, White Sands, 1947 · NASA"),
 "v2abrigo": (str(NA / "v2_abrigo.jpg"), 0.45, "V-2 saindo do abrigo camuflado, Alemanha · NASA"),
 "braunf1": (str(NA / "vonbraun_f1.jpg"), 0.45, "Von Braun sob os motores F-1 do Saturno V · NASA"),
 "ladybird": (str(NA / "ladybird_marshall.jpg"), 0.30, "Von Braun e Lady Bird Johnson no Centro Marshall, 1964 · NASA"),
 "braun1960": (str(NA / "vonbraun_retrato_1960.jpg"), 0.25, "Wernher von Braun, diretor do Centro Marshall · NASA"),
 "lua": (str(NA / "lua_aldrin.jpg"), 0.30, "Buzz Aldrin na Lua, 20 de julho de 1969 · NASA"),
 "luabandeira": (str(NA / "lua_bandeira.jpg"), 0.35, "Apollo 11 na superfície da Lua · NASA"),
 "certificado": (str(DOC / "certificado_1945.png"), 0.45, "Certificado do Exército dos EUA sobre os filmes dos campos, 1945"),
 "d_kohnstein": (str(DOC / "d_kohnstein.png"), 0.5, None),
}

# ---------- filmes ----------
A11 = lambda *t: C("A11L", *t); PAD = lambda *t: C("A11P", *t); GS = lambda *t: C("GS", *t); VR = lambda *t: C("VR", *t); GT = lambda *t: C("GT", *t)
PE = lambda *t: C("PE", *t); TE = lambda *t: C("TE", *t); Y45 = lambda *t: C("Y45", *t); AO = lambda *t: C("AO", *t); AB = lambda *t: C("AB", *t); SAT = lambda *t: C("SAT", *t)
AR = {k: 4/3 for k in CENAS}
PRE = {"A11L": "crop=960:720:160:0", "A11P": "crop=960:720:160:0", "GT": "crop=1440:1080:240:0", "PE": "crop=1440:1080:240:0", "Y45": "crop=1440:1080:240:0"}
TITULO = ("PAPERCLIP", "O filtro que deixou passar", ("foto", "fortbliss"))
T_ = {"ABERTURA": "ambar", "A CORRIDA": "petroleo", "A FÁBRICA": "vermelho", "O PEDIDO": "petroleo", "O FILTRO": "verde", "OS CIENTISTAS": "ambar",
      "OS QUE PASSARAM": "verde", "A LUA": "azul", "A CONTA": "vermelho", "O QUE SABEMOS": "petroleo", "FECHO": "ambar"}
_M = pathlib.Path("/home/user/estudio-ia/05-biblioteca/musica/mixkit")
ESTILO = dict(cinema=True, tint=T_, dur_plano=4.0, zoom=0.045, nasce=4.0, brilho=-0.10, cama=-24, golpe=-3, lufs=-16.0,
              trilha=[(_M / "echoes-andrew-ev.mp3", "ABERTURA", -15), (_M / "piano-horror-francisco-alvear.mp3", "A FÁBRICA", -17),
                      (_M / "tapis-eugenio-mininni.mp3", "O PEDIDO", -19), (_M / "echoes-andrew-ev.mp3", "A LUA", -15),
                      (_M / "piano-horror-francisco-alvear.mp3", "A CONTA", -17), (_M / "echoes-andrew-ev.mp3", "O QUE SABEMOS", -15)])
AVISO = "REGISTROS DE ARQUIVO · DOCUMENTOS EM TRANSCRIÇÃO OFICIAL"

R = [
# ABERTURA
("Em julho de 1969, um foguete", A11(118, 128)), ("O gerente do programa que construiu", Fo("grupo1959")),
("Vinte e cinco anos antes", Fo("d_kohnstein")), ("Quem montava os mísseis eram prisioneiros", GT(831)), ("Milhares deles morreram ali", Fo("certificado")),
("Em 1984, depois de uma investigação", Dc("nara_rudolph")), ("O nome dele era Arthur Rudolph", Fo("grupo1959")), ("E ele não chegou sozinho", Fo("fortbliss")),
("Entre 1945 e o fim dos anos 1950", Dc("nara_1500")), ("Em segredo", GS(93)), ("Com um filtro que deveria barrar", Dc("memo_exclui")),
("Esta é a história desse filtro", GS(517)), ("E de quem passou por ele", GS(146)),
# A CORRIDA
("Maio de 1945", Y45(240)), ("A Alemanha se rende", Y45(266)), ("E, antes mesmo do fim da guerra", AO(61)), ("Os aliados não queriam só fábricas", AO(184)),
("Queriam as pessoas que sabiam", GT(893)), ("A Alemanha estava à frente", GT(646, 1755)), ("Quem levasse esses especialistas", GT(1077)),
("Os americanos chegaram primeiro", AO(160)), ("Os soviéticos chegaram a outros", Y45(89)), ("E o medo era o mesmo", Y45(114)), ("que o rival ficasse", GT(954)),
("Do lado americano, a operação começou", Dc("jioa_nomes")), ("Overcast", Dc("jioa_nomes")), ("Depois, ganhou o nome", Dc("jioa_nomes")), ("Paperclip.", GS(13)),
("Clipe de papel", GS(13)), ("A explicação mais contada", GS(146)), ("os arquivos dos cientistas escolhidos", Dc("jioa_dossie")),
("Os soviéticos agiram de outro jeito", Y45(63)), ("Em uma única noite de outubro de 1946", AO(135, 160)), ("Não houve convite", Y45(89)), ("Houve ordem", Y45(114)),
("A disputa por cérebros", GT(462)),
# A FÁBRICA
("Para entender quem estava nesses arquivos", Fo("d_kohnstein")), ("No fim do verão de 1943", Fo("v2abrigo", "d_kohnstein")), ("A fábrica se chamava Mittelwerk", GT(831)),
("Para escavar os túneis", GT(1755)), ("Primeiro de Buchenwald", Fo("certificado")), ("Depois, um campo próprio", Fo("d_kohnstein")), ("Dora.", Fo("d_kohnstein")),
("Os prisioneiros que faziam o trabalho", GT(1262)), ("Os que eram acusados de sabotagem", PE(20)), ("Nos primeiros meses, os prisioneiros dormiam", Fo("d_kohnstein")),
("Só na primavera de 1944", GT(1016)), ("O Museu Nacional do Ar e do Espaço", Dc("smith_mortos")), ("Pelo menos dez mil dessas mortes", Dc("smith_10mil")),
("E o museu registra um dado", Dc("smith_dobro")), ("Morreram mais que o dobro", Dc("smith_dobro")), ("Em abril de 1945, soldados americanos chegaram", AO(61, 184)),
("Encontraram a fábrica quase intacta", GT(831)), ("E encontraram os corpos", Fo("certificado")),
# O PEDIDO
("Os americanos tinham pressa", AO(160)), ("Os engenheiros que sabiam fazer o V-2", GT(893, 1755)), ("O mais famoso deles se entregou", Fo("rendicao")),
("Wernher von Braun.", Fo("rendicao")), ("Trinta e três anos", Fo("rendicao")), ("O diretor técnico do programa do V-2", PE(60)),
("Nos primeiros meses, a operação funcionava", Dc("memo_curto")), ("Mas, no verão de 1946", Dc("memo_perda")), ("muitos desses especialistas poderiam", Dc("memo_perda")),
("Em 30 de agosto de 1946", Dc("memo_800")), ("O documento propunha ampliar", Dc("memo_800")), ("Os alemães poderiam trazer as famílias", Dc("memo_familias")),
("A custódia ficaria mais frouxa", Dc("memo_familias")), ("E, mais adiante, os escolhidos receberiam", Dc("memo_status")), ("Era um programa pensado", GS(464)), ("Isso nunca aconteceu", AB(669)),
# O FILTRO
("O mesmo memorando trazia uma condição", Dc("memo_exclui")), ("O Departamento de Guerra seria responsável", Dc("memo_exclui")), ("Quem verificaria isso", Dc("jioa_nomes")),
("Em inglês, JIOA", Dc("jioa_nomes")), ("Ela reunia representantes", GS(199)), ("Entre as tarefas dela", Dc("jioa_dossie")), ("A JIOA também recolhia", Dc("jioa_brit")),
("Ou seja:", AB(615)), ("era ela quem montava o dossiê", Dc("jioa_dossie")), ("Truman aprovou o memorando", Dc("memo_truman")), ("Está escrito à mão", Dc("memo_truman")),
("No papel, o filtro existia", GS(517)), ("A pergunta é o que aconteceu", GS(305)),
# OS CIENTISTAS
("Von Braun entrou para o Partido Nazista", Fo("rendicao")), ("Em 1940, entrou para as SS", Fo("rendicao")), ("Chegou ao posto de major", GT(92)),
("Ele sempre disse que entrou por pressão", Fo("braun1960")), ("Também disse que não tinha responsabilidade", GT(831)), ("Historiadores que estudaram os arquivos", Fo("d_kohnstein")),
("O grau exato da responsabilidade", Fo("braun1960")), ("Nos Estados Unidos, o grupo de von Braun", Fo("fortbliss")), ("Lá, e no campo de testes de White Sands", GS(438) + Fo("v2estatico")),
("Os foguetes que tinham caído sobre Londres", VR(14) + Fo("v2ws")), ("Em 1950, o grupo foi transferido para Huntsville", AB(187)), ("A cidade viraria o centro", AB(1365)),
("E, depois, da NASA", AB(562)), ("Von Braun não estava sozinho", AB(241)), ("Com ele vieram engenheiros", AB(883)), ("Em poucos anos, uma cidade pequena", AB(722, 669)),
# OS QUE PASSARAM
("Os arquivos da própria agência", Dc("nara_1500")), ("O Arquivo Nacional americano guarda os dossiês", Dc("nara_1500")), ("Três deles ajudam", AB(615)),
("Georg Rickhey era um dos dirigentes", Dc("nara_rickhey")), ("Chegou aos Estados Unidos em 1946", Dc("nara_rickhey")), ("No ano seguinte, foi mandado de volta", Dc("nara_rickhey")),
("Foi absolvido", Dc("nara_rickhey")), ("Walter Schreiber era médico", Dc("nara_schreiber")), ("Segundo o Arquivo Nacional, teve papel", Dc("nara_schreiber")),
("Trabalhou para a Força Aérea", GS(491)), ("Em 1952, depois que uma coluna", Dc("nara_schreiber")), ("E Arthur Rudolph.", Dc("nara_rudolph")),
("O gerente de produção da Mittelwerk", GT(831)), ("Há ainda um detalhe", Dc("nara_braun")), ("O dossiê de Wernher von Braun não está lá", Dc("nara_braun")),
("Segundo o próprio Arquivo Nacional, ele nunca", Dc("nara_braun")), ("Isso não prova que alguém escondeu", Fo("braun1960")), ("Prova que o documento mais importante", Dc("nara_braun")),
# A LUA
("Nos anos 1960, a corrida passou", SAT(7)), ("Chegar à Lua antes dos soviéticos", TE(43, 101)), ("Von Braun virou o rosto público", SAT(49)),
("Apareceu em programas de televisão", Fo("ladybird", "braunf1")), ("Arthur Rudolph foi o gerente do programa do Saturno Cinco", Fo("braunf1")),
("Em 16 de julho de 1969", PAD(10) + A11(118)), ("Quatro dias depois, Neil Armstrong", Fo("lua")), ("Na época, ninguém fora do governo", Fo("luabandeira")),
("Os nomes dos mais famosos", SAT(49)), ("Os dossiês, não", Dc("jioa_dossie")), ("Para o público, a Paperclip", A11(135)), ("A história contada era a de cientistas", Fo("braunf1")),
("Era uma história confortável", Fo("apollo2")), ("Ela só deixava de fora os túneis", Fo("d_kohnstein")),
# A CONTA
("Em 1979, o Departamento de Justiça criou", Dc("nara_rudolph")), ("O Escritório de Investigações Especiais", AB(1204)), ("Os investigadores reabriram", GT(831)),
("E chegaram a Arthur Rudolph", Fo("grupo1959")), ("Segundo a acusação", GT(1262)), ("Rudolph negou", Fo("grupo1959")), ("Em vez de enfrentar um processo", AB(1204)),
("Deixaria os Estados Unidos", Dc("nara_rudolph")), ("Em troca, não seria processado", Fo("grupo1959")), ("Em 1984, mudou-se para a Alemanha", Dc("nara_rudolph")),
("Morreu lá, em 1996", Fo("grupo1959")), ("Um ano depois da saída de Rudolph", Dc("jioa_dossie")), ("A agência já não existia desde 1962", Dc("jioa_1962")),
("As acusações nunca foram confirmadas", AB(615)), ("E muitos dos papéis que poderiam", Dc("nara_braun")), ("Eles só começaram a sair em massa", Dc("nara_1500")),
("Foi por essa lei que os dossiês", Dc("nara_rickhey", "nara_schreiber")),
# O QUE SABEMOS
("A Paperclip virou combustível", TE(217)), ("Bases secretas, tecnologias escondidas", TE(72)), ("Vale separar o que está nos documentos", Dc("nara_1500")),
("Está nos documentos que o programa existiu", Dc("nara_1500")), ("Está nos documentos que a regra exigia", Dc("memo_exclui")), ("Está nos documentos que von Braun foi membro", Fo("rendicao")),
("Está nos documentos que pelo menos um homem", Dc("nara_rudolph")), ("E que outro deixou o país", Dc("nara_schreiber")), ("O que os documentos não mostram", Fo("fortbliss")),
("Os papéis mostram outra coisa", Dc("memo_perda")), ("A pressa e o interesse militar", Dc("memo_perda")), ("E a acusação de dossiês alterados", Dc("jioa_dossie")),
("Forte, com documentos citados", Dc("jioa_dossie")), ("Mas sem uma conclusão oficial", Dc("jioa_1962")), ("Também não é possível dizer", Fo("apollo")), ("Isso é uma suposição", TE(101)),
# FECHO
("Quando a Apollo 11 pousou", Fo("luabandeira")), ("Poucos sabiam que parte daquele caminho", A11(125)), ("Em túneis onde milhares", Fo("d_kohnstein")),
("Para os prisioneiros de Dora", Fo("certificado")), ("O filtro existia no papel", Dc("memo_exclui")), ("Na prática, ele foi tão forte", Fo("grupo1959")),
("Fica uma pergunta", A11(163)), ("Até onde um país deve ir", A11(188)), ("Me conta nos comentários", Fo("apollo")), ("E, para acompanhar outras histórias", Fo("fortbliss")),
]
POOL = {c: GS(146, 464, 517) + GT(893, 954) + AB(241) for c in T_}
KEY = [("Em julho de 1969, um foguete", "JULHO DE 1969"), ("O nome dele era Arthur Rudolph", "ARTHUR RUDOLPH"), ("Maio de 1945", "MAIO DE 1945"),
       ("A fábrica se chamava Mittelwerk", "MITTELWERK"), ("Wernher von Braun.", "WERNHER VON BRAUN"), ("Em 30 de agosto de 1946", "30 DE AGOSTO DE 1946"),
       ("Truman aprovou o memorando", "3 DE SETEMBRO DE 1946"), ("Georg Rickhey era um dos dirigentes", "GEORG RICKHEY"), ("Walter Schreiber era médico", "WALTER SCHREIBER"),
       ("Em 1950, o grupo foi transferido", "HUNTSVILLE, 1950"), ("Em 16 de julho de 1969", "16 DE JULHO DE 1969"), ("Em 1984, mudou-se para a Alemanha", "1984"),
       ("Eles só começaram a sair em massa", "1998")]
CARDS = [("Não houve convite.", "NÃO HOUVE CONVITE.", "branco"), ("Houve ordem.", "HOUVE ORDEM.", "vermelho"), ("Isso nunca aconteceu.", "ISSO NUNCA ACONTECEU.", "branco"),
         ("Os dossiês, não.", "OS DOSSIÊS, NÃO.", "vermelho")]
LISTA = []
