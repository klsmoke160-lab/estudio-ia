# Cadeia completa da v10 (cópia de /home/user/editonny-cenas/cadeia_v9b.sh). Rodar: bash motor/cadeia_v10.sh
set -e
cd /home/user/estudio-ia/04-projetos/2026-11-13-rockefeller-escola
export NOVO=1 NOVAS_IMAGENS=1 CENAS_EDITONNY=1 SEM_CAPITULOS=1 SEM_GRAFICO=1
df -h / | tail -1 | awk '{print "livre no início:",$4}'
python3 motor/montar.py edl >/dev/null
rm -f render/doc/segs/*.mp4
python3 motor/montar.py render | grep -v "^ok" | tail -4
python3 - <<'E'
import json,pathlib
e=json.load(open("render/doc/edl.json")); bad=[]
for n,s in enumerate(e["shots"]):
    f=pathlib.Path(f"render/doc/segs/s{n:04d}.mp4")
    if not f.exists() or f.stat().st_size<5000: bad.append(n)
print("planos faltando:",bad); assert not bad
open("render/doc/lista.txt","w").write("".join(f"file 'segs/s{n:04d}.mp4'\n" for n in range(len(e["shots"]))))
E
(cd render/doc && ffmpeg -loglevel error -y -f concat -safe 0 -i lista.txt -c copy /home/user/editonny-cenas/base_v9.mp4)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /home/user/editonny-cenas/base_v9.mp4); T=$(python3 -c "import json;print(json.load(open('render/doc/edl.json'))['total'])")
echo "base: $D s | esperado: $T s"; python3 -c "import sys;assert abs($D-$T)<1.0,'base com duração errada'"
python3 audio/mixar.py
python3 audio/final_14lufs.py
rm -rf render/cenas-v9; rm -rf /home/user/editonny-cenas/v6-*; rm -rf /tmp/hyperframes-extract-cache-0
python3 - <<'E' > /tmp/nomes.txt
import sys; sys.path.insert(0,"motor"); sys.argv=["x"]
import importlib.util
s=importlib.util.spec_from_file_location("cv","motor/cenas_v6.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
print(" ".join(n for n,*_ in m.J))
E
set -- $(cat /tmp/nomes.txt)
while [ $# -gt 0 ]; do lote="${@:1:4}"; python3 motor/cenas_v6.py $lote 2>&1 | grep -v " ok$" | cut -c1-160 | tail -3; rm -rf /tmp/hyperframes-extract-cache-0; shift $(( $# < 4 ? $# : 4 )); done
python3 motor/cenas_v6.py montar 2>&1 | tail -2
rm -rf /tmp/hyperframes-extract-cache-0
echo CADEIA_FIM
