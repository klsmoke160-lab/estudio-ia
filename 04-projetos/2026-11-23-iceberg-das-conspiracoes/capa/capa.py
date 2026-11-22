"""Capa do Iceberg das Conspirações (1280x720): filmagem real de iceberg (Mixkit) com a parte submersa visível,
carimbo "PROVADO" sobre o topo do gelo e frase curta. Sem imagem gerada por IA."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageChops
import pathlib, sys
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s); mq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
CREAM, RED = (246, 241, 230), (232, 30, 40)
src = sys.argv[1] if len(sys.argv) > 1 else "/home/user/mk/ice/quadros/capa_18.5.png"
im = Image.open(src).convert("RGB")
# iceberg para a direita: amplia 18% e desloca
z = 0.98; im = im.resize((int(im.width * z), int(im.height * z)), Image.LANCZOS)
base = Image.new("RGB", (W, H), (8, 22, 30)); base.paste(im.crop((0, 0, W - 300, H)), (300, 0)); im = base
im = ImageEnhance.Contrast(im).enhance(1.25); im = ImageEnhance.Color(im).enhance(1.35); im = ImageEnhance.Sharpness(im).enhance(1.5)
# escurece a esquerda (texto) e o fundo da imagem (a parte "submersa")
mL = Image.new("L", (W, 1)); [mL.putpixel((x, 0), int(250 * max(0, min(1, (720 - x) / 420)))) for x in range(W)]
im = Image.composite(Image.new("RGB", (W, H), (5, 8, 14)), im, mL.resize((W, H)))
mB = Image.new("L", (1, H)); [mB.putpixel((0, y), int(170 * max(0, min(1, (y - 470) / 250)))) for y in range(H)]
im = Image.composite(Image.new("RGB", (W, H), (3, 10, 20)), im, mB.resize((W, H)))
# vinheta
v = Image.new("L", (W, H), 0); ImageDraw.Draw(v).ellipse([-260, -200, W + 260, H + 200], fill=255); v = v.filter(ImageFilter.GaussianBlur(120))
im = Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), v).convert("RGBA")
# carimbo sobre o topo do gelo
st = Image.new("RGBA", (360, 104), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rectangle([5, 5, 355, 99], outline=RED + (235,), width=9); f = an(66); w = sd.textlength("PROVADO", font=f); sd.text(((360 - w) / 2, 6), "PROVADO", font=f, fill=RED + (235,))
st = st.rotate(-9, expand=True, resample=Image.BICUBIC)
sh = Image.new("RGBA", st.size, (0, 0, 0, 0)); sh.putalpha(st.getchannel("A").point(lambda a: a // 2)); sh = sh.filter(ImageFilter.GaussianBlur(6))
im.alpha_composite(sh, (888, 128)); im.alpha_composite(st, (880, 120))
d = ImageDraw.Draw(im)
def tx(x, y, t, f, cor, s=6): d.text((x + s, y + s), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=cor)
tx(62, 70, "O ICEBERG DAS CONSPIRAÇÕES", mq(34), (230, 220, 200), 3)
d.rectangle([62, 122, 230, 128], fill=RED)
tx(56, 150, "O TOPO", an(178), CREAM); tx(52, 352, "É REAL", an(178), RED)
im.convert("RGB").save("../render/capa-final.jpg", quality=95); print("ok")
