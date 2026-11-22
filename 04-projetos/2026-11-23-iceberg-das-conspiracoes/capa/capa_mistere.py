"""Capa no estilo da referência Mistère (iceberg vermelho + rostos com tarja), só com imagens reais:
iceberg = foto da NASA (North Star Bay, Groenlândia) recolorida em vermelho, com o reflexo dela na água;
rostos = Gottlieb (governo dos EUA), Johnson (cinejornal Universal, 1964), von Braun (NASA), Powers e Eisenhower (cinejornais Universal, 1960)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps, ImageChops
import pathlib
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
R = pathlib.Path("/home/user/mk/ice/rostos")
serif = lambda s: ImageFont.truetype(str(F / "serif.ttf"), s); an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s)
tela = Image.new("RGB", (W, H), (6, 2, 2))
# brilho vermelho de fundo
g = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse([40, 120, 720, 640], fill=(120, 14, 8)); g = g.filter(ImageFilter.GaussianBlur(150))
tela = ImageChops.add(tela, g)
# iceberg real recolorido e isolado do céu
src = Image.open("/home/user/mk/ice/nasa/ice/GSFC_20171208_Archive_e000736.jpg").convert("L").crop((560, 760, 1560, 1330))
src = ImageEnhance.Contrast(src).enhance(1.6)
ice = ImageOps.colorize(src, black=(10, 0, 0), mid=(200, 30, 12), white=(255, 205, 140), midpoint=110)
ice = ice.resize((680, int(680 * ice.height / ice.width)), Image.LANCZOS); srcr = src.resize(ice.size)
CONT = [(0,348),(60,340),(120,310),(135,280),(150,220),(200,180),(260,120),(300,75),(330,60),(400,55),(440,90),(470,125),(520,135),(560,180),(600,230),(650,270),(700,300),(745,325),(775,358),(830,390),(900,420),(1000,455),(1000,528),(0,528)]
k = ice.width / 1000; mask = Image.new("L", ice.size, 0); ImageDraw.Draw(mask).polygon([(x * k, y * k) for x, y in CONT], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(1.5)); ice = ice.crop((0, 0, ice.width, int(528 * k))); mask = mask.crop((0, 0, mask.width, int(528 * k)))
AG = 380; ix = 30; iy = AG - ice.height
ice = ImageEnhance.Brightness(ice).enhance(1.45)
brilho = Image.new("RGB", (W, H), (0, 0, 0)); bm = Image.new("L", (W, H), 0); bm.paste(mask, (ix, iy)); bm = bm.filter(ImageFilter.GaussianBlur(40))
brilho.paste(Image.new("RGB", (W, H), (200, 40, 10)), (0, 0), bm.point(lambda v: int(v * 0.8)))
tela = ImageChops.add(tela, brilho)
tela.paste(ice, (ix, iy), mask)
# reflexo (parte "submersa"): a própria foto espelhada, mais escura, ondulada
ref = ImageOps.flip(ice); rm = ImageOps.flip(mask)
ref = ImageEnhance.Brightness(ref).enhance(0.55).filter(ImageFilter.GaussianBlur(2.5))
fade = Image.new("L", (1, ref.height)); [fade.putpixel((0, y), int(230 * max(0, 1 - y / ref.height))) for y in range(ref.height)]
rm = ImageChops.multiply(rm, fade.resize(ref.size))
tela.paste(ref, (ix, AG + 4), rm)
d = ImageDraw.Draw(tela); d.line([(0, AG + 2), (760, AG + 2)], fill=(150, 40, 30), width=2)
# rostos
CX = {"gottlieb.jpg": (927, 619, 1434), "johnson.png": (349, 218, 233), "vonbraun_retrato_1960.jpg": (674, 574, 888), "powers.png": (140, 80, 140), "eisenhower.png": (455, 75, 125)}
OLHO = {"gottlieb.jpg": 0.37, "johnson.png": 0.33, "vonbraun_retrato_1960.jpg": 0.38}
def rosto(nome, lado):
    im = Image.open(R / nome).convert("L"); x, y, s = CX[nome]
    cx, cy = x + s / 2, y + s * 0.62; hw = s * 0.95; hh = hw * 1.2
    l, t = cx - hw, cy - hh; im = im.crop((int(l), int(t), int(cx + hw), int(cy + hh)))
    k = lado / (2 * hw); im = im.resize((lado, int(2 * hh * k)), Image.LANCZOS); im = ImageEnhance.Contrast(im).enhance(1.35); im = im.point(lambda v: int(255 * (v / 255) ** 1.25))
    rgb = ImageOps.colorize(im, black=(12, 4, 4), white=(238, 226, 214))
    a = Image.new("L", rgb.size, 0); ImageDraw.Draw(a).ellipse([lado * 0.12, rgb.height * 0.04, lado * 0.88, rgb.height * 1.2], fill=255); a = a.filter(ImageFilter.GaussianBlur(lado * 0.09))
    olho = ((y + s * OLHO.get(nome, 0.40) - t) * k, (x - s * 0.02 - l) * k, (x + s * 1.02 - l) * k, s * 0.15 * k)
    return rgb, a, olho
pos = [("gottlieb.jpg", 760, 10, 300), ("johnson.png", 990, 60, 290), ("vonbraun_retrato_1960.jpg", 850, 330, 290)]
for nome, px, py, lado in pos:
    rgb, a, (oy, ox0, ox1, oh) = rosto(nome, lado)
    tela.paste(rgb, (px, py), a)
    d.rectangle([px + ox0, py + oy, px + ox1, py + oy + oh], fill=(0, 0, 0))
# título
def tx(x, y, t, f, cor, s=7):
    for k in range(1, s): d.text((x + k, y + k), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=cor)
tx(40, 438, "O ICEBERG DAS", serif(64), (245, 238, 228), 5)
tx(30, 505, "CONSPIRAÇÕES", serif(128), (255, 250, 240), 8)
tela.save("../render/capa-mistere.jpg", quality=95); print("ok")
