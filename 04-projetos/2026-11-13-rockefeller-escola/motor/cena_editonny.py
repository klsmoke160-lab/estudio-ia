"""Renderiza uma cena do catálogo do editonny por cima de um trecho do vídeo.
Uso (módulo): render_cena(base_mp4, a, b, usos, saida) — usos = [(tipo, id, ini_rel, fim_rel, {troca: valor})]
tipo: 'use' | 'transition' | 'effect'. As trocas são feitas na cópia da cena dentro do projeto, nunca no pacote."""
import json, subprocess, pathlib, shutil, re
EDITONNY=pathlib.Path.home()/".local/share/editonny"; CLI=["python3",str(EDITONNY/"scripts/editonny.py")]
W=pathlib.Path("/home/user/editonny-cenas")
def sh(cmd,cwd=None):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
    if r.returncode: raise RuntimeError(" ".join(map(str,cmd))+"\n"+r.stdout[-800:]+r.stderr[-800:])
    return r.stdout
def render_cena(base,a,b,usos,saida,nome):
    d=W/nome; shutil.rmtree(d,ignore_errors=True); (d/"edit/transcripts").mkdir(parents=True)
    dur=round(b-a,3)
    sh(["ffmpeg","-loglevel","error","-y","-ss",f"{a:.3f}","-t",f"{dur:.3f}","-i",str(base),"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-map","0:v","-map","1:a","-shortest","-c:a","aac","-c:v","libx264","-preset","veryfast","-crf","16","-r","24",str(d/"edit/cut.mp4")])
    json.dump({"duration":dur,"fps":24,"fps_str":"24/1","width":1920,"height":1080,"segments":[{"out_start":0.0,"out_end":dur,"src_start":0.0,"src_end":dur}]},open(d/"edit/cut_timeline.json","w"))
    json.dump({"words":[]},open(d/"edit/transcripts/cut.json","w"))
    sh(CLI+["new",str(d/"project"),"--edit",str(d/"edit"),"--style","night"])
    pj=d/"project/project.json"; c=json.load(open(pj)); c.update(format="16:9",title=nome); c["captions"]["enabled"]=False; json.dump(c,open(pj,"w"),indent=1)
    (d/"project/assets/doc").mkdir(parents=True,exist_ok=True)
    for fnt in ("font1.ttf","font2.ttf","sans.ttf"): shutil.copy(pathlib.Path(__file__).parent/fnt,d/"project/assets/doc"/fnt)
    for tipo,sid,s0,s1,trocas in usos:
        if tipo=="custom": out=sh(CLI+["scene","--project",str(d/"project"),"--use","year-hook","--start",f"{s0:.3f}","--end",f"{s1:.3f}"])
        elif tipo=="use": out=sh(CLI+["scene","--project",str(d/"project"),"--use",sid,"--start",f"{s0:.3f}","--end",f"{s1:.3f}"])
        else:
            out=sh(CLI+["scene","--project",str(d/"project"),f"--{tipo}",sid]+(["--cuts",f"{s0:.3f}"] if tipo=="transition" else ["--start",f"{s0:.3f}","--end",f"{s1:.3f}"]))
            rows=json.loads(out[out.index("["):])   # transição e efeito: o editonny só imprime a linha; registro aqui
            for r in rows:
                if tipo=="effect": r["start"],r["end"]=round(s0,3),round(s1,3)
            c=json.load(open(pj)); c.setdefault("scenes",[]).extend(rows); json.dump(c,open(pj,"w"),ensure_ascii=False,indent=1)
            out="Applied "+rows[0]["file"].split("/")[-1]
        m=re.search(r"Applied (\S+\.html)",out)
        if tipo=="custom" and m:
            f=d/"project/compositions/scenes"/m.group(1); cid=m.group(1)[:-5]; f.write_text(sid(cid,round(s1-s0,3))); continue
        if m:
            f=d/"project/compositions/scenes"/m.group(1); t=f.read_text()
            t=t.replace('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"')   # moldura interna no formato 16:9
            t=t.replace("ellipse 880px 1420px at 540px 960px","ellipse 1500px 880px at 960px 540px")
            trocas=trocas or {}
            for x,y in trocas.items():
                if x not in t: raise RuntimeError(f"texto não encontrado em {m.group(1)}: {x}")
                t=t.replace(x,y)
            f.write_text(t)
    c=json.load(open(pj)); c["sounds"]=[]; json.dump(c,open(pj,"w"),indent=1)   # nenhum som novo (aprovado assim)
    sh(["python3","build.py","prepare"],cwd=d/"project"); sh(["python3","build.py","compose"],cwd=d/"project")
    sh(["python3","build.py","hf","lint"],cwd=d/"project")
    sh(["python3","build.py","hf","render","--quality","standard","--output","renders/cena.mp4"],cwd=d/"project")
    shutil.copy(d/"project/renders/cena.mp4",saida); return saida
