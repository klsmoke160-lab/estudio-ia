"""v6: cenas do editonny por cima da base limpa (títulos que viraram cena saem com CENAS_EDITONNY=1 no montar.py).
Uso: python3 motor/cenas_v6.py [nome ...]   — renderiza as janelas (ou só as nomeadas) e monta o vídeo final."""
import sys, json, subprocess, pathlib, concurrent.futures as cf
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from cena_editonny import render_cena
from cenas_doc import contador, comparacao
P=pathlib.Path(__file__).resolve().parent.parent
BASE="/home/user/editonny-cenas/base_v6.mp4"; CEN=P/"render/cenas"; CEN.mkdir(exist_ok=True)
V5=P/"render/perfeita-docilidade-v5-editonny.mp4"; SAIDA=P/"render/perfeita-docilidade-v6-cenas.mp4"
J=[]  # (nome, a, b, usos)  — tempos relativos ao início da janela
J.append(("ano-1913",0.0,8.0,[("use","year-hook",1.4,6.6,{'x: 540':'x: 960','y: 230':'y: 170','number: "2027"':'number: "1913"','label: "save this video"':'label: "um texto sobre educação"','badge: "LIKE THIS"':'badge: "ROCKEFELLER"','color: "#ff593d"':'color: "#E2333B"'})]))
for nome,a,b,ano,val,tot,ci,cf_ in [("doacao-1902",122.5,128.4,"1902",1000000,"US$ 1 milhão",123.3,125.4),
                                    ("doacao-1905",132.0,137.2,"1905",10000000,"US$ 11 milhões",132.9,134.9),
                                    ("doacao-1907",144.6,150.0,"1907",32000000,"US$ 43 milhões",145.5,147.9)]:
    J.append((nome,a,b,[("custom",(lambda ano,val,tot,ci,cf_,a: lambda cid,dur: contador(cid,dur,ano,val,tot,ci-a,cf_-a))(ano,val,tot,ci,cf_,a),0.0,b-a,None)]))
J.append(("frase-sem-fonte",700.8,706.3,[("use","crossed-out-quote",0.3,5.5,{})]))
_e=[(742.26,"O modelo de escola nasceu na Prússia, para formar súditos"),(749.13,"Foi copiado de propósito por reformadores americanos"),
    (757.99,"Bilionários gastaram fortunas para moldar o ensino"),(761.01,"E escreveram o que esperavam das pessoas comuns")]
_d=[(766.05,"Rockefeller inventou a escola obrigatória"),(772.78,"Um plano secreto para manter as pessoas ignorantes")]
J.append(("fato-ou-nao",741.7,780.3,[("custom",lambda cid,dur: comparacao(cid,dur,[(t-741.7,x) for t,x in _e],[(t-741.7,x) for t,x in _d]),0.0,780.3-741.7,None)]))
J.append(("comente",833.9,838.6,[("use","comment-call-to-action",0.0,4.6,{})]))
for k,(a,b) in enumerate([(74.46,77.76),(93.98,114.3),(290.93,298.91),(301.85,307.72),(333.19,346.72),(706.3,719.89)]):
    J.append((f"tv-{k}",a,b,[("effect","tv-lines",0.0,b-a,{})]))
caps=[63.34,66.19,114.95,190.4,257.28,349.96,409.19,505.08,565.4,627.16,689.66,738.42,791.51]
for k,t in enumerate(caps): J.append((f"queima-{k:02d}",t-0.7,t+0.7,[("transition","film-burn",0.7,None,{})]))
PARAM={"crossed-out-quote":{'x: 540':'x: 960','y: 418':'y: 300','label: "Hire an editor"':'label: "Atribuída a Rockefeller"',
        'oldValue: "R$ 1,500/month"':'oldValue: "nação de trabalhadores"','newValue: "R$ 0.48"':'newValue: "SEM FONTE"','newColor: "#30d158"':'newColor: "#E2333B"'},
       "comment-call-to-action":{'x: 540':'x: 960','y: 230':'y: 170','label: "Comment"':'label: "Me conta nos comentários"','word: "I WANT IT"':'word: "QUEM ESCOLHE HOJE?"','accent: "#ff593d"':'accent: "#E2333B"','Add a comment...':'Escreva um comentário...'},
       "tv-lines":{'strength: 0.6':'strength: 0.45'}}
def fazer(j):
    nome,a,b,usos=j; out=CEN/f"{nome}.mp4"
    usos=[(t,s,x,y,(tr if tr or callable(s) else PARAM.get(s,{}))) for t,s,x,y,tr in usos]
    try: render_cena(BASE,a,b,usos,str(out),"v6-"+nome); return nome,"ok"
    except Exception as e: return nome,"ERRO "+str(e)[-600:]
def montar():
    ok=[(n,a,b) for n,a,b,_ in J if (CEN/f"{n}.mp4").exists()]
    ins=["-i",BASE]; fc=[]; last="[0:v]"
    for i,(n,a,b) in enumerate(ok,1):
        ins+=["-i",str(CEN/f"{n}.mp4")]
        fc.append(f"[{i}:v]trim=0:{b-a:.3f},setpts=PTS-STARTPTS+{a:.3f}/TB[s{i}]")
        fc.append(f"{last}[s{i}]overlay=enable='between(t,{a:.3f},{b-0.02:.3f})':eof_action=pass[o{i}]"); last=f"[o{i}]"
    ins+=["-i",str(V5)]; na=len(ok)+1
    cmd=["ffmpeg","-loglevel","error","-y",*ins,"-filter_complex",";".join(fc),"-map",last,"-map",f"{na}:a","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","24","-c:a","copy","-movflags","+faststart",str(SAIDA)]
    subprocess.run(cmd,check=True); print("montado:",SAIDA,len(ok),"cenas")
if __name__=="__main__":
    sel=sys.argv[1:]
    if sel!=["montar"]:
        js=[j for j in J if not sel or j[0] in sel]
        with cf.ThreadPoolExecutor(max_workers=2) as ex:
            for n,r in ex.map(fazer,js): print(n,r,flush=True)
    if not sel or sel==["montar"]: montar()
