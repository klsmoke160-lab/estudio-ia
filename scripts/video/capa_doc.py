"""Capa de documentário do Rasura (1280×720): frase grande, recorte de documento com marca-texto e carimbo, e a imagem do caso à direita.

Uso: python3 scripts/video/capa_doc.py capa.json saida.jpg
capa.json:
{"imagem": "foto.jpg", "foco": [0.5, 0.35], "zoom": 1.0, "cor": "pb" | "vermelho" | "azul",
 "linhas": [["A CIA QUEIMOU", "creme"], ["QUASE TUDO", "vermelho"]],
 "recorte": {"arq": "pagina.png", "caixa": [x0,y0,x1,y1], "marcas": [[x0,y0,x1,y1], ...], "largura": 560, "giro": -2.5},
 "carimbo": "SENADO, 1977",
 "extra": {"arq": "assinatura.png", "caixa": [...], "largura": 300, "pos": [x, y], "giro": 3}}
As caixas e marcas estão em pixels da página original.
"""
import json, sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

FONTES = pathlib.Path(__file__).resolve().parents[2] / "05-biblioteca/fontes"
ANTON = str(FONTES / "font1.ttf"); MAQ = str(FONTES / "font2.ttf")
W, H = 1280, 720
CORES = {"creme": (242, 235, 221), "vermelho": (227, 38, 46), "amarelo": (255, 214, 10)}

def fundo(c):
    im = Image.open(c["imagem"]).convert("RGB"); fx, fy = c.get("foco", [0.5, 0.4]); z = c.get("zoom", 1.0)
    alvo_w, alvo_h = int(W * 0.66), H      # a imagem ocupa os 2/3 da direita
    esc = max(alvo_w / im.width, alvo_h / im.height) * z
    im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)
    x = min(max(0, int(im.width * fx - alvo_w / 2)), im.width - alvo_w); y = min(max(0, int(im.height * fy - alvo_h / 2)), im.height - alvo_h)
    im = im.crop((x, y, x + alvo_w, y + alvo_h))
    g = ImageOps.grayscale(im); g = ImageOps.autocontrast(g, cutoff=1); g = ImageEnhance.Contrast(g).enhance(1.25)
    tint = {"pb": ((14, 12, 10), (236, 228, 214)), "vermelho": ((18, 4, 4), (240, 120, 110)), "azul": ((3, 10, 18), (150, 210, 235))}[c.get("cor", "pb")]
    im = ImageOps.colorize(g, tint[0], tint[1])
    tela = Image.new("RGB", (W, H), (10, 9, 8)); tela.paste(im, (W - alvo_w, 0))
    # degradê para o texto ler bem à esquerda, e vinheta
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    for x in range(W):
        a = 255 if x < W - alvo_w else max(0, 255 - int(255 * (x - (W - alvo_w)) / (alvo_w * 0.55)))
        d.line([(x, 0), (x, H)], fill=a)
    tela = Image.composite(Image.new("RGB", (W, H), (10, 9, 8)), tela, m)
    vin = Image.new("L", (W, H), 0); ImageDraw.Draw(vin).ellipse((-250, -200, W + 250, H + 200), fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(120))
    return Image.composite(tela, Image.new("RGB", (W, H), (0, 0, 0)), vin)

def texto(tela, linhas):
    d = ImageDraw.Draw(tela); y = 34
    for txt, cor in linhas:
        tam = 150
        while True:
            f = ImageFont.truetype(ANTON, tam); bb = d.textbbox((0, 0), txt, font=f)
            if bb[2] - bb[0] <= 760 or tam < 70: break
            tam -= 4
        sombra = Image.new("RGBA", tela.size, (0, 0, 0, 0)); ImageDraw.Draw(sombra).text((54, y + 8 - bb[1]), txt, font=f, fill=(0, 0, 0, 200))
        tela.paste(sombra.filter(ImageFilter.GaussianBlur(8)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(8)))
        d.text((46, y - bb[1]), txt, font=f, fill=CORES[cor], stroke_width=5, stroke_fill=(0, 0, 0))
        y += (bb[3] - bb[1]) + 22
    return y

def recorte(r):
    pg = Image.open(r["arq"]).convert("RGB"); x0, y0, x1, y1 = r["caixa"]; cr = pg.crop((x0, y0, x1, y1))
    cr = ImageOps.autocontrast(ImageOps.grayscale(cr), cutoff=1).convert("RGB")
    amarelo = Image.new("RGB", cr.size, (255, 255, 255)); da = ImageDraw.Draw(amarelo)
    for a, b, c_, e in r.get("marcas", []):
        da.rectangle((a - x0 - 8, b - y0 - 6, c_ - x0 + 8, e - y0 + 8), fill=CORES["amarelo"])
    from PIL import ImageChops
    cr = ImageChops.multiply(cr, amarelo)
    pad = 18; papel = Image.new("RGB", (cr.width + 2 * pad, cr.height + 2 * pad), (246, 241, 230)); papel.paste(cr, (pad, pad))
    lw = r.get("largura", 560); papel = papel.resize((lw, int(papel.height * lw / papel.width)), Image.LANCZOS)
    return papel

def colar(tela, peca, pos, giro):
    rgba = peca.convert("RGBA").rotate(giro, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", rgba.size, (0, 0, 0, 0)); sh.putalpha(rgba.split()[3].point(lambda v: int(v * 0.75)))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    tela.paste(sh, (pos[0] + 10, pos[1] + 14), sh); tela.paste(rgba, pos, rgba)
    return rgba.size

def carimbo(txt):
    f = ImageFont.truetype(MAQ, 40); d = ImageDraw.Draw(Image.new("RGB", (1, 1))); bb = d.textbbox((0, 0), txt, font=f)
    w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 30
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w - 1, h - 1), fill=(246, 241, 230, 255), outline=CORES["vermelho"], width=5)
    d.text((20, 15 - bb[1]), txt, font=f, fill=CORES["vermelho"]); return im

if __name__ == "__main__":
    c = json.load(open(sys.argv[1])); tela = fundo(c)
    if "extra" in c:
        e = c["extra"]; pg = Image.open(e["arq"]).convert("RGB").crop(e["caixa"])
        pg = ImageOps.autocontrast(ImageOps.grayscale(pg), cutoff=1).convert("RGB")
        pg = pg.resize((e["largura"], int(pg.height * e["largura"] / pg.width)), Image.LANCZOS)
        colar(tela, pg, tuple(e["pos"]), e.get("giro", 0))
    yt = texto(tela, c["linhas"])
    if "recorte" in c:
        r = c["recorte"]; p = recorte(r); y = max(yt + 10, r.get("y", 0)); tam = colar(tela, p, (40, y), r.get("giro", -2.5))
        if c.get("carimbo"):
            s = carimbo(c["carimbo"]); colar(tela, s, (40 + tam[0] - s.width - 10, y + tam[1] - 28), -4)
    ImageDraw.Draw(tela).rectangle((0, H - 10, W, H), fill=CORES["vermelho"])
    tela.save(sys.argv[2], quality=93); print("ok", sys.argv[2])
