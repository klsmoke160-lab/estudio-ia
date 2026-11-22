"""Gera as páginas de documento do Golfo de Tonkin como transcrições (texto oficial publicado), com as caixas do marca-texto, e o esquema dos túneis.
Saída: /home/user/mk/tk/docs/*.png e docs.json {chave: [arquivo, [[x0,y0,x1,y1],...]]}."""
import json, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
OUT = pathlib.Path("/home/user/mk/tk/docs"); OUT.mkdir(parents=True, exist_ok=True)
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


import csv, re as _re
def nsa(chave, png, ini, fim):
    """Caixas (por linha) do trecho entre `ini` e `fim` numa página escaneada, pelas posições do OCR (tesseract tsv)."""
    rows=[r for r in csv.DictReader(open(OUT/(png[:-4]+".tsv")),delimiter="\t") if (r.get("text") or "").strip()]
    nm=lambda s:_re.sub(r"[^a-z0-9]","",s.lower())
    ws=[(nm(r["text"]),int(r["left"]),int(r["top"]),int(r["left"])+int(r["width"]),int(r["top"])+int(r["height"])) for r in rows]
    ws=[w for w in ws if w[0]]
    a=[nm(x) for x in ini.split() if nm(x)]; b=[nm(x) for x in fim.split() if nm(x)]
    i=next((i for i in range(len(ws)) if [w[0] for w in ws[i:i+len(a)]]==a),None)
    if i is None: raise SystemExit(f"início não achado: {chave}: {ini}")
    j=next((j for j in range(i,len(ws)) if [w[0] for w in ws[j:j+len(b)]]==b),None)
    if j is None: raise SystemExit(f"fim não achado: {chave}: {fim}")
    linhas={}
    for t,x0,y0,x1,y1 in ws[i:j+len(b)]:
        k=round(y0/25); L=linhas.get(k,[1e9,1e9,0,0]); linhas[k]=[min(L[0],x0),min(L[1],y0),max(L[2],x1),max(L[3],y1)]
    RES[chave]=[str(OUT/png),[linhas[k] for k in sorted(linhas)]]

# 1) Estudo da NSA (Hanyok), páginas escaneadas originais
nsa("nsa_titulo","nsa_p02.png","Skunks,","Fish:")
nsa("nsa_noattack","nsa_p04.png","no attack happened","that night.")
nsa("nsa_90","nsa_p04.png","The withheld","available SIGINT.")
nsa("nsa_sonar","nsa_p25.png","the rud-","ships' own propellers.")
nsa("nsa_duvidas","nsa_p25.png","ENTIRE ACTION LEAVES","AT BEGINNING.")
nsa("nsa_3horas","nsa_p25.png","Within three hours","retaliatory strike")
nsa("nsa_doubtful","nsa_p25.png","a review of the action","doubtful")
nsa("nsa_nohappen","nsa_p50.png","whelming body of reports,","had happened.")
nsa("nsa_fit","nsa_p50.png","make SIGINT fit","Gulf of Tonkin.")

# 2) Transcrições (texto oficial publicado), com marca-texto
res=[("Whereas naval units of the Communist regime in Vietnam, in violation of the principles of the Charter of the United Nations and of international law, have deliberately and repeatedly attacked United States naval vessels lawfully present in international waters, and have thereby created a serious threat to international peace;",["have deliberately and repeatedly attacked United States naval vessels"]),
 ("Resolved by the Senate and House of Representatives of the United States of America in Congress assembled, That the Congress approves and supports the determination of the President, as Commander in Chief, to take all necessary measures to repel any armed attack against the forces of the United States and to prevent further aggression.",["to take all necessary measures","to prevent further aggression"]),
 ("Section 3. This resolution shall expire when the President shall determine that the peace and security of the area is reasonably assured by international conditions created by action of the United Nations or otherwise, except that it may be terminated earlier by concurrent resolution of the Congress.",[])]
r=pagina("resolucao_t",["PUBLIC LAW 88-408","88th Congress, H. J. Res. 1145","August 10, 1964","Joint Resolution"],res,["Transcrição: Tonkin Gulf Resolution, Arquivo Nacional dos EUA (Record Group 11)","archives.gov/milestone-documents/tonkin-gulf-resolution"],fonte=SERIF,larg=54)
RES["res_ataque"]=[r[0],r[1]["have deliberately and repeatedly attacked United States naval vessels"]]
RES["res_medidas"]=[r[0],r[1]["to take all necessary measures"]+r[1]["to prevent further aggression"]]
lbj=[("My fellow Americans: As President and Commander in Chief, it is my duty to the American people to report that renewed hostile actions against United States ships on the high seas in the Gulf of Tonkin have today required me to order the military forces of the United States to take action in reply.",["renewed hostile actions against United States ships on the high seas in the Gulf of Tonkin"]),
 ("The initial attack on the destroyer Maddox, on August 2, was repeated today by a number of hostile vessels attacking two U.S. destroyers with torpedoes.",["was repeated today"])]
r=pagina("lbj_discurso",["THE WHITE HOUSE","Report to the American People","on the Gulf of Tonkin Incident","August 4, 1964"],lbj,["Transcrição: discurso do presidente Lyndon B. Johnson, 4 de agosto de 1964","Miller Center / The American Presidency Project"],fonte=SERIF,larg=54)
RES["lbj"]=[r[0],r[1]["renewed hostile actions against United States ships on the high seas in the Gulf of Tonkin"]+r[1]["was repeated today"]]
mc=[("Our Navy played absolutely no part in, was not associated with, was not aware of, any South Vietnamese actions, if there were any.",["played absolutely no part in","was not aware of"])]
r=pagina("mcnamara64",["U.S. SENATE","Committees on Foreign Relations and Armed Services","Executive session, August 6, 1964","Testimony of Secretary of Defense Robert S. McNamara"],mc,["Citação: depoimento em sessão fechada, 6 de agosto de 1964","citado por John Prados, National Security Archive (2004)"],fonte=SERIF,larg=50)
RES["mcnamara64"]=[r[0],r[1]["played absolutely no part in"]+r[1]["was not aware of"]]
mc68=[("Intelligence reports from a highly classified and unimpeachable source reported that North Vietnam was making preparations to attack our destroyers with two Swatow boats and one PT boat if the PT could be made ready in time.",["highly classified and unimpeachable source"]),
 ("The same source reported, while the engagement was in progress on August 4, that the attack was underway.",["while the engagement was in progress on August 4"])]
r=pagina("mcnamara68",["U.S. SENATE","Committee on Foreign Relations","The Gulf of Tonkin, the 1964 Incidents","February 20, 1968"],mc68,["Citação: depoimento de Robert S. McNamara, 1968","citado por John Prados, National Security Archive (2004)"],fonte=SERIF,larg=54)
RES["mcnamara68"]=[r[0],r[1]["highly classified and unimpeachable source"]+r[1]["while the engagement was in progress on August 4"]]
jones=[("Of the several messages we were allowed to scan, only one was from August 4. The others clearly related to the incident on August 2. My reading of the Aug. 4 intercept was that it was a boastful summary of the attack on August 2.",["a boastful summary of the attack on August 2"]),
 ("Curiously, NSA could not find the original of the Aug. 4 intercept, although it did have originals of the others.",["NSA could not find the original of the Aug. 4 intercept"])]
r=pagina("jones",["J. NORVILL JONES","Senate Foreign Relations Committee staff","Recollection of the Tonkin intercepts"],jones,["Citação: J. Norvill Jones, funcionário da Comissão de Relações Exteriores do Senado","citado por John Prados, National Security Archive (2004)"],fonte=SERIF,larg=54)
RES["jones"]=[r[0],r[1]["a boastful summary of the attack on August 2"]+r[1]["NSA could not find the original of the Aug. 4 intercept"]]
st=[("There was absolutely no gunfire except our own, no PT boat wakes, not a candle light let alone a burning ship. None could have been there and not have been seen on such a black night.",["There was absolutely no gunfire except our own","not a candle light let alone a burning ship"])]
r=pagina("stockdale",["JAMES B. STOCKDALE","Pilot over the Gulf of Tonkin, night of August 4, 1964"],st,["Citação: James e Sybil Stockdale, In Love and War (1984)","citado por John Prados, National Security Archive (2004)"],fonte=SERIF,larg=50)
RES["stockdale"]=[r[0],r[1]["There was absolutely no gunfire except our own"]+r[1]["not a candle light let alone a burning ship"]]
rel=[("The largest U.S. intelligence agency, the National Security Agency, today declassified over 140 formerly top secret documents -- histories, chronologies, signals intelligence reports, and oral history interviews -- on the August 1964 Gulf of Tonkin incident.",["declassified over 140 formerly top secret documents"]),
 ("Included in the release is a controversial article by Agency historian Robert J. Hanyok on SIGINT and the Tonkin Gulf which confirms what historians have long argued: that there was no second attack on U.S. ships in Tonkin on August 4, 1964.",["there was no second attack on U.S. ships in Tonkin on August 4, 1964"])]
r=pagina("release2005",["NATIONAL SECURITY ARCHIVE","George Washington University","Washington, D.C., December 1, 2005"],rel,["Transcrição: National Security Archive, 1º de dezembro de 2005","nsarchive2.gwu.edu/NSAEBB/NSAEBB132/press20051201.htm"],fonte=SERIF,larg=54)
RES["release"]=[r[0],r[1]["declassified over 140 formerly top secret documents"]+r[1]["there was no second attack on U.S. ships in Tonkin on August 4, 1964"]]
herr=[("A review of the action makes many reported contacts and torpedoes fired 'appear doubtful'. 'Freak weather effects' on radar, and 'over-eager' sonarmen may have accounted for many reports.",["'appear doubtful'","'Freak weather effects'","'over-eager' sonarmen"]),
 ("'No visual sightings' have been reported by the Maddox, and the Commander suggests that a 'complete evaluation' be undertaken before any further action.",["'No visual sightings'","a 'complete evaluation' be undertaken before any further action"])]
r=pagina("herrick",["TOP SECRET","Chronology prepared for the President","August 28, 1964","Message from Captain John J. Herrick, August 4, 1964"],herr,["Transcrição: cronologia ultrassecreta de 28/08/1964, citada pelo","National Security Archive (2004)"],fonte=SERIF,larg=54)
RES["herrick"]=[r[0],r[1]["'appear doubtful'"]+r[1]["'Freak weather effects'"]+r[1]["'over-eager' sonarmen"]]
RES["herrick2"]=[r[0],r[1]["'No visual sightings'"]+r[1]["a 'complete evaluation' be undertaken before any further action"]]
mc3=[("I think I should also, or we should also at that time, Mr. President, explain this OPLAN 34-A. There's no question but what that had bearing on.",["explain this OPLAN 34-A","There's no question but what that had bearing on"])]
r=pagina("tel3ago",["THE WHITE HOUSE TAPES","Telephone conversation, August 3, 1964, 10:30 a.m.","President Johnson and Secretary McNamara"],mc3,["Transcrição: gravação da Casa Branca, 3 de agosto de 1964","John Prados, The White House Tapes (2003) / National Security Archive"],fonte=SERIF,larg=50)
RES["tel3ago"]=[r[0],r[1]["explain this OPLAN 34-A"]+r[1]["There's no question but what that had bearing on"]]
json.dump(RES, open(OUT / "docs.json", "w"), ensure_ascii=False, indent=1)
print({k: (pathlib.Path(v[0]).name, len(v[1])) for k, v in RES.items()})
