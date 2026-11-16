"""Motor de documentário do estúdio (Rasura): monta um vídeo a partir da narração alinhada e de um plano.
Uso: python3 scripts/video/doc_motor.py <projeto> edl | render [n ...] | juntar | som | final
O projeto precisa de audio/timeline_novo.json, narracao/narracao_tratada.wav e motor/plano.py, que define:
RAW (filmes), CENAS (cortes por filme), D (documentos), FOTOS, R (regras por frase), POOL (por capítulo), KEY (rótulos),
CARDS (cartões de tela cheia), LISTA (lista que cresce), TITULO, ESTILO, NOMES_CAP (opcional)."""
import json, re, subprocess, sys, pathlib, itertools, os, unicodedata, importlib.util, concurrent.futures as cf
AQUI=pathlib.Path(__file__).resolve().parent; sys.path.insert(0,str(AQUI))
import doc_plano as doc
P=pathlib.Path(sys.argv[1]).resolve(); FPS=24
spec=importlib.util.spec_from_file_location("plano",P/"motor/plano.py"); PL=importlib.util.module_from_spec(spec); spec.loader.exec_module(PL)
FONT=AQUI.parents[1]/"05-biblioteca/fontes"; ANTON=FONT/"font1.ttf"; ELITE=FONT/"font2.ttf"; SERIF=FONT/"serif.ttf"; SANS=FONT/"sans.ttf"
OUT=P/"render/doc"; SEG=OUT/"segs"; SEG.mkdir(parents=True,exist_ok=True); TXT=OUT/"txt"; TXT.mkdir(exist_ok=True)
T=json.load(open(P/"audio/timeline_novo.json")); F=T["frases"]; TOTAL=T["total"]
E=getattr(PL,"ESTILO",{}); CINE=E.get("cinema",False); BAR=133 if CINE else 0; DUR_PLANO=E.get("dur_plano",3.0); TINT=E.get("tint",{})
def _norm(x): return re.sub(r"[^a-z0-9 ]","",unicodedata.normalize("NFD",x.lower()).encode("ascii","ignore").decode())
def esc(p): return str(p).replace(":","\\:")
def tf(txt):
    f=TXT/f"o{abs(hash(txt))%10**9}.txt"; f.write_text(txt); return esc(f)
def t_palavra(f,trecho):
    """instante em que começa `trecho` dentro da frase f"""
    if trecho not in f["texto"] or not f.get("t"): return f["ini"]
    ix=len(_norm(f["texto"].split(trecho)[0]).split()); return f["t"][min(ix,len(f["t"])-1)]
def shot_src(film,t,need):
    c=PL.CENAS[film]; a=max(x for x in c if x<=t); b=min(x for x in c if x>t); a+=0.25; b-=0.25; L=b-a
    if L>=need: s=min(max(t-need/2,a),b-need); return s,need,1.0
    if L>=need/1.8: return a,L,need/L
    return max(0,t-need/2),need,1.0
def build():
    cyc={k:itertools.cycle(v) for k,v in PL.POOL.items()}; shots=[]; ov=[]; cap=None; ncap=0; lista=[]
    for n,f in enumerate(F):
        txt=f["texto"]; ini=0.0 if n==0 else f["ini"]-0.12; nxt=F[n+1]["ini"]-0.12 if n+1<len(F) else TOTAL; end=f.get("titulo_ini",nxt)
        if f["cap"]!=cap:
            if lista: [o.__setitem__("b",f["ini"]-2.2) for o in lista]; lista=[]
            cap=f["cap"]
            if n>0:
                ncap+=1; nome=getattr(PL,"NOMES_CAP",{}).get(cap,cap); ult=(n==max(i for i,x in enumerate(F) if x["cap"]!=F[i-1]["cap"] or i==0))
                ov.append(dict(tipo="cap",txt=nome,num=("FINAL" if cap==F[-1]["cap"] else f"PARTE {ncap}"),a=f["ini"]-1.8,b=f["ini"]-0.05))
        for k,word in getattr(PL,"KEY",[]):
            if k in txt:
                ka=t_palavra(f,k)-0.2; ov.append(dict(tipo="key",txt=word,a=max(0,ka),b=min(max(f["fim"]+0.4,ka+2.5),ka+4.5)))
        for k,word,estilo in getattr(PL,"CARDS",[]):
            if txt.strip()==k: ov.append(dict(tipo="card",txt=word,estilo=estilo,a=f["ini"]-0.45,b=f["fim"]+0.5))
        for k,word in getattr(PL,"LISTA",[]):
            if k in txt:
                o=dict(tipo="lista",txt=word,a=t_palavra(f,k)-0.1,b=TOTAL,i=len(lista)); lista.append(o); ov.append(o)
        if not any(o["tipo"]=="card" and o["a"]<f["fim"] and o["b"]>f["ini"] for o in ov):
            pal=txt.split(); ch=[" ".join(pal[i:i+7]) for i in range(0,len(pal),7)]; tot=sum(len(c) for c in ch); t0=f["ini"]
            for c in ch:
                dd=(f["fim"]-f["ini"])*len(c)/tot; ov.append(dict(tipo="leg",txt=c,a=t0,b=t0+dd)); t0+=dd
        rule=next((r for s,r in PL.R if s in txt),None); D_=end-ini
        plan=list(rule) if rule else [next(cyc[cap]) for _ in range(max(1,round(D_/DUR_PLANO)))]
        while len(plan)>1 and D_/len(plan)<(2.4 if any(x[0]=="doc" for x in plan) else 1.5): plan.pop()
        for j,sp in enumerate(plan):
            a=ini+D_*j/len(plan); b=ini+D_*(j+1)/len(plan); s=dict(tipo=sp[0],a=a,b=b,cap=cap,par=len(shots)%2==0)
            if sp[0]=="clip": s.update(film=sp[1],t=sp[2])
            else: s.update(k=sp[1])
            shots.append(s)
        if "titulo_ini" in f:
            shots.append(dict(tipo=PL.TITULO[2][0],k=PL.TITULO[2][1],a=f["titulo_ini"],b=nxt,cap=cap,titulo=True,par=True))
            ov.append(dict(tipo="titulo",txt=PL.TITULO[0],sub=PL.TITULO[1],a=f["titulo_ini"]+0.4,b=nxt-1.95))
    for s in shots: s["fa"]=round(s["a"]*FPS); s["fb"]=round(s["b"]*FPS)
    shots=[s for s in shots if s["fb"]>s["fa"]]
    ov.append(dict(tipo="aviso",txt="FILMES DE ARQUIVO ILUSTRATIVOS · DOCUMENTOS ORIGINAIS",a=1.0,b=7.0))
    return shots,ov
def overlays(s,ov):
    a0=s["fa"]/FPS; b0=s["fb"]/FPS; fl=[]; yl=f"h-{96 if CINE else 150}"
    for o in sorted(ov,key=lambda o:{"lista":0,"leg":1,"key":2,"aviso":3,"cap":4,"titulo":5,"card":6}[o["tipo"]]):
        if o["b"]<=a0 or o["a"]>=b0: continue
        a=o["a"]-a0; b=o["b"]-a0
        al=f"if(lt(t\\,{a:.3f})\\,0\\,if(lt(t\\,{a+0.15:.3f})\\,(t-{a:.3f})/0.15\\,if(lt(t\\,{b-0.3:.3f})\\,1\\,max(0\\,({b:.3f}-t)/0.3))))"
        en=f"enable='between(t,{a:.3f},{b:.3f})'"; tp=o["tipo"]
        ia,ib=max(o["a"],a0),min(o["b"],b0)   # só conta cobertura dentro deste plano
        cob=any(x["tipo"] in("cap","titulo","card") and x["a"]<ib and x["b"]>ia for x in ov)
        if tp=="cap":
            fs=150 if len(o["txt"])<20 else (112 if len(o["txt"])<30 else 84)
            fl+=[f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.80:t=fill:{en}",
                 f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['num'])}:fontsize=40:fontcolor=0xD8D2C2:x=(w-text_w)/2:y=h/2-{fs}*0.9:alpha='{al}'",
                 f"drawtext=fontfile={esc(ANTON)}:textfile={tf(o['txt'])}:fontsize={fs}:fontcolor=0xECE6D6:x=(w-text_w)/2:y=(h-text_h)/2+10:alpha='{al}':shadowcolor=black@0.8:shadowx=4:shadowy=5",
                 f"drawbox=x=(iw-420)/2:y=ih/2+{fs}*0.72:w=420:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.2:.3f},{b-0.2:.3f})'"]
        elif tp=="titulo":
            fl+=[f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.74:t=fill:{en}",
                 f"drawtext=fontfile={esc(ANTON)}:textfile={tf(o['txt'])}:fontsize={170 if len(o['txt'])<22 else 120}:fontcolor=0xECE6D6:x=(w-text_w)/2:y=(h-text_h)/2-60:alpha='{al}':shadowcolor=black@0.8:shadowx=5:shadowy=6",
                 f"drawbox=x=(iw-760)/2:y=ih/2+70:w=760:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.3:.3f},{b-0.2:.3f})'",
                 f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['sub'])}:fontsize=40:fontcolor=0xD8D2C2:x=(w-text_w)/2:y=h/2+120:alpha='{al}'"]
        elif tp=="card":
            fonte,cor,fs={"vermelho":(ELITE,"0xE2333B",150),"amarelo":(ELITE,"0xF4E04D",130),"branco":(SERIF,"0xF2EEE4",170)}[o["estilo"]]
            jit=f"+3*sin(t*37)" if o["estilo"]=="vermelho" else ""
            fl+=[f"drawbox=x=0:y=0:w=iw:h=ih:color=black@1:t=fill:{en}",
                 f"drawtext=fontfile={esc(fonte)}:textfile={tf(o['txt'])}:fontsize={fs}:fontcolor={cor}:x=(w-text_w)/2{jit}:y=(h-text_h)/2:enable='between(t,{a+0.4:.3f},{b-0.05:.3f})'"]
        elif tp=="leg":
            if cob: continue
            fl.append(f"drawtext=fontfile={esc(SANS)}:textfile={tf(o['txt'])}:fontsize=40:fontcolor=0xF4E04D:x=(w-text_w)/2:y={yl}:borderw=3:bordercolor=black@0.85:{en}")
        elif tp=="key":
            if cob: continue
            fs=96 if len(o["txt"])<14 else (72 if len(o["txt"])<24 else 54)
            fl+=[f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['txt'])}:fontsize={fs}:fontcolor=white:x=110:y={110+BAR}:alpha='{al}':shadowcolor=black@0.9:shadowx=3:shadowy=4:borderw=2:bordercolor=black@0.5",
                 f"drawbox=x=112:y={110+BAR}+{fs}*1.25:w=140:h=6:color=0xE2333B@0.95:t=fill:enable='between(t,{a+0.15:.3f},{b-0.3:.3f})'"]
        elif tp=="lista":
            if cob: continue
            fl.append(f"drawbox=x=70:y={122+BAR+o['i']*54}:w=760:h=50:color=black@0.72:t=fill:enable='between(t,{a:.3f},{b:.3f})'")
            fl.append(f"drawtext=fontfile={esc(ELITE)}:textfile={tf('· '+o['txt'])}:fontsize=38:fontcolor=0xF2EEE4:x=90:y={130+BAR+o['i']*54}:alpha='min(1\\,max(0\\,(t-{a:.3f})/0.25))':shadowcolor=black@0.95:shadowx=2:shadowy=3:borderw=2:bordercolor=black@0.6:{en}")
        else:
            fl.append(f"drawtext=fontfile={esc(ELITE)}:textfile={tf(o['txt'])}:fontsize=26:fontcolor=0xD8D2C2:x=w-text_w-70:y={64+BAR}:alpha='{al}':shadowcolor=black@0.9:shadowx=2:shadowy=2")
    return fl
MIX={"vermelho":"rr=1.2:gr=0:br=0:rg=0.15:gg=0.05:bg=0:rb=0.1:gb=0:bb=0.05","petroleo":"rr=0.1:gr=0.8:br=0.75:rg=0:gg=0.15:bg=0.1:rb=0:gb=0:bb=0.15","ambar":"rr=1.1:gr=0.7:br=0.2:rg=0.1:gg=0.1:bg=0:rb=0:gb=0:bb=0.05",
     "verde":"rr=0.25:gr=0.95:br=0.45:rg=0.05:gg=0.15:bg=0.05:rb=0:gb=0:bb=0.1","azul":"rr=0.15:gr=0.45:br=1.1:rg=0:gg=0.1:bg=0.2:rb=0:gb=0:bb=0.2"}
def grade(s,n):
    if TINT:
        c=TINT.get(s["cap"],"petroleo")
        return ["hue=s=0",f"eq=contrast=1.45:brightness={E.get('brilho',-0.10)}:gamma=0.85",f"colorchannelmixer={MIX[c]}"]
    pal=n%4
    if pal==1: return ["hue=s=0","eq=contrast=1.35:brightness=-0.05","colorchannelmixer=rr=0.95:gr=0.85:br=0.35:rg=0.05:gg=0.15:bg=0.05:rb=0:gb=0:bb=0.15","eq=saturation=1.4"]
    if pal==3: return ["hue=s=0","eq=contrast=1.35:brightness=-0.06","colorchannelmixer=rr=0.55:gr=0.85:br=0.70:rg=0.05:gg=0.15:bg=0.20:rb=0:gb=0:bb=0.10","eq=saturation=1.3"]
    return ["hue=s=0","eq=contrast=1.32:brightness=-0.05:gamma=0.9","colorchannelmixer=rr=1.0:gr=0.80:br=0.45:rg=0.0:gg=0.12:bg=0.05:rb=0:gb=0:bb=0.12","eq=saturation=1.5"]
def fim_vf(s,n,d,extra,novo_cap):
    vf=[]
    if CINE: vf+=[f"drawbox=x=0:y=0:w=iw:h={BAR}:color=black:t=fill",f"drawbox=x=0:y=ih-{BAR}:w=iw:h={BAR}:color=black:t=fill"]
    vf+=extra
    if E.get("nasce") and novo_cap: vf.append(f"fade=t=in:st=0:d={min(d*0.8,E['nasce']):.2f}")
    return vf
def render_one(args):
    n,s,ov,last,novo_cap=args; out=SEG/f"s{n:04d}.mp4"; d=(s["fb"]-s["fa"])/FPS; nf=s["fb"]-s["fa"]; extra=fim_vf(s,n,d,overlays(s,ov),novo_cap)
    if last: extra.append(f"fade=t=out:st={max(0,d-1.2):.3f}:d=1.2")
    vig="vignette=angle=PI/2.7" if CINE else "vignette=angle=PI/3.3"
    if s["tipo"]=="doc":
        arq,hl,foco,fonte=PL.D[s["k"]]; boxes=hl
        from PIL import Image
        pw,ph=Image.open(arq).size; fc=(foco[0]*pw,foco[1]*ph,foco[2]*pw*1.38) if foco else None
        tem=any(o["tipo"] in("key","cap","titulo","card","lista") and o["a"]<s["b"] and o["b"]>s["a"] for o in ov)
        if fonte and not tem and not s.get("titulo") and s["a"]>7.5:
            extra=[f"drawtext=fontfile={esc(ELITE)}:textfile={tf(fonte)}:fontsize=28:fontcolor=0xD8D2C2@0.92:x=80:y={56+BAR}:shadowcolor=black@0.9:shadowx=2:shadowy=2:alpha='min(1\\,t/0.5)'"]+extra
        if TINT: extra=grade(s,n)+extra
        doc.render_doc(str(arq),str(out),d,boxes=boxes,t_marca=min(d*0.3,2.2) if boxes else None,foco=fc,extra_vf=extra,marca_dur=0.5)
        return n,0,""
    zr=E.get("zoom",0.06); z=f"(1+{zr}*t/{d:.3f})" if s["par"] else f"({1+zr}-{zr}*t/{d:.3f})"
    if s["tipo"]=="foto":
        arq,fy,fonte=PL.FOTOS[s["k"]]
        if fonte and not any(o["tipo"] in("key","cap","titulo","card","lista") and o["a"]<s["b"] and o["b"]>s["a"] for o in ov):
            extra=[f"drawtext=fontfile={esc(ELITE)}:textfile={tf(fonte)}:fontsize=26:fontcolor=0xD8D2C2@0.92:x=80:y=h-{60+BAR}:shadowcolor=black@0.9:shadowx=2:shadowy=2"]+extra
        from PIL import Image
        im=Image.open(arq).convert("RGB"); iw,ih=im.size; zr_=E.get("zoom",0.06)
        if iw/ih>16/9: ch=ih; cw=ih*16/9
        else: cw=iw; ch=iw*9/16
        x0=(iw-cw)/2; y0=(ih-ch)*fy
        cru=s["k"].startswith(("d_","painel"))   # esquemas feitos por nós: sem tratamento de cor
        vf=(["noise=alls=6:allf=t+u"] if cru else [*grade(s,n),vig,"noise=alls=7:allf=t+u"])+extra+["format=yuv420p"]
        ff=subprocess.Popen(["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-vf",",".join(vf),"-frames:v",str(nf),
            "-c:v","libx264","-preset","veryfast","-crf","23","-video_track_timescale","12288",str(out)],stdin=subprocess.PIPE)
        for k in range(nf):
            u=k/max(1,nf-1); zz=(1+zr_*u) if s["par"] else (1+zr_-zr_*u); w=cw/zz; h=ch/zz; cx=x0+cw/2; cy=y0+ch/2
            ff.stdin.write(im.transform((1920,1080),Image.EXTENT,(cx-w/2,cy-h/2,cx+w/2,cy+h/2),Image.BICUBIC).tobytes())
        ff.stdin.close(); ff.wait(); return n,ff.returncode,""
    else:
        ss,L,slow=shot_src(s["film"],s["t"],d)
        vf=[f"setpts=(PTS-STARTPTS)*{slow:.4f}",f"fps={FPS}","hqdn3d=3:3:6:6",
            f"scale=w='2*trunc(960*{z})':h='2*trunc(720*{z})':eval=frame:flags=lanczos","crop=1920:1080:(iw-1920)/2:(ih-1080)*0.42",
            *grade(s,n),"unsharp=5:5:0.7",vig,"noise=alls=10:allf=t+u"]+extra+["format=yuv420p"]
        cmd=["ffmpeg","-loglevel","error","-y","-ss",f"{ss:.3f}","-t",f"{L+0.2:.3f}","-i",str(PL.RAW[s["film"]]),"-an","-vf",",".join(vf),"-frames:v",str(nf),"-r",str(FPS),
             "-c:v","libx264","-preset","veryfast","-crf","23","-video_track_timescale","12288",str(out)]
    r=subprocess.run(cmd,capture_output=True,text=True); return n,r.returncode,r.stderr[-300:]
if __name__=="__main__":
    modo=sys.argv[2]
    if modo in("edl","render"):
        shots,ov=build(); json.dump({"shots":shots,"overlays":ov,"total":TOTAL},open(OUT/"edl.json","w"),ensure_ascii=False,indent=1)
        from collections import Counter
        usadas=[s for s,_ in PL.R if not any(s in f["texto"] for f in F)]; print("regras sem frase:",usadas)
        print(len(shots),"planos;",round(TOTAL/60,2),"min;",dict(Counter(s["tipo"] for s in shots)),"| cortes/min",round(len(shots)/TOTAL*60,1))
        if modo=="render":
            sel=[int(x) for x in sys.argv[3:]] or range(len(shots))
            jobs=[(n,shots[n],ov,n==len(shots)-1,n>0 and shots[n]["cap"]!=shots[n-1]["cap"] or n==0) for n in sel]
            with cf.ProcessPoolExecutor(max_workers=4) as ex:
                for n,rc,err in ex.map(render_one,jobs):
                    if rc: print("ERRO",n,err,flush=True)
            print("FIM")
    elif modo=="juntar":
        e=json.load(open(OUT/"edl.json")); bad=[n for n in range(len(e["shots"])) if not (SEG/f"s{n:04d}.mp4").exists() or (SEG/f"s{n:04d}.mp4").stat().st_size<3000]
        assert not bad,f"planos faltando: {bad}"
        (OUT/"lista.txt").write_text("".join(f"file 'segs/s{n:04d}.mp4'\n" for n in range(len(e["shots"]))))
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i","lista.txt","-c","copy","base.mp4"],cwd=OUT,check=True)
        d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(OUT/"base.mp4")],capture_output=True,text=True).stdout)
        print("base",round(d,2),"s | esperado",e["total"]); assert abs(d-e["total"])<1.0
    elif modo=="som":
        SFX=AQUI.parents[1]/"05-biblioteca/som/sfx"; e=json.load(open(OUT/"edl.json")); tot=e["total"]; EV=[(0.3,"riser/riser-1",-16)]
        for o in e["overlays"]:
            if o["tipo"]=="cap": EV+=[(o["a"]-0.2,"whoosh-grande/whoosh-grande-1",-16),(o["a"]+0.15,"impacto/impacto-2",-10)]
            if o["tipo"]=="key": EV+=[(o["a"],"carimbo/carimbo-1",-14)]
            if o["tipo"]=="lista": EV+=[(o["a"],"carimbo/carimbo-1",-16)]
            if o["tipo"]=="card": EV+=[(o["a"]+0.4,"impacto/impacto-1",E.get("golpe",-5))]
            if o["tipo"]=="titulo": EV+=[(o["a"]-1.2,"riser/riser-2",-11),(o["a"],"impacto/impacto-1",-5)]
        for s in e["shots"]:
            if s["tipo"]=="doc" and not s.get("titulo"): EV.append((s["a"],"papel/papel-%d"%(1+len(EV)%3),-19))
        EV=[x for x in EV if (SFX/(x[1]+".wav")).exists()]
        inp=["-i",str(P/"narracao/narracao_tratada.wav")]; bed=E.get("cama",-27)
        fl=[f"[0:a]aresample=48000,apad=whole_dur={tot}[n]",
            f"sine=f=55:r=48000:d={tot},volume={bed+1}dB[b1];sine=f=82.5:r=48000:d={tot},tremolo=f=0.13:d=0.7,volume={bed-3}dB[b2];anoisesrc=r=48000:c=brown:d={tot},lowpass=f=260,tremolo=f=0.11:d=0.6,volume={bed-1}dB[b3]",
            f"[b1][b2][b3]amix=inputs=3:normalize=0,afade=t=in:d=2,afade=t=out:st={tot-1.5}:d=1.5[bed]"]; mix=["[n]","[bed]"]
        for k,(t,f,g) in enumerate(EV,1):
            inp+=["-i",str(SFX/(f+".wav"))]; fl.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=mono,volume={g}dB,adelay={max(0,int(t*1000))}[e{k}]"); mix.append(f"[e{k}]")
        fl.append("".join(mix)+f"amix=inputs={len(mix)}:normalize=0,alimiter=limit=0.5:level=0,atrim=0:{tot}[out]")
        (P/"audio/mix.filter").write_text(";".join(fl))
        subprocess.run(["ffmpeg","-loglevel","error","-y",*inp,"-filter_complex_script",str(P/"audio/mix.filter"),"-map","[out]","-ar","48000",str(P/"audio/mix.wav")],check=True)
        def med(f):
            r=subprocess.run(["ffmpeg","-nostats","-i",str(f),"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
            return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",r)[-1]),float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",r)[-1])
        I,_=med(P/"audio/mix.wav"); g=-14.0-I
        for _ in range(3):
            subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(P/"audio/mix.wav"),"-af",f"volume={g:.2f}dB,alimiter=limit=0.80:level=0","-ar","48000","-c:a","pcm_s16le",str(P/"audio/final.wav")],check=True)
            I2,pk=med(P/"audio/final.wav")
            if abs(I2+14)<0.15: break
            g+=-14.0-I2
        print("som:",len(EV),"eventos |",I2,"LUFS | pico",pk)
    elif modo=="final":
        nome=sys.argv[3]
        subprocess.run(["ffmpeg","-loglevel","error","-y","-i",str(OUT/"base.mp4"),"-i",str(P/"audio/final.wav"),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(P/"render"/nome)],check=True); print("ok",nome)
