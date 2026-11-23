"""Gera as páginas de documento com marca-texto para o vídeo dos testes biológicos.

Fontes (as duas públicas):
  hearing1977.pdf  Senado dos EUA, Health and Scientific Research Subcommittee,
                   "Biological Testing Involving Human Subjects by the Department of Defense, 1977"
                   (com camada de texto -> caixas por pdftotext -bbox)
  subway1968.pdf   "Subway Vulnerability Trials", Fort Detrick, jan/1968, liberado ao público
                   (escaneado -> caixas por OCR do tesseract)

Saída: /home/user/mk/bio/docs2/*.png e docs.json {chave: [arquivo, [[x0,y0,x1,y1],...]]}
"""
import csv, json, pathlib, re, html, subprocess as sp

SRC = pathlib.Path("/home/user/mk/bio/pg")
OUT = pathlib.Path("/home/user/mk/bio/docs2"); OUT.mkdir(parents=True, exist_ok=True)
RES = {}
nm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def _linhas(ws, i, j, esc, div):
    L = {}
    for t, x0, y0, x1, y1 in ws[i:j]:
        k = round(y0 * esc / div); A = L.get(k, [1e9, 1e9, 0, 0])
        L[k] = [min(A[0], x0*esc), min(A[1], y0*esc), max(A[2], x1*esc), max(A[3], y1*esc)]
    return [L[k] for k in sorted(L)]


def _acha(ws, ini, fim):
    a = [nm(x) for x in ini.split() if nm(x)]; b = [nm(x) for x in fim.split() if nm(x)]
    i = next((i for i in range(len(ws)) if [w[0] for w in ws[i:i+len(a)]] == a), None)
    if i is None: return None, None
    j = next((j for j in range(i, len(ws)) if [w[0] for w in ws[j:j+len(b)]] == b), None)
    return i, (j + len(b) if j is not None else None)


_BB = {}
def pdfdoc(chave, pdf, pag, ini, fim):
    """PDF com camada de texto. pag = índice 0-based da página do PDF."""
    if pdf not in _BB:
        _BB[pdf] = re.findall(r"<page[^>]*>(.*?)</page>",
                              open(SRC/(pdf+".bbox.html"), encoding="utf-8", errors="replace").read(), re.S)
    pgt = _BB[pdf][pag]
    ws = [(nm(html.unescape(w)), float(a), float(b), float(c), float(d))
          for a, b, c, d, w in re.findall(
              r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', pgt)]
    ws = [w for w in ws if w[0]]
    i, j = _acha(ws, ini, fim)
    if i is None or j is None: raise SystemExit(f"nao achado: {chave}")
    png = OUT / f"{pdf}_p{pag+1:03d}.png"
    if not png.exists():
        sp.run(["pdftoppm", "-r", "220", "-f", str(pag+1), "-l", str(pag+1), "-png", "-singlefile",
                str(SRC/(pdf+".pdf")), str(png)[:-4]], check=True)
    RES[chave] = [str(png), _linhas(ws, i, j, 220/72, 6)]


def scan(chave, pdf, pag, ini, fim):
    """Página escaneada: renderiza a 220 dpi e acha o trecho pelo OCR. pag = 1-based."""
    png = OUT / f"{pdf}_p{pag:03d}.png"
    if not png.exists():
        sp.run(["pdftoppm", "-r", "220", "-f", str(pag), "-l", str(pag), "-png", "-singlefile",
                str(SRC/(pdf+".pdf")), str(png)[:-4]], check=True)
    tsv = str(png)[:-4] + ".tsv"
    if not pathlib.Path(tsv).exists():
        sp.run(["tesseract", str(png), str(png)[:-4], "-l", "eng", "tsv"], capture_output=True)
    rows = [r for r in csv.DictReader(open(tsv), delimiter="\t") if (r.get("text") or "").strip()]
    ws = [(nm(r["text"]), int(r["left"]), int(r["top"]), int(r["left"])+int(r["width"]),
           int(r["top"])+int(r["height"])) for r in rows]
    ws = [w for w in ws if w[0]]
    i, j = _acha(ws, ini, fim)
    if i is None or j is None: raise SystemExit(f"nao achado: {chave}: {ini} / {fim}")
    RES[chave] = [str(png), _linhas(ws, i, j, 1, 25)]


H = "hearing1977"; S = "subway1968"

# --- Audiência do Senado, 1977 ---
pdfdoc("d_schweiker", H, 8, "the Army had run tests in populated", "to potentially")
pdfdoc("d_penn",      H, 8, "in Mechanicsburg", "Pennsylvania Turnpike")
pdfdoc("d_sf1950",    H, 18, "A test in San Francisco", "population of our cities")
pdfdoc("d_wheat",     H, 18, "some 11 cases of infection", "that you used in that test")
pdfdoc("d_1968",      H, 20, "we continued testing with the organism", "18 years after that time")
pdfdoc("d_hosp",      H, 20, "would not be released over areas", "hospitals and sanitariums")
pdfdoc("d_cidades",   H, 25, "Release in mid near cities", "was unknown")
pdfdoc("d_morreu",    H, 25, "One person did die", "Yes, sir")
pdfdoc("d_tabela",    H, 129, "Table 1", "involving public domain")
pdfdoc("d_lista1",    H, 130, "Washington, DC 18 Aug 1949", "11 Mar 1950")
pdfdoc("d_lista2",    H, 131, "National Airport", "7-10 Jun 1966")
pdfdoc("d_parecer",   H, 149, "use as a simulant should be continued", "advancement of the BW program")
pdfdoc("d_mina",      H, 271, "releasing bacteria in the New York City subways", "deserted mine shaft")
pdfdoc("d_whitecoat", H, 270, "exposure to large numbers", "sick people")

# --- Estudo do metrô, 1968 ---
scan("d_abstract", S, 3, "trials was conducted to evaluate the", "covert biological attack")
scan("d_milhao",   S, 7, "one million workers", "business district daily")
scan("d_concl",    S, 23, "personnel using", "covert attack")
scan("d_relato",   S, 66, "The people of the big city", "see what is going")

json.dump(RES, open(OUT/"docs.json", "w"), ensure_ascii=False, indent=1)
print({k: (pathlib.Path(v[0]).name, len(v[1])) for k, v in RES.items()})
