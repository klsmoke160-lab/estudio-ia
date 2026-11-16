"""Short vertical (1080x1920) a partir de um trecho do vídeo final de um documentário do Rasura.
Uso: python3 scripts/video/short_doc.py <projeto> <video_16x9> <inicio> <fim> <saida.mp4> "GANCHO LINHA 1" "GANCHO LINHA 2" [--cinema]
--cinema: o vídeo tem faixas pretas de 133 px (o recorte pega só a imagem).
Legenda grande gerada da linha do tempo da narração (audio/timeline_novo.json); marca Rasura no topo; cartão final de 2,2 s."""
import json, subprocess, sys, pathlib, math
from PIL import Image, ImageDraw, ImageFont
P=pathlib.Path(sys.argv[1]).resolve(); FON=pathlib.Path(__file__).resolve().parents[2]/"05-biblioteca/fontes"
VID,A,B,OUT,G1,G2=sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),sys.argv[5],sys.argv[6],sys.argv[7]; CINE="--cinema" in sys.argv
TMP=pathlib.Path("/tmp/short_tmp_"+pathlib.Path(OUT).stem); TMP.mkdir(exist_ok=True)
ANTON=str(FON/"font1.ttf"); MAQ=str(FON/"font2.ttf")
CREAM=(236,230,214); RED=(226,51,59); YEL=(244,224,77)
anton=lambda s:ImageFont.truetype(ANTON,s); maq=lambda s:ImageFont.truetype(MAQ,s)
def risco(d,x0,x1,y,esp,tilt=-1.6):
    dy=math.tan(math.radians(tilt))*(x1-x0); d.line([(x0,y),(x1,y+dy)],fill=RED,width=esp); r=esp//2
    for cx,cy in ((x0,y),(x1,y+dy)): d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=RED)
def centro(d,y,t,f,fill,stroke=0):
    w=d.textlength(t,font=f); d.text(((1080-w)/2,y),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0)); return w
# camada fixa: marca + gancho
L=Image.new("RGBA",(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(L)
f=anton(70); w=d.textlength("RASURA",font=f); x=(1080-w)/2; d.text((x,120),"RASURA",font=f,fill=CREAM); bb=d.textbbox((x,120),"RASURA",font=f)
risco(d,x-12,x+w+12,(bb[1]+bb[3])//2,9)
def caber(t,s=104):
    while d.textlength(t,font=anton(s))>1000: s-=4
    return anton(s)
centro(d,250,G1,caber(G1),CREAM,4)
centro(d,375,G2,caber(G2),RED,4)
L.save(TMP/"camada.png")
# cartão final
E=Image.new("RGB",(1080,1920),(10,10,10)); d=ImageDraw.Draw(E)
centro(d,640,"VÍDEO COMPLETO",anton(120),CREAM)
centro(d,790,"NO CANAL",anton(80),(216,208,190))
f=anton(190); w=d.textlength("RASURA",font=f); x=(1080-w)/2; d.text((x,900),"RASURA",font=f,fill=CREAM); bb=d.textbbox((x,900),"RASURA",font=f)
risco(d,x-16,x+w+16,(bb[1]+bb[3])//2,18)
centro(d,1180,"histórias investigadas a partir de documentos",maq(36),(216,208,190))
E.save(TMP/"fim.png")
# legenda: blocos de até 3 palavras / 20 letras, no tempo de cada palavra
F=json.load(open(P/"audio/timeline_novo.json"))["frases"]; blocos=[]
for f in F:
    if f["fim"]<=A or f["ini"]>=B: continue
    pal=f["texto"].split(); ts=f["t"]; i=0
    while i<len(pal):
        j=i+1
        while j<len(pal) and j-i<3 and len(" ".join(pal[i:j+1]))<=20: j+=1
        ini=ts[i]-0.05; fim=ts[j]-0.05 if j<len(pal) else f["fim"]+0.15
        blocos.append((max(A,ini)-A,min(B,fim)-A," ".join(pal[i:j]).upper())); i=j
dt=[]
for n,(a,b,t) in enumerate(blocos):
    tf=TMP/f"l{n:03d}.txt"; tf.write_text(t)
    dt.append(f"drawtext=fontfile={ANTON}:textfile={tf}:fontsize=84:fontcolor=0xECE6D6:borderw=7:bordercolor=black:x=(w-text_w)/2:y=1430:enable='between(t,{a:.3f},{b:.3f})'")
D=B-A; FIM=2.2
RECORTE="[b]crop=1920:814:0:133,scale=2030:860,crop=1080:860[fg];" if CINE else "[b]crop=1920:810:0:110,scale=2039:860,crop=1080:860[fg];"
fc=(f"[0:v]trim={A}:{B},setpts=PTS-STARTPTS,fps=24,split[a][b];"
    f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:2,eq=brightness=-0.25[bg];"
    f"{RECORTE}"
    f"[bg][fg]overlay=0:520[v1];[v1][1:v]overlay=0:0:shortest=1,{','.join(dt)},fade=t=out:st={D-0.25:.2f}:d=0.25,setsar=1,format=yuv420p[v2];"
    f"[2:v]trim=0:{FIM},setpts=PTS-STARTPTS,fps=24,setsar=1,format=yuv420p,fade=t=in:d=0.2[v3];"
    f"[0:a]atrim={A}:{B},asetpts=PTS-STARTPTS,afade=t=out:st={D-0.5:.2f}:d=0.5[a1];"
    f"anullsrc=r=48000:cl=stereo,atrim=0:{FIM}[a2];"
    f"[v2][a1][v3][a2]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",VID,"-loop","1","-t",f"{D:.3f}","-i",str(TMP/"camada.png"),"-loop","1","-t",f"{FIM:.3f}","-i",str(TMP/"fim.png"),
    "-filter_complex",fc,"-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
    "-c:a","aac","-b:a","192k","-movflags","+faststart",OUT],check=True)
print("ok",OUT,len(blocos),"blocos de legenda")
