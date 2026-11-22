"""Capa do Iceberg das Conspirações (1280x720): foto real da NASA, "Iceberg in North Star Bay, Greenland"
(Operation IceBridge, Jeremy Harbeck/NASA Goddard, 2015), carimbo "PROVADO" no topo do iceberg e frase curta. Sem IA."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import pathlib
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s); mq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
CREAM, RED = (246, 241, 230), (232, 30, 40)
src = Image.open("/home/user/mk/ice/nasa/ice/GSFC_20171208_Archive_e000736.jpg").convert("RGB")
sw, sh = src.size; ch = int(sw * H / W); y0 = int(sh * 0.30); y0 = min(y0, sh - ch)
foto = src.crop((0, y0, sw, y0 + ch)).resize((W, H), Image.LANCZOS)
foto = ImageEnhance.Brightness(foto).enhance(1.25)
DX = 300   # empurra o iceberg para a direita; à esquerda fica o céu, com a cor do próprio céu da foto
ceu = foto.crop((0, 0, 60, H)).resize((1, H)).resize((DX + 220, H))
im = Image.new("RGB", (W, H)); im.paste(ceu, (0, 0))
m = Image.new("L", (W - DX, 1)); [m.putpixel((x, 0), int(255 * min(1, x / 220))) for x in range(W - DX)]
im.paste(foto.crop((0, 0, W - DX, H)), (DX, 0), m.resize((W - DX, H)))
im = ImageEnhance.Contrast(im).enhance(1.15); im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Sharpness(im).enhance(1.3)
mL = Image.new("L", (W, 1)); [mL.putpixel((x, 0), int(200 * max(0, min(1, (560 - x) / 420)))) for x in range(W)]
im = Image.composite(Image.new("RGB", (W, H), (4, 6, 14)), im, mL.resize((W, H)))
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-240, -180, W + 240, H + 180], fill=255); v = v.filter(ImageFilter.GaussianBlur(110))
im = Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), v).convert("RGBA")
st = Image.new("RGBA", (330, 96), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rectangle([5, 5, 325, 91], outline=RED + (240,), width=8); f = an(60); w = sd.textlength("PROVADO", font=f); sd.text(((330 - w) / 2, 6), "PROVADO", font=f, fill=RED + (240,))
st = st.rotate(-9, expand=True, resample=Image.BICUBIC)
sh2 = Image.new("RGBA", st.size, (0, 0, 0, 0)); sh2.putalpha(st.getchannel("A").point(lambda a: a // 2)); sh2 = sh2.filter(ImageFilter.GaussianBlur(6))
SX, SY = 830, 300
im.alpha_composite(sh2, (SX + 8, SY + 8)); im.alpha_composite(st, (SX, SY))
d = ImageDraw.Draw(im)
def tx(x, y, t, f, cor, s=6): d.text((x + s, y + s), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=cor)
tx(62, 70, "O ICEBERG DAS CONSPIRAÇÕES", mq(34), (230, 220, 200), 3); d.rectangle([62, 122, 230, 128], fill=RED)
tx(56, 150, "O TOPO", an(178), CREAM); tx(52, 352, "É REAL", an(178), RED)
im.convert("RGB").save("../render/capa-final.jpg", quality=95); print("ok")
