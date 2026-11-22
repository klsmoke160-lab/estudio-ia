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
W2,H2=1920,1080; TOP,AGUA,FUNDO=175,305,905; BANDAS=[(TOP,AGUA)]+[(AGUA+k*150,AGUA+(k+1)*150) for k in range(4)]   # tudo dentro da área sem as faixas de cinema (133 px)
ANT=ImageFont.truetype(str(FON/"font1.ttf"),50); ANTs=ImageFont.truetype(str(FON/"font1.ttf"),34); MQ=ImageFont.truetype(str(FON/"font2.ttf"),27)
def iceberg(dest):
    im=Image.new("RGB",(W2,H2)); d=ImageDraw.Draw(im)
    for y in range(H2):
        if y<AGUA: c=(10,12,18)
        else: k=min(1,(y-AGUA)/(FUNDO-AGUA)); c=(int(14*(1-k)+2),int(42*(1-k)+4),int(70*(1-k)+8))
        d.line([(0,y),(W2,y)],fill=c)
    cx=1240; sy=(FUNDO-AGUA)/790
    pts=[(-120,0),(-330,160),(-420,420),(-360,620),(-250,760),(-60,790),(120,720),(300,560),(410,330),(260,120),(150,0)]
    sub=[(cx+x,AGUA+y*sy) for x,y in pts]
    ov=Image.new("RGBA",(W2,H2),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for k,(y0,y1) in enumerate(BANDAS):
        if dest==k+1: od.rectangle([0,y0,W2,y1],fill=(226,51,59,40)); od.rectangle([0,y0,14,y1],fill=(226,51,59,255))
    im=Image.alpha_composite(im.convert("RGBA"),ov)
    ov=Image.new("RGBA",(W2,H2),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.polygon(sub,fill=(150,200,225,70)); od.polygon([(cx-150,AGUA),(cx-60,TOP+40),(cx+10,TOP+8),(cx+90,TOP+55),(cx+170,AGUA)],fill=(235,244,250,255))
    im=Image.alpha_composite(im,ov).convert("RGB"); d=ImageDraw.Draw(im)
    d.line([(0,AGUA),(W2,AGUA)],fill=(120,170,200),width=3)
    for k,(y0,y1) in enumerate(BANDAS):
        on=(dest==k+1); vis=(dest==0 or on); cor=(242,235,221) if vis else (80,96,110)
        y=y0+((y1-y0)-(132 if on else 84))//2
        d.text((70,y),NIV[k][0],font=ANTs,fill=(226,51,59) if on else ((200,190,170) if vis else (70,84,96)))
        d.text((70,y+38),NIV[k][1],font=ANT if on else ANTs,fill=cor)
        if on: d.text((70,y+106),NIV[k][2],font=MQ,fill=(230,222,205))
        if k>0: d.line([(0,y0),(W2,y0)],fill=(40,70,95),width=1)
    im.save(OUT/f"iceberg_{dest}.png")
for k in range(6): iceberg(k)
json.dump(RES, open(OUT / "docs.json", "w"), ensure_ascii=False, indent=1)
print({k: (pathlib.Path(v[0]).name, len(v[1])) for k, v in RES.items()})
