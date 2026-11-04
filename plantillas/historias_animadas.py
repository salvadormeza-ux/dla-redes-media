"""Historias animadas Informática DLA: 1080x1920, 12 s, 30 fps. Uso: python3 anim.py OUTDIR [nombre ...]"""
import asyncio, os, sys, subprocess, shutil
from playwright.async_api import async_playwright

OUT = sys.argv[1]; ONLY = sys.argv[2:]
os.makedirs(OUT, exist_ok=True)
DUR, FPS = 12, 30

def G(i): return f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F472B6"/><stop offset="1" stop-color="#A78BFA"/></linearGradient></defs>'
LOGO = f'''<div class="logo"><svg width="130" height="130" viewBox="0 0 100 100">{G('lg')}
<circle cx="50" cy="50" r="48" fill="#0A0F28" stroke="url(#lg)" stroke-width="2.5"/>
<g fill="none" stroke="url(#lg)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
<rect x="24" y="27" width="52" height="34" rx="4"/><path d="M42 72h16M50 61v11"/><path d="M32 44h8l4-7 6 14 4-7h14"/></g>
<g fill="url(#lg)"><circle cx="32" cy="44" r="2.6"/><circle cx="68" cy="44" r="2.6"/></g></svg>
<div class="wm">INFORMÁTICA<br><span class="g" style="font-size:56px">DLA</span></div></div>'''

def ic(name, s=64, sw=2.6):
    p = {
      'mail': '<rect x="6" y="11" width="36" height="26" rx="3"/><path d="M7 13l17 13 17-13"/>',
      'key': '<circle cx="16" cy="24" r="8"/><path d="M24 24h18M36 24v7M41 24v5"/>',
      'bug': '<rect x="15" y="14" width="18" height="24" rx="9"/><path d="M24 14v24M8 22h7M33 22h7M8 32h7M33 32h7M18 9l3 5M30 9l-3 5"/>',
      'disk': '<ellipse cx="24" cy="12" rx="15" ry="5"/><path d="M9 12v24c0 3 7 5 15 5s15-2 15-5V12"/><path d="M9 24c0 3 7 5 15 5s15-2 15-5"/>',
      'cloud': '<path d="M14 36h22a9 9 0 0 0 0-18 12 12 0 0 0-23 3 8 8 0 0 0 1 15z"/>',
      'building': '<rect x="10" y="8" width="20" height="34"/><path d="M30 20h10v22H30M15 15h4M21 15h4M15 22h4M21 22h4M15 29h4M21 29h4M18 42v-6h4v6"/>',
      'lock': '<rect x="10" y="21" width="28" height="20" rx="3"/><path d="M16 21v-6a8 8 0 0 1 16 0v6"/>',
      'phone': '<rect x="14" y="4" width="20" height="40" rx="4"/><path d="M21 38h6"/>',
      'server': '<rect x="8" y="6" width="32" height="14" rx="2"/><rect x="8" y="26" width="32" height="14" rx="2"/><path d="M14 13h2M14 33h2M24 13h10M24 33h10"/>',
      'router': '<rect x="6" y="26" width="36" height="12" rx="3"/><path d="M14 26l-4-14M34 26l4-14M12 32h2M18 32h2"/>',
      'shield': '<path d="M24 5l15 6v11c0 10-7 17-15 21C16 39 9 32 9 22V11z"/><path d="M17 24l5 5 9-10"/>',
      'file': '<path d="M12 5h16l9 9v29H12z"/><path d="M28 5v9h9"/>',
    }[name]
    return f'<svg width="{s}" height="{s}" viewBox="0 0 48 48" fill="none" stroke="url(#i{name}{s})" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{G(f"i{name}{s}")}{p}</svg>'

BASE_CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0D1330;font-family:Inter,sans-serif;color:#fff;overflow:hidden;position:relative}
.g{background:linear-gradient(90deg,#F472B6,#A78BFA);-webkit-background-clip:text;background-clip:text;color:transparent}
.ring{position:absolute;border:2px solid rgba(167,139,250,.11);border-radius:50%;animation:spin 12s linear both}
@keyframes spin{from{transform:rotate(0) scale(1)}to{transform:rotate(25deg) scale(1.08)}}
.logo{position:absolute;left:88px;top:90px;display:flex;align-items:center;gap:26px;animation:fadeD .6s ease-out both}
.wm{font-weight:900;font-size:38px;letter-spacing:4px;line-height:1}
.foot{position:absolute;left:88px;bottom:110px;font-weight:800;font-size:38px;color:#C7CCE6;animation:fade .6s 10.4s both}
.src{position:absolute;left:88px;right:88px;bottom:60px;font-size:24px;color:#7F87B5;font-weight:500;animation:fade .5s 1s both}
.bar{position:absolute;left:0;bottom:0;height:10px;background:linear-gradient(90deg,#F472B6,#A78BFA);animation:grow 12s linear both}
@keyframes grow{from{width:0}to{width:100%}}
h1{font-weight:900;line-height:1.03;letter-spacing:-2px}
p{color:#C7CCE6;line-height:1.35;font-weight:500}
.card{background:#161E45;border:2px solid #2A3470;border-radius:28px;padding:36px}
.tag{display:inline-block;border:2px solid #2A3470;color:#C7CCE6;border-radius:999px;padding:10px 26px;font-weight:800;font-size:28px;letter-spacing:2px}
.alert{border-color:#F472B6;color:#F9A8D4;animation:pulse 1s ease-in-out 8 both}
.btn{display:inline-block;background:linear-gradient(90deg,#F472B6,#A78BFA);color:#0D1330;font-weight:900;border-radius:999px;padding:26px 46px;font-size:42px}
.abs{position:absolute;left:88px;right:88px}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes fadeD{from{opacity:0;transform:translateY(-20px)}to{opacity:1;transform:none}}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
@keyframes pop{0%{opacity:0;transform:scale(.6)}70%{opacity:1;transform:scale(1.06)}100%{opacity:1;transform:scale(1)}}
@keyframes out{from{opacity:1}to{opacity:0;transform:translateY(-40px)}}
@keyframes left{from{opacity:0;transform:translateX(-120px)}to{opacity:1;transform:none}}
@keyframes right{from{opacity:0;transform:translateX(160px)}to{opacity:1;transform:none}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(244,114,182,0)}50%{box-shadow:0 0 0 14px rgba(244,114,182,.18)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.15}}
@keyframes shake{0%,100%{transform:none}20%{transform:translateX(-14px)}40%{transform:translateX(14px)}60%{transform:translateX(-8px)}80%{transform:translateX(8px)}}
@keyframes draw{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
@keyframes hl{from{opacity:0;transform:scale(1.15)}to{opacity:1;transform:scale(1)}}
.hook{animation:pop .55s .15s both}
'''
RINGS = '<div class="ring" style="width:1190px;height:1190px;right:-486px;top:-378px"></div><div class="ring" style="width:810px;height:810px;right:-292px;top:-184px"></div><div class="ring" style="width:972px;height:972px;left:-540px;bottom:-432px"></div>'
def A(name, delay, dur=.6, ease='cubic-bezier(.2,.8,.2,1)'):
    return f'animation:{name} {dur}s {ease} {delay}s both'
CTA = f'<div class="abs" style="bottom:200px;{A("up",10.2)}"><span class="btn">Escríbenos por mensaje directo</span></div>'

S = {}  # nombre -> (html, js_tick)

# 1. Zyxel GS1900
ports = ''.join(f'<div style="width:46px;height:38px;border:3px solid #2A3470;border-radius:6px;background:#0A0F28;position:relative"><div style="position:absolute;top:-14px;left:16px;width:10px;height:10px;border-radius:50%;background:{"#86EFAC" if i%3 else "#FBBF24"};animation:blink {.5+i%4*.17}s steps(1) infinite"></div></div>' for i in range(12))
S['2026-11-05_zyxel'] = (f'''
<div class="abs" style="top:330px"><span class="tag alert" style="{A('pop',.1,.5)}">ALERTA DE SEGURIDAD</span></div>
<h1 class="abs hook" style="top:430px;font-size:104px">¿Tu oficina tiene un switch <span class="g">Zyxel GS1900</span>?</h1>
<div class="abs card" style="top:820px;padding:44px;{A('up',1.6)}"><div style="display:flex;gap:16px;justify-content:space-between">{ports}</div>
<div style="margin-top:26px;font-weight:800;font-size:30px;color:#7F87B5;letter-spacing:3px">SWITCH · OFICINA</div></div>
<div class="abs card" style="top:1110px;border-color:#F472B6;{A('pop',3,.5)}"><p style="font-size:40px;color:#fff;font-weight:800">CVE-2026-7273</p>
<p style="font-size:36px">Falla que permite tomar control del switch. CISA la incluyó en su lista de vulnerabilidades <b style="color:#fff">explotadas activamente</b>.</p></div>
<div class="abs" style="top:1470px;display:flex;flex-direction:column;gap:18px">
<p style="font-size:40px;color:#fff;font-weight:800;{A('left',6)}">→ Revisa el modelo y la versión</p>
<p style="font-size:40px;color:#fff;font-weight:800;{A('left',6.8)}">→ Actualiza el firmware</p>
<p style="font-size:40px;color:#fff;font-weight:800;{A('left',7.6)}">→ Administración cerrada a internet</p></div>
<div class="src">Fuentes: CISA KEV y BleepingComputer, sept. 2026</div>''', '')

# 2. Phishing
S['2026-11-06_phishing'] = (f'''
<h1 class="abs hook" style="top:320px;font-size:100px">Este correo parece real. <span class="g">¿Lo abrirías?</span></h1>
<div class="abs card" style="top:700px;padding:0;overflow:hidden;{A('right',1.2,.7)}">
<div style="background:#1E2756;padding:26px 36px;display:flex;gap:20px;align-items:center">{ic('mail',56)}<p style="font-size:30px;color:#fff;font-weight:800">Bandeja de entrada</p></div>
<div style="padding:40px 36px;display:flex;flex-direction:column;gap:30px;position:relative">
<div id="h1" style="position:relative;border-radius:16px;padding:12px 16px"><p style="font-size:28px;color:#7F87B5">De:</p><p style="font-size:34px;color:#fff;font-weight:700">Tu Banco &lt;seguridad@tubanco-verifica.co&gt;</p></div>
<div id="h2" style="position:relative;border-radius:16px;padding:12px 16px"><p style="font-size:42px;color:#fff;font-weight:900">Tu cuenta será bloqueada HOY</p><p style="font-size:32px">Confirma tus datos en las próximas 2 horas.</p></div>
<div id="h3" style="position:relative;border-radius:16px;padding:16px;align-self:flex-start"><span style="background:#3B82F6;color:#fff;font-weight:800;font-size:34px;padding:20px 40px;border-radius:12px;display:inline-block">Verificar ahora</span></div>
</div></div>
<style>#h1{{animation:hlb .4s 3.4s both}}#h2{{animation:hlb .4s 4.9s both}}#h3{{animation:hlb .4s 6.4s both}}
@keyframes hlb{{from{{box-shadow:0 0 0 0 transparent}}to{{box-shadow:0 0 0 5px #F472B6}}}}</style>
<div class="abs" style="top:1460px;display:flex;gap:18px;flex-wrap:wrap">
<span class="tag alert" style="font-size:32px;{A('pop',3.5,.4)}">Remitente raro</span>
<span class="tag alert" style="font-size:32px;{A('pop',5,.4)}">Urgencia</span>
<span class="tag alert" style="font-size:32px;{A('pop',6.5,.4)}">Enlace sospechoso</span></div>
<h1 class="abs" style="top:1600px;font-size:60px;{A('up',8.2)}">Ante la duda, <span class="g">no hagas clic</span>: entra tú mismo al sitio.</h1>
<div class="foot">informaticadla.cl</div>''', '')

# 3. Doble factor
S['2026-11-07_2fa'] = (f'''
<h1 class="abs hook" style="top:320px;font-size:104px">Te robaron la contraseña. <span class="g">¿Y ahora?</span></h1>
<div class="abs card" style="top:720px;{A('up',1.2)}"><p style="font-size:30px;color:#7F87B5;font-weight:700">correo@tuempresa.cl</p>
<div style="margin-top:20px;background:#0A0F28;border:2px solid #2A3470;border-radius:14px;padding:22px 26px;font-size:50px;letter-spacing:10px;color:#fff" id="pw">&nbsp;</div>
<p id="st" style="margin-top:22px;font-size:34px;font-weight:800;color:#FBBF24">&nbsp;</p></div>
<div class="abs" style="top:1070px;display:flex;justify-content:center;{A('up',4.2,.7)}">
<div style="width:640px;height:420px;border:4px solid #2A3470;border-radius:56px;background:#0A0F28;padding:44px 36px;display:flex;flex-direction:column;align-items:center;gap:26px;{A('shake',6.2,.5,'ease')}">
{ic('shield',90)}<p style="font-size:36px;color:#fff;font-weight:800;text-align:center">¿Estás intentando iniciar sesión?</p>
<div style="display:flex;gap:16px"><span style="border:2px solid #2A3470;border-radius:14px;padding:14px 22px;font-size:28px;font-weight:800">Sí, soy yo</span>
<span style="background:linear-gradient(90deg,#F472B6,#A78BFA);color:#0D1330;border-radius:14px;padding:14px 22px;font-size:28px;font-weight:900;{A('pop',5.6,.4)}">No fui yo</span></div></div></div>
<h1 class="abs" style="top:1530px;font-size:72px;text-align:center;{A('pop',6.8,.5)}"><span class="g">Acceso bloqueado</span></h1>
<p class="abs" style="top:1650px;font-size:42px;color:#fff;font-weight:700;{A('up',8.2)}">Con doble factor, la contraseña sola no basta. Actívalo hoy en tu correo.</p>
''',
'''var pw="••••••••••••";var n=Math.max(0,Math.min(pw.length,Math.floor((t-1.8)*7)));
document.getElementById('pw').textContent=n?pw.slice(0,n):'\\u00a0';
document.getElementById('st').textContent=t<3.6?'\\u00a0':(t<6.6?'Contraseña correcta. Verificando…':'Intento bloqueado');
document.getElementById('st').style.color=t<6.6?'#FBBF24':'#86EFAC';''')

# 4. Contraseñas
S['2026-11-08_contrasenas'] = (f'''
<h1 class="abs hook" style="top:320px;font-size:100px">¿Tu contraseña es <span class="g">la de siempre</span>?</h1>
<div class="abs card" style="top:740px;{A('up',1)}"><p style="font-size:30px;color:#7F87B5;font-weight:700">Nueva contraseña</p>
<div style="margin-top:18px;background:#0A0F28;border:2px solid #2A3470;border-radius:14px;padding:24px;font-size:52px;font-weight:800;color:#fff;min-height:110px" id="pw"></div>
<div style="margin-top:28px;height:24px;background:#0A0F28;border-radius:12px;overflow:hidden"><div id="m" style="height:100%;width:0;border-radius:12px"></div></div>
<p id="lv" style="margin-top:18px;font-size:40px;font-weight:900">&nbsp;</p></div>
<div class="abs" style="top:1250px;display:flex;flex-direction:column;gap:22px">
<p style="font-size:42px;color:#fff;font-weight:800;{A('left',7.6)}">→ Usa frases largas, no palabras con año</p>
<p style="font-size:42px;color:#fff;font-weight:800;{A('left',8.3)}">→ Una distinta para cada servicio</p>
<p style="font-size:42px;color:#fff;font-weight:800;{A('left',9)}">→ Guárdalas en un gestor de contraseñas</p></div>
<div class="foot">informaticadla.cl</div>''',
'''var a="Empresa2024",b="caballo-azul-lluvia-mesa",s,w,c,l;
if(t<4){var n=Math.max(0,Math.min(a.length,Math.floor((t-1.4)*9)));s=a.slice(0,n);w=n/a.length*22;c='#F87171';l=n==a.length?'Débil':'';}
else{var n=Math.max(0,Math.min(b.length,Math.floor((t-4.2)*11)));s=b.slice(0,n);w=Math.max(22,n/b.length*100);c=n==b.length?'#86EFAC':'#FBBF24';l=n==b.length?'Fuerte':'';}
document.getElementById('pw').textContent=s;var m=document.getElementById('m');m.style.width=w+'%';m.style.background=c;
var L=document.getElementById('lv');L.textContent=l||'\\u00a0';L.style.color=c;''')

# 5. Dato Sophos
S['2026-11-09_dato'] = (f'''
<div class="abs" style="top:330px"><span class="tag" style="{A('pop',.1,.5)}">DATO DE LA SEMANA · CHILE</span></div>
<h1 class="abs hook" style="top:440px;font-size:250px;letter-spacing:-8px"><span class="g" id="n">0%</span></h1>
<h1 class="abs" style="top:760px;font-size:76px;{A('up',2.4)}">de los ataques de ransomware entró por una <span class="g">vulnerabilidad sin parchar</span></h1>
<div class="abs" style="top:1230px;display:flex;gap:22px;{A('up',5)}">
{''.join(f'<div class="card" style="flex:1;text-align:center;padding:40px 10px;{A("pop",5.2+i*.35,.45)}">{ic(x,100)}<p style="margin-top:14px;font-size:30px;color:#fff;font-weight:800">{y}</p></div>' for i,(x,y) in enumerate([("bug","33%"),("mail","31%"),("key","21%")]))}</div>
<p class="abs" style="top:1560px;font-size:44px;color:#fff;font-weight:700;{A('up',7.8)}">Actualizar Windows, firewall y servidores es cerrar la primera puerta.</p>
<div class="src">Fuente: Sophos, The State of Ransomware in Chile 2026</div>''',
'''var v=Math.round(Math.min(1,Math.max(0,(t-.4)/1.6))**.6*33);document.getElementById('n').textContent=v+'%';''')

# 6. Teaser reel
doors = ''.join(f'''<div style="flex:1;height:520px;position:relative;perspective:900px">
<div class="card" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px">{ic(x,120)}<p style="font-size:34px;color:#fff;font-weight:800">{y}</p></div>
<div style="position:absolute;inset:0;background:#1E2756;border:2px solid #2A3470;border-radius:28px;transform-origin:left;animation:door 7s {1.6+i*.4}s both"><div style="position:absolute;right:30px;top:250px;width:16px;height:16px;border-radius:50%;background:#A78BFA"></div></div>
<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);{A('pop',7.4+i*.3,.4)}">{ic('lock',110,3.2)}</div></div>''' for i,(x,y) in enumerate([("bug","Parches"),("mail","Correo"),("key","Claves")]))
S['2026-11-10_reel'] = (f'''<style>@keyframes door{{0%{{transform:rotateY(0)}}18%,80%{{transform:rotateY(-78deg)}}100%{{transform:rotateY(0)}}}}</style>
<div class="abs" style="top:330px"><span class="tag" style="{A('pop',.1,.5)}">NUEVO REEL</span></div>
<h1 class="abs hook" style="top:440px;font-size:100px">Las <span class="g">3 puertas</span> por donde entra el ransomware</h1>
<div class="abs" style="top:900px;display:flex;gap:24px">{doors}</div>
<p class="abs" style="top:1520px;font-size:46px;color:#fff;font-weight:700;{A('up',8.6)}">Y cómo cerrarlas. Míralo completo en nuestro perfil.</p>
<div class="foot">informaticadla.cl</div>''', '')

# 7. Regla 3-2-1
S['2026-11-11_321'] = (f'''
<h1 class="abs hook" style="top:320px;font-size:100px">La regla <span class="g">3-2-1</span> de los respaldos</h1>
<div class="abs card" style="top:640px;display:flex;align-items:center;gap:34px;{A('left',1.2)}"><h1 style="font-size:130px" class="g">3</h1>
<div><p style="font-size:42px;color:#fff;font-weight:900">copias de tu información</p><div style="display:flex;gap:14px;margin-top:12px">{''.join(f'<span style="{A("pop",1.8+i*.3,.35)}">{ic("file",64)}</span>' for i in range(3))}</div></div></div>
<div class="abs card" style="top:960px;display:flex;align-items:center;gap:34px;{A('left',3.4)}"><h1 style="font-size:130px" class="g">2</h1>
<div><p style="font-size:42px;color:#fff;font-weight:900">medios distintos</p><div style="display:flex;gap:14px;margin-top:12px"><span style="{A('pop',4,.35)}">{ic('disk',64)}</span><span style="{A('pop',4.3,.35)}">{ic('cloud',64)}</span></div></div></div>
<div class="abs card" style="top:1280px;display:flex;align-items:center;gap:34px;{A('left',5.6)}"><h1 style="font-size:130px" class="g">1</h1>
<div><p style="font-size:42px;color:#fff;font-weight:900">fuera de la oficina</p><div style="display:flex;gap:14px;margin-top:12px"><span style="{A('pop',6.2,.35)}">{ic('building',64)}</span></div></div></div>
<p class="abs" style="top:1620px;font-size:44px;color:#fff;font-weight:700;{A('up',8)}">¿Tu empresa la cumple? Cuéntanos por mensaje directo.</p>''', '')

# 8. Las 3 puertas (barras)
bars = ''.join(f'''<div style="display:flex;flex-direction:column;gap:14px;{A('up',1.4+i*.6)}"><div style="display:flex;justify-content:space-between;align-items:center">
<div style="display:flex;gap:20px;align-items:center">{ic(x,64)}<p style="font-size:38px;color:#fff;font-weight:800">{y}</p></div><h1 style="font-size:64px" class="g">{v}%</h1></div>
<div style="height:30px;background:#161E45;border:2px solid #2A3470;border-radius:16px;overflow:hidden"><div style="height:100%;width:{v*2.5}%;background:linear-gradient(90deg,#F472B6,#A78BFA);border-radius:16px;animation:gw 1.2s cubic-bezier(.2,.8,.2,1) {1.8+i*.6}s both"></div></div></div>''' for i,(x,y,v) in enumerate([("bug","Vulnerabilidades sin parchar",33),("mail","Correos maliciosos",31),("key","Credenciales robadas",21)]))
S['2026-11-12_puertas'] = (f'''<style>@keyframes gw{{from{{transform:scaleX(0);transform-origin:left}}to{{transform:scaleX(1);transform-origin:left}}}}</style>
<h1 class="abs hook" style="top:320px;font-size:96px">¿Por dónde entra el <span class="g">ransomware</span> en Chile?</h1>
<div class="abs" style="top:780px;display:flex;flex-direction:column;gap:60px">{bars}</div>
<p class="abs" style="top:1500px;font-size:44px;color:#fff;font-weight:700;{A('up',6.5)}">Cómo cerrar cada puerta: mira nuestro carrusel de hoy.</p>
<div class="src">Fuente: Sophos, The State of Ransomware in Chile 2026 · causas técnicas más frecuentes</div>''', '')

# 9. Wifi visitas
S['2026-11-13_wifi'] = (f'''<style>@keyframes gx{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}</style>
<div class="abs" style="top:330px"><span class="tag" style="{A('pop',.1,.5)}">TIP DE REDES</span></div>
<h1 class="abs hook" style="top:430px;font-size:96px">El wifi de visitas <span class="g">no debería llegar</span> a tus servidores</h1>
<div class="abs" style="top:960px;display:flex;align-items:center">
<div class="card" style="text-align:center;padding:24px;{A('pop',1,.45)}">{ic('phone',96)}<p style="font-size:28px;color:#fff;font-weight:800;margin-top:10px">Visita</p></div>
<div style="flex:1;height:10px;margin:0 6px;border-radius:5px;background:linear-gradient(90deg,#F472B6,#A78BFA);transform-origin:left;animation:gx 1s 1.8s both"></div>
<div class="card" style="text-align:center;padding:30px;{A('pop',1.3,.45)}">{ic('router',110)}<p style="font-size:28px;color:#fff;font-weight:800;margin-top:10px">Router</p></div>
<div style="flex:1;margin:0 6px;position:relative;height:10px"><div style="position:absolute;inset:0;border-radius:5px;background:#F87171;transform-origin:left;animation:gx .9s 3.2s both, fade .3s 5s reverse both"></div>
<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);{A('pop',4.8,.4)}">{ic('shield',84,3.4)}</div></div>
<div class="card" style="text-align:center;padding:30px;{A('pop',1.6,.45)}">{ic('server',110)}<p style="font-size:28px;color:#fff;font-weight:800;margin-top:10px">Servidor</p></div></div>
<p class="abs" style="top:1240px;font-size:36px;font-weight:800;color:#F9A8D4;{A('pop',3.6,.4)}">Un equipo infectado de una visita podría llegar a tus servidores…</p>
<h1 class="abs" style="top:1400px;font-size:62px;{A('up',5.8)}">Red de visitas <span class="g">separada</span>: solo internet, nada más.</h1>
<p class="abs" style="top:1580px;font-size:40px;color:#fff;font-weight:700;{A('up',7.6)}">Cámaras e impresoras también en su propio segmento.</p>
<div class="foot">informaticadla.cl</div>''', '')

# 10. VMware ESXi
leds = ''.join(f'<div style="width:14px;height:14px;border-radius:50%;background:#86EFAC;animation:blink {.4+i*.13}s steps(1) infinite"></div>' for i in range(5))
rack = ''.join(f'<div class="card" style="padding:24px 30px;display:flex;justify-content:space-between;align-items:center;{A("left",1.4+i*.3,.5)}"><p style="font-size:30px;color:#fff;font-weight:800">ESXi-0{i+1}</p><div style="display:flex;gap:12px">{leds}</div></div>' for i in range(3))
S['2026-11-14_esxi'] = (f'''
<div class="abs" style="top:330px"><span class="tag alert" style="{A('pop',.1,.5)}">ALERTA DE SEGURIDAD</span></div>
<h1 class="abs hook" style="top:430px;font-size:100px">¿Tienes servidores con <span class="g">VMware ESXi</span>?</h1>
<div class="abs" style="top:780px;display:flex;flex-direction:column;gap:18px">{rack}</div>
<div class="abs card" style="top:1180px;border-color:#F472B6;{A('pop',3.2,.5)}"><p style="font-size:40px;color:#fff;font-weight:800">CVE-2026-41709</p>
<p style="font-size:36px">Atacantes con acceso de administrador la usaron para que sus acciones <b style="color:#fff">no quedaran en los registros</b>. Parche disponible desde julio.</p></div>
<div class="abs" style="top:1540px;display:flex;flex-direction:column;gap:18px">
<p style="font-size:40px;color:#fff;font-weight:800;{A('left',6.4)}">→ Actualiza ESXi a la versión corregida</p>
<p style="font-size:40px;color:#fff;font-weight:800;{A('left',7.2)}">→ Revisa registros y cuentas de administración</p></div>
<div class="src">Fuentes: CISA KEV (28-10-2026) y The Hacker News</div>''', '')

# 11. Costo
S['2026-11-15_costo'] = (f'''
<h1 class="abs hook" style="top:320px;font-size:92px">¿Cuánto cuesta recuperarse de un <span class="g">ransomware</span>?</h1>
<h1 class="abs" style="top:700px;font-size:150px;white-space:nowrap;letter-spacing:-5px;{A('pop',1.4,.4)}"><span class="g" id="n">US$ 0</span></h1>
<p class="abs" style="top:940px;font-size:42px;{A('up',3.6)}">Promedio en Chile, <b style="color:#fff">sin contar el rescate</b>.</p>
<div class="abs card" style="top:1120px;display:flex;align-items:center;gap:30px;{A('up',5.2)}">{ic('disk',110)}
<p style="font-size:42px;color:#fff;font-weight:800">Respaldos automáticos, fuera de la red y probados: tu plan B.</p></div>
<p class="abs" style="top:1420px;font-size:42px;{A('up',7)}">En Informática DLA los dejamos funcionando y te avisamos si algo falla.</p>
{CTA}<div class="foot" style="bottom:110px">informaticadla.cl</div>
<div class="src">Fuente: Sophos, The State of Ransomware in Chile 2026</div>''',
'''var k=Math.min(1,Math.max(0,(t-1.6)/1.8));k=1-Math.pow(1-k,3);var v=1.04*k;
document.getElementById('n').textContent='US$ '+v.toFixed(2).replace('.',',')+' M';''')

async def render(b, name, html, js):
    page = await b.new_page(viewport={'width': 1080, 'height': 1920})
    doc = f'<html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{RINGS}{LOGO}{html}<div class="bar"></div><script>window.tick=function(t){{{js}}}</script></body></html>'
    await page.set_content(doc); await page.wait_for_timeout(300)
    fdir = f'{OUT}/_f_{name}'; shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
    for i in range(DUR*FPS):
        t = i / FPS
        await page.evaluate('t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});window.tick(t)}', t)
        await page.screenshot(path=f'{fdir}/{i:04d}.jpg', type='jpeg', quality=92)
    await page.close()
    return fdir

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (html, js) in S.items():
            if ONLY and name not in ONLY: continue
            fdir = await render(b, name, html, js)
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{fdir}/%04d.jpg','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',f'{OUT}/v_{name}.mp4'], check=True)
            print('ok', name, flush=True)
        await b.close()
asyncio.run(main())
