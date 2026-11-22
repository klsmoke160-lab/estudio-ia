"""Plano do Iceberg das Conspirações: junta o material já conferido de MKUltra, Northwoods, Paperclip e Golfo de Tonkin
com as páginas novas (COINTELPRO, CIA/OVNIs, visão remota, Roswell, Clinton/Tuskegee), fotos da NASA e filmes de domínio público.
Os cartões dos níveis usam filmagem real de icebergs (Mixkit). Sem imagem gerada por IA."""
import importlib.util, json, pathlib
P = pathlib.Path("/home/user/estudio-ia/04-projetos")
def _load(nome, rel):
    sp = importlib.util.spec_from_file_location("plano_" + nome, P / rel / "motor/plano.py"); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
MK = _load("mk", "2026-11-17-mkultra-v3"); NW = _load("nw", "2026-11-15-operacao-northwoods")
PC = _load("pc", "2026-11-18-operacao-paperclip"); TK = _load("tk", "2026-11-22-golfo-de-tonkin")
ICE = pathlib.Path("/home/user/mk/ice"); DOC = ICE / "docs"; NASA = ICE / "nasa"

# ---------- material juntado (o primeiro que define um nome vale) ----------
CENAS, RAW, D, FOTOS, AR, PRE = {}, {}, {}, {}, {}, {}
for m in (MK, NW, PC, TK):
    for k, v in m.CENAS.items(): CENAS.setdefault(k, v); RAW.setdefault(k, m.RAW[k])
    for k, v in m.D.items(): D.setdefault(k, v)
    for k, v in getattr(m, "FOTOS", {}).items(): FOTOS.setdefault(k, v)
    for k, v in getattr(m, "AR", {}).items(): AR.setdefault(k, v)
    for k, v in getattr(m, "PRE", {}).items(): PRE.setdefault(k, v)
_C = json.load(open(ICE / "cenas.json"))
for k, v in _C.items(): CENAS[k] = v; RAW[k] = next((ICE / "raw").glob(k + ".*"))
AR.update({k: 16/9 for k in _C if k.startswith("mx")}); AR.update({"FBI": 4/3, "PW": 4/3, "SC": 4/3})

_DJ = json.load(open(DOC / "docs.json"))
_FT = {"coin": "Senado dos EUA, Comissão Church, livro III (1976)", "ufo": "Gerald K. Haines, \"CIA's Role in the Study of UFOs, 1947-90\", CIA (1997)",
       "rv": "American Institutes for Research, avaliação da visão remota para a CIA (1995)", "roswell": "Força Aérea dos EUA, The Roswell Report (1994)",
       "clinton": "Discurso de Bill Clinton, 16 de maio de 1997 (The American Presidency Project)"}
for k, (arq, bx) in _DJ.items(): D[k] = (arq, bx, None, _FT[k.split("_")[0]])

for k in range(6): FOTOS[f"d_iceberg{k}"] = (str(DOC / f"iceberg_{k}.png"), 0.5, None)
FOTOS["d_gelo"] = (str(DOC / "gelo_titulo.png"), 0.5, None)
FOTOS.update({"d_lro_apollo": (str(NASA / "PIA12889.jpg"), 0.5, "Locais de pouso da Apollo vistos pela sonda LRO · NASA"),
              "d_lro_a17": (str(NASA / "PIA12920.jpg"), 0.5, "Apollo 17: o estágio de descida do módulo lunar, visto pela sonda LRO · NASA"),
              "d_terra_lua": (str(NASA / "GSFC_20171208_Archive_e000496.png"), 0.45, "A Terra vista da órbita da Lua pela sonda LRO · NASA"),
              "d_terra_iss": (str(NASA / "iss066e152099.jpg"), 0.5, "O horizonte da Terra visto da Estação Espacial Internacional, 2022 · NASA"),
              "u2": (str(NASA / "GRC-1973-C-03389.jpg"), 0.5, "Avião U-2 · NASA (1973)")})

def C(k, *ts): return [("clip", k, t) for t in ts]
def Dc(*ks): return [("doc", k) for k in ks]
def Fo(*ks): return [("foto", k) for k in ks]
NWc = NW.C; LS, SF, HE, VS = MK.LS, MK.SF, MK.HE, MK.VS
GELO = C("mx25244", 10, 30) ; GELO2 = C("mx25245", 8); DEGELO = C("mx8128", 4); BORDA = C("mx15233", 12)
FICHAS, ARQ, GAVETA = MK.FICHAS, MK.ARQ, MK.GAVETA
PAPEL = C("mx34154", 8)
TITULO = ("ICEBERG", "Até onde vai a verdade", ("foto", "d_gelo"))
T_ = {"ABERTURA": "ambar", "O ICEBERG": "azul", "NÍVEL 1: CONFESSADO": "vermelho", "NÍVEL 2: PROVADO NOS PAPÉIS": "ambar",
      "NÍVEL 3: O SEGREDO QUE VIROU LENDA": "verde", "NÍVEL 4: SEM PROVA": "azul", "NÍVEL 5: O FUNDO": "azul",
      "O QUE O ICEBERG ENSINA": "petroleo", "FECHO": "azul"}
NOMES_CAP = {"NÍVEL 1: CONFESSADO": "CONFESSADO", "NÍVEL 2: PROVADO NOS PAPÉIS": "PROVADO NOS PAPÉIS", "NÍVEL 3: O SEGREDO QUE VIROU LENDA": "O SEGREDO QUE VIROU LENDA",
             "NÍVEL 4: SEM PROVA": "SEM PROVA", "NÍVEL 5: O FUNDO": "O FUNDO"}
_M = pathlib.Path("/home/user/estudio-ia/05-biblioteca/musica/mixkit")
ESTILO = dict(cinema=True, tint=T_, dur_plano=4.0, zoom=0.045, nasce=4.0, nasce_abertura=0.4, brilho=-0.10, cama=-24, golpe=-3, lufs=-16.0,
              trilha=[(_M / "echoes-andrew-ev.mp3", "ABERTURA", -15), (_M / "tapis-eugenio-mininni.mp3", "CONFESSADO", -19),
                      (_M / "piano-horror-francisco-alvear.mp3", "PROVADO NOS PAPÉIS", -17), (_M / "echoes-andrew-ev.mp3", "O SEGREDO QUE VIROU LENDA", -15),
                      (_M / "piano-horror-francisco-alvear.mp3", "SEM PROVA", -18), (_M / "echoes-andrew-ev.mp3", "O QUE O ICEBERG ENSINA", -15)])
AVISO = "DOCUMENTOS ORIGINAIS · FILMES DE ARQUIVO · IMAGENS REAIS DE ICEBERGS (MIXKIT)"

R = [
# ABERTURA (gancho: o memorando da Northwoods, assinado)
("Em 13 de março de 1962, o general", Dc("navio")), ("Isso não é teoria da conspiração", Dc("assunto")), ("Está escrito, assinado e guardado", Dc("capa")),
("O plano nunca foi executado", NWc("CC", 63)), ("Mas ele existiu", Dc("navio")), ("E ficou em segredo por trinta e cinco anos", ARQ),
("Então, onde termina a conspiração", GELO), ("Para responder, imagine um iceberg", C("mx25245", 5)),
# O ICEBERG
("Na internet, as teorias da conspiração", GELO2), ("No topo, o que todo mundo já ouviu", Fo("d_iceberg0")), ("Lá embaixo, no escuro", DEGELO),
("Aqui, a regra vai ser outra", FICHAS), ("Cada nível vai ser medido", PAPEL), ("o que está nos documentos", Dc("navio")),
("No topo, conspirações que os próprios", Fo("d_iceberg1")), ("Quanto mais fundo, menos papel", Fo("d_iceberg0")), ("Até chegar a um ponto onde", BORDA),
("E há uma surpresa nessa descida", GELO), ("A parte mais assustadora do iceberg", Fo("d_iceberg0")), ("Está no topo", GELO),
# NÍVEL 1
("O primeiro nível é o das conspirações", Fo("d_iceberg1")), ("A primeira você já conhece", Dc("assunto")), ("O memorando de 1962 se chama", Dc("assunto")),
("Ele listava pretextos", Dc("pedido")), ("Afundar um barco com refugiados", Dc("boatload")), ("Explodir bombas em Miami", Dc("bombas")),
("Simular que um avião cheio de estudantes", Dc("estudantes")), ("O plano falava até em funerais falsos", Dc("funerais", "terror")),
("O general que assinou, Lyman Lemnitzer", NWc("CC", 141)), ("O documento foi liberado em 1997", ARQ + GAVETA),
("A segunda aconteceu no Alabama", PAPEL), ("Durante quarenta anos, médicos", Dc("clinton_cura")), ("Em 1997, o presidente Bill Clinton", Dc("clinton_sorry")),
("Disse que, mesmo depois que a cura", Dc("clinton_cura")),
("A terceira começou em 1953, dentro da CIA", Dc("aprovado")), ("Chamava-se MKUltra", Dc("aprovado")), ("A agência financiou pesquisas", Dc("inst80")),
("Universidades, hospitais e prisões", Dc("univ44")), ("E deu LSD a pessoas que não sabiam", MK.GOTA + C("mx41439", 5)), ("Uma delas foi um cientista do Exército", LS(942)),
("Ele recebeu a droga sem saber", C("mx22336", 5)), ("Em 1975, o presidente Gerald Ford", Dc("ford")), ("Em 1973, o diretor da CIA mandou destruir", Dc("destruidos")),
("Mas cerca de oito mil páginas", Dc("oitomil")), ("Em 1977, o Senado americano", Dc("caixas")), ("Três casos", Fo("d_iceberg1")), ("Três confissões", Dc("clinton_sorry")),
("Nenhum deles precisa de teoria", Dc("navio")), ("Todos têm papel", FICHAS),
# NÍVEL 2
("Descendo um pouco, chegamos", Fo("d_iceberg2")), ("Elas foram arrancadas", GAVETA), ("Na noite de 8 de março de 1971", C("FBI", 5) + Dc("coin_media")),
("Levaram documentos e mandaram", Dc("coin_media")), ("Os papéis revelaram um programa secreto", C("FBI", 5)), ("Entre 1956 e 1971, o FBI usou", Dc("coin_inicio")),
("Um dos alvos foi Martin Luther King", C("FBI", 181)), ("Segundo a investigação do Senado, o FBI mandou", Dc("coin_king")), ("Junto, ia um bilhete", Dc("coin_king")),
("divulgar a gravação", Dc("coin_king")), ("Uma comissão do Senado concluiu em 1976", Dc("coin_2000")),
("O segundo caso deste nível é o Golfo", TK.TC(600)), ("Dois navios americanos atiraram", TK.TEMP + TK.UN(32)), ("O ataque serviu de motivo", TK.WV(941)),
("Em 2005, um estudo da própria agência", Dc("nsa_titulo")), ("A conclusão:", Dc("nsa_noattack")), ("naquela noite, não houve ataque nenhum", Dc("nsa_noattack")),
("E o próprio comandante dos navios", Dc("herrick")), ("E o terceiro é a Operação Paperclip", Fo("fortbliss")), ("Depois da Segunda Guerra", Dc("nara_1500")),
("Alguns tinham passado nazista", Fo("rendicao")), ("Um deles, Arthur Rudolph", Fo("grupo1959")), ("Em 1984, deixou o país", Dc("nara_rudolph")),
("Neste nível, a lição é outra", Fo("d_iceberg2")), ("Quem revelou esses segredos", PAPEL), ("Foram ladrões de documentos", Dc("coin_media")),
# NÍVEL 3
("Agora a água fica mais escura", DEGELO), ("Este é o nível mais interessante", Fo("d_iceberg3")), ("Aqui, existe um segredo verdadeiro", Fo("d_iceberg3")),
("Só que em cima dele cresceu", BORDA), ("Comece pela Área 51", Fo("u2")), ("Durante décadas, o governo americano não falava", C("SC", 22)),
("E a falta de resposta virou combustível", C("SC", 13)), ("O U-2 era real", C("SC", 21)), ("Em maio de 1960, um deles foi derrubado", C("SC", 5, 28)),
("O caso virou crise internacional", C("SC", 42) + C("PW", 30)), ("Em 2013, a CIA liberou", Fo("u2")), ("Ali, a base aparece", C("SC", 21)),
("E tem mais", PAPEL), ("Em 1997, a revista interna da CIA", Dc("ufo_metade")), ("Segundo ele, mais da metade", Dc("ufo_metade")),
("Ou seja, havia um segredo", Fo("u2")), ("Só não era o que as pessoas imaginavam", C("SC", 13)),
("Com Roswell, em 1947, foi parecido", Dc("roswell_mogul")), ("Algo caiu no deserto do Novo México", BORDA), ("Em 1994, a Força Aérea", Dc("roswell_mogul")),
("Os destroços eram de um projeto ultrassecreto", Dc("roswell_mogul")), ("Era um balão", GELO2), ("Mas um balão secreto", Dc("roswell_mogul")),
("O governo escondeu a verdade", Fo("d_iceberg3")), ("E o último caso deste nível", PAPEL), ("Durante anos, o governo americano pagou", Dc("rv_nunca")),
("O programa ficou conhecido como Stargate", Dc("rv_nunca")), ("Ele existiu", FICHAS), ("Entre os papéis liberados pela CIA", ARQ),
("Em 1995, uma avaliação encomendada", Dc("rv_nunca")), ("E que não valia a pena continuar", Dc("rv_fim")), ("O programa era real", Dc("rv_fim")), ("O poder, não", DEGELO),
# NÍVEL 4
("Mais fundo, a luz quase não chega", Fo("d_iceberg4")), ("Aqui estão as teorias que têm milhões", DEGELO), ("A mais famosa diz que o homem nunca", PC.A11(118, 128)),
("Que tudo foi filmado num estúdio", Fo("lua")), ("Só que a sonda americana que orbita", Fo("d_lro_apollo")), ("Na imagem da Apollo 17", Fo("d_lro_a17")),
("Para que o pouso fosse falso", PC.SAT(49) + PC.TE(43)), ("Enquanto isso, segredos bem menores", Fo("d_iceberg1")),
("Neste nível, a falta de papel", Fo("d_iceberg4")), ("É sinal de que não há nada para esconder", Fo("luabandeira")),
# NÍVEL 5
("E então chegamos ao fundo do iceberg", Fo("d_iceberg5")), ("Aqui ficam as ideias que contrariam", BORDA), ("A mais conhecida é a de que a Terra é plana", Fo("d_terra_iss")),
("Não existe um único documento", Fo("d_iceberg5")), ("Existe o contrário", Fo("d_terra_lua")), ("Fotografias da Terra feitas da estação", Fo("d_terra_iss", "d_terra_lua")),
("O fundo do iceberg é o lugar", C("mx8128", 9)),
# O QUE O ICEBERG ENSINA
("Agora olhe o iceberg inteiro de novo", Fo("d_iceberg0")), ("As conspirações que se provaram verdadeiras", Fo("d_iceberg1")), ("Elas não foram descobertas por quem", PAPEL),
("Foram descobertas por gente que pediu", Dc("coin_media")), ("E elas têm algo em comum", Fo("d_iceberg1")), ("Quase sempre envolvem pessoas comuns", TK.WV(950)),
("Os soldados do Vietnã", TK.WV(941)), ("Os homens de Tuskegee", Dc("clinton_cura")), ("As pessoas que tomaram LSD sem saber", MK.GOTA),
("Já as teorias do fundo têm o efeito contrário", Fo("d_iceberg5")), ("Elas desviam a atenção", DEGELO), ("Enquanto alguém discute se a Terra é plana", FICHAS),
("Da próxima vez que uma teoria aparecer", PAPEL), ("Existe um documento?", Dc("navio")), ("Quem liberou esse documento?", Dc("nsa_titulo")),
("E dá para ler o original", Dc("coin_inicio")), ("As conspirações do topo passam", Fo("d_iceberg1")), ("As do fundo, não", Fo("d_iceberg5")),
("A pergunta certa não é em que acreditar", GELO), ("É o que dá para provar", Dc("navio")),
# FECHO
("No topo, governos que confessaram", Fo("d_iceberg1")), ("No meio, segredos verdadeiros", Fo("d_iceberg3")), ("No fundo, muita certeza", Fo("d_iceberg5")),
("Até onde vai a verdade?", GELO), ("Até onde vão os documentos", Fo("d_iceberg0")),
]
POOL = {c: GELO + FICHAS + PAPEL for c in T_}
KEY = [("Em 13 de março de 1962, o general", "13 DE MARÇO DE 1962"), ("O memorando de 1962 se chama", "OPERAÇÃO NORTHWOODS"), ("A segunda aconteceu no Alabama", "TUSKEGEE, ALABAMA"),
       ("Chamava-se MKUltra", "MKULTRA"), ("Os papéis revelaram um programa secreto", "COINTELPRO"), ("O segundo caso deste nível é o Golfo", "GOLFO DE TONKIN, 1964"),
       ("E o terceiro é a Operação Paperclip", "OPERAÇÃO PAPERCLIP"), ("Comece pela Área 51", "ÁREA 51"), ("Com Roswell, em 1947, foi parecido", "ROSWELL, 1947"),
       ("O programa ficou conhecido como Stargate", "STARGATE"), ("A mais famosa diz que o homem nunca", "O POUSO FALSO NA LUA"), ("A mais conhecida é a de que a Terra é plana", "TERRA PLANA")]
CARDS = [("Está no topo.", "ESTÁ NO TOPO.", "vermelho"), ("Todos têm papel.", "TODOS TÊM PAPEL.", "branco"), ("O poder, não.", "O PODER, NÃO.", "amarelo")]
LISTA = []
