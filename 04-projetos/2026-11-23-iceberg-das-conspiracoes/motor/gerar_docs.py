"""Gera as páginas de documento e os esquemas do Iceberg das Conspirações como transcrições (texto oficial publicado), com as caixas do marca-texto, e o esquema dos túneis.
Saída: /home/user/mk/ice/docs/*.png e docs.json {chave: [arquivo, [[x0,y0,x1,y1],...]]}."""
import json, pathlib, textwrap
from PIL import Image, ImageDraw, ImageFont
OUT = pathlib.Path("/home/user/mk/ice/docs"); OUT.mkdir(parents=True, exist_ok=True)
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


import csv, re as _re, subprocess as _sp, html as _h
nm=lambda s:_re.sub(r"[^a-z0-9]","",s.lower())
def _linhas(ws,i,j,esc,div):
    L={}
    for t,x0,y0,x1,y1 in ws[i:j]:
        k=round(y0*esc/div); A=L.get(k,[1e9,1e9,0,0]); L[k]=[min(A[0],x0*esc),min(A[1],y0*esc),max(A[2],x1*esc),max(A[3],y1*esc)]
    return [L[k] for k in sorted(L)]
def _acha(ws,ini,fim):
    a=[nm(x) for x in ini.split() if nm(x)]; b=[nm(x) for x in fim.split() if nm(x)]
    i=next((i for i in range(len(ws)) if [w[0] for w in ws[i:i+len(a)]]==a),None)
    if i is None: return None,None
    j=next((j for j in range(i,len(ws)) if [w[0] for w in ws[j:j+len(b)]]==b),None)
    return i,(j+len(b) if j is not None else None)
def pdfdoc(chave,pdf,pag,ini,fim):
    """PDF com camada de texto: caixas pelas posições do pdftotext -bbox (pontos -> 220 dpi)."""
    t=open(OUT/(pdf+".bbox.html"),encoding="utf-8",errors="replace").read(); pg=_re.findall(r"<page[^>]*>(.*?)</page>",t,_re.S)[pag]
    ws=[(nm(_h.unescape(w)),float(a),float(b),float(c),float(d)) for a,b,c,d,w in _re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',pg)]
    ws=[w for w in ws if w[0]]; i,j=_acha(ws,ini,fim)
    if i is None or j is None: raise SystemExit(f"não achado: {chave}")
    png=OUT/f"{pdf}_p{pag+1:03d}.png"
    if not png.exists(): _sp.run(["pdftoppm","-r","220","-f",str(pag+1),"-l",str(pag+1),"-png","-singlefile",str(OUT/(pdf+".pdf")),str(png)[:-4]],check=True)
    RES[chave]=[str(png),_linhas(ws,i,j,220/72,6)]
def scan(chave,pdf,pag,ini,fim):
    """Página escaneada: renderiza a 220 dpi e acha o trecho pelo OCR (tesseract tsv)."""
    png=OUT/f"{pdf}_p{pag:03d}.png"
    if not png.exists(): _sp.run(["pdftoppm","-r","220","-f",str(pag),"-l",str(pag),"-png","-singlefile",str(OUT/(pdf+".pdf")),str(png)[:-4]],check=True)
    tsv=str(png)[:-4]+".tsv"
    if not pathlib.Path(tsv).exists(): _sp.run(["tesseract",str(png),str(png)[:-4],"-l","eng","tsv"],capture_output=True)
    rows=[r for r in csv.DictReader(open(tsv),delimiter="\t") if (r.get("text") or "").strip()]
    ws=[(nm(r["text"]),int(r["left"]),int(r["top"]),int(r["left"])+int(r["width"]),int(r["top"])+int(r["height"])) for r in rows]; ws=[w for w in ws if w[0]]
    i,j=_acha(ws,ini,fim)
    if i is None or j is None: raise SystemExit(f"não achado: {chave}: {ini} / {fim}")
    RES[chave]=[str(png),_linhas(ws,i,j,1,25)]

# 1) Páginas originais
pdfdoc("coin_inicio","coin",6,"COINTELPRO began in 1956","in 1971")
pdfdoc("coin_media","coin",6,"On March 8, 1971,","were widely circulated")
pdfdoc("coin_2000","coin",6,"more than 2,000","COINTELPRO actions.")
pdfdoc("coin_king","coin",84,"The tape recording was accompanied","committed suicide.")
pdfdoc("ufo_metade","haines",7,"over half of all","reconnaissance flights")
scan("rv_nunca","air",8,"case had the information","intelligence")
scan("rv_fim","air",9,"Thus, we conclude","is not warranted.")
scan("roswell_mogul","roswell",4,"Project MOGUL,","Roswell Incident.")

# 2) Transcrição: pedido de desculpas de Clinton (1997)
cl=[("They were betrayed. Medical people are supposed to help when we need care, but even once a cure was discovered, they were denied help, and they were lied to by their Government.",["even once a cure was discovered, they were denied help","they were lied to by their Government"]),
    ("What the United States Government did was shameful, and I am sorry.",["What the United States Government did was shameful, and I am sorry."])]
r=pagina("clinton_1997",["THE WHITE HOUSE","Remarks in Apology to African-Americans","on the Tuskegee Experiment","May 16, 1997"],cl,["Transcrição: discurso de Bill Clinton, 16 de maio de 1997","The American Presidency Project (UC Santa Barbara)"],fonte=SERIF,larg=54)
RES["clinton_cura"]=[r[0],r[1]["even once a cure was discovered, they were denied help"]+r[1]["they were lied to by their Government"]]
RES["clinton_sorry"]=[r[0],r[1]["What the United States Government did was shameful, and I am sorry."]]

# 3) Esquema do iceberg (feito pelo canal): 0 = visão geral, 1..5 = nível em destaque
NIV=[("NÍVEL 1","CONFESSADO","Northwoods · Tuskegee · MKUltra"),("NÍVEL 2","PROVADO NOS PAPÉIS","COINTELPRO · Golfo de Tonkin · Paperclip"),
     ("NÍVEL 3","O SEGREDO QUE VIROU LENDA","Área 51 · Roswell · Stargate"),("NÍVEL 4","SEM PROVA","O pouso falso na Lua"),("NÍVEL 5","O FUNDO","Terra plana")]
W2,H2=1920,1080
ANT=ImageFont.truetype(str(FON/"font1.ttf"),118); ANTm=ImageFont.truetype(str(FON/"font1.ttf"),46); ANTs=ImageFont.truetype(str(FON/"font1.ttf"),40); MQ=ImageFont.truetype(str(FON/"font2.ttf"),36)
Q=pathlib.Path("/home/user/mk/ice/quadros")
# cartões dos níveis sobre FILMAGEM REAL de icebergs (Mixkit), cada vez mais escura quanto mais fundo
FUNDO={0:"mx25245_5.png",1:"mx25244_25.png",2:"mx25244_45.png",3:"mx25244_5.png",4:"mx25245_15.png",5:"mx8128_9.png"}
LUZ={0:0.55,1:0.62,2:0.48,3:0.36,4:0.24,5:0.14}
from PIL import ImageEnhance as _E, ImageFilter as _F
def iceberg(dest):
    im=Image.open(Q/FUNDO[dest]).convert("RGB").resize((W2,H2),Image.LANCZOS)
    im=_E.Brightness(im).enhance(LUZ[dest]); im=_E.Color(im).enhance(0.75 if dest<3 else 0.55)
    g=Image.new("L",(W2,1))
    for x in range(W2): g.putpixel((x,0),int(255*max(0,min(1,(1100-x)/900))))
    im=Image.composite(Image.new("RGB",(W2,H2),(6,8,12)),im,g.resize((W2,H2)).point(lambda v:int(v*0.8)))
    d=ImageDraw.Draw(im)
    def t(x,y,s,f,c): d.text((x+4,y+5),s,font=f,fill=(0,0,0)); d.text((x,y),s,font=f,fill=c)
    if dest==0:
        t(110,190,"ATÉ ONDE VAI A VERDADE?",ANTm,(242,235,221)); y=280
        for k,(n,nome,_c) in enumerate(NIV):
            t(110,y,n,ANTs,(226,51,59)); t(290,y,nome,ANTs,(242,235,221)); y+=110
    else:
        n,nome,casos=NIV[dest-1]
        t(110,300,n,ANTm,(226,51,59)); d.rectangle([110,365,260,371],fill=(226,51,59))
        y=400
        for linha in nome.split(" QUE ") if len(nome)>14 and " QUE " in nome else [nome]:
            pass
        palavras=nome.split(); linhas=[]; cur=""
        for p in palavras:
            if d.textlength((cur+" "+p).strip(),font=ANT)>1150: linhas.append(cur); cur=p
            else: cur=(cur+" "+p).strip()
        linhas.append(cur)
        for l in linhas: t(110,y,l,ANT,(242,235,221)); y+=128
        t(110,y+40,casos,MQ,(220,212,195))
    im.save(OUT/f"iceberg_{dest}.png")
for k in range(6): iceberg(k)
json.dump(RES, open(OUT / "docs.json", "w"), ensure_ascii=False, indent=1)
print({k: (pathlib.Path(v[0]).name, len(v[1])) for k, v in RES.items()})
