import asyncio, pathlib
from playwright.async_api import async_playwright

OUT = pathlib.Path("/home/claude/pichanga/semana1")
OUT.mkdir(parents=True, exist_ok=True)

BALL = """<svg viewBox="0 0 100 100" width="{s}" height="{s}"><circle cx="50" cy="50" r="46" fill="#FFF8E7" stroke="#1B1B1B" stroke-width="6"/>
<polygon points="50,30 68,43 61,64 39,64 32,43" fill="#1B1B1B"/>
<line x1="50" y1="30" x2="50" y2="6" stroke="#1B1B1B" stroke-width="5"/><line x1="68" y1="43" x2="92" y2="36" stroke="#1B1B1B" stroke-width="5"/>
<line x1="61" y1="64" x2="76" y2="86" stroke="#1B1B1B" stroke-width="5"/><line x1="39" y1="64" x2="24" y2="86" stroke="#1B1B1B" stroke-width="5"/>
<line x1="32" y1="43" x2="8" y2="36" stroke="#1B1B1B" stroke-width="5"/></svg>"""

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Inter',sans-serif;overflow:hidden;position:relative;
 background:#2F7D3B;color:#FFF8E7}
.field{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#2F7D3B 0 135px,#2A7235 135px 270px)}
.dirt{position:absolute;left:0;right:0;bottom:0;height:260px;background:#C97B3D;
 box-shadow:inset 0 18px 0 #B56A30}
.chalk{position:absolute;border:8px solid rgba(255,248,231,.22)}
.circle{width:560px;height:560px;border-radius:50%;left:260px;top:520px}
.half{left:-10px;right:-10px;top:800px;height:0;border-width:8px 0 0 0}
.brand{position:absolute;top:56px;left:64px;display:flex;align-items:center;gap:18px;z-index:5}
.brand b{font-weight:900;font-size:44px;letter-spacing:1px;color:#FFF8E7}
.brand b span{color:#FFD23F}
.content{position:absolute;left:64px;right:64px;top:190px;z-index:5}
.kicker{display:inline-block;background:#FFD23F;color:#1B1B1B;font-weight:900;font-size:34px;
 padding:10px 22px;border-radius:12px;transform:rotate(-2deg);margin-bottom:34px}
h1{font-weight:900;font-size:112px;line-height:.98;letter-spacing:-2px;text-shadow:0 6px 0 rgba(0,0,0,.25)}
h1 em{font-style:normal;color:#FFD23F}
p.sub{font-weight:700;font-size:44px;line-height:1.25;margin-top:34px;max-width:900px}
.card{background:#FFF8E7;color:#1B1B1B;border-radius:28px;padding:24px 34px;margin-top:20px;
 box-shadow:0 10px 0 rgba(0,0,0,.22);font-size:42px;font-weight:800;line-height:1.2;display:flex;gap:26px;align-items:center}
.card .tag{flex:none;width:86px;height:86px;border-radius:20px;background:#C97B3D;color:#FFF8E7;
 display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900}
.footer{position:absolute;left:64px;right:64px;bottom:70px;z-index:5;font-weight:900;font-size:46px;color:#FFF8E7;
 display:flex;justify-content:space-between;align-items:center}
.footer .pill{background:#1B1B1B;padding:16px 28px;border-radius:999px;font-size:38px}
.big-emoji{font-size:240px;line-height:1}
body.list h1{font-size:92px}
body.char p.sub{max-width:600px}
.slidenum{font-weight:800;font-size:32px;opacity:.85}
"""

def page(body, num=None, cls="", char=""):
    brand = f'<div class="brand">{BALL.format(s=64)}<b>PICHANGA <span>BRAVA</span></b></div>'
    n = f'<span class="slidenum">{num}</span>' if num else '<span></span>'
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">
<div class="field"></div><div class="chalk circle"></div><div class="chalk half"></div><div class="dirt"></div>
{brand}<div class="content">{body}</div>{char}
<div class="footer"><span class="pill">@pichangabrava</span>{n}</div></body></html>"""

def character(color, shirt_text, extra=""):
    # personaje genérico simple tipo juguete
    return f"""<svg viewBox="0 0 300 380" width="300" height="380" style="position:absolute;right:70px;bottom:250px;z-index:4">
<ellipse cx="150" cy="372" rx="110" ry="10" fill="rgba(0,0,0,.25)"/>
<rect x="104" y="250" width="34" height="110" rx="16" fill="#1B1B1B"/><rect x="162" y="250" width="34" height="110" rx="16" fill="#1B1B1B"/>
<rect x="80" y="140" width="140" height="130" rx="40" fill="{color}"/>
<text x="150" y="222" font-family="Inter" font-weight="900" font-size="64" fill="#FFF8E7" text-anchor="middle">{shirt_text}</text>
<rect x="40" y="150" width="40" height="100" rx="20" fill="{color}"/><rect x="220" y="150" width="40" height="100" rx="20" fill="{color}"/>
<circle cx="150" cy="90" r="62" fill="#E8B38A"/>
<circle cx="128" cy="86" r="8" fill="#1B1B1B"/><circle cx="172" cy="86" r="8" fill="#1B1B1B"/>
<path d="M126 116 Q150 132 174 116" stroke="#1B1B1B" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M92 66 Q150 4 208 66 Q170 44 150 50 Q120 44 92 66Z" fill="#3B2416"/>
{extra}</svg>"""

POSTS = {
 # Carrusel lunes
 "01_carrusel_1_portada": page("""<div class="kicker">CARRUSEL · DESLIZA →</div>
<h1>Los tipos de jugadores que hay en <em>toda</em> pichanga</h1>
<p class="sub">Si no te reconoces en ninguno… eres tú el comilón.</p>""", "1/5"),
 "01_carrusel_2_comilon": page("""<div class="kicker">TIPO #1</div>
<h1>El <em>comilón</em></h1>
<p class="sub">Dribla a tres, a su sombra y al perro de la cancha.<br>El compañero solo frente al arco sigue esperando el pase.</p>""", char=character("#B5584F", "10", '<circle cx="250" cy="350" r="26" fill="#FFF8E7" stroke="#1B1B1B" stroke-width="5"/>'), num="2/5", cls="char"),
 "01_carrusel_3_arquero": page("""<div class="kicker">TIPO #2</div>
<h1>El arquero que se cree <em>volante</em></h1>
<p class="sub">Sale jugando hasta la mitad de la cancha.<br>El arco queda más solo que el dueño de la pelota.</p>""", char=character("#4F6F8F", "1", '<rect x="20" y="230" width="60" height="44" rx="14" fill="#D9B860"/><rect x="220" y="230" width="60" height="44" rx="14" fill="#D9B860"/>'), num="3/5", cls="char"),
 "01_carrusel_4_atrasado": page("""<div class="kicker">TIPO #3</div>
<h1>El que llega <em>tarde</em> y quiere ser titular</h1>
<p class="sub">Cuarenta minutos de atraso, zapatillas impecables<br>y reclamando faltas que nadie vio.</p>""", char=character("#6E5A7E", "7", '<rect x="96" y="352" width="50" height="18" rx="8" fill="#FFFFFF"/><rect x="156" y="352" width="50" height="18" rx="8" fill="#FFFFFF"/>'), num="4/5", cls="char"),
 "01_carrusel_5_cierre": page("""<div class="kicker">TU TURNO</div>
<h1>¿Cuál eres <em>tú</em>?</h1>
<p class="sub">Comenta tu número y etiqueta al compañero que es los tres al mismo tiempo.</p>
<div class="card"><div class="tag">1</div>El comilón</div>
<div class="card"><div class="tag">2</div>El arquero volante</div>
<div class="card"><div class="tag">3</div>El que llega tarde</div>""", "5/5", cls="list"),
 # Miércoles
 "02_reglas_no_escritas": page("""<div class="kicker">LEY DEL BARRIO</div>
<h1>Reglas <em>no escritas</em> de la pichanga</h1>
<div class="card"><div class="tag">✓</div>El dueño de la pelota no sale nunca</div>
<div class="card"><div class="tag">✓</div>El arco se rota cada vez que entra un gol</div>
<div class="card"><div class="tag">✓</div>"El último gol gana" anula todo el partido</div>
<div class="card"><div class="tag">✓</div>Se juega hasta que no se ve la pelota</div>""", cls="list"),
 # Viernes
 "03_frases_tipicas": page("""<div class="kicker">LAS DE SIEMPRE</div>
<h1>Frases que se escuchan en <em>toda</em> pichanga</h1>
<div class="card"><div class="tag">“</div>¡Pásala, pásala!</div>
<div class="card"><div class="tag">“</div>Esa fue mano, yo la vi</div>
<div class="card"><div class="tag">“</div>Juguemos la última y nos vamos</div>
<div class="card"><div class="tag">“</div>¿Quién trajo la pelota?</div>""", cls="list"),
 # Sábado
 "04_encuesta_cancha": page("""<div class="kicker">DEBATE</div>
<h1>¿Tierra o <em>sintética</em>?</h1>
<p class="sub">La eterna discusión del barrio.<br>Una deja las rodillas peladas, la otra cuesta plata.</p>
<div class="card"><div class="tag">A</div>Cancha de tierra, como antes</div>
<div class="card"><div class="tag">B</div>Sintética, aunque haya que pagar</div>"""),
 # Domingo
 "05_etiqueta_amigo": page("""<div class="kicker">ETIQUETA A ESE AMIGO</div>
<h1>El que dice <em>"voy"</em> y nunca llega</h1>
<p class="sub">Confirmó en el grupo, pidió que lo esperaran<br>y a las once de la noche manda: "¿todavía están jugando?"</p>""", char=character("#5E7F5A", "?", '<rect x="230" y="60" width="44" height="74" rx="10" fill="#1B1B1B"/><rect x="236" y="68" width="32" height="52" rx="4" fill="#9AD1FF"/>'), cls="char"),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        for name, html in POSTS.items():
            await pg.set_content(html)
            await pg.wait_for_timeout(150)
            await pg.screenshot(path=str(OUT/f"{name}.png"))
        await b.close()
if __name__=='__main__':
    asyncio.run(main())
    print("ok", len(POSTS))
