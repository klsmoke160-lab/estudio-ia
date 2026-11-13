"""Prepara o texto para o Supertonic: números por extenso em português (anos, valores) e siglas."""
import re
from num2words import num2words
def ext(n): return num2words(int(n),lang='pt_BR').replace(',','')
def preparar(t):
    t=t.replace("1700s","mil e setecentos")
    t=re.sub(r"\b(1[0-9]{3})\b",lambda m:ext(m.group(1)),t)          # anos
    t=re.sub(r"\b(\d+)\b",lambda m:ext(m.group(1)),t)
    return t
if __name__=="__main__":
    import sys; print(preparar(sys.argv[1]))
