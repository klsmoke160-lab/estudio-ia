"""Busca imagens e filmagens para um trecho de narração em vários acervos de uma vez e devolve a licença de cada resultado.

Uso: python3 scripts/video/buscar_acervos.py consultas.json saida.json
consultas.json = [{"id":"t01","ia":["burning documents"],"wm":["MKUltra"],"mix":["fire"]}, ...]
  ia  = Internet Archive (filmes; tira as coleções de TV, que têm direitos de emissora)
  wm  = Wikimedia Commons (arquivos; licença lida dos metadados)
  mix = Mixkit (vídeos de banco com licença gratuita)
"""
import json, re, sys, time, urllib.parse, urllib.request

UA = "RasuraResearch/1.0 (documentary research)"
def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        except Exception as e:
            if k == tries - 1: return ""
            time.sleep(3 * (k + 1))

BOM = {"prelinger": "Prelinger (domínio público / CC0 indicado pelo acervo)", "universal_newsreels": "Universal Newsreels (domínio público nos EUA)",
       "FedFlix": "FedFlix (obra do governo dos EUA, domínio público)", "nasa": "NASA (domínio público)", "computerchronicles": None}
def ia(q, n=6):
    qq = f"({q}) AND mediatype:(movies) AND NOT collection:(tvarchive OR tvnews)"
    u = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode({"q": qq, "rows": n, "output": "json"}) + \
        "".join(f"&fl[]={f}" for f in ["identifier", "title", "year", "licenseurl", "collection", "rights", "downloads"])
    try: docs = json.loads(get(u))["response"]["docs"]
    except Exception: return []
    out = []
    for d in docs:
        col = d.get("collection", []); col = col if isinstance(col, list) else [col]
        lic = d.get("licenseurl") or ""
        nota = next((BOM[c] for c in col if BOM.get(c)), None)
        if not nota:
            nota = ("licença: " + lic) if lic else "SEM licença declarada: conferir antes de usar"
        out.append({"fonte": "Internet Archive", "titulo": d.get("title"), "ano": d.get("year"), "link": "https://archive.org/details/" + d["identifier"],
                    "colecao": ",".join(col[:3]), "direitos": nota, "rights": d.get("rights"), "downloads": d.get("downloads")})
    return out

def wm(q, n=6):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6,
        "gsrlimit": n, "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "format": "json"})
    time.sleep(1.5)
    try: pages = json.loads(get(u))["query"]["pages"].values()
    except Exception: return []
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
        val = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", ""))[:160]
        out.append({"fonte": "Wikimedia Commons", "titulo": p["title"], "link": ii.get("descriptionurl"), "arquivo": ii.get("url"),
                    "tamanho": f"{ii.get('width')}x{ii.get('height')}", "tipo": ii.get("mime"), "direitos": val("LicenseShortName"),
                    "autor": val("Artist"), "data": val("DateTimeOriginal"), "descricao": val("ImageDescription")})
    return out

def mix(q, n=6):
    h = get("https://mixkit.co/free-stock-video/" + urllib.parse.quote(q.replace(" ", "-")) + "/")
    links = list(dict.fromkeys(re.findall(r'href="(/free-stock-video/[a-z0-9-]+-\d+/)"', h)))[:n]
    return [{"fonte": "Mixkit", "titulo": l.split("/")[2].rsplit("-", 1)[0].replace("-", " "), "link": "https://mixkit.co" + l,
             "direitos": "Mixkit Stock Video Free License (uso comercial permitido, inclusive monetizado; não revender o clipe solto)"} for l in links]

if __name__ == "__main__":
    cons = json.load(open(sys.argv[1])); res = {}
    for c in cons:
        r = []
        for q in c.get("ia", []): r += [dict(x, consulta=q) for x in ia(q)]
        for q in c.get("wm", []): r += [dict(x, consulta=q) for x in wm(q)]
        for q in c.get("mix", []): r += [dict(x, consulta=q) for x in mix(q)]
        res[c["id"]] = r; print(c["id"], len(r), flush=True)
    json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
