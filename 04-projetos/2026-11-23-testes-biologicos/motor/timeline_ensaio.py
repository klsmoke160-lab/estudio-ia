"""Monta uma narração de ENSAIO (silêncio) com os tempos estimados do roteiro.

Serve só para montar e conferir o vídeo antes de a voz chegar. Imita o que o
scripts/som/tratar_narracao.py produz: audio/timeline_novo.json e
narracao/narracao_tratada.wav. Quando a narração de verdade chegar, roda-se o
tratar_narracao.py normalmente e estes arquivos são substituídos.

Uso: python3 motor/timeline_ensaio.py [palavras_por_minuto]
"""
import json, pathlib, re, subprocess, sys

P = pathlib.Path(__file__).resolve().parent.parent
PPM = float(sys.argv[1]) if len(sys.argv) > 1 else 150.0   # ritmo da voz Davi nos vídeos anteriores
SR = 48000
LINHA, CURTA, CAP, TIT = 0.45, 0.8, 1.9, 5.0

F = []; cap = None
for l in (P / "roteiro-completo.txt").read_text().split("\n"):
    l = l.strip()
    if not l: continue
    if l.startswith("#"):
        cap = l[1:].strip()
        if F: F[-1]["fim_cap"] = True
        continue
    ss = re.split(r"(?<=[.?!:])\s+", l)
    for k, s in enumerate(ss):
        F.append(dict(texto=s, cap=cap, fim_linha=k == len(ss) - 1, fim_cap=False))

curta = lambda k: len(F[k]["texto"].split()) <= 5
ult_abertura = max(k for k, f in enumerate(F) if f["cap"] == F[0]["cap"])

t = 1.5; out = []
for k, f in enumerate(F):
    pal = f["texto"].split()
    dur = max(0.9, len(pal) / PPM * 60)
    ini, fim = t, t + dur
    g = dict(i=k + 1, texto=f["texto"], cap=f["cap"], ini=round(ini, 3), fim=round(fim, 3))
    # um instante por palavra, repartido por igual (o alinhador real dá os certos)
    g["t"] = [round(ini + dur * i / max(1, len(pal)), 3) for i in range(len(pal))]
    pausa = 0.0
    if k + 1 < len(F):
        if k == ult_abertura: pausa = 1.0 + TIT
        elif f["fim_cap"]: pausa = CAP
        elif curta(k) or curta(k + 1): pausa = CURTA
        elif f["fim_linha"]: pausa = LINHA
        else: pausa = 0.25
    g["pausa"] = round(pausa, 3)
    if k == ult_abertura: g["titulo_ini"] = round(fim + 1.0, 3)
    out.append(g); t = fim + pausa
total = round(t + 2.0, 3)

(P / "audio").mkdir(exist_ok=True); (P / "narracao").mkdir(exist_ok=True)
json.dump(dict(intro=1.5, total=total, voz="ENSAIO (silêncio)", frases=out),
          open(P / "audio/timeline_novo.json", "w"), ensure_ascii=False)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi",
                "-i", f"anoisesrc=d={total}:c=pink:a=0.0002:r={SR}",
                "-ac", "1", "-c:a", "pcm_s16le", str(P / "narracao/narracao_tratada.wav")], check=True)
print(f"frases {len(out)} · total {total/60:.1f} min")
