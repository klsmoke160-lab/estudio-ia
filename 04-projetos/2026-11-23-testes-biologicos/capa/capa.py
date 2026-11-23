"""Capa do vídeo: só imagens reais.

Fundo: plataforma do metrô de Nova York em "Arteries of New York City" (1941, arquivo público).
Recorte de documento: página 126 da audiência do Senado de 1977, com a linha
"New York, NY — 7-10 Jun 1966" marcada em amarelo.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps, ImageChops
import pathlib, subprocess, re, html, json

F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes")
OUT = pathlib.Path(__file__).resolve().parent.parent / "render"; OUT.mkdir(exist_ok=True)
W, H = 1280, 720
serif = lambda s: ImageFont.truetype(str(F / "serif.ttf"), s)
anton = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s)
maq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)

# ---------- fundo: quadro real da plataforma ----------
TMP = pathlib.Path("/tmp/capa_bio"); TMP.mkdir(exist_ok=True)
quadro = TMP / "fundo.png"
if not quadro.exists():
    subprocess.run(["ffmpeg", "-v", "error", "-ss", "197", "-i", "/home/user/mk/bio/raw/SUB41.mp4",
                    "-frames:v", "1", str(quadro), "-y"], check=True)
bg = Image.open(quadro).convert("RGB")
k = max(W / bg.width, H / bg.height)
bg = bg.resize((int(bg.width * k), int(bg.height * k)), Image.LANCZOS)
bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2 - 20, (bg.width - W) // 2 + W, (bg.height - H) // 2 - 20 + H))
bg = ImageEnhance.Contrast(bg).enhance(1.25)
bg = ImageEnhance.Brightness(bg).enhance(0.62)
# tom frio, de documento antigo em arquivo
bg = ImageOps.colorize(bg.convert("L"), black=(6, 10, 16), mid=(78, 92, 102), white=(225, 232, 236), midpoint=118)
tela = bg.copy()

# escurecer a esquerda, onde entra o título
sombra = Image.new("L", (W, 1))
for x in range(W):
    sombra.putpixel((x, 0), int(228 * max(0.0, min(1.0, (660 - x) / 560)) ** 0.85))
tela = Image.composite(Image.new("RGB", (W, H), (4, 7, 11)), tela, sombra.resize((W, H)))
# vinheta
vin = Image.new("L", (W, H), 0)
ImageDraw.Draw(vin).ellipse([-260, -200, W + 260, H + 200], fill=255)
vin = vin.filter(ImageFilter.GaussianBlur(170))
tela = Image.composite(tela, Image.new("RGB", (W, H), (0, 0, 0)), vin)

# ---------- recorte do documento com marca-texto ----------
pg = TMP / "pag126.png"
if not pg.exists():
    subprocess.run(["pdftoppm", "-r", "400", "-f", "132", "-l", "132", "-png", "-singlefile",
                    "/home/user/mk/bio/pg/hearing1977.pdf", str(pg)[:-4]], check=True)
doc = Image.open(pg).convert("RGB")
esc = doc.width / 792.0                       # as caixas de docs.json estão na escala de 792 px
bx = json.load(open("/home/user/mk/bio/docs2/docs.json"))["d_lista2"][1]
dd = ImageDraw.Draw(doc, "RGBA")
for x0, y0, x1, y1 in bx[-2:]:                # as duas últimas: a linha de Nova York
    dd.rectangle([x0 * esc - 6, y0 * esc - 8, x1 * esc + 6, y1 * esc + 10], fill=(252, 206, 0, 150))
rec = doc.crop((int(96 * esc), int(96 * esc), int(700 * esc), int(500 * esc)))
rec = rec.resize((446, int(446 * rec.height / rec.width)), Image.LANCZOS)
rec = ImageEnhance.Contrast(rec).enhance(1.15)
rec = rec.rotate(-2.2, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
# papel com sombra
sh = Image.new("L", (rec.width + 60, rec.height + 60), 0)
ImageDraw.Draw(sh).rectangle([30, 34, rec.width + 26, rec.height + 30], fill=215)
sh = sh.filter(ImageFilter.GaussianBlur(18))
px, py = 782, 162
tela.paste(Image.new("RGB", sh.size, (0, 0, 0)), (px - 30, py - 30), sh)
m = Image.new("L", rec.size, 0)
ImageDraw.Draw(m).rectangle([0, 0, rec.width, rec.height], fill=255)
m = Image.composite(m, Image.new("L", rec.size, 0),
                    rec.convert("L").point(lambda v: 255 if v > 14 else 0))
tela.paste(rec, (px, py), m)

d = ImageDraw.Draw(tela)

def tx(x, y, t, f, cor, s=7):
    for i in range(1, s): d.text((x + i, y + i), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=cor)

# ---------- título ----------
tx(52, 300, "NOVA YORK, 1966", maq(42), (252, 206, 0), 4)
d.rectangle([54, 352, 300, 357], fill=(196, 42, 30))
tx(46, 378, "O TESTE QUE", serif(78), (244, 240, 232), 6)
tx(46, 456, "NINGUÉM VIU", serif(104), (255, 252, 246), 8)
tx(52, 598, "O QUE O EXÉRCITO ENTREGOU AO SENADO", maq(35), (224, 228, 232), 4)

tela.save(OUT / "capa.jpg", quality=95)
print("ok", OUT / "capa.jpg")
