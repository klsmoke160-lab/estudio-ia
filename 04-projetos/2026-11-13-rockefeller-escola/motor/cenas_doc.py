"""Cenas próprias no estilo do documentário (16:9), no formato de cena do editonny/HyperFrames.
Substituem o arquivo da cena 'portadora' (year-hook) dentro do projeto; o id da composição é mantido."""
import json
FONTES='''@font-face{font-family:"Anton";src:url("assets/doc/font1.ttf");font-display:block}
@font-face{font-family:"Elite";src:url("assets/doc/font2.ttf");font-display:block}
@font-face{font-family:"DocSans";src:url("assets/doc/sans.ttf");font-display:block}'''
def _wrap(cid,dur,css,html,js):
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8"/><title>{cid}</title></head><body>
<template id="{cid}-template">
<style>{FONTES}
#root{{position:absolute;inset:0;overflow:hidden}}
{css}</style>
<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{dur}">{html}</div>
<script>
(function(){{
  window.__timelines=window.__timelines||{{}};
  const tl=gsap.timeline({{paused:true}}); const D={dur};
  const $=s=>document.querySelector(s);
{js}
  tl.to({{}},{{duration:D}},0);
  window.__timelines["{cid}"]=tl;
}})();
</script>
</template></body></html>'''
def contador(cid,dur,ano,valor,total,t_ini,t_fim):
    """Doação: ano em máquina de escrever, valor em dólares contando de 0, total acumulado embaixo."""
    css='''#v{position:absolute;left:70px;top:110px;width:820px;height:350px;border-radius:18px;background:rgba(12,10,8,.78);box-shadow:0 20px 60px rgba(0,0,0,.55),inset 0 0 0 1px rgba(236,230,214,.12);opacity:0}
#l{position:absolute;left:112px;top:132px;font-family:"Elite";font-size:38px;color:#ECE6D6;letter-spacing:.06em;opacity:0;text-shadow:0 3px 8px #000}
#l i{display:inline-block;width:16px;height:16px;border-radius:50%;background:#E2333B;margin-right:16px;box-shadow:0 0 14px #E2333B}
#n{position:absolute;left:108px;top:180px;font-family:"Anton";font-size:132px;line-height:1.1;color:#fff;white-space:nowrap;font-variant-numeric:tabular-nums;opacity:0;text-shadow:0 8px 26px rgba(0,0,0,.8)}
#n small{font-size:80px;margin-right:18px;color:#ECE6D6}
#u{position:absolute;left:114px;top:362px;height:8px;width:0;background:#E2333B}
#t{position:absolute;left:114px;top:390px;font-family:"DocSans";font-size:36px;color:#D8D2C2;opacity:0;text-shadow:0 3px 8px #000}
#t b{color:#fff}'''
    html=f'<div id="v"></div><div id="l"><i></i>DOAÇÃO DE ROCKEFELLER · {ano}</div><div id="n"><small>US$</small><span id="c">0</span></div><i id="u"></i><div id="t">total doado até aqui: <b>{total}</b></div>'
    js=f'''  const fmt=v=>Math.round(v).toLocaleString("pt-BR");
  tl.to("#v",{{opacity:1,duration:.4}},0);
  tl.fromTo("#l",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},.1);
  tl.fromTo("#n",{{opacity:0,y:40,filter:"blur(10px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.45,ease:"expo.out"}},.3);
  const o={{v:0}}; tl.to(o,{{v:{valor},duration:{t_fim-t_ini:.2f},ease:"power2.out",onUpdate:()=>{{$("#c").textContent=fmt(o.v)}}}},{t_ini:.2f});
  tl.set("#c",{{textContent:fmt({valor})}},{t_fim+.01:.2f});
  tl.fromTo("#n",{{scale:1}},{{scale:1.06,duration:.12,yoyo:true,repeat:1,transformOrigin:"0% 50%"}},{t_fim:.2f});
  tl.to("#u",{{width:520,duration:.45,ease:"power3.out"}},{t_fim:.2f});
  tl.fromTo("#t",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.35}},{t_fim+.3:.2f});
  tl.to(["#v","#l","#n","#u","#t"],{{opacity:0,y:-30,duration:.35,ease:"power2.in",stagger:.03}},D-.5);'''
    return _wrap(cid,dur,css,html,js)
def comparacao(cid,dur,esq,dir_):
    """Painel 'Confirmado × Não comprovado'; cada item entra quando a narração o diz. esq/dir_: [(t, texto)]."""
    css='''#v{position:absolute;inset:0;background:rgba(6,5,4,.70);opacity:0}
.col{position:absolute;top:150px;width:780px}
#a{left:150px}#b{left:990px}
.h{font-family:"Anton";font-size:64px;letter-spacing:.04em;color:#ECE6D6;padding-bottom:14px;border-bottom:6px solid;opacity:0}
#a .h{border-color:#8fb873}#b .h{border-color:#E2333B}
.it{display:flex;gap:22px;align-items:flex-start;margin-top:34px;font-family:"DocSans";font-size:40px;line-height:1.22;color:#F2EEE4;opacity:0;text-shadow:0 3px 10px #000}
.ic{flex:0 0 52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:"DocSans";font-weight:700;font-size:34px;color:#111}
#a .ic{background:#8fb873}#b .ic{background:#E2333B;color:#fff}
#vs{position:absolute;left:930px;top:154px;width:60px;text-align:center;font-family:"Elite";font-size:34px;color:#bdb6a6;opacity:0}'''
    li=lambda xs,ic:"".join(f'<div class="it"><span class="ic">{ic}</span><span>{t}</span></div>' for _,t in xs)
    html=f'<div id="v"></div><div class="col" id="a"><div class="h">CONFIRMADO</div>{li(esq,"✓")}</div><div id="vs">×</div><div class="col" id="b"><div class="h">NÃO COMPROVADO</div>{li(dir_,"✗")}</div>'
    tA=json.dumps([t for t,_ in esq]); tB=json.dumps([t for t,_ in dir_])
    js=f'''  tl.to("#v",{{opacity:1,duration:.5}},0);
  tl.fromTo("#a .h",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},.2);
  tl.to("#vs",{{opacity:1,duration:.4}},.4);
  tl.fromTo("#b .h",{{opacity:0,y:-20}},{{opacity:.45,y:0,duration:.4,ease:"power3.out"}},.5);
  document.querySelectorAll("#a .it").forEach((e,i)=>tl.fromTo(e,{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.45,ease:"back.out(1.6)"}},{tA}[i]));
  tl.to("#b .h",{{opacity:1,duration:.3}},{tB}[0]-.2);
  document.querySelectorAll("#b .it").forEach((e,i)=>tl.fromTo(e,{{opacity:0,x:40}},{{opacity:1,x:0,duration:.45,ease:"back.out(1.6)"}},{tB}[i]));
  tl.to(["#a","#b","#vs","#v"],{{opacity:0,duration:.45,ease:"power2.in"}},D-.55);'''
    return _wrap(cid,dur,css,html,js)
def capitulo(cid,dur,num,titulo):
    """Cartão de capítulo animado: número em máquina de escrever, título letra a letra, traço vermelho; o filme segue rodando atrás."""
    fs=min(176,int(1600/(len(titulo)*0.52)))
    css=f'''#v{{position:absolute;inset:0;background:radial-gradient(75% 70% at 50% 50%,rgba(0,0,0,.55),rgba(0,0,0,.86));opacity:0}}
#k{{position:absolute;left:0;width:1920px;top:{410-fs//2}px;text-align:center;font-family:"Elite";font-size:42px;letter-spacing:.42em;color:#D8D2C2;opacity:0}}
#w{{position:absolute;left:0;width:1920px;top:{470-fs//2}px;text-align:center;white-space:nowrap}}
#w span{{display:inline-block;font-family:"Anton";font-size:{fs}px;line-height:1.15;color:#ECE6D6;opacity:0;text-shadow:0 8px 30px rgba(0,0,0,.8)}}
#u{{position:absolute;left:960px;top:{470+int(fs*0.6)+40}px;width:0;height:6px;background:#E2333B;box-shadow:0 0 18px rgba(226,51,59,.6)}}'''
    letras="".join(f"<span>{'&nbsp;' if c==' ' else c}</span>" for c in titulo)
    html=f'<div id="v"></div><div id="k">{num}</div><div id="w">{letras}</div><i id="u"></i>'
    js=f'''  const L=document.querySelectorAll("#w span"), st=Math.min(.045,.7/L.length);
  tl.to("#v",{{opacity:1,duration:.3,ease:"power1.out"}},0);
  tl.fromTo("#k",{{opacity:0,y:-14,scale:1.08}},{{opacity:1,y:0,scale:1,duration:.6,ease:"expo.out"}},.12);
  tl.fromTo(L,{{opacity:0,y:46,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.42,ease:"expo.out",stagger:st}},.22);
  tl.fromTo("#w",{{scale:1.0}},{{scale:1.035,duration:D,ease:"none"}},0);
  tl.to("#u",{{width:560,x:-280,duration:.55,ease:"power3.out"}},.5);
  tl.to(["#k","#w","#u"],{{opacity:0,y:-18,duration:.3,ease:"power2.in"}},D-.38);
  tl.to("#v",{{opacity:0,duration:.35,ease:"power1.in"}},D-.3);'''
    return _wrap(cid,dur,css,html,js)
