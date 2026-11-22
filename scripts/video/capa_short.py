"""Capa vertical (1080x1920) de Short do Rasura: frase grande, recorte de documento com marca-texto e foto do caso ao fundo.
Uso: python3 scripts/video/capa_short.py capa.json saida.jpg
capa.json: {"foto": "x.jpg", "foco": [0.5,0.3], "linhas": [["PARABÉNS,","creme"],["VOCÊ CRIOU","creme"],["O MKULTRA","vermelho"]],
 "recorte": {"arq":"pagina.png","caixa":[x0,y0,x1,y1],"marcas":[[x0,y0,x1,y1]],"largura":900,"giro":-2.2}, "legenda": "Senado dos EUA, 1977"}
Caixas e marcas em pixels da página original."""
import json, sys, pathlib, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
F = pathlib.Path(__file__).resolve().parents[2] / "05-biblioteca/fontes"; ANTON = str(F / "font1.ttf"); MAQ = str(F / "font2.ttf")
W, H = 1080, 1920; COR = {"creme": (242, 235, 221), "vermelho": (227, 38, 46), "amarelo": (255, 214, 10)}
c = json.load(open(sys.argv[1])); base = pathlib.Path(sys.argv[1]).resolve().parent
P = lambda p: p if pathlib.Path(p).is_absolute() else str(base / p)
# fundo: foto em preto e branco, escurecida embaixo e em cima
im = Image.open(P(c["foto"])).convert("RGB"); esc = max(W / im.width, H / im.height); im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
fx, fy = c.get("foco", [0.5, 0.4]); x = min(max(0, int(im.width * fx - W / 2)), im.width - W); y = min(max(0, int(im.height * fy - H / 2)), im.height - H)
im = ImageOps.grayscale(im.crop((x, y, x + W, y + H))).convert("RGB"); im = ImageEnhance.Contrast(im).enhance(1.25); im = ImageEnhance.Brightness(im).enhance(0.75)
g = Image.new("L", (1, H)); 
for yy in range(H): g.putpixel((0, yy), int(255 * min(1, max(0.12, (yy - 900) / 350))) if not c.get('dy') else int(255 * min(1, max(0.08, (yy - 1050) / 300))))
dy = c.get("dy", 0)
if dy:
    t = Image.new("RGB", (W, H), (10, 10, 10)); t.paste(im, (0, dy)); im = t
im = Image.composite(im, Image.new("RGB", (W, H), (10, 10, 10)), g.resize((W, H)))
d = ImageDraw.Draw(im); an = lambda s: ImageFont.truetype(ANTON, s)
def riscar(x0, x1, yc, esp):
    d.line([(x0, yc), (x1, yc - 14)], fill=COR["vermelho"], width=esp)
w = d.textlength("RASURA", font=an(76)); x0 = (W - w) / 2; d.text((x0, 110), "RASURA", font=an(76), fill=COR["creme"]); riscar(x0 - 12, x0 + w + 12, 110 + 46, 10)
# frase
y = 250
for txt, cor in c["linhas"]:
    s = 190
    while d.textlength(txt, font=an(s)) > 960: s -= 6
    w = d.textlength(txt, font=an(s)); d.text(((W - w) / 2, y), txt, font=an(s), fill=COR[cor], stroke_width=6, stroke_fill=(0, 0, 0)); y += int(s * 1.12)
# recorte do documento com marca-texto
r = c["recorte"]; pg = Image.open(P(r["arq"])).convert("RGB"); x0, y0, x1, y1 = r["caixa"]; cr = pg.crop((x0, y0, x1, y1)).convert("RGBA")
ov = Image.new("RGBA", cr.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
for mx0, my0, mx1, my1 in r["marcas"]: od.rectangle([mx0 - x0 - 6, my0 - y0 - 3, mx1 - x0 + 6, my1 - y0 + 5], fill=(255, 226, 0, 135))
cr = Image.alpha_composite(cr, ov).convert("RGB"); lw = r.get("largura", 900); cr = cr.resize((lw, int(cr.height * lw / cr.width)), Image.LANCZOS)
cr = ImageOps.expand(cr, border=10, fill=(236, 230, 214)); sh = Image.new("RGBA", (cr.width + 80, cr.height + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([40, 50, cr.width + 40, cr.height + 50], fill=(0, 0, 0, 170))
sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.paste(cr.convert("RGBA"), (40, 40)); sh = sh.rotate(r.get("giro", -2), expand=True, resample=Image.BICUBIC)
im.paste(sh, ((W - sh.width) // 2, max(y + 40, 1020 - sh.height // 2)), sh)
if c.get("legenda"):
    f = ImageFont.truetype(MAQ, 38); w = d.textlength(c["legenda"], font=f); d.text(((W - w) / 2, 1760), c["legenda"], font=f, fill=(216, 208, 190), stroke_width=3, stroke_fill=(0, 0, 0))
im.save(sys.argv[2], quality=93); print("capa:", sys.argv[2], im.size)
