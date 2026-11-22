"""Capa limpa do Iceberg das Conspirações (1280x720): iceberg desenhado, topo carimbado, uma frase curta."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pathlib
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s); mq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
CREAM, RED = (244, 238, 226), (230, 36, 44); AG = 250
im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
for y in range(H):
    if y < AG: c = (8, 10, 16)
    else: k = (y - AG) / (H - AG); c = (int(10 * (1 - k) + 2), int(46 * (1 - k) + 4), int(78 * (1 - k) + 8))
    d.line([(0, y), (W, y)], fill=c)
cx = 930
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
od.polygon([(cx-95,AG),(cx-260,AG+120),(cx-330,AG+300),(cx-260,AG+430),(cx-40,H+40),(cx+170,AG+430),(cx+290,AG+250),(cx+190,AG+90),(cx+115,AG)], fill=(150,200,225,60))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow); gd.polygon([(cx-125,AG),(cx-40,92),(cx+15,62),(cx+80,110),(cx+140,AG)], fill=(255,255,255,160)); glow = glow.filter(ImageFilter.GaussianBlur(22))
im = Image.alpha_composite(Image.alpha_composite(im.convert("RGBA"), glow), ov)
od = ImageDraw.Draw(im); od.polygon([(cx-125,AG),(cx-40,92),(cx+15,62),(cx+80,110),(cx+140,AG)], fill=(240,247,252,255))
od.line([(0, AG), (W, AG)], fill=(120, 170, 200), width=3)
# carimbo no topo
st = Image.new("RGBA", (330, 92), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.rectangle([4, 4, 326, 88], outline=RED, width=7); f = an(56); w = sd.textlength("PROVADO", font=f); sd.text(((330 - w) / 2, 6), "PROVADO", font=f, fill=RED)
st = st.rotate(-8, expand=True, resample=Image.BICUBIC); im.alpha_composite(st, (cx - 40, 120))
# interrogações no fundo, apagadas
qf = an(120)
for x, y, a in ((cx - 140, 330, 70), (cx + 60, 450, 50), (cx - 40, 560, 35)):
    t = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(t).text((x, y), "?", font=qf, fill=(200, 225, 240, a)); im = Image.alpha_composite(im, t)
d = ImageDraw.Draw(im)
def tx(x, y, t, f, cor): d.text((x + 5, y + 6), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=cor)
tx(60, 150, "O TOPO", an(170), CREAM); tx(56, 345, "É REAL", an(170), RED)
d.text((64, 575), "O ICEBERG DAS CONSPIRAÇÕES", font=mq(36), fill=(220, 210, 190))
im.convert("RGB").save("../render/capa-final.jpg", quality=94); print("ok")
