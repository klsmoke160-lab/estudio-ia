"""Plano do Golfo de Tonkin: fontes, documentos (páginas originais da NSA com marca-texto e transcrições oficiais), filmes e regras por frase.
Filmes de arquivo do governo dos EUA (domínio público) e cenas de atmosfera do Mixkit; sem imagem gerada por IA."""
import json, pathlib
TK = pathlib.Path("/home/user/mk/tk"); RAWD = TK / "raw"; DOC = TK / "docs"
CENAS = json.load(open(TK / "cenas.json"))
RAW = {k: next(RAWD.glob(k + ".*")) for k in CENAS}
def C(k, *ts): return [("clip", k, t) for t in ts]
def Dc(*ks): return [("doc", k) for k in ks]
def Fo(*ks): return [("foto", k) for k in ks]

# ---------- documentos ----------
_DJ = json.load(open(DOC / "docs.json"))
NSA = "Robert J. Hanyok, \"Skunks, Bogies, Silent Hounds, and the Flying Fish\", NSA, Cryptologic Quarterly (2001; liberado em 2005)"
FONTES = {"nsa": NSA, "res": "Resolução do Golfo de Tonkin, Public Law 88-408 (Arquivo Nacional dos EUA)", "lbj": "Discurso de Lyndon B. Johnson, 4 de agosto de 1964",
          "mcnamara64": "Depoimento de McNamara ao Senado, 6 de agosto de 1964 (via National Security Archive)",
          "mcnamara68": "Depoimento de McNamara ao Senado, 20 de fevereiro de 1968 (via National Security Archive)",
          "jones": "J. Norvill Jones, Comissão de Relações Exteriores do Senado (via National Security Archive)",
          "stockdale": "James e Sybil Stockdale, In Love and War (1984), citado pelo National Security Archive",
          "release": "National Security Archive, Universidade George Washington, 1º de dezembro de 2005",
          "herrick": "Cronologia ultrassecreta para o presidente, 28 de agosto de 1964 (via National Security Archive)",
          "tel": "Gravação da Casa Branca, 3 de agosto de 1964 (John Prados, The White House Tapes)",
          "int": "Interceptações da NSA, Biblioteca LBJ (liberadas em 2003, via National Security Archive)"}
D = {}
for k, (arq, bx) in _DJ.items():
    f = "nsa" if k.startswith("nsa") else "res" if k.startswith("res") else "herrick" if k.startswith("herrick") else "tel" if k == "tel3ago" else k
    D[k] = (arq, bx, None, FONTES[f])
D["int_capa"] = (str(DOC / "int_p1.png"), None, (0.5, 0.30, 0.95), FONTES["int"])
D["int_msg"] = (str(DOC / "int_p6.png"), None, (0.45, 0.35, 0.80), FONTES["int"])
D["int_msg2"] = (str(DOC / "int_p5.png"), None, (0.45, 0.40, 0.80), FONTES["int"])

# ---------- fotos ----------
FOTOS = {}
D["res_scan"] = (str(DOC / "resolucao.jpg"), None, (0.5, 0.33, 0.95), "Resolução do Golfo de Tonkin, 1964 · Arquivo Nacional dos EUA")

# ---------- filmes ----------
# UN: cinejornal Universal de 06/08/1964 (NARA) · TC: coletivas sobre o incidente, 05/08/1964 (Exército, NARA) · WV: "Why Vietnam?" (Depto. de Defesa, 1965)
# A4: convés de porta-aviões no Golfo de Tonkin, 1967 (Marinha, NARA) · mx*: Mixkit (licença gratuita)
UN = lambda *t: C("UN", *t); TC = lambda *t: C("TC", *t); WV = lambda *t: C("WV", *t); A4 = lambda *t: C("A4", *t)
TEMP = C("mx4059", 3) ; TEMP2 = C("mx4060", 8); PAPEL = C("mx34154", 8); MAQ = C("mx10395", 4)
AR = {k: 4/3 for k in CENAS}; AR.update({"mx4059": 16/9, "mx4060": 16/9, "mx34154": 16/9, "mx10395": 16/9})
PRE = {"UN": "crop=960:720:160:0", "TC": "scale=640:480,setsar=1", "mx4059": "eq=gamma=2.4:brightness=0.14:contrast=1.2", "mx4060": "eq=gamma=2.4:brightness=0.14:contrast=1.2"}
TITULO = ("GOLFO DE TONKIN", "A batalha que não aconteceu", ("doc", "nsa_titulo"))
T_ = {"ABERTURA": "azul", "O PRIMEIRO ATAQUE": "petroleo", "A SEGUNDA NOITE": "azul", "O QUE O SONAR OUVIA": "verde", "O TELEGRAMA": "ambar",
      "A DECISÃO": "vermelho", "A RESOLUÇÃO": "ambar", "A GUERRA": "vermelho", "A CARTA NA MANGA": "petroleo", "O ESTUDO": "verde",
      "O QUE OS DOCUMENTOS PROVAM": "petroleo", "FECHO": "azul"}
_M = pathlib.Path("/home/user/estudio-ia/05-biblioteca/musica/mixkit")
ESTILO = dict(cinema=True, tint=T_, dur_plano=4.0, zoom=0.045, nasce=4.0, nasce_abertura=0.4, brilho=-0.10, cama=-24, golpe=-3, lufs=-16.0,
              trilha=[(_M / "echoes-andrew-ev.mp3", "ABERTURA", -15), (_M / "piano-horror-francisco-alvear.mp3", "A SEGUNDA NOITE", -17),
                      (_M / "tapis-eugenio-mininni.mp3", "A DECISÃO", -19), (_M / "piano-horror-francisco-alvear.mp3", "A CARTA NA MANGA", -17),
                      (_M / "echoes-andrew-ev.mp3", "O QUE OS DOCUMENTOS PROVAM", -15)])
AVISO = "FILMES DE ARQUIVO DO GOVERNO DOS EUA · DOCUMENTOS ORIGINAIS E TRANSCRIÇÕES"

R = [
# ABERTURA (gancho: a frase do estudo da NSA, igual à capa; primeiro quadro = a página, marca-texto entra com a voz)
("Naquela noite, não houve ataque nenhum.", Dc("nsa_noattack")), ("A frase está num estudo ultrassecreto", Dc("nsa_titulo")), ("E fala da noite de 4 de agosto", TC(600)),
("Naquela noite, dois navios de guerra", TEMP + UN(32)), ("Três dias depois, por causa desse ataque", UN(100) + Dc("res_scan")),
("Como um combate que não aconteceu", Dc("int_capa")), ("E por que a prova ficou guardada", Dc("int_capa")),
# O PRIMEIRO ATAQUE
("Começo de agosto de 1964", WV(385)), ("O Vietnã está dividido em dois", WV(385)), ("No norte, um governo comunista", WV(405)),
("No sul, um governo apoiado", WV(780)), ("No Golfo de Tonkin, na costa", TC(600) + UN(36)), ("Oficialmente, ele faz uma patrulha", UN(44)),
("Na prática, a missão é espionar", Dc("int_msg")), ("A bordo há uma equipe", Dc("int_msg2")), ("E há um detalhe que o público", WV(497)),
("Naqueles mesmos dias, lanchas", WV(503) + TC(640)), ("Era uma operação secreta", Dc("tel3ago")), ("No dia 2 de agosto, à luz do dia", UN(30) + UN(64)),
("Esse combate aconteceu", UN(40)), ("Foi de dia, houve fotografias", UN(62)), ("As lanchas foram repelidas", UN(54)),
("O presidente Lyndon Johnson decidiu não revidar", UN(100)), ("Em vez disso, mandou um segundo", UN(46)), ("E os dois voltaram para o golfo", TC(660)),
# A SEGUNDA NOITE
("Dois dias depois, na noite de 4 de agosto", TEMP), ("Não há lua", TEMP2), ("O mar está agitado", TEMP),
("Os radares dos dois navios", UN(38)), ("Os operadores de sonar, o aparelho", UN(48)), ("Os navios manobram", UN(34) + TEMP2),
("Durante horas, as mensagens para Washington", MAQ + UN(78)), ("A Marinha chega a informar", Dc("int_msg")),
("Mas não aparece nenhum destroço", TEMP), ("Nenhum corpo", TEMP2), ("Nenhuma fotografia", TEMP),
("No céu, sobre os navios, voava o piloto", A4(25) + WV(1087)), ("Anos depois, ele escreveu", Dc("stockdale")), ("Não havia tiros, a não ser os nossos", Dc("stockdale")),
("Nenhum rastro de lancha", Dc("stockdale")), ("Nem uma luz de vela", Dc("stockdale")),
# O QUE O SONAR OUVIA
("Décadas depois, a agência de espionagem", Dc("nsa_titulo")), ("Tudo começou com um ponto no radar", UN(38)), ("Quando um dos sinais mudou", TC(620)),
("Os operadores de sonar foram avisados", UN(48)), ("Quatro marinheiros do Turner Joy", TEMP2), ("Então os dois navios começaram", UN(30) + UN(36)),
("E cada curva gerava", Dc("nsa_sonar")), ("O sonar ouvia o som rápido", Dc("nsa_sonar")), ("Só que o som vinha", Dc("nsa_sonar")),
("Os lemes refletiam", Dc("nsa_sonar")), ("Os navios estavam fugindo", TEMP),
# O TELEGRAMA
("Ainda naquele dia, o comandante", MAQ), ("Uma revisão da ação faz", Dc("herrick")), ("Ele explicou por quê", Dc("herrick")),
("Efeitos estranhos do tempo", Dc("herrick")), ("Operadores de sonar ansiosos", Dc("herrick")), ("Nenhum barco inimigo", Dc("herrick2")),
("E terminou com um pedido", Dc("herrick2")), ("Que houvesse uma avaliação completa", Dc("herrick2")), ("Em outra mensagem, ele escreveu", Dc("nsa_duvidas")),
("O resumo desse telegrama", Dc("nsa_doubtful")),
# A DECISÃO
("Mas Washington já tinha decidido", UN(78)), ("Segundo o estudo da própria agência", Dc("nsa_3horas")), ("O estudo diz que não está totalmente claro", Dc("nsa_3horas")),
("Naquela mesma noite, Lyndon Johnson", WV(1060) + UN(120)), ("Ele disse aos americanos", Dc("lbj")), ("Pouco depois, aviões americanos", UN(62, 70) + WV(1102)),
("Havia ainda uma eleição", UN(300)), ("O adversário de Johnson", UN(140)), ("Um presidente que hesitasse", WV(1070)),
# A RESOLUÇÃO
("No dia 6 de agosto, o secretário de Defesa", WV(1110)), ("Disse que a Marinha americana", Dc("mcnamara64")), ("Não era verdade", WV(1120)),
("Os ataques às ilhas eram", WV(497)), ("E o próprio McNamara sabia disso", WV(1115)), ("No dia 3 de agosto, num telefonema", Dc("tel3ago")),
("No dia 7 de agosto, o Congresso votou", Dc("res_scan")), ("O texto dizia que o Vietnã do Norte", Dc("res_ataque")), ("E aprovava que o presidente", Dc("res_medidas")),
("Na Câmara, ninguém votou contra", Dc("res_scan")), ("No Senado, foram 88 votos", Dc("res_scan")), ("Era um cheque em branco", Dc("res_medidas")),
# A GUERRA
("Com aquela resolução, a guerra cresceu", UN(220, 240)), ("Em março de 1969", WV(941, 950)), ("Ao fim da guerra", WV(1026, 1021)),
("A resolução só foi revogada", Dc("res_scan")),
# A CARTA NA MANGA
("As dúvidas sobre a noite de 4 de agosto", TEMP2), ("Poucas semanas depois, um jornalista", MAQ), ("Elas nunca desapareceram", PAPEL),
("Em 1968, o Senado reabriu", Dc("mcnamara68")), ("McNamara voltou a depor", WV(1110)), ("Mensagens interceptadas do rádio", Dc("mcnamara68")),
("Os senadores pediram cópias", Dc("int_capa")), ("McNamara se recusou", WV(1125)), ("Anos depois, dois funcionários", Dc("int_msg2")),
("A de 4 de agosto, escreveu um deles", Dc("jones")), ("E a agência de espionagem não conseguiu", Dc("jones")),
# O ESTUDO
("Em 2001, um historiador da Agência", Dc("nsa_titulo")), ("O título usava gírias", Dc("nsa_titulo")), ("A conclusão era direta", PAPEL),
("Naquela noite, não aconteceu ataque nenhum", Dc("nsa_noattack")), ("Segundo ele, quase noventa", Dc("nsa_90")), ("E as que entraram foram escolhidas", Dc("nsa_nohappen")),
("Hanyok escreveu que houve um esforço", Dc("nsa_fit")), ("O estudo ficou secreto até dezembro de 2005", Dc("release")),
# O QUE OS DOCUMENTOS PROVAM
("Os documentos provam algumas coisas", PAPEL), ("O ataque de 2 de agosto aconteceu", UN(40)), ("O de 4 de agosto, segundo", Dc("nsa_noattack")),
("O comandante no local pediu cautela", Dc("herrick2")), ("O Congresso votou sem saber", Dc("res_scan")), ("O que os documentos não provam", Dc("nsa_fit")),
("O próprio Hanyok diz", Dc("nsa_titulo")), ("O que eles mostram é algo", WV(1070)), ("Um governo que já queria agir", UN(130)),
# FECHO
("Dois navios atirando contra o escuro", TEMP + UN(34)), ("Um telegrama pedindo calma", Dc("herrick2")), ("E uma guerra que ainda duraria", WV(941, 1021)),
("Tudo começou numa noite", TEMP2),
]
POOL = {c: UN(32, 52) + TEMP + PAPEL for c in T_}
KEY = [("E fala da noite de 4 de agosto", "4 DE AGOSTO DE 1964"), ("No Golfo de Tonkin, na costa", "USS MADDOX"), ("No dia 2 de agosto, à luz do dia", "2 DE AGOSTO DE 1964"),
       ("No céu, sobre os navios, voava o piloto", "JAMES STOCKDALE"), ("Ainda naquele dia, o comandante", "CAPITÃO JOHN HERRICK"),
       ("No dia 6 de agosto, o secretário de Defesa", "ROBERT McNAMARA"), ("No dia 7 de agosto, o Congresso votou", "7 DE AGOSTO DE 1964"),
       ("No Senado, foram 88 votos", "SENADO: 88 A 2"), ("Em março de 1969", "548 MIL SOLDADOS"), ("Ao fim da guerra", "CERCA DE 59 MIL AMERICANOS"),
       ("Em 1968, o Senado reabriu", "1968"), ("Em 2001, um historiador da Agência", "ROBERT HANYOK · NSA"), ("Segundo ele, quase noventa", "QUASE 90 POR CENTO"),
       ("O estudo ficou secreto até dezembro de 2005", "DEZEMBRO DE 2005")]
CARDS = [("Mas Washington já tinha decidido.", "JÁ ESTAVA DECIDIDO.", "branco"),
         ("Era um cheque em branco.", "CHEQUE EM BRANCO.", "amarelo")]
LISTA = []
