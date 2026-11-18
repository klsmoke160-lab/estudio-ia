"""Gera as páginas de documento da Paperclip como transcrições (texto oficial publicado), com as caixas do marca-texto, e o esquema dos túneis.
Saída: /home/user/mk/pc/docs/*.png e docs.json {chave: [arquivo, [[x0,y0,x1,y1],...]]}."""
import json, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
OUT = pathlib.Path("/home/user/mk/pc/docs"); OUT.mkdir(parents=True, exist_ok=True)
FON = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes")
MAQ = ImageFont.truetype(str(FON / "font2.ttf"), 46); MAQB = ImageFont.truetype(str(FON / "font2.ttf"), 54)
SERIF = ImageFont.truetype(str(FON / "serif.ttf"), 50); SANS = ImageFont.truetype(str(FON / "sans.ttf"), 34)
W, H = 1870, 2420; M = 170
RES = {}

def pagina(nome, cab, blocos, rodape, fonte=MAQ, larg=58, passo=66, alt=54):
    """blocos: lista de (texto, [trechos a marcar]). Quebra o texto e guarda as caixas das linhas que contêm cada trecho."""
    im = Image.new("RGB", (W, H), (246, 242, 232)); d = ImageDraw.Draw(im); y = 150
    for linha in cab:
        d.text((M, y), linha, font=MAQB if linha.isupper() else MAQ, fill=(25, 25, 25)); y += 70
    y += 50; caixas = {}
    for texto, marcas in blocos:
        linhas = textwrap.wrap(texto, larg); pos = []
        for l in linhas:
            d.text((M, y), l, font=fonte, fill=(20, 20, 20)); pos.append((l, y)); y += passo
        y += passo*0.6
        corrido = " ".join(l for l, _ in pos)
        for mk in marcas:
            i = corrido.find(mk); j = i + len(mk)
            if i < 0: raise SystemExit(f"trecho não achado: {mk}")
            k = 0; bx = []
            for l, ly in pos:
                a, b = k, k + len(l)
                if b > i and a < j:
                    ini = max(i, a) - a; fim = min(j, b) - a
                    x0 = M + d.textlength(l[:ini], font=fonte); x1 = M + d.textlength(l[:fim], font=fonte)
                    bx.append([x0, ly - 4, x1, ly + alt])
                k = b + 1
            caixas[mk] = bx
    for i, linha in enumerate(rodape):
        d.text((M, H - 260 + i * 48), linha, font=SANS, fill=(90, 90, 90))
    arq = OUT / f"{nome}.png"; im.save(arq)
    return str(arq), caixas

# 1) Memorando de Acheson a Truman (FRUS 1946, vol. V, doc. 448)
memo = [
 ("I am presenting for your approval a statement of United States policy on the interim exploitation of selected German and Austrian specialists in the United States.", []),
 ("Since shortly after V-E Day the War Department has operated a project known as \"Paperclip,\" under which selected German scientists have been brought to this country under military custody for short-term exploitation.", ["for short-term exploitation"]),
 ("General McNarney has reported that the services of many of these specialists may be lost to us unless steps are taken quickly to assure exploitation under favorable circumstances.", ["may be lost to us unless steps are taken quickly"]),
 ("The statement provides for expanding \"Paperclip\" to include a total of between 800 and 1000 specialists. Since cooperation of the specialists is necessary to successful exploitation, provision is made for bringing members of specialists' families to this country, and for relaxing the formerly strict custody arrangements.",
  ["between 800 and 1000 specialists", "bringing members of specialists' families"]),
 ("The War Department would be responsible for custody and for excluding from the program persons with Nazi or militaristic records. It is contemplated that at a later date selected persons would be granted regular status under the immigration laws.",
  ["excluding from the program persons with Nazi or militaristic records", "granted regular status under the immigration laws"]),
 ("DEAN ACHESON", []),
 ("[Anotação à margem:] Approved 9/3/46 Harry S Truman", ["Approved 9/3/46 Harry S Truman"]),
]
RES["memo"] = pagina("memo_1946", ["TOP SECRET", "Memorandum by the Acting Secretary of State", "to President Truman", "Washington, August 30, 1946"], memo,
    ["Transcrição: Foreign Relations of the United States, 1946, vol. V, doc. 448", "history.state.gov/historicaldocuments/frus1946v05/d448"], fonte=ImageFont.truetype(str(FON / "font2.ttf"), 40), larg=66, passo=56, alt=46)

# 2) Arquivo Nacional, RG 330 (JIOA)
jioa = [
 ("The Joint Intelligence Objectives Agency (JIOA) was established in 1945 as a subcommittee of the Joint Intelligence Committee (JIC) of the Joint Chiefs of Staff (JCS).", ["established in 1945"]),
 ("The JIOA was given direct responsibility for operating the foreign scientist program, initially code-named Overcast and subsequently code-named Paperclip.", ["initially code-named Overcast", "subsequently code-named Paperclip"]),
 ("Among the JIOA's duties were administering the program's policies and procedures, compiling dossiers, and serving as liaison to British intelligence officers operating a similar project.", ["compiling dossiers", "liaison to British intelligence officers"]),
 ("The JIOA was disbanded in 1962.", ["The JIOA was disbanded in 1962."]),
]
RES["jioa"] = pagina("nara_jioa", ["NATIONAL ARCHIVES", "Records of the Secretary of Defense (RG 330)", "Joint Intelligence Objectives Agency"], jioa,
    ["Transcrição: Arquivo Nacional dos EUA, Interagency Working Group", "archives.gov/iwg/declassified-records/rg-330-defense-secretary"], fonte=SERIF, larg=54)
nara = [
 ("Foreign Scientist Case Files 1945-1958 (Entry A1-1B). This series consists of personnel dossiers on over 1,500 German and other foreign scientists, technicians, and engineers who were brought to the United States under Project Paperclip and similar programs.", ["over 1,500 German and other foreign scientists"]),
 ("Among the dossiers are those on Georg Rickhey, a former official at the Nordhausen underground V-2 rocket factory who arrived in 1946 but who left the United States in 1947 when he was tried (and acquitted) for war crimes by a U.S. military tribunal;", ["Georg Rickhey", "tried (and acquitted) for war crimes"]),
 ("Walter Schreiber, who had been instrumental in medical experiments on concentration camp inmates and who fled the United States to Argentina in 1952 after the appearance of a newspaper column about his activities;", ["Walter Schreiber", "fled the United States to Argentina in 1952"]),
 ("and, Arthur Rudolph who had been a V-2 project engineer and who left the United States in 1984 following the Department of Justice's discovery of his role in the persecution of prisoners at the Nordhausen factory.", ["Arthur Rudolph", "left the United States in 1984"]),
 ("Not included among the dossiers is one for rocket scientist Wernher von Braun. It was never transferred to NARA.", ["one for rocket scientist Wernher von Braun. It was never transferred to NARA."]),
]
RES["nara"] = pagina("nara_dossies", ["NATIONAL ARCHIVES", "Records of the Secretary of Defense (RG 330)"], nara,
    ["Transcrição: Arquivo Nacional dos EUA, Interagency Working Group", "archives.gov/iwg/declassified-records/rg-330-defense-secretary"], fonte=SERIF, larg=54)

# 3) Smithsonian (citação curta, com fonte)
smith = [
 ("It is estimated that 20,000 to 25,000 detainees died in the Mittelbau camp system, out of 60,000 sent there.", ["20,000 to 25,000 detainees died", "out of 60,000 sent there"]),
 ("A minimum of 10,000 deaths might be attributed the V-2 program at the Mittelwerk.", ["A minimum of 10,000 deaths"]),
 ("In the case of the V-2, more than twice as many Allied prisoners died outfitting the factory and producing it than did Allied civilians and soldiers hit by it in rocket attacks.", ["more than twice as many Allied prisoners died"]),
]
RES["smith"] = pagina("smithsonian", ["SMITHSONIAN", "National Air and Space Museum", "\"Wonder Weapons and Slave Labor\", Michael J. Neufeld, 2020"], smith,
    ["Citação: airandspace.si.edu/stories/editorial/wonder-weapons-and-slave-labor"], fonte=SERIF, larg=54)

# 4) Esquema dos túneis (feito por nós, a partir do texto do Smithsonian)
im = Image.new("RGB", (2400, 1350), (14, 14, 16)); d = ImageDraw.Draw(im)
d.polygon([(150, 1040), (700, 640), (1050, 540), (1400, 570), (1800, 720), (2250, 1040)], fill=(52, 50, 46))
for yy, nome in ((850, "TÚNEL A"), (930, "TÚNEL B")):
    d.rectangle((420, yy, 1980, yy + 40), fill=(10, 10, 10)); d.text((440, yy - 2), nome, font=SANS, fill=(150, 150, 150))
for x in range(520, 1950, 110): d.rectangle((x, 890, x + 18, 930), fill=(10, 10, 10))
f = ImageFont.truetype(str(FON / "font1.ttf"), 90)
d.text((150, 300), "MONTE KOHNSTEIN · NORDHAUSEN", font=f, fill=(236, 230, 214))
d.text((150, 420), "Mittelwerk: dois túneis paralelos atravessando a montanha, ligados por galerias", font=SANS, fill=(200, 196, 186))
d.text((150, 1080), "Esquema ilustrativo, fora de escala. Fonte: Smithsonian (Neufeld, 2020)", font=SANS, fill=(140, 140, 140))
im.save(OUT / "d_kohnstein.png")
json.dump(RES, open(OUT / "docs.json", "w"), ensure_ascii=False, indent=1)
print({k: (v[0], len(v[1])) for k, v in RES.items()})
