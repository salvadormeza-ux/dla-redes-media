import asyncio, os, sys, base64
from playwright.async_api import async_playwright

OUT = sys.argv[1]
LOGO_FILE = sys.argv[2] if len(sys.argv) > 2 else None   # archivo de logo real, si existe
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

def grad(id_):
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F472B6"/><stop offset="1" stop-color="#A78BFA"/></linearGradient></defs>'

# Logo: ícono de monitor/circuito en degradado sobre círculo azul marino + wordmark blanco
def logo_badge(size=150):
    if LOGO_FILE:
        mime = 'image/png' if LOGO_FILE.lower().endswith('png') else 'image/jpeg'
        b64 = base64.b64encode(open(LOGO_FILE, 'rb').read()).decode()
        return f'<img src="data:{mime};base64,{b64}" style="height:{size}px">'
    s = size
    return f'''<div style="display:flex;align-items:center;gap:28px">
<svg width="{s}" height="{s}" viewBox="0 0 100 100">{grad('lg')}
<circle cx="50" cy="50" r="48" fill="#0A0F28" stroke="url(#lg)" stroke-width="2.5"/>
<g fill="none" stroke="url(#lg)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
<rect x="24" y="27" width="52" height="34" rx="4"/><path d="M42 72h16M50 61v11"/>
<path d="M32 44h8l4-7 6 14 4-7h14"/></g>
<g fill="url(#lg)"><circle cx="32" cy="44" r="2.6"/><circle cx="68" cy="44" r="2.6"/></g></svg>
<div style="font-weight:900;font-size:{int(s*0.3)}px;letter-spacing:{int(s*0.03)}px;color:#fff;line-height:1">INFORMÁTICA<br><span style="font-size:{int(s*0.42)}px" class="g">DLA</span></div></div>'''

def icon(name, s=64):
    p = {
      'shield': '<path d="M24 5l15 6v11c0 10-7 17-15 21C16 39 9 32 9 22V11z"/><path d="M17 24l5 5 9-10"/>',
      'mail': '<rect x="6" y="11" width="36" height="26" rx="3"/><path d="M7 13l17 13 17-13"/>',
      'key': '<circle cx="16" cy="24" r="8"/><path d="M24 24h18M36 24v7M41 24v5"/>',
      'bug': '<rect x="15" y="14" width="18" height="24" rx="9"/><path d="M24 14v24M8 22h7M33 22h7M8 32h7M33 32h7M18 9l3 5M30 9l-3 5"/>',
      'disk': '<ellipse cx="24" cy="12" rx="15" ry="5"/><path d="M9 12v24c0 3 7 5 15 5s15-2 15-5V12"/><path d="M9 24c0 3 7 5 15 5s15-2 15-5"/>',
      'refresh': '<path d="M39 20A15 15 0 0 0 11 15M9 28a15 15 0 0 0 28 5"/><path d="M11 7v8h8M37 41v-8h-8"/>',
      'lock': '<rect x="10" y="21" width="28" height="20" rx="3"/><path d="M16 21v-6a8 8 0 0 1 16 0v6"/>',
      'check': '<circle cx="24" cy="24" r="17"/><path d="M16 24l6 6 11-12"/>',
      'wifi': '<path d="M6 18a26 26 0 0 1 36 0M12 25a17 17 0 0 1 24 0M18 32a8 8 0 0 1 12 0"/><circle cx="24" cy="38" r="2"/>',
      'bolt': '<path d="M27 4L10 27h12l-3 17 17-24H24z"/>',
      'pulse': '<rect x="5" y="9" width="38" height="26" rx="3"/><path d="M12 22h6l3-6 5 12 3-6h7"/><path d="M18 41h12"/>',
      'phone2fa': '<rect x="14" y="4" width="20" height="40" rx="4"/><path d="M19 22l4 4 7-8"/>',
      'wrench': '<path d="M30 6a10 10 0 0 0-9 14L7 34l7 7 14-14a10 10 0 0 0 14-9l-6 6-6-2-2-6z"/>',
      'play': '<circle cx="24" cy="24" r="18"/><path d="M20 16l12 8-12 8z"/>',
      'firewall': '<rect x="6" y="10" width="36" height="28" rx="2"/><path d="M6 19h36M6 28h36M18 10v9M30 19v9M18 28v10"/>',
    }[name]
    return f'<svg width="{s}" height="{s}" viewBox="0 0 48 48" fill="none" stroke="url(#i{name}{s})" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{grad(f"i{name}{s}")}{p}</svg>'

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#0D1330;font-family:Inter,sans-serif;color:#fff;overflow:hidden;position:relative}
.rings div{position:absolute;border:2px solid rgba(167,139,250,.10);border-radius:50%}
.wrap{position:relative;height:100%;display:flex;flex-direction:column;padding:90px 88px 110px}
.g{background:linear-gradient(90deg,#F472B6,#A78BFA);-webkit-background-clip:text;background-clip:text;color:transparent}
h1{font-weight:900;line-height:1.03;letter-spacing:-2px}
p{color:#C7CCE6;line-height:1.35;font-weight:500}
.card{background:#161E45;border:2px solid #2A3470;border-radius:28px;padding:40px}
.btn{display:inline-block;background:linear-gradient(90deg,#F472B6,#A78BFA);color:#0D1330;font-weight:900;border-radius:999px;padding:26px 46px;font-size:42px}
.src{color:#7F87B5;font-size:26px;font-weight:500}
.tag{display:inline-block;align-self:flex-start;border:2px solid #2A3470;color:#C7CCE6;border-radius:999px;padding:10px 26px;font-weight:700;font-size:28px;letter-spacing:1px}
.row{display:flex;gap:28px;align-items:center}
.ok{color:#86EFAC;border-color:#2F6B4A}
'''
RINGS = '<div class="rings"><div style="width:1190px;height:1190px;right:-486px;top:-378px"></div><div style="width:810px;height:810px;right:-292px;top:-184px"></div><div style="width:972px;height:972px;left:-540px;bottom:-432px"></div></div>'
SRC = '<div class="src">Fuente: Sophos, The State of Ransomware in Chile 2026</div>'
CTA = '<div style="display:flex;flex-direction:column;gap:26px;align-items:flex-start"><span class="btn">Escríbenos por mensaje directo</span><span style="font-weight:800;font-size:40px;color:#C7CCE6">informaticadla.cl</span></div>'
WEB = '<div style="font-weight:800;font-size:36px;color:#C7CCE6">informaticadla.cl</div>'

def mid(inner, gap=46):
    return f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:{gap}px">{inner}</div>'

H_ = {}
# ---- Semana actual ----
H_['2026-11-05_firewall'] = mid(f'''<span class="tag">TIP DE REDES</span>{icon('firewall',120)}
<h1 style="font-size:96px">¿Cuándo cambiaste la <span class="g">contraseña del firewall</span>?</h1>
<div class="card"><p style="font-size:40px">Las credenciales de firewalls y VPN son hoy una de las puertas favoritas para entrar a una red. Doble factor y contraseñas nuevas cierran buena parte del riesgo.</p></div>''') + WEB
H_['2026-11-06_automatizar'] = mid(f'''<span class="tag">PREGUNTA RÁPIDA</span>{icon('bolt',120)}
<h1 style="font-size:96px">¿Qué tarea <span class="g">repetitiva</span> le quita más tiempo a tu equipo?</h1>
<div class="card" style="display:flex;flex-direction:column;gap:26px">
<div class="row">{icon('mail',56)}<p style="font-size:40px;color:#fff;font-weight:700">Ordenar correos y formularios</p></div>
<div class="row">{icon('disk',56)}<p style="font-size:40px;color:#fff;font-weight:700">Copiar datos a planillas</p></div>
<div class="row">{icon('pulse',56)}<p style="font-size:40px;color:#fff;font-weight:700">Armar los mismos reportes</p></div></div>
<p style="font-size:38px">Esas tareas se pueden automatizar con IA. Cuéntanos la tuya por mensaje directo.</p>''')
H_['2026-11-07_2fa'] = mid(f'''<span class="tag">TIP DE SEGURIDAD</span>{icon('phone2fa',130)}
<h1 style="font-size:100px">Activa el <span class="g">doble factor</span> en tu correo</h1>
<div class="card" style="display:flex;flex-direction:column;gap:22px">
<p style="font-size:38px"><b style="color:#fff">1.</b> Configuración de seguridad de tu cuenta</p>
<p style="font-size:38px"><b style="color:#fff">2.</b> Verificación en dos pasos con app autenticadora</p>
<p style="font-size:38px"><b style="color:#fff">3.</b> Guarda los códigos de respaldo</p></div>
<p style="font-size:38px">Una contraseña robada no debería bastar para entrar.</p>''') + WEB
H_['2026-11-08_monitor'] = mid(f'''<span class="tag">DLA MONITOR</span>
<h1 style="font-size:100px">Vigilamos tu red y servidores <span class="g">24/7</span></h1>
<div class="card" style="display:flex;flex-direction:column;gap:24px">
<div style="display:flex;justify-content:space-between;align-items:center"><p style="font-size:36px;color:#fff;font-weight:800">Servidor principal</p><span class="tag ok">OK</span></div>
<div style="display:flex;justify-content:space-between;align-items:center"><p style="font-size:36px;color:#fff;font-weight:800">Temperatura · Discos</p><span class="tag ok">OK</span></div>
<div style="display:flex;justify-content:space-between;align-items:center"><p style="font-size:36px;color:#fff;font-weight:800">Internet y firewall</p><span class="tag ok">OK</span></div></div>
<p style="font-size:40px">Si algo se sale de lo normal, te avisamos antes de que se convierta en un problema.</p>''') + CTA
# ---- Semana 9–15 ----
H_['2026-11-09_dato'] = mid(f'''<span class="tag">DATO DE LA SEMANA</span>
<h1 style="font-size:132px">1 de cada 3</h1>
<h1 style="font-size:76px">ataques de ransomware en Chile entró por una <span class="g">vulnerabilidad sin parchar</span></h1>
<div class="card row">{icon('refresh',88)}<p style="font-size:40px">Mantener sistemas y equipos actualizados es la primera puerta que conviene cerrar.</p></div>''') + SRC
H_['2026-11-10_reel'] = mid(f'''<span class="tag">NUEVO REEL</span>{icon('play',140)}
<h1 style="font-size:104px">Las <span class="g">3 puertas</span> por donde entra el ransomware</h1>
<p style="font-size:44px">Y cómo cerrarlas en tu empresa. Míralo en nuestro perfil.</p>''') + WEB
H_['2026-11-11_pregunta'] = mid(f'''<span class="tag">PREGUNTA RÁPIDA</span>
<h1 style="font-size:96px">¿Cuándo fue la última vez que <span class="g">probaste restaurar</span> un respaldo?</h1>
<div class="card" style="display:flex;flex-direction:column;gap:26px">
<div class="row">{icon('check',60)}<p style="font-size:40px;color:#fff;font-weight:700">Este mes</p></div>
<div class="row">{icon('disk',60)}<p style="font-size:40px;color:#fff;font-weight:700">Hace más de un año</p></div>
<div class="row">{icon('lock',60)}<p style="font-size:40px;color:#fff;font-weight:700">Nunca lo hemos probado</p></div></div>
<p style="font-size:38px">Un respaldo que nunca se restauró es una promesa, no una garantía. Cuéntanos por mensaje directo.</p>''')
H_['2026-11-12_puertas'] = mid(f'''<h1 style="font-size:92px">Por dónde entra el <span class="g">ransomware</span> en Chile</h1>
<div class="card row">{icon('bug',80)}<div><h1 style="font-size:64px">33%</h1><p style="font-size:36px">Vulnerabilidades sin parchar</p></div></div>
<div class="card row">{icon('mail',80)}<div><h1 style="font-size:64px">31%</h1><p style="font-size:36px">Correos maliciosos</p></div></div>
<div class="card row">{icon('key',80)}<div><h1 style="font-size:64px">21%</h1><p style="font-size:36px">Credenciales robadas</p></div></div>
<p style="font-size:36px">Cómo cerrar cada una: revisa nuestro carrusel de hoy.</p>''', 38) + SRC
H_['2026-11-13_wifi'] = mid(f'''<span class="tag">TIP DE REDES</span>{icon('wifi',130)}
<h1 style="font-size:96px">El wifi de visitas <span class="g">no debería ver</span> tus equipos</h1>
<div class="card" style="display:flex;flex-direction:column;gap:22px">
<p style="font-size:38px"><b style="color:#fff">1.</b> Red de visitas separada, solo con internet</p>
<p style="font-size:38px"><b style="color:#fff">2.</b> Cámaras e impresoras en su propio segmento</p>
<p style="font-size:38px"><b style="color:#fff">3.</b> Reglas de firewall entre segmentos</p></div>''') + WEB
H_['2026-11-14_soporte'] = mid(f'''<span class="tag">SOPORTE Y MANTENCIÓN</span>{icon('wrench',120)}
<h1 style="font-size:100px">Que la tecnología <span class="g">no frene</span> tu trabajo</h1>
<div class="card" style="display:flex;flex-direction:column;gap:22px">
<div class="row">{icon('check',52)}<p style="font-size:38px;color:#fff;font-weight:700">Soporte remoto y en terreno</p></div>
<div class="row">{icon('check',52)}<p style="font-size:38px;color:#fff;font-weight:700">Mantención preventiva de equipos</p></div>
<div class="row">{icon('check',52)}<p style="font-size:38px;color:#fff;font-weight:700">Notebooks, monitores y servidores</p></div></div>''') + CTA
H_['2026-11-15_respaldos'] = mid(f'''<h1 style="font-size:100px">¿Tus respaldos se hacen <span class="g">solos</span>?</h1>
<div class="card" style="display:flex;flex-direction:column;gap:22px">
<div style="display:flex;justify-content:space-between;align-items:center"><p style="font-size:34px;color:#fff;font-weight:800">Respaldo diario</p><span class="tag ok">OK · 03:00</span></div>
<div style="height:14px;background:#0D1330;border-radius:9px"><div style="width:100%;height:100%;border-radius:9px;background:linear-gradient(90deg,#F472B6,#A78BFA)"></div></div>
<p style="font-size:32px">Copia fuera de la red · Prueba de restauración mensual · Aviso si algo falla</p></div>
<p style="font-size:42px">Automatizamos los respaldos de tu empresa y te avisamos si algo no anda bien.</p>''') + CTA

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': W, 'height': H})
        for name, body in H_.items():
            html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{RINGS}<div class="wrap">{logo_badge()}{body}</div></body></html>'
            await pg.set_content(html); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'{OUT}/historia_{name}.png')
        await b.close()
asyncio.run(main())
print('ok', len(H_))
