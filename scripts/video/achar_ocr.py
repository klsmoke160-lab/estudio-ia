"""Localiza um trecho no OCR de um livro do Internet Archive: devolve a página e as caixas das linhas."""
import re,sys,json,functools,os
DOCS=os.environ.get('DOCS_OCR','/home/user/escola/docs')
@functools.lru_cache(None)
def pages(id):
    x=open(f'{DOCS}/{id}_djvu.xml',errors='ignore').read(); out=[]
    for o in re.split(r'<OBJECT ',x)[1:]:
        W=int(re.search(r'width="(\d+)"',o).group(1)); H=int(re.search(r'height="(\d+)"',o).group(1)); lines=[]
        for ln in re.findall(r'<LINE>(.*?)</LINE>',o,flags=re.S):
            ws=[(m.group(2).strip(),[int(v) for v in m.group(1).split(',')[:4]]) for m in re.finditer(r'<WORD coords="([\d,]+)"[^>]*>([^<]*)</WORD>',ln)]
            if ws: lines.append(ws)
        out.append((W,H,lines))
    return out
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower())
def find(id,ini,fim,start=0):
    """da primeira palavra de `ini` até a última de `fim`; devolve (pagina,(W,H),[caixas por linha l,t,r,b])"""
    P=pages(id); a=[norm(w) for w in ini.split()]; b=[norm(w) for w in fim.split()]
    for n in range(start,len(P)):
        W,H,lines=P[n]; flat=[(norm(w),c,li) for li,l in enumerate(lines) for w,c in l]; ws=[f[0] for f in flat]
        for i in range(len(ws)-len(a)+1):
            if ws[i:i+len(a)]==a:
                for j in range(i,len(ws)-len(b)+1):
                    if ws[j:j+len(b)]==b:
                        sel=flat[i:j+len(b)]; boxes={}
                        for w,c,li in sel:
                            l,bt,r,t=c; x=boxes.get(li,[1e9,1e9,0,0]); boxes[li]=[min(x[0],l),min(x[1],t),max(x[2],r),max(x[3],bt)]
                        return n,(W,H),[boxes[k] for k in sorted(boxes)]," ".join(w for l in lines for w,_ in l)[:0]
    return None
if __name__=="__main__":
    r=find(sys.argv[1],sys.argv[2],sys.argv[3]); print(r)
