"""Capa 1280x720 a partir de um quadro do vídeo. Uso: uv run python capa/capa.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import pathlib
p=pathlib.Path(__file__).parent; W,H=1280,720
im=Image.open(p/"base.png").convert("RGB").resize((W,H),Image.LANCZOS)
im=ImageEnhance.Contrast(im).enhance(1.25); im=ImageEnhance.Color(im).enhance(1.15)
# cobertura escura à esquerda (leitura do texto) e vinheta
ov=Image.new("L",(W,H),0); d=ImageDraw.Draw(ov)
for x in range(W): d.line([(x,0),(x,H)],fill=int(235*max(0,1-x/(W*0.78))**1.15))
im=Image.composite(Image.new("RGB",(W,H),(4,6,8)),im,ov)
vg=Image.new("L",(W,H),0); ImageDraw.Draw(vg).ellipse([-W*.25,-H*.35,W*1.25,H*1.35],fill=255); vg=vg.filter(ImageFilter.GaussianBlur(120))
im=Image.composite(im,Image.new("RGB",(W,H),(0,0,0)),vg)
# brilho vermelho na parte inferior
glow=Image.new("RGB",(W,H),(170,18,26)); m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rectangle([0,H-120,W,H],fill=120); m=m.filter(ImageFilter.GaussianBlur(70))
im=Image.composite(glow,im,m)
A=ImageFont.truetype(str(p.parent/"motor"/"font1.ttf"),150); B=ImageFont.truetype(str(p.parent/"motor"/"font1.ttf"),52); C=ImageFont.truetype(str(p.parent/"motor"/"font2.ttf"),30)
d=ImageDraw.Draw(im)
def sombra(xy,t,f,fill,off=4):
    x,y=xy; d.text((x+off,y+off),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=fill)
sombra((60,150),"A NÉVOA",A,(240,235,220)); sombra((60,290),"DE 1950",A,(226,51,59))
sombra((60,480),"A CIDADE QUE VIROU",B,(236,230,214),3); sombra((60,540),"UM EXPERIMENTO SECRETO",B,(236,230,214),3)
sombra((62,640),"SÃO FRANCISCO · SETEMBRO DE 1950",C,(190,184,170),2)
im.save(p/"capa-nevoa-1950.jpg",quality=92); print(p/"capa-nevoa-1950.jpg")
