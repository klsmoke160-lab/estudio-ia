"""Short vertical (1080x1920) no modelo "Parabéns, você criou…": narração palavra por palavra, documentos com marca-texto,
filmes de arquivo recortados em 9:16, etiquetas fixas no alto e cartão final.
Uso: python3 scripts/video/short_voce.py <projeto> [edl|render|final <saida.mp4>]
Lê <projeto>/short/plano.py, que define: PL (módulo com D, CENAS, RAW, AR, PRE), AUDIO, PALAVRAS (json do make_captions), CORRIGE,
BEATS [(inicio_s, [fontes], tint)], ETIQUETAS [(ini, fim, linha1, linha2|None)], AVISO, MUSICA (arquivo, ganho dB), TOTAL_CARTAO."""
import json, subprocess, sys, pathlib, re, importlib.util, math, shutil, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
AQUI = pathlib.Path(__file__).resolve().parent; FON = AQUI.parents[1] / "05-biblioteca/fontes"
P = pathlib.Path(sys.argv[1]).resolve(); modo = sys.argv[2] if len(sys.argv) > 2 else "render"
spec = importlib.util.spec_from_file_location("splano", P / "short/plano.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
PL = S.PL; FPS = 24; W, H = 1080, 1920
OUT = P / "render/short"; SEG = OUT / "segs"; SEG.mkdir(parents=True, exist_ok=True)
MIX = {"vermelho": "rr=1.2:gr=0:br=0:rg=0.15:gg=0.05:bg=0:rb=0.1:gb=0:bb=0.05", "petroleo": "rr=0.1:gr=0.8:br=0.75:rg=0:gg=0.15:bg=0.1:rb=0:gb=0:bb=0.15",
       "ambar": "rr=1.1:gr=0.7:br=0.2:rg=0.1:gg=0.1:bg=0:rb=0:gb=0:bb=0.05", "verde": "rr=0.25:gr=0.95:br=0.45:rg=0.05:gg=0.15:bg=0.05:rb=0:gb=0:bb=0.1"}
CREAM = (236, 230, 214); RED = (226, 51, 59)

# ---------- palavras ----------
def palavras():
    pal = json.load(open(P / S.PALAVRAS)); out = []
    for w in pal:
        t = w["text"].strip()
        for a, b in S.CORRIGE.items(): t = t.replace(a, b)
        out.append(dict(t=t, a=w["startMs"] / 1000, b=w["endMs"] / 1000))
    return out
def dur_audio():
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(P / S.AUDIO)], capture_output=True, text=True).stdout)
def plano_shots(total):
    shots = []; B = S.BEATS
    for i, (t0, fontes, tint) in enumerate(B):
        t1 = B[i + 1][0] if i + 1 < len(B) else total
        # cada fonte recebe um pedaço igual; documento precisa de 2,4 s, filme de 1,2 s
        fs = list(fontes)
        while len(fs) > 1 and (t1 - t0) / len(fs) < (2.4 if any(f[0] == "doc" for f in fs) else 1.2): fs.pop()
        for j, f in enumerate(fs):
            a = t0 + (t1 - t0) * j / len(fs); b = t0 + (t1 - t0) * (j + 1) / len(fs)
            shots.append(dict(f=f, a=a, b=b, tint=tint, par=len(shots) % 2 == 0))
    for s in shots: s["fa"] = round(s["a"] * FPS); s["fb"] = round(s["b"] * FPS)
    return [s for s in shots if s["fb"] > s["fa"]]

# ---------- renderização de cada plano ----------
def grade(tint):
    return ["hue=s=0", "eq=contrast=1.40:brightness=-0.13:gamma=0.88", f"colorchannelmixer={MIX[tint]}"]
def shot_src(film, t, need):
    c = PL.CENAS[film]; a = max(x for x in c if x <= t); b = min(x for x in c if x > t); a += 0.25; b -= 0.25; L = b - a
    if L >= need: s = min(max(t - need / 2, a), b - need); return s, need, 1.0
    if L >= need / 1.8: return a, L, need / L
    return max(0, t - need / 2), need, 1.0
def render_clip(n, s):
    """Decodifica o filme em tamanho original, aplica o zoom e o recorte 9:16 em Python (o filtro scale com eval=frame do ffmpeg travava) e codifica com a cor."""
    out = SEG / f"s{n:04d}.mp4"; nf = s["fb"] - s["fa"]; d = nf / FPS; film, t = s["f"][1], s["f"][2]
    ss, L, slow = shot_src(film, t, d); pre = [PL.PRE[film]] if film in getattr(PL, "PRE", {}) else []
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(PL.RAW[film])], capture_output=True, text=True).stdout.strip().split(",")
    sw, sh = int(pr[0]), int(pr[1])
    for f in pre:
        m = re.match(r"crop=(\d+):(\d+)", f)
        if m: sw, sh = int(m.group(1)), int(m.group(2))
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", f"{ss:.3f}", "-t", f"{L + 0.2:.3f}", "-i", str(PL.RAW[film]), "-an", "-vf", ",".join(pre + [f"setpts=(PTS-STARTPTS)*{slow:.4f}", f"fps={FPS}", "hqdn3d=3:3:6:6"]),
                            "-frames:v", str(nf), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    vf = [*grade(s["tint"]), "unsharp=5:5:0.7", "vignette=angle=PI/2.6", "noise=alls=9:allf=t+u", "format=yuv420p"]
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-vf", ",".join(vf),
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-video_track_timescale", "12288", str(out)], stdin=subprocess.PIPE)
    fsz = sw * sh * 3; k = 0; ult = None
    while k < nf:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            if ult is None: break
            buf = ult   # o filme acabou antes: segura o último quadro
        ult = buf; im = Image.frombytes("RGB", (sw, sh), buf); u = k / max(1, nf - 1); z = (1 + 0.07 * u) if s["par"] else (1.07 - 0.07 * u)
        h = sh / z; w = min(sw, h * W / H); h = w * H / W; cx, cy = sw / 2, sh / 2
        enc.stdin.write(im.transform((W, H), Image.EXTENT, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), Image.BICUBIC).tobytes()); k += 1
    enc.stdin.close(); dec.stdout.close(); dec.wait(); enc.wait()
    return n, enc.returncode if k == nf else 1, ("faltaram quadros" if k != nf else "")
_PG = {}
def pagina(arq, boxes):
    pg = Image.open(arq).convert("RGB"); M = 1500; can = Image.new("RGB", (pg.width + 2 * M, pg.height + 2 * M), (16, 16, 16)); can.paste(pg, (M, M))
    hl = can.copy(); ov = Image.new("RGBA", can.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x0, y0, x1, y1 in boxes or []: d.rectangle([x0 + M - 6, y0 + M - 2, x1 + M + 6, y1 + M + 4], fill=(255, 226, 0, 120))
    hl = Image.alpha_composite(hl.convert("RGBA"), ov).convert("RGB"); return can, hl, M, pg.size
def render_doc(n, s):
    out = SEG / f"s{n:04d}.mp4"; nf = s["fb"] - s["fa"]; arq, boxes, foco, fonte = PL.D[s["f"][1]]; can, hl, M, (pw, ph) = pagina(arq, boxes)
    if boxes: ux0 = min(b[0] for b in boxes); uy0 = min(b[1] for b in boxes); ux1 = max(b[2] for b in boxes); uy1 = max(b[3] for b in boxes)
    else: ux0, uy0, ux1, uy1 = pw * .1, ph * .3, pw * .9, ph * .5
    cx1 = (ux0 + ux1) / 2 + M; cy1 = (uy0 + uy1) / 2 + M; w1 = min(max((ux1 - ux0) * 0.85, 760), 980); w0 = min(w1 * 1.7, pw * 1.1)
    cx0 = pw / 2 + M; cy0 = cy1 - 300
    vf = ["eq=brightness=-0.06:contrast=1.10:saturation=0.85", "vignette=angle=PI/2.8", "noise=alls=6:allf=t+u", "format=yuv420p"]
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-vf", ",".join(vf), "-frames:v", str(nf),
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-video_track_timescale", "12288", str(out)], stdin=subprocess.PIPE)
    for k in range(nf):
        u = k / max(1, nf - 1); e = 1 - (1 - u) ** 2; w = w0 + (w1 - w0) * e; h = w * H / W; cx = cx0 + (cx1 - cx0) * e; cy = cy0 + (cy1 - cy0) * e
        cy = cy + 0.14 * h; box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2); a = Image.BICUBIC
        A = can.transform((W, H), Image.EXTENT, box, a); al = min(1, max(0, (u - 0.18) / 0.22))
        if al > 0: A = Image.blend(A, hl.transform((W, H), Image.EXTENT, box, a), al)
        ff.stdin.write(A.tobytes())
    ff.stdin.close(); ff.wait(); return n, ff.returncode, ""
def render_one(a):
    n, s = a
    return render_doc(n, s) if s["f"][0] == "doc" else render_clip(n, s)

# ---------- legenda e etiquetas (ASS) ----------
def ass_t(x):
    h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60; return f"{h}:{m:02d}:{sec:05.2f}"
COR = {"b": "&HFFFFFF&", "v": "&H3B33E2&", "a": "&H4DE0F4&", "g": "&H6EDC3C&"}
def cor_palavra(t):
    n = re.sub(r"[^a-z0-9-]", "", t.lower().replace("ã", "a").replace("é", "e").replace("í", "i").replace("ú", "u").replace("ç", "c").replace("ô", "o").replace("á", "a").replace("ê", "e"))
    if n.isdigit() or n in ("mil",): return "a"
    if n in S.VERMELHO: return "v"
    if n in S.VERDE: return "g"
    return "b"
def ass(shots, total):
    hd = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "", "[V4+ Styles]",
          "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
          "Style: Pal,Anton,128,&HFFFFFF&,&HFFFFFF&,&H000000&,&H80000000&,0,0,0,0,100,100,1,0,1,8,2,5,40,40,0,1",
          "Style: Et1,Anton,76,&H4DE0F4&,&HFFFFFF&,&H000000&,&H80000000&,0,0,0,0,100,100,1,0,1,6,2,8,50,50,230,1",
          "Style: Et2,Special Elite,40,&HD6E6EC&,&HFFFFFF&,&H000000&,&H80000000&,0,0,0,0,100,100,0,0,1,4,1,8,50,50,330,1",
          "Style: Fonte,Special Elite,28,&HD6E6EC&,&HFFFFFF&,&H000000&,&H80000000&,0,0,0,0,100,100,0,0,1,3,1,2,50,50,150,1", "",
          "[Events]", "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    ev = []; PW = palavras()
    G = []; i = 0
    while i < len(PW):
        w = dict(PW[i]); lim = lambda x: re.sub(r"[^\w-]", "", x)
        while len(lim(w["t"])) <= 2 and not lim(w["t"]).isdigit() and i + 1 < len(PW) and PW[i + 1]["a"] - w["b"] < 0.4 and not w["t"].endswith((".", ",", ";", ":")):
            nx = PW[i + 1]; w = dict(t=w["t"] + " " + nx["t"], a=w["a"], b=nx["b"], main=nx["t"]); i += 1
        G.append(w); i += 1
    PW = G
    for i, w in enumerate(PW):
        nxt = PW[i + 1]["a"] if i + 1 < len(PW) else total; fim = min(nxt, w["b"] + 0.18, w["a"] + 1.2)
        if fim <= w["a"] + 0.05: fim = w["a"] + 0.12
        txt = w["t"].upper().strip(".,;:!?")
        ev.append(f"Dialogue: 1,{ass_t(w['a'])},{ass_t(fim)},Pal,,0,0,0,,{{\\pos({W // 2},1230)\\c{COR[cor_palavra(w.get('main', w['t']))]}\\fscx125\\fscy125\\t(0,90,\\fscx100\\fscy100)}}{txt}")
    for a, b, l1, l2 in S.ETIQUETAS:
        ev.append(f"Dialogue: 2,{ass_t(a)},{ass_t(b)},Et1,,0,0,0,,{{\\fad(180,180)}}{l1}")
        if l2: ev.append(f"Dialogue: 2,{ass_t(a + 0.3)},{ass_t(b)},Et2,,0,0,0,,{{\\fad(180,180)}}{l2}")
    ev.append(f"Dialogue: 2,{ass_t(0.4)},{ass_t(5.5)},Fonte,,0,0,0,,{{\\fad(300,400)}}{S.AVISO}")
    for s in shots:
        if s["f"][0] == "doc":
            fonte = PL.D[s["f"][1]][3]
            if fonte and s["a"] > 5.6: ev.append(f"Dialogue: 2,{ass_t(s['a'] + 0.3)},{ass_t(s['b'] - 0.1)},Fonte,,0,0,0,,{{\\fad(200,200)}}Fonte: {quebra(fonte)}")
    (OUT / "legenda.ass").write_text("\n".join(hd + ev), encoding="utf-8")

def quebra(t, n=44):
    pal = t.split(); lin = [""]
    for x in pal:
        if len(lin[-1]) + len(x) + 1 > n: lin.append("")
        lin[-1] = (lin[-1] + " " + x).strip()
    return "\\N".join(lin)

def cartao(total):
    E = Image.new("RGB", (W, H), (10, 10, 10)); d = ImageDraw.Draw(E); an = lambda s: ImageFont.truetype(str(FON / "font1.ttf"), s)
    def centro(y, t, f, fill): w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=fill)
    centro(640, "VÍDEO COMPLETO", an(120), CREAM); centro(790, "NO CANAL", an(80), (216, 208, 190))
    f = an(190); w = d.textlength("RASURA", font=f); x = (W - w) / 2; d.text((x, 900), "RASURA", font=f, fill=CREAM); bb = d.textbbox((x, 900), "RASURA", font=f)
    y = (bb[1] + bb[3]) // 2; d.line([(x - 16, y), (x + w + 16, y - 6)], fill=RED, width=18)
    centro(1180, "histórias investigadas a partir de documentos", ImageFont.truetype(str(FON / "font2.ttf"), 36), (216, 208, 190))
    E.save(OUT / "fim.png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{S.CARTAO:.2f}", "-i", str(OUT / "fim.png"), "-vf", f"fps={FPS},fade=t=in:d=0.4,format=yuv420p", "-c:v", "libx264", "-crf", "22",
                    "-video_track_timescale", "12288", str(SEG / "zfim.mp4")], check=True)

if __name__ == "__main__":
    total = dur_audio(); shots = plano_shots(total)
    if modo == "edl":
        for n, s in enumerate(shots): print(n, f"{s['a']:6.2f}-{s['b']:6.2f}", s["f"][0], s["f"][1:], s["tint"])
        sys.exit()
    if modo == "render":
        todos = list(enumerate(shots)); sel = [int(x) for x in sys.argv[3:]] or [n for n, _ in todos]
        with cf.ThreadPoolExecutor(3) as ex:
            for n, rc, err in ex.map(render_one, [todos[i] for i in sel]):
                print("plano", n, "ok" if rc == 0 else "ERRO " + err, flush=True)
        cartao(total); ass(shots, total)
        lst = [str(SEG / f"s{n:04d}.mp4") for n in range(len(shots))] + [str(SEG / "zfim.mp4")]
        (OUT / "lista.txt").write_text("".join(f"file '{x}'\n" for x in lst))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(OUT / "lista.txt"), "-c", "copy", str(OUT / "base.mp4")], check=True)
        print("base pronta:", OUT / "base.mp4")
    if modo == "final":
        nome = sys.argv[3]; tot = total + S.CARTAO; mus, g = S.MUSICA
        fl = [f"[0:a]aresample=48000,apad=whole_dur={tot:.2f},asplit=2[n][sc]",
              f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{tot:.2f},asetpts=PTS-STARTPTS,afade=t=in:d=2,afade=t=out:st={tot - 3:.2f}:d=3,volume={g}dB[m]",
              "[m][sc]sidechaincompress=threshold=0.02:ratio=5:attack=60:release=700:makeup=1[bed]",
              f"[n][bed]amix=inputs=2:normalize=0,atrim=0:{tot:.2f}[mix]"]
        (OUT / "mix.filter").write_text(";".join(fl))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(P / S.AUDIO), "-stream_loop", "-1", "-i", str(mus), "-filter_complex_script", str(OUT / "mix.filter"), "-map", "[mix]",
                        "-ar", "48000", "-c:a", "pcm_f32le", str(OUT / "mix.wav")], check=True)
        def med(f):
            r = subprocess.run(["ffmpeg", "-nostats", "-i", str(f), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
            return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]), float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
        ALVO = S.LUFS; I, _ = med(OUT / "mix.wav"); gg = ALVO - I
        for _ in range(3):
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(OUT / "mix.wav"), "-af", f"volume={gg:.2f}dB,alimiter=limit=0.891:level=0:attack=5:release=150", "-ar", "48000", "-c:a", "pcm_s16le", str(OUT / "final.wav")], check=True)
            I2, pk = med(OUT / "final.wav")
            if abs(I2 - ALVO) < 0.15: break
            gg += ALVO - I2
        print("som:", I2, "LUFS | pico", pk)
        (P / "render").mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(OUT / "base.mp4"), "-i", str(OUT / "final.wav"), "-vf", f"ass={OUT / 'legenda.ass'}:fontsdir={FON}", "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(P / "render" / nome)], check=True)
        print("pronto:", P / "render" / nome)
