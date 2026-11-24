"""Capa B, mais chamativa: só imagens reais.

Fundo: passageiros andando em direção à câmera na plataforma do metrô de Nova York
("Arteries of New York City", 1941, arquivo público). Ninguém olha para cima: é o vídeo.
Documento: a linha "New York, NY — 7-10 Jun 1966" da lista entregue ao Senado em 1977.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps, ImageChops
import pathlib, subprocess, json, random

F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes")
OUT = pathlib.Path(__file__).resolve().parent.parent / "render"
W, H = 1280, 720
anton = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s)
maq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
TMP = pathlib.Path("/tmp/capa_bio"); TMP.mkdir(exist_ok=True)

# ---------- fundo ----------
q = TMP / "f199.png"
if not q.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-ss", "199", "-i", "/home/user/mk/bio/raw/SUB41.mp4",
                    "-frames:v", "1", str(q), "-y"], check=True)
bg = Image.open(q).convert("L")
bg = bg.resize((1920, 1440), Image.LANCZOS)
bg = bg.crop((40, 465, 40 + W, 465 + H))            # rostos na faixa de baixo do quadro
bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=120, threshold=2))
bg = ImageEnhance.Contrast(bg).enhance(1.5)
bg = ImageEnhance.Brightness(bg).enhance(1.05)
# duotom: sombras vermelho-sangue, luzes papel
tela = ImageOps.colorize(bg, black=(14, 2, 2), mid=(120, 28, 22), white=(244, 232, 214), midpoint=105)
# grão de filme
random.seed(7)
gr = Image.effect_noise((W, H), 28).convert("L")
tela = Image.blend(tela, ImageOps.colorize(gr, (0, 0, 0), (255, 255, 255)), 0.06)

# escurecer a esquerda para o título
g = Image.new("L", (W, 1))
for x in range(W):
    g.putpixel((x, 0), int(235 * max(0.0, min(1.0, (620 - x) / 520)) ** 0.9))
tela = Image.composite(Image.new("RGB", (W, H), (8, 2, 2)), tela, g.resize((W, H)))
# vinheta
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-200, -160, W + 200, H + 160], fill=255)
tela = Image.composite(tela, Image.new("RGB", (W, H), (0, 0, 0)), v.filter(ImageFilter.GaussianBlur(140)))

d = ImageDraw.Draw(tela)

# ---------- círculo vermelho num passageiro ----------
cx, cy, r = 856, 292, 104
for k in range(3):
    d.ellipse([cx - r - k, cy - r - k, cx + r + k, cy + r + k], outline=(232, 30, 30), width=5)

# ---------- recorte do documento ----------
pg = TMP / "pag126.png"
if not pg.exists():
    subprocess.run(["pdftoppm", "-r", "400", "-f", "132", "-l", "132", "-png", "-singlefile",
                    "/home/user/mk/bio/pg/hearing1977.pdf", str(pg)[:-4]], check=True)
doc = Image.open(pg).convert("RGB"); esc = doc.width / 792.0
bx = json.load(open("/home/user/mk/bio/docs2/docs.json"))["d_lista2"][1]
y0 = min(b[1] for b in bx) * esc; y1 = max(b[3] for b in bx) * esc
tira = doc.crop((int(100 * esc), int(y0 - 22 * esc), int(560 * esc), int(y1 + 22 * esc)))
dd = ImageDraw.Draw(tira, "RGBA")
for x0, a, x1, b in bx:
    dd.rectangle([x0 * esc - 100 * esc - 6, a * esc - (y0 - 22 * esc) - 8,
                  x1 * esc - 100 * esc + 6, b * esc - (y0 - 22 * esc) + 10], fill=(252, 206, 0, 120))
tira = tira.resize((560, int(560 * tira.height / tira.width)), Image.LANCZOS)
tira = ImageEnhance.Contrast(tira).enhance(1.2)
tira = tira.rotate(3, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
m = tira.convert("L").point(lambda p: 255 if p > 12 else 0)
px, py = 640, 548
sh = Image.new("L", (tira.width + 50, tira.height + 50), 0)
ImageDraw.Draw(sh).rectangle([25, 30, tira.width + 22, tira.height + 26], fill=220)
tela.paste(Image.new("RGB", sh.size, (0, 0, 0)), (px - 25, py - 25), sh.filter(ImageFilter.GaussianBlur(14)))
tela.paste(tira, (px, py), m)

d = ImageDraw.Draw(tela)
def tx(x, y, t, f, cor, s=7):
    for i in range(1, s): d.text((x + i, y + i), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=cor)

# ---------- título ----------
tx(54, 150, "NOVA YORK · 1966", maq(40), (252, 206, 0), 4)
tx(46, 205, "NINGUÉM", anton(170), (255, 250, 242), 8)
tx(46, 385, "VIU.", anton(170), (232, 30, 30), 8)

tela.save(OUT / "capa-B.jpg", quality=95)
tela.resize((336, 189), Image.LANCZOS).save(TMP / "mini-B.png")
print("ok")
