"""Capas limpas (1280x720): uma imagem forte, uma frase curta, alto contraste."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
import pathlib
F = pathlib.Path("/home/user/estudio-ia/05-biblioteca/fontes"); W, H = 1280, 720
an = lambda s: ImageFont.truetype(str(F / "font1.ttf"), s); maq = lambda s: ImageFont.truetype(str(F / "font2.ttf"), s)
CREAM, RED, YEL = (244, 238, 226), (230, 36, 44), (255, 214, 10)
def foto(arq, alvo_w, fx=0.5, fy=0.4, zoom=1.0):
    im = ImageOps.grayscale(Image.open(arq)).convert("RGB"); esc = max(alvo_w / im.width, H / im.height) * zoom
    im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
    x = min(max(0, int(im.width * fx - alvo_w / 2)), im.width - alvo_w); y = min(max(0, int(im.height * fy - H / 2)), im.height - H)
    im = im.crop((x, y, x + alvo_w, y + H)); im = ImageEnhance.Contrast(im).enhance(1.35); return ImageEnhance.Sharpness(im).enhance(1.6)
def degrade(tela, x0, x1):
    m = Image.new("L", (W, 1))
    for x in range(W): m.putpixel((x, 0), 255 if x < x0 else 0 if x > x1 else int(255 * (1 - (x - x0) / (x1 - x0))))
    return Image.composite(Image.new("RGB", (W, H), (8, 8, 9)), tela, m.resize((W, H)))
def texto(d, x, y, t, f, cor, sombra=True):
    if sombra: d.text((x + 5, y + 6), t, font=f, fill=(0, 0, 0))
    d.text((x, y), t, font=f, fill=cor)
# A: Johnson + "NÃO HOUVE ATAQUE"
t = Image.new("RGB", (W, H), (8, 8, 9)); p = foto("lbj_un.png", 900, 0.5, 0.35, 1.15); t.paste(p, (W - 900, 0)); t = degrade(t, 380, 700)
d = ImageDraw.Draw(t); texto(d, 56, 118, "NÃO HOUVE", an(150), CREAM); texto(d, 52, 300, "ATAQUE", an(230), RED)
d.rectangle([60, 590, 470, 596], fill=YEL); texto(d, 60, 612, "4 DE AGOSTO DE 1964", maq(40), CREAM, False)
t.save("../render/capa-limpa-A.jpg", quality=94)
# B: a linha do documento com marca-texto, gigante, sobre o navio
t = foto("navio_un.png", W, 0.5, 0.5, 1.0); t = ImageEnhance.Brightness(t).enhance(0.45).filter(ImageFilter.GaussianBlur(1.2))
d = ImageDraw.Draw(t, "RGBA")
f = maq(78); linha = "no attack happened"; w = d.textlength(linha, font=f); x = (W - w) / 2; y = 250
d.rectangle([x - 18, y - 6, x + w + 18, y + 92], fill=(246, 241, 228, 255)); d.rectangle([x - 6, y + 8, x + w + 6, y + 82], fill=(255, 214, 10, 235)); d.text((x, y + 4), linha, font=f, fill=(15, 15, 15))
l2 = "that night."; w2 = d.textlength(l2, font=f); x2 = (W - w2) / 2; y2 = y + 104
d.rectangle([x2 - 18, y2 - 6, x2 + w2 + 18, y2 + 92], fill=(246, 241, 228, 255)); d.rectangle([x2 - 6, y2 + 8, x2 + w2 + 6, y2 + 82], fill=(255, 214, 10, 235)); d.text((x2, y2 + 4), l2, font=f, fill=(15, 15, 15))
for tt, ff, yy, cor in (("A BATALHA QUE NÃO ACONTECEU", an(74), 70, CREAM), ("ESTUDO SECRETO DA NSA · LIBERADO EM 2005", maq(34), 560, (220, 210, 190))):
    ww = d.textlength(tt, font=ff); texto(d, (W - ww) / 2, yy, tt, ff, cor)
t.convert("RGB").save("../render/capa-limpa-B.jpg", quality=94)
print("ok")
