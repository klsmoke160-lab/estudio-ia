"""Filma uma página de documento como plano de cinema: câmera que se aproxima do trecho e marca-texto que corre pelas linhas.
Gera quadros com PIL e manda para o ffmpeg (tratamento: contraste, vinheta, grão)."""
import subprocess, math, sys
from PIL import Image, ImageDraw, ImageChops, ImageFilter
W,H,FPS=1920,1080,24
ease=lambda x: (lambda t:t*t*(3-2*t))(min(1,max(0,x)))
def render_doc(page,out,dur,boxes=None,t_marca=None,foco=None,extra_vf=None,zoom_fim=None,marca_dur=0.55):
    """page: caminho da imagem; boxes: [[l,t,r,b],...] em pixels da página; t_marca: segundo em que o marca-texto começa;
    foco: (cx,cy,largura) final da câmera em pixels da página (se não houver boxes)."""
    im=Image.open(page).convert("RGB"); pw,ph=im.size; PAD=int(max(pw,ph)*1.2)
    cv=Image.new("RGB",(pw+2*PAD,ph+2*PAD),(9,8,7))
    sh=Image.new("L",cv.size,0); ImageDraw.Draw(sh).rectangle([PAD+18,PAD+26,PAD+pw+18,PAD+ph+26],fill=150); sh=sh.filter(ImageFilter.GaussianBlur(40))
    cv.paste((0,0,0),mask=sh); cv.paste(im,(PAD,PAD))
    # enquadramentos (em coordenadas do canvas)
    h0=ph*0.86; w0=h0*16/9; c0=(PAD+pw/2,PAD+ph/2)
    if boxes:
        l=min(b[0] for b in boxes); t=min(b[1] for b in boxes); r=max(b[2] for b in boxes); b_=max(b[3] for b in boxes)
        w1=max((r-l)*1.28,(b_-t)*2.4*16/9,pw*0.62); c1=(PAD+(l+r)/2,PAD+(t+b_)/2)
    elif foco: c1=(PAD+foco[0],PAD+foco[1]); w1=foco[2]
    else: c1=(PAD+pw/2,PAD+ph*0.36); w1=w0*(zoom_fim or 0.62)
    nf=round(dur*FPS); tm=t_marca if t_marca is not None else dur*0.38
    vf=["eq=contrast=1.24:brightness=-0.08:saturation=1.35","colorbalance=rs=0.04:gs=0.03:bs=-0.10:rm=0.06:gm=0.04:bm=-0.12","vignette=angle=PI/3.2","noise=alls=9:allf=t+u"]+(extra_vf or [])+["format=yuv420p"]
    ff=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-vf",",".join(vf),
        "-frames:v",str(nf),"-c:v","libx264","-preset","veryfast","-crf","22","-video_track_timescale","12288",out],stdin=subprocess.PIPE)
    for f in range(nf):
        t=f/FPS; k=ease(t/min(dur*0.42,3.2)); drift=1-0.035*(t/dur)
        w=(w0+(w1-w0)*k)*drift; h=w*9/16
        cx=c0[0]+(c1[0]-c0[0])*k+6*math.sin(t*0.6); cy=c0[1]+(c1[1]-c0[1])*k+4*math.sin(t*0.47+1)
        fr=cv.transform((W,H),Image.EXTENT,(cx-w/2,cy-h/2,cx+w/2,cy+h/2),Image.BICUBIC)
        if boxes and t>=tm-0.4:
            s=W/w; dim=ease((t-(tm-0.4))/0.8); g=int(255-70*dim)
            lay=Image.new("RGB",(W,H),(g,g,g)); d=ImageDraw.Draw(lay)
            for i,(l,tp,r,bt) in enumerate(boxes):
                p=ease((t-tm-i*marca_dur*0.8)/marca_dur)
                x0=(PAD+l-cx+w/2)*s; y0=(PAD+tp-cy+h/2)*s; x1=(PAD+r-cx+w/2)*s; y1=(PAD+bt-cy+h/2)*s; padx=8*s/1.2; pady=5*s/1.2
                d.rectangle([x0-padx,y0-pady,x1+padx,y1+pady],fill=(255,255,255))          # tira o escurecimento da linha
                if p>0: d.rectangle([x0-padx,y0-pady,x0-padx+(x1-x0+2*padx)*p,y1+pady],fill=(255,222,70))
            fr=ImageChops.multiply(fr,lay.filter(ImageFilter.GaussianBlur(1.2)))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
if __name__=="__main__":
    sys.path.insert(0,"/home/user/escola"); import achar
    n,_,bx,_=achar.find("countryschooloft00gates","In our dream","molding hand")
    render_doc("/home/user/escola/full/gates_006.jpg","/tmp/doc_teste.mp4",8,boxes=bx,t_marca=3.4)
