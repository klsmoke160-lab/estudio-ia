"""Plano do vídeo sobre os testes biológicos em cidades americanas.

Documentos: páginas originais da audiência do Senado de 1977 e do estudo de vulnerabilidade
do metrô de 1968, com marca-texto (geradas por motor/gerar_docs.py).
Filmes: arquivo público dos EUA (Prelinger / Internet Archive). Nenhuma imagem gerada por IA.
"""
import json, pathlib

B = pathlib.Path("/home/user/mk/bio"); RAWD = B / "raw"; DOC = B / "docs2"
CENAS = json.load(open(B / "cenas.json"))
RAW = {k: RAWD / f"{k}.mp4" for k in CENAS}
def C(k, *ts): return [("clip", k, t) for t in ts]
def Dc(*ks): return [("doc", k) for k in ks]

# ---------- documentos ----------
_DJ = json.load(open(DOC / "docs.json"))
F_SEN = ('Senado dos EUA, Subcomissão de Saúde e Pesquisa Científica, "Biological Testing Involving '
         'Human Subjects by the Department of Defense", 8 e 23 de março de 1977')
F_SUB = 'Fort Detrick, "Subway Vulnerability Trials", janeiro de 1968 (liberado ao público)'
# foco (x, y, zoom em fração da largura) para as páginas do estudo do metrô, que são
# altas e deixariam muita borda preta se entrassem inteiras
FOCO = {"d_abstract": (0.55, 0.16, 0.95), "d_milhao": (0.47, 0.46, 0.92),
        "d_concl": (0.48, 0.20, 0.95), "d_relato": (0.56, 0.64, 0.92)}
D = {k: (arq, bx, FOCO.get(k), F_SUB if "subway" in arq else F_SEN) for k, (arq, bx) in _DJ.items()}

FOTOS = {}

# ---------- filmes ----------
# BW51 "What You Should Know About Biological Warfare" (Defesa Civil Federal, 1951)
# BAC  "Bacteria: Friend and Foe" (Encyclopaedia Britannica Films, 1953)
# ATB  "The Atom and Biological Science" (laboratórios e instalações, anos 1950)
# NY47 "The Story of a City: New York" (1947) · SUB41 "Arteries of New York City" (1941)
# TA50 "Third Avenue El" (Nova York, 1950) · SF50 cinejornal de São Francisco (1950)
BW = lambda *t: C("BW51", *t); BAC = lambda *t: C("BAC", *t); ATB = lambda *t: C("ATB", *t)
NY = lambda *t: C("NY47", *t); SUB = lambda *t: C("SUB41", *t); TA = lambda *t: C("TA50", *t); SF = lambda *t: C("SF50", *t)

LAB = ATB(404, 420)              # laboratório, vidraria
PLACA = BAC(574, 578)            # placas de Petri
COLONIA = ATB(307, 318)          # colônias no microscópio
MICRO = BAC(588, 376)            # cientistas no microscópio
SPRAY = BW(183)                  # jato de aerossol
CIDADE = BW(34, 342)             # cidade e rua residencial
GENTE = BW(88, 391)              # pessoas, sala cheia
HOSP = BW(340, 229)              # doente na cama, enfermaria
PAPEL = BW(283)                  # telegramas
NAVIO = NY(278, 321, 993)
SKY = NY(44, 563, 847)
PLAT = SUB(187, 197, 245)        # plataforma de metrô cheia
TUNEL = SUB(204)                 # túnel de metrô
TREM = SUB(248) + TA(385)
GRADE = TA(128, 184, 187)        # grades de ventilação na calçada
TRILHO = TA(323, 437)
MULT = SF(2, 30)                 # multidão em São Francisco, 1950
PERIGO = ATB(632, 491)
INST = ATB(647, 664)

AR = {k: 4/3 for k in CENAS}
PRE = {}

TITULO = ("A LISTA", "As cidades americanas que o Exército testou", ("doc", "d_tabela"))

T_ = {"ABERTURA": "petroleo", "POR QUE UMA CIDADE": "azul", "O PACIENTE": "verde", "O PARECER DE 1952": "ambar",
      "O MAPA": "vermelho", "NOVA YORK": "petroleo", "NINGUÉM VIU": "azul", "A CONTRADIÇÃO": "ambar",
      "O QUE FICOU": "vermelho", "FECHO": "petroleo"}
NOMES_CAP = {k: k for k in T_}

_M = pathlib.Path("/home/user/estudio-ia/05-biblioteca/musica/mixkit")
ESTILO = dict(cinema=True, tint=T_, dur_plano=4.0, zoom=0.045, nasce=4.0, nasce_abertura=0.4,
              brilho=0.05, cama=-24, golpe=-3, lufs=-16.0,
              trilha=[(_M / "echoes-andrew-ev.mp3", "ABERTURA", -15),
                      (_M / "piano-horror-francisco-alvear.mp3", "O PACIENTE", -17),
                      (_M / "tapis-eugenio-mininni.mp3", "O MAPA", -19),
                      (_M / "piano-horror-francisco-alvear.mp3", "NOVA YORK", -17),
                      (_M / "echoes-andrew-ev.mp3", "O QUE FICOU", -15)])
AVISO = "DOCUMENTOS ORIGINAIS DO SENADO E DO EXÉRCITO DOS EUA · FILMES DE ARQUIVO PÚBLICO"

R = [
# ABERTURA — gancho: a lista. Primeiro quadro é a página da tabela.
("Em 1977, o Exército dos Estados", Dc("d_lista1")), ("Não era uma lista de inimigos", Dc("d_tabela")),
("Era uma lista de cidades americanas", Dc("d_lista2")),
("Washington.", Dc("d_lista1")), ("São Francisco.", MULT), ("Key West.", Dc("d_lista2")),
("Panama City.", NY(1131)), ("Nova York.", SKY),
("A tabela tem um título seco", Dc("d_tabela")), ('"testes envolvendo domínio público"', Dc("d_tabela")),
("Em português simples", GENTE), ("lugares onde havia gente", BW(391)),
("Essa lista não vazou", PAPEL), ("Foi o governo que entregou, impressa", Dc("d_schweiker")),
("E ela existe até hoje", Dc("d_lista2")),
# POR QUE UMA CIDADE
("Setembro de 1950.", CIDADE), ("Guerra da Coreia, medo da bomba", BW(65)),
("E uma pergunta que ninguém em", BW(77)), ("se um inimigo soltasse germes perto", SPRAY),
("Num laboratório, dá para estimar", LAB), ("Mas uma cidade de verdade tem", BW(34) + NY(847)),
("O secretário de Defesa explicou isso", Dc("d_cidades")), ("soltar o material perto de cidades", Dc("d_cidades")),
("A escolhida foi São Francisco", MULT), ("Durante dias, em setembro de 1950", NAVIO),
("o Bacillus globigii e a Serratia", Dc("d_sf1950")), ("A Serratia tinha uma vantagem prática", PLACA),
("ela forma colônias vermelhas, fáceis de", COLONIA), ("Na época, o Exército a considerava", Dc("d_sf1950")),
("Em audiência no Senado, anos depois", Dc("d_schweiker")), ("O Exército respondeu que não tinha", Dc("d_schweiker")),
("O que ninguém disputa é o", HOSP),
# O PACIENTE
("Entre setembro de 1950 e fevereiro", HOSP), ("Onze pacientes infectados por uma bactéria", Dc("d_wheat")),
("A mesma Serratia marcescens", COLONIA), ("Um deles se chamava Edward Nevin", BW(340)),
("Tinha passado por uma cirurgia", BW(229)), ("A infecção chegou ao coração", BW(340)),
("Edward Nevin morreu", Dc("d_morreu")),
("Os médicos publicaram o caso numa", Dc("d_wheat")), ("Eles não sabiam de teste nenhum", MICRO),
("O teste era secreto", Dc("d_sf1950")),
("E aqui o vídeo precisa ser", PAPEL), ("até hoje ninguém provou que a", Dc("d_morreu")),
("O Exército sustenta que foi coincidência", Dc("d_morreu")), ("Todos os onze pacientes tinham passado", BW(229)),
("É o tipo de paciente em", HOSP), ("Décadas depois, a família de Nevin", PAPEL), ("E perdeu.", BW(354)),
("Mas o Exército não esperou esse", Dc("d_hosp")), ("E é a decisão que importa", Dc("d_hosp")),
# O PARECER DE 1952
("Em 1952, o oficial de segurança", INST), ("Vieram do que hoje é o", MICRO),
("Eles leram o artigo do hospital", Dc("d_wheat")), ("Reconheceram que um paciente tinha morrido", Dc("d_parecer")),
("E escreveram a conclusão", PAPEL), ("Está impressa no relatório que o", Dc("d_parecer")),
("o uso daquela bactéria deveria continuar", Dc("d_parecer")), ("Repare na frase", Dc("d_parecer")),
("Mesmo sobre áreas povoadas", Dc("d_parecer")),
("O mesmo grupo recomendou acompanhar hospitais", BW(391)), ("E o diretor de segurança de", Dc("d_hosp")),
("aquela bactéria não podia ser usada", Dc("d_hosp")), ("Pare um segundo nisso", BW(340)),
("Criar uma regra para proteger hospitais", HOSP), ("Em 1952, o Exército já trabalhava", Dc("d_1968")),
("E continuou soltando por mais dezesseis", Dc("d_1968")),
# O MAPA
("É por isso que a lista", Dc("d_tabela")), ("Ela é a prova de que", Dc("d_lista1")),
("A primeira linha é Washington, 1949", Dc("d_lista1")), ("O alvo era o Pentágono", NY(367)),
("descobrir se alguém conseguiria contaminar o", ATB(79, 69)), ("Depois vieram navios na entrada de", NAVIO),
("Key West, na Flórida, em 1952", Dc("d_lista1")), ("Fort McClellan, no Alabama, no mesmo", BW(34)),
("Panama City, em 1953", NY(993)), ("Em 1955, os túneis Kittatinny e", NY(578) + Dc("d_penn")),
("Em maio de 1965, o Aeroporto", Dc("d_aeroporto")), ("E havia uma segunda lista, de", Dc("d_tabela")),
("Minneapolis e Saint Louis em 1953", CIDADE), ("Nenhuma dessas cidades foi avisada", GENTE),
("Nenhuma pessoa dessas cidades foi consultada", BW(88)), ("E em junho de 1966, a", PLAT),
# NOVA YORK
("O estudo tem um nome burocrático", Dc("d_abstract")), ("vulnerabilidade de linhas de metrô a", Dc("d_abstract")),
("Foi escrito pela equipe de Fort", INST), ("A justificativa está na introdução", Dc("d_milhao")),
("Cerca de um milhão de pessoas", PLAT), ("Três em cada quatro no horário", SUB(173, 53)),
("Entre 7 e 10 de junho", TUNEL), ("A bactéria usada foi o Bacillus", PLACA),
("Ela existe no feno, na poeira", BAC(124, 131)), ("O que interessava ao Exército não", COLONIA),
("Era o caminho que ela fazia", TRILHO), ("E o caminho é a parte", TUNEL),
("O relatório registra que o material", Dc("d_abstract")), ("O tempo médio que a equipe", PLAT),
("O relatório diz, com essas palavras", Dc("d_concl")), ("E a conclusão do estudo não", Dc("d_concl")),
("com um agente causador de doença", Dc("d_concl")), ("Isso é o Exército avaliando um", PERIGO),
("Mas quem estava dentro daquelas estações", SUB(197) + TA(369)),
# NINGUÉM VIU
("Tem um anexo nesse relatório que", Dc("d_relato")), ("É a parte em que cada", PAPEL),
("Um deles conta que levava o", SUB(245)), ("Outro diz que um homem sentou", SUB(187)),
("Ele respondeu que era o rádio", BW(88)), ("O homem achou razoável e pegou", TREM),
("Outro conta que uma mulher perguntou", SUB(239)), ("Um colega respondeu que ele estava", GRADE),
("Ela aceitou.", SUB(173)), ("Outro foi parado por um policial", SUB(53)),
("Não pelo equipamento, mas por estar", TA(78)),
("E um deles escreveu a frase", Dc("d_relato")), ("as pessoas da cidade grande andam", SUB(53, 173)),
("Em quatro dias, em uma das", PLAT), ("Não porque fosse sofisticado", GRADE), ("Porque ninguém esperava", SUB(197)),
# A CONTRADIÇÃO
("Em 1977, o Senado chamou cientistas", Dc("d_whitecoat")), ("E um deles apontou a contradição", Dc("d_mina")),
("No mesmo período, o Exército mantinha", ATB(494, 499)), ("O especialista descreveu o cuidado desse", ATB(447)),
("A mesma instituição que fazia isso", SPRAY + CIDADE), ("E ele fez a pergunta mais", Dc("d_mina")),
("o que exatamente se aprendeu soltando", Dc("d_mina")), ("Até hoje não existe uma resposta", PAPEL),
("A única coisa que esses testes", SKY), ("E isso, disse ele, era óbvio", NY(1131)),
# O QUE FICOU
("Em novembro de 1969, o presidente", INST), ("O país destruiu seus estoques e", ATB(664)),
("Os testes sobre cidades pararam", CIDADE),
("Mas repare na ordem das datas", PAPEL), ("Os testes começaram em 1949", Dc("d_lista1")),
("O artigo médico sobre as infecções", Dc("d_wheat")), ("O parecer que autorizou continuar", Dc("d_parecer")),
("Os testes seguiram até 1968", Dc("d_1968")), ("E o país só ficou sabendo", PAPEL),
("A audiência no Senado veio em", Dc("d_schweiker")), ("Vinte e sete anos depois de", MULT),
("Nenhuma das pessoas que estavam naquelas", PLAT + BW(391)),
("E essa é a diferença entre", Dc("d_tabela")), ("Uma teoria da conspiração pede que", PAPEL),
("Um documento pede que você leia", Dc("d_parecer")), ("Esse aqui tem número de página", Dc("d_lista2")),
# FECHO
("Se você quiser conferir, os dois", Dc("d_schweiker")), ("a audiência do Senado de março", Dc("d_abstract")),
("No próximo vídeo, eu vou atrás", PAPEL),
]

POOL = {c: PAPEL + CIDADE + LAB for c in T_}
POOL["NOVA YORK"] = PLAT + TUNEL + TRILHO
POOL["NINGUÉM VIU"] = PLAT + GRADE + SUB(53)
POOL["O MAPA"] = Dc("d_lista1", "d_lista2") + CIDADE

KEY = [("Em 1977, o Exército dos Estados", "SENADO DOS EUA · 1977"),
       ("A escolhida foi São Francisco", "SÃO FRANCISCO · 1950"),
       ("Um deles se chamava Edward Nevin", "EDWARD NEVIN"),
       ("Em 1952, o oficial de segurança", "FORT DETRICK · 1952"),
       ("A primeira linha é Washington, 1949", "WASHINGTON · 1949"),
       ("Em maio de 1965, o Aeroporto", "AEROPORTO NACIONAL · 1965"),
       ("Entre 7 e 10 de junho", "NOVA YORK · JUNHO DE 1966"),
       ("Cerca de um milhão de pessoas", "1 MILHÃO POR DIA"),
       ("Em novembro de 1969, o presidente", "NOVEMBRO DE 1969"),
       ("E o país só ficou sabendo", "DEZEMBRO DE 1976")]

CARDS = [("Mesmo sobre áreas povoadas.", "ÁREAS POVOADAS.", "amarelo"),
         ("Porque ninguém esperava.", "NINGUÉM ESPERAVA.", "branco")]

LISTA = []
