"""Medições quadro a quadro de um vídeo de referência (complementa o measure_reference do editonny).
Vídeo: brilho, saturação, cor média, nitidez, diferença entre quadros e movimento de câmera (escala, deslocamento, rotação)
entre quadros vizinhos, via ECC (OpenCV). Áudio: volume momentâneo (LUFS), batidas, golpes (onsets) e brilho espectral.
Uso: uv run --with opencv-python-headless --with librosa python scripts/video/analisar_edicao.py <video> <pasta_saida>"""
import sys, json, subprocess, re, pathlib, math
import numpy as np, cv2
V=sys.argv[1]; O=pathlib.Path(sys.argv[2]); O.mkdir(parents=True,exist_ok=True)
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cols={k:[] for k in ("luma","sat","r","g","b","sharp","diff","hist","scale","tx","ty","rot","ok","center","corner","top_black","bot_black","sh_hue","hi_hue","sh_sat","hi_sat")}
prev=None; prevh=None; warp_mode=cv2.MOTION_AFFINE; crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,40,1e-4); i=0
while True:
    ok,fr=cap.read()
    if not ok: break
    g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY); s=cv2.resize(g,(160,90),interpolation=cv2.INTER_AREA).astype(np.float32)
    hsv=cv2.cvtColor(cv2.resize(fr,(160,90),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2HSV)
    b,gg,r=[float(x) for x in cv2.mean(fr)[:3]]
    cols["r"].append(r); cols["g"].append(gg); cols["b"].append(b)
    y=float(g.mean()); cols["luma"].append(y); cols["sat"].append(float(hsv[...,1].mean()))
    cols["sharp"].append(float(cv2.Laplacian(cv2.resize(g,(320,180)),cv2.CV_64F).var()))
    h,w=g.shape; cols["center"].append(float(g[h//4:3*h//4,w//4:3*w//4].mean()))
    cols["corner"].append(float(np.mean([g[:h//6,:w//6].mean(),g[:h//6,-w//6:].mean(),g[-h//6:,:w//6].mean(),g[-h//6:,-w//6:].mean()])))
    rows=g.mean(axis=1); cols["top_black"].append(int(np.argmax(rows>18)) if (rows>18).any() else h); cols["bot_black"].append(int(np.argmax(rows[::-1]>18)) if (rows>18).any() else h)
    # tom das sombras e das altas luzes (split toning)
    L=hsv[...,2]; H=hsv[...,0].astype(np.float32)*2; Sa=hsv[...,1]
    def tom(m):
        if m.sum()<20: return float("nan"),float("nan")
        a=np.deg2rad(H[m]); wgt=Sa[m].astype(np.float32)+1
        return float((np.rad2deg(math.atan2((np.sin(a)*wgt).sum(),(np.cos(a)*wgt).sum()))+360)%360),float(Sa[m].mean())
    hh,ss=tom((L>25)&(L<80)); cols["sh_hue"].append(hh); cols["sh_sat"].append(ss)
    hh,ss=tom(L>170); cols["hi_hue"].append(hh); cols["hi_sat"].append(ss)
    hist=cv2.calcHist([hsv],[0,1],None,[30,32],[0,180,0,256]); cv2.normalize(hist,hist)
    if prev is None:
        for k in ("diff","hist","scale","tx","ty","rot"): cols[k].append(float("nan"))
        cols["ok"].append(0)
    else:
        cols["diff"].append(float(np.abs(s-prev).mean())); cols["hist"].append(float(cv2.compareHist(prevh,hist,cv2.HISTCMP_CORREL)))
        W=np.eye(2,3,dtype=np.float32)
        try:
            _,W=cv2.findTransformECC(prev,s,W,warp_mode,crit,None,3); okk=1
        except cv2.error: okk=0
        A=W[:,:2]; sc=math.sqrt(abs(np.linalg.det(A))); rot=math.degrees(math.atan2(A[1,0],A[0,0]))
        # deslocamento em fração da largura/altura por quadro, descontando o efeito do zoom em torno do centro
        cx,cy=80,45; tx=(W[0,2]-(cx-(A[0,0]*cx+A[0,1]*cy)))/160; ty=(W[1,2]-(cy-(A[1,0]*cx+A[1,1]*cy)))/90
        cols["scale"].append(sc if okk else float("nan")); cols["tx"].append(float(tx) if okk else float("nan")); cols["ty"].append(float(ty) if okk else float("nan")); cols["rot"].append(rot if okk else float("nan")); cols["ok"].append(okk)
    prev=s; prevh=hist; i+=1
    if i%3000==0: print("quadros",i,"/",n,flush=True)
np.savez_compressed(O/"quadros.npz",fps=fps,**{k:np.array(v,dtype=np.float32) for k,v in cols.items()})
print("vídeo ok",i,"quadros a",fps,"fps",flush=True)
# ---- áudio
import librosa
wav=O/"audio22k.wav"; subprocess.run(["ffmpeg","-loglevel","error","-y","-i",V,"-ac","1","-ar","22050",str(wav)],check=True)
yv,sr=librosa.load(str(wav),sr=22050,mono=True); hop=512
rms=librosa.feature.rms(y=yv,hop_length=hop)[0]; oenv=librosa.onset.onset_strength(y=yv,sr=sr,hop_length=hop)
tempo,beats=librosa.beat.beat_track(onset_envelope=oenv,sr=sr,hop_length=hop)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=hop,units="frames")
cent=librosa.feature.spectral_centroid(y=yv,sr=sr,hop_length=hop)[0]
low=librosa.feature.rms(y=librosa.effects.preemphasis(yv,coef=-0.95),hop_length=hop)[0]
r=subprocess.run(["ffmpeg","-nostats","-i",V,"-af","ebur128=framelog=verbose","-f","null","-"],capture_output=True,text=True).stderr
mom=[(float(a),float(b)) for a,b in re.findall(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)",r)]
I=re.findall(r"I:\s+(-?[\d.]+) LUFS",r); LRA=re.findall(r"LRA:\s+([\d.]+) LU",r)
json.dump(dict(sr=sr,hop=hop,tempo=float(np.atleast_1d(tempo)[0]),beats=[float(x) for x in librosa.frames_to_time(beats,sr=sr,hop_length=hop)],
               onsets=[[float(t),float(oenv[f])] for t,f in zip(librosa.frames_to_time(on,sr=sr,hop_length=hop),on)],
               lufs_I=float(I[-1]) if I else None,LRA=float(LRA[-1]) if LRA else None,momentary=mom[::5]),open(O/"audio.json","w"))
np.savez_compressed(O/"audio_curvas.npz",rms=rms,oenv=oenv,cent=cent,low=low,hop_t=hop/sr)
print("áudio ok: tempo",float(np.atleast_1d(tempo)[0]),"batidas",len(beats),"golpes",len(on),"LUFS",I[-1] if I else None)
