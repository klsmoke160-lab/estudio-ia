"""Cruza as medições: cortes (measure_reference) + quadros/áudio (analisar_edicao.py) + palavras (Whisper).
Saída: resumo.json e momentos.json na pasta 'aprofundado'.
Uso: python3 cruzar_edicao.py <pasta_medicao> <palavras.json>"""
import sys, json, math, pathlib, statistics as st
import numpy as np
W=pathlib.Path(sys.argv[1]); A=W/"aprofundado"; PAL=json.load(open(sys.argv[2]))
Q=np.load(A/"quadros.npz"); fps=float(Q["fps"]); N=len(Q["luma"])
AU=json.load(open(A/"audio.json")); AC=np.load(A/"audio_curvas.npz"); ht=float(AC["hop_t"])
C=json.load(open(W/"measurements/cuts.json"))["cuts"]
cortes=sorted(c["t"] for c in C if c["type"] in ("cut","probable")); dur=N/fps
bounds=[0.0]+cortes+[dur]; shots=[(a,b) for a,b in zip(bounds,bounds[1:]) if b-a>0.05]
L=Q["luma"]; S=Q["sat"]; D=Q["diff"]; SH=Q["sharp"]; SC=Q["scale"]; TX=Q["tx"]; TY=Q["ty"]
words=[w for s in PAL["seg"] for w in s["w"]]
# ---------- 1. transições em cada corte
def janela(t,r=10):
    f=int(round(t*fps)); return max(1,f-r),min(N-1,f+r),f
trans=[]
for t in cortes:
    a,b,f=janela(t); l=L[a:b]; d=np.nan_to_num(D[a:b]); sh=SH[a:b]
    tipo="corte seco"
    if l.min()<10 and (l[:3].mean()>25 or l[-3:].mean()>25): tipo="passagem pelo preto"
    elif l.max()>205 and l.max()-np.median(l)>60: tipo="clarão (flash)"
    elif (d>5).sum()>=5 and d.max()<25: tipo="dissolvência / fusão"
    elif sh.min()<0.35*np.median(sh): tipo="borrão (blur/whip)"
    trans.append(dict(t=round(t,2),tipo=tipo))
from collections import Counter
tc=Counter(x["tipo"] for x in trans)
# ---------- 2. movimento dentro de cada plano
mov=[]
for a,b in shots:
    fa,fb=int(a*fps)+3,int(b*fps)-3
    if fb-fa<12: continue
    sc=SC[fa:fb]; tx=TX[fa:fb]; ty=TY[fa:fb]; ok=~np.isnan(sc)
    if ok.sum()<0.7*(fb-fa): mov.append(dict(a=a,b=b,tipo="indefinido")); continue
    zoom=(math.exp(np.nansum(np.log(sc[ok])))**(fps/ok.sum())-1)*100   # % por segundo
    px=np.nansum(tx)*fps/ok.sum()*100; py=np.nansum(ty)*fps/ok.sum()*100  # % da largura/altura por segundo
    jit=float(np.nanstd(np.diff(tx[ok])))*100
    if abs(zoom)<0.6 and abs(px)<0.8 and abs(py)<0.8: tipo="parado"
    elif abs(zoom)>=max(abs(px),abs(py))*0.5 and abs(zoom)>=0.6: tipo="aproximação (zoom in)" if zoom>0 else "afastamento (zoom out)"
    elif abs(px)>=abs(py): tipo="panorâmica p/ direita" if px<0 else "panorâmica p/ esquerda"
    else: tipo="vertical p/ baixo" if py<0 else "vertical p/ cima"
    if jit>0.35 and tipo=="parado": tipo="câmera tremida"
    mov.append(dict(a=round(a,2),b=round(b,2),dur=round(b-a,2),tipo=tipo,zoom=round(zoom,2),pan_x=round(px,2),pan_y=round(py,2),tremor=round(jit,3)))
mc=Counter(m["tipo"] for m in mov)
zin=[m["zoom"] for m in mov if m["tipo"].startswith("aproxima")]; zout=[m["zoom"] for m in mov if m["tipo"].startswith("afasta")]
pans=[abs(m["pan_x"]) for m in mov if m["tipo"].startswith("panor")]
# saltos de zoom dentro do plano (punch-in)
punch=[round(i/fps,2) for i in range(1,N) if not np.isnan(SC[i]) and SC[i]>1.06 and D[i]<12]
# ---------- 3. cor por plano
cor=[]
for a,b in shots:
    fa,fb=int(a*fps),int(b*fps)
    if fb<=fa: continue
    r,g,bb=[float(np.mean(Q[k][fa:fb])) for k in ("r","g","b")]
    cor.append(dict(a=round(a,2),luma=round(float(np.mean(L[fa:fb])),1),sat=round(float(np.mean(S[fa:fb])),1),quente=round(r-bb,1),
                    vinheta=round(float(np.mean(Q["corner"][fa:fb])/max(1,np.mean(Q["center"][fa:fb]))),2),
                    pb=bool(np.mean(S[fa:fb])<18)))
pb=sum(1 for c in cor if c["pb"])/len(cor)
def circ(v):
    v=v[~np.isnan(v)]; a=np.deg2rad(v); return float((np.rad2deg(math.atan2(np.sin(a).mean(),np.cos(a).mean()))+360)%360)
# ---------- 4. fala, pausas e sincronia dos cortes
fala=[(w["a"],w["b"]) for w in words]
gaps=[(fala[i][1],fala[i+1][0]) for i in range(len(fala)-1) if fala[i+1][0]-fala[i][1]>0.25]
fim_frase=[w["b"] for w in words if w["w"].strip()[-1:] in ".?!"]
def em_pausa(t): return any(g0-0.05<=t<=g1+0.05 for g0,g1 in gaps)
def dist(t,xs): return min((abs(t-x) for x in xs),default=99)
starts=[w["a"] for w in words]
sync=dict(cortes_em_pausa=round(100*sum(em_pausa(t) for t in cortes)/len(cortes),1),
          cortes_ate_150ms_de_fim_de_frase=round(100*sum(dist(t,fim_frase)<0.15 for t in cortes)/len(cortes),1),
          cortes_ate_120ms_de_inicio_de_palavra=round(100*sum(dist(t,starts)<0.12 for t in cortes)/len(cortes),1))
# atraso do corte em relação ao início da palavra seguinte (corte antecipa a fala?)
lead=[]
for t in cortes:
    nxt=[s for s in starts if s>=t-0.3]
    if nxt and nxt[0]-t<1.0: lead.append(nxt[0]-t)
sync["corte_antes_da_palavra_mediana_s"]=round(st.median(lead),3) if lead else None
dur_fala=sum(b-a for a,b in fala); wpm=len(words)/(dur_fala/60) if dur_fala else 0
pausas=[g1-g0 for g0,g1 in gaps]
# base aleatória: quanto daria por acaso
rng=np.random.default_rng(1); rnd=rng.uniform(5,dur-5,2000)
base=dict(em_pausa=round(100*np.mean([em_pausa(t) for t in rnd]),1),fim_frase=round(100*np.mean([dist(t,fim_frase)<0.15 for t in rnd]),1))
# ---------- 5. trilha: batidas e golpes
beats=np.array(AU["beats"]); ons=np.array([o[0] for o in AU["onsets"]]); onv=np.array([o[1] for o in AU["onsets"]])
fortes=ons[onv>np.percentile(onv,90)]
def frac(ts,ref,tol): return round(100*np.mean([np.min(np.abs(ref-t))<tol for t in ts]),1)
som=dict(tempo_bpm=round(AU["tempo"],1),cortes_na_batida_60ms=frac(cortes,beats,0.06),acaso_batida=frac(rnd,beats,0.06),
         cortes_com_golpe_forte_100ms=frac(cortes,fortes,0.1),acaso_golpe=frac(rnd,fortes,0.1),lufs=AU["lufs_I"],lra=AU["LRA"])
mom=np.array(AU["momentary"])
# volume nos trechos sem fala (trilha sozinha) e com fala
def niveis(intervals):
    v=[m for t,m in mom if any(a<=t<=b for a,b in intervals) and m>-70]; return round(float(np.median(v)),1) if v else None
som["lufs_momentaneo_com_fala"]=niveis([(a,b) for a,b in fala]); som["lufs_momentaneo_pausas_>0.6s"]=niveis([g for g in gaps if g[1]-g[0]>0.6])
# ---------- 6. momentos: telas pretas, telas claras, picos de ritmo, picos de volume
pretas=[]; i=0
while i<N:
    if L[i]<8:
        j=i
        while j<N and L[j]<8: j+=1
        if (j-i)/fps>=0.25: pretas.append([round(i/fps,2),round((j-i)/fps,2)])
        i=j
    else: i+=1
cps=[sum(1 for t in cortes if s<=t<s+20)*3 for s in range(0,int(dur)-20,5)]
picos=sorted(range(len(cps)),key=lambda k:-cps[k])[:6]; lentos=sorted(range(len(cps)),key=lambda k:cps[k])[:6]
loud=sorted([m for m in mom if m[1]>-70],key=lambda m:-m[1])[:8]
resumo=dict(duracao=round(dur,1),cortes=len(cortes),cortes_por_min=round(len(cortes)/dur*60,1),
            plano_medio=round(st.mean([b-a for a,b in shots]),2),plano_mediano=round(st.median([b-a for a,b in shots]),2),
            planos_percentis={p:round(float(np.percentile([b-a for a,b in shots],p)),2) for p in (10,25,50,75,90)},
            transicoes=dict(tc),movimento=dict(mc),zoom_in_mediano_pct_s=round(st.median(zin),2) if zin else None,zoom_in_p90=round(float(np.percentile(zin,90)),2) if zin else None,
            zoom_out_mediano_pct_s=round(st.median(zout),2) if zout else None,pan_mediano_pct_s=round(st.median(pans),2) if pans else None,
            saltos_de_zoom=len(punch),
            cor=dict(luma_media=round(float(L.mean()),1),sat_media=round(float(S.mean()),1),planos_quase_pb_pct=round(100*pb,1),
                     tom_sombras=round(circ(Q["sh_hue"]),0),tom_luzes=round(circ(Q["hi_hue"]),0),
                     vinheta_mediana=round(st.median([c["vinheta"] for c in cor]),2),quente_mediano=round(st.median([c["quente"] for c in cor]),1),
                     letterbox_pct=round(100*float(np.mean(Q["top_black"]>8)),1)),
            fala=dict(palavras=len(words),palavras_por_min_falando=round(wpm,1),pausa_mediana=round(st.median(pausas),2) if pausas else None,
                      pausas_maiores_1s=sum(p>1 for p in pausas),fala_pct_do_video=round(100*dur_fala/dur,1)),
            sincronia=sync,base_acaso=base,som=som,
            ritmo_20s_mais_rapidos=[dict(inicio=k*5,cortes_por_min=cps[k]) for k in picos],ritmo_20s_mais_lentos=[dict(inicio=k*5,cortes_por_min=cps[k]) for k in lentos],
            telas_pretas=pretas,mais_alto=[dict(t=round(t,1),lufs=m) for t,m in loud])
json.dump(resumo,open(A/"resumo.json","w"),ensure_ascii=False,indent=1)
json.dump(dict(transicoes=trans,movimento=mov,cor=cor,saltos_zoom=punch[:200]),open(A/"detalhe.json","w"),ensure_ascii=False)
print(json.dumps(resumo,ensure_ascii=False,indent=1))
