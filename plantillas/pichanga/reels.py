"""Reels Pichanga Brava 1080x1920, 15 s, 30 fps. Uso: python3 reels.py OUTDIR [nombre...]"""
import asyncio, os, sys, subprocess, shutil
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import BALL

OUT = sys.argv[1]; ONLY = sys.argv[2:]
os.makedirs(OUT, exist_ok=True)
DUR, FPS = 15, 30

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:Inter,sans-serif;color:#FFF8E7;overflow:hidden;position:relative;
 background:repeating-linear-gradient(90deg,#2F7D3B 0 135px,#2A7235 135px 270px)}
.chalk{position:absolute;border:8px solid rgba(255,248,231,.16)}
.dirt{position:absolute;left:0;right:0;bottom:0;height:300px;background:#C97B3D;box-shadow:inset 0 18px 0 #B56A30}
.brand{position:absolute;top:120px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:18px;animation:fadeD .6s both}
.brand b{font-weight:900;font-size:48px}.brand b span{color:#FFD23F}
.abs{position:absolute;left:80px;right:80px}
h1{font-weight:900;line-height:1;letter-spacing:-2px;text-shadow:0 6px 0 rgba(0,0,0,.22)}
h1 em{font-style:normal;color:#FFD23F}
.kicker{display:inline-block;background:#FFD23F;color:#1B1B1B;font-weight:900;font-size:42px;padding:12px 28px;border-radius:14px;transform:rotate(-2deg)}
.card{background:#FFF8E7;color:#1B1B1B;border-radius:30px;padding:30px 36px;box-shadow:0 10px 0 rgba(0,0,0,.2);font-size:50px;font-weight:800;display:flex;gap:26px;align-items:center}
.tag{flex:none;width:92px;height:92px;border-radius:22px;background:#C97B3D;color:#FFF8E7;display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:900}
.pill{display:inline-block;background:#1B1B1B;color:#FFF8E7;font-weight:900;font-size:48px;padding:24px 44px;border-radius:999px}
.foot{position:absolute;left:0;right:0;bottom:110px;text-align:center}
.bar{position:absolute;left:0;bottom:0;height:12px;background:#FFD23F;animation:grow 15s linear both}
.bubble{position:absolute;background:#FFF8E7;color:#1B1B1B;border-radius:34px;padding:34px 40px;font-weight:900;font-size:56px;line-height:1.1;box-shadow:0 10px 0 rgba(0,0,0,.2)}
.bubble:after{content:"";position:absolute;bottom:-34px;left:90px;border:20px solid transparent;border-top:24px solid #FFF8E7}
@keyframes grow{from{width:0}to{width:100%}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes fadeD{from{opacity:0;transform:translateY(-20px)}to{opacity:1;transform:none}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.06)}100%{opacity:1;transform:scale(1)}}
@keyframes out{from{opacity:1}to{opacity:0}}
@keyframes left{from{opacity:0;transform:translateX(-140px)}to{opacity:1;transform:none}}
@keyframes right{from{opacity:0;transform:translateX(140px)}to{opacity:1;transform:none}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes shake{0%,100%{transform:rotate(0)}25%{transform:rotate(-4deg)}75%{transform:rotate(4deg)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.2}}
'''
def A(name, delay, dur=.6, extra=''):
    return f'animation:{name} {dur}s cubic-bezier(.2,.8,.2,1) {delay}s both{extra}'
def window(a, b, name='pop'):
    # aparece en a, desaparece en b
    return f'animation:{name} .45s cubic-bezier(.2,.8,.2,1) {a}s both, out .3s {b}s forwards'

def guy(color, num, x, y, s=1.0, extra='', cap=False, mustache=False, anim=''):
    hat = '<path d="M86 60 Q150 6 214 60 Z" fill="#3E4A3A"/><rect x="150" y="52" width="80" height="12" rx="6" fill="#3E4A3A"/>' if cap else '<path d="M92 66 Q150 4 208 66 Q170 44 150 50 Q120 44 92 66Z" fill="#3B2416"/>'
    mus = '<path d="M118 108 Q150 96 182 108 Q150 118 118 108Z" fill="#3B2416"/>' if mustache else ''
    return f'''<svg viewBox="0 0 300 380" width="{300*s}" height="{380*s}" style="position:absolute;left:{x}px;top:{y}px;{anim}">
<ellipse cx="150" cy="372" rx="110" ry="10" fill="rgba(0,0,0,.25)"/>
<rect x="104" y="250" width="34" height="110" rx="16" fill="#1B1B1B"/><rect x="162" y="250" width="34" height="110" rx="16" fill="#1B1B1B"/>
<rect x="80" y="140" width="140" height="130" rx="40" fill="{color}"/>
<text x="150" y="222" font-family="Inter" font-weight="900" font-size="64" fill="#FFF8E7" text-anchor="middle">{num}</text>
<rect x="40" y="150" width="40" height="100" rx="20" fill="{color}"/><rect x="220" y="150" width="40" height="100" rx="20" fill="{color}"/>
<circle cx="150" cy="90" r="62" fill="#E8B38A"/>
<circle cx="128" cy="86" r="8" fill="#1B1B1B"/><circle cx="172" cy="86" r="8" fill="#1B1B1B"/>
{mus}<path d="M126 120 Q150 134 174 120" stroke="#1B1B1B" stroke-width="7" fill="none" stroke-linecap="round"/>
{hat}{extra}</svg>'''

BRAND = f'<div class="brand">{BALL.format(s=70)}<b>PICHANGA <span>BRAVA</span></b></div>'
FIELD = '<div class="chalk" style="width:640px;height:640px;border-radius:50%;left:220px;top:980px"></div><div class="chalk" style="left:-10px;right:-10px;top:1300px;height:0;border-width:8px 0 0 0"></div><div class="dirt"></div>'

R = {}

# ---------- 1. PON PAUSA ----------
tipos = ["El comilón", "El arquero volante", "El que llega tarde", "El que reclama todo",
         "El dueño de la pelota", "El que solo empuja al arco", "El que se lesiona a los 5 minutos",
         "El que organiza y no juega", "El que pide la última", "El que juega con zapatos"]
R['reel1_pon_pausa'] = (FIELD + BRAND + f'''
<div class="abs" style="top:300px;text-align:center;{A('pop',.1,.5)}"><span class="kicker">RETO</span></div>
<h1 class="abs" style="top:420px;font-size:120px;text-align:center;{A('pop',.3,.5)}"><em>PON PAUSA</em><br>y descubre qué pichanguero eres</h1>
<div class="abs" style="top:960px;{A('pop',2.2,.4)}"><div class="card" style="justify-content:center;min-height:240px;font-size:66px;text-align:center" id="t">?</div></div>
{guy('#4F6F8F','?',380,1360,1.0,'',False,False,A('bob',2,1.2,' infinite').replace(' both','')+', out .3s 10.6s forwards')}
<div class="abs" style="top:1240px;text-align:center;z-index:5;{A('up',10.8)}"><span class="kicker" style="font-size:52px">¿Qué te salió? Comenta</span></div>
<div class="foot" style="{A('up',11.2)}"><span class="pill">@pichangabrava</span></div>''',
'''var L=%s;var e=document.getElementById('t');
if(t<2.4){e.textContent='?';}else if(t<10.5){var i=Math.floor((t-2.4)/0.18)%%L.length;e.textContent=L[i];}
else{e.textContent='¡Comenta el tuyo!';}''' % (repr(tipos)))

# ---------- 2. ARMA TU EQUIPO ----------
rows = [("ARCO", "El que sale jugando", "El que no se mueve de la raya"),
        ("DEFENSA", "El leñero", "El que pide offside sin línea"),
        ("ADELANTE", "El comilón", "El que solo empuja al arco")]
rh = ''
for i, (pos, a, b) in enumerate(rows):
    d = 1.8 + i * 2.6
    top = 700 + i * 360
    rh += f'''<div class="abs" style="top:{top}px;{A('pop',d,.4)}"><span class="kicker" style="font-size:36px">{pos}</span></div>
<div class="abs" style="top:{top+80}px;display:flex;flex-direction:column;gap:16px">
<div class="card" style="font-size:44px;padding:22px 30px;{A('left',d+.3,.5)}"><div class="tag" style="width:76px;height:76px;font-size:40px">A</div>{a}</div>
<div class="card" style="font-size:44px;padding:22px 30px;{A('right',d+.6,.5)}"><div class="tag" style="width:76px;height:76px;font-size:40px">B</div>{b}</div></div>'''
R['reel2_arma_equipo'] = (FIELD + BRAND + f'''
<h1 class="abs" style="top:300px;font-size:116px;{A('pop',.1,.5)}">Arma tu equipo de <em>barrio</em></h1>
<p class="abs" style="top:560px;font-size:48px;font-weight:800;{A('up',.9)}">Elige A o B en cada línea</p>
{rh}
<div class="abs" style="top:1780px;text-align:center;{A('pop',10.6,.5)}"><span class="kicker" style="font-size:46px">Comenta tu equipo: ej. A-B-A</span></div>''', '')

# ---------- 3. CAMARÍN DE BARRIO 1998 ----------
lockers = ''.join(f'<div style="position:absolute;left:{40+i*205}px;top:260px;width:190px;height:820px;background:#8A6A4A;border:6px solid #6E533A;border-radius:10px"><div style="margin:40px auto 0;width:110px;height:14px;background:#6E533A;border-radius:7px"></div><div style="margin:30px auto 0;width:110px;height:14px;background:#6E533A;border-radius:7px"></div><div style="position:absolute;right:22px;top:400px;width:16px;height:60px;background:#C9B48A;border-radius:6px"></div></div>' for i in range(5))
poster = f'''<div style="position:absolute;left:640px;top:330px;width:330px;height:430px;background:#E9DFC6;border:8px solid #CDBF9F;transform:rotate(3deg);box-shadow:0 8px 0 rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px">
{BALL.format(s=160)}<div style="color:#4F6F8F;font-weight:900;font-size:58px;letter-spacing:2px">MUNDIAL</div><div style="color:#B5584F;font-weight:900;font-size:90px">98</div></div>'''
radio = '<div style="position:absolute;left:110px;top:560px;width:250px;height:140px;background:#5A5A5A;border-radius:20px;border:6px solid #3F3F3F"><div style="position:absolute;left:20px;top:28px;width:84px;height:84px;border-radius:50%;background:#2F2F2F;border:6px solid #777"></div><div style="position:absolute;right:20px;top:34px;width:100px;height:24px;background:#D9B860;border-radius:6px"></div><div style="position:absolute;left:60px;top:-60px;width:8px;height:70px;background:#777;transform:rotate(-20deg)"></div></div>'
bench = '<div style="position:absolute;left:0;right:0;top:1330px;height:60px;background:#9C7A55;border-top:8px solid #B48E64"></div><div style="position:absolute;left:0;right:0;top:1080px;bottom:0;background:#BFB6A0;z-index:-1"></div>'
players = (guy('#B5584F','7',20,1040,.95,'',False,True,A('fade',.2,.6))
           + guy('#B5584F','10',250,1060,.95,'',False,False,A('fade',.3,.6))
           + guy('#B5584F','1',740,1040,.95,'<rect x="20" y="230" width="60" height="44" rx="14" fill="#D9B860"/><rect x="220" y="230" width="60" height="44" rx="14" fill="#D9B860"/>',False,False,A('fade',.4,.6)))
coach = guy('#4F6F8F','DT',420,980,1.25,'',True,True,'animation:shake .5s ease-in-out 1.2s 4')
lines = [(1.0, 4.0, 'Muchachos…<br>esto es una <span style="color:#B5584F">final</span>.'),
         (4.2, 7.2, 'El rival tiene al comilón más grande de la comuna.'),
         (7.4, 10.0, 'Pero nosotros tenemos algo que ellos no…'),
         (10.2, 12.2, '¡La pelota! Es mía.')]
bub = ''.join(f'<div class="bubble" style="left:70px;right:70px;top:820px;{window(a,b)}">{txt}</div>' for a, b, txt in lines)
R['reel3_camarin_98'] = (f'''<div style="position:absolute;inset:0;background:#D8CCB0"></div>{lockers}{poster}{radio}{bench}{players}{coach}
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(40,25,10,.45) 100%);pointer-events:none"></div>
<div class="abs" style="top:110px;text-align:center;{A('pop',.1,.5)}"><span class="kicker" style="font-size:40px">CAMARÍN DE BARRIO · 1998</span></div>
{bub}
<div style="position:absolute;inset:0;background:rgba(30,60,30,.92);{A('fade',12.3,.4)}"></div>
<h1 class="abs" style="top:600px;font-size:110px;text-align:center;{A('pop',12.5,.5)}">¿Qué charla les darías <em>tú</em>?</h1>
<div class="abs" style="top:1020px;text-align:center;{A('up',12.9)}"><span class="kicker" style="font-size:50px">Comenta abajo</span></div>
<div class="foot" style="{A('up',13.1)}"><span class="pill">@pichangabrava</span></div>''', '')

async def render(b, name, html, js):
    page = await b.new_page(viewport={'width': 1080, 'height': 1920})
    doc = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}<div class="bar"></div><script>window.tick=function(t){{{js}}}</script></body></html>'
    await page.set_content(doc); await page.wait_for_timeout(300)
    fdir = f'{OUT}/_f_{name}'; shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
    for i in range(DUR*FPS):
        t = i / FPS
        await page.evaluate('t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});window.tick(t)}', t)
        await page.screenshot(path=f'{fdir}/{i:04d}.jpg', type='jpeg', quality=90)
    await page.close()
    return fdir

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (html, js) in R.items():
            if ONLY and name not in ONLY: continue
            await render(b, name, html, js)
            print('frames', name, flush=True)
        await b.close()
asyncio.run(main())
