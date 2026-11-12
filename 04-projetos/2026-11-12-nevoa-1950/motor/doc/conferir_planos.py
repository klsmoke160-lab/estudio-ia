"""Folha de contato dos planos escolhidos (quadro do meio de cada um), por categoria, para revisão."""
import subprocess, sys, pathlib
sys.argv=[sys.argv[0],"edl"]; sys.path.insert(0,str(pathlib.Path(__file__).parent))
import montar as M
out=pathlib.Path("/tmp/planos"); out.mkdir(exist_ok=True)
for cat,v in M.LIB.items():
    items=[(f,t) for f,ts in v.items() for t in ts]; files=[]
    for k,(f,t) in enumerate(items):
        ss,L,slow=M.shot_src(f,t,4.5); fn=out/f"{cat}_{k:03d}.jpg"
        lab=f"{f[:9]} {t}"
        subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",f"{ss+L/2:.2f}","-i",str(M.RAW/(f+".mp4")),"-frames:v","1","-vf",f"scale=240:180,drawtext=text='{lab}':fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.7:x=2:y=2",str(fn)],check=True)
    n=len(items); cols=8; rows=-(-n//cols)
    subprocess.run(["ffmpeg","-loglevel","error","-y","-pattern_type","glob","-i",str(out/f"{cat}_*.jpg"),"-vf",f"tile={cols}x{rows}","-frames:v","1",f"/tmp/planos_{cat}.jpg"],check=True)
    print(cat,n)
