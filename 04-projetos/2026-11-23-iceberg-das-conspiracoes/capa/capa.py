"""Capa do Iceberg das Conspirações (1280x720): foto real de iceberg (Mixkit), carimbo e frase curta."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pathlib
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s); mq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
CREAM, RED = (244, 238, 226), (230, 36, 44)
im = Image.open("/home/user/mk/ice/quadros/mx25244_25.png").convert("RGB").resize((W, H), Image.LANCZOS)
im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(0.8)).enhance(1.15)
g = Image.new("L", (W, 1))
for x in range(W): g.putpixel((x, 0), int(235 * max(0, min(1, (700 - x) / 520))))
im = Image.composite(Image.new("RGB", (W, H), (6, 8, 12)), im, g.resize((W, H)))
im = im.convert("RGBA")
st = Image.new("RGBA", (330, 92), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.rectangle([4, 4, 326, 88], outline=RED, width=7)
f = an(56); w = sd.textlength("PROVADO", font=f); sd.text(((330 - w) / 2, 6), "PROVADO", font=f, fill=RED)
st = st.rotate(-8, expand=True, resample=Image.BICUBIC); im.alpha_composite(st, (860, 70))
d = ImageDraw.Draw(im)
def tx(x, y, t, f, cor): d.text((x + 5, y + 6), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=cor)
tx(60, 150, "O TOPO", an(170), CREAM); tx(56, 345, "É REAL", an(170), RED)
tx(64, 575, "O ICEBERG DAS CONSPIRAÇÕES", mq(36), (225, 215, 195))
im.convert("RGB").save("../render/capa-final.jpg", quality=94); print("ok")
