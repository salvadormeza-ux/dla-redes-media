import asyncio, pathlib
from playwright.async_api import async_playwright
from render import BALL, character

OUT = pathlib.Path("/home/claude/pichanga/historias1")
OUT.mkdir(exist_ok=True)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:'Inter',sans-serif;overflow:hidden;position:relative;color:#FFF8E7;
 background:repeating-linear-gradient(90deg,#2F7D3B 0 135px,#2A7235 135px 270px)}
.chalk{position:absolute;border:8px solid rgba(255,248,231,.18)}
.circle{width:640px;height:640px;border-radius:50%;left:220px;top:900px}
.half{left:-10px;right:-10px;top:1220px;height:0;border-width:8px 0 0 0}
.dirt{position:absolute;left:0;right:0;bottom:0;height:360px;background:#C97B3D;box-shadow:inset 0 18px 0 #B56A30}
.brand{position:absolute;top:150px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:18px}
.brand b{font-weight:900;font-size:50px}
.brand b span{color:#FFD23F}
.content{position:absolute;left:80px;right:80px;top:330px}
.kicker{display:inline-block;background:#FFD23F;color:#1B1B1B;font-weight:900;font-size:40px;padding:12px 26px;border-radius:14px;transform:rotate(-2deg);margin-bottom:40px}
h1{font-weight:900;font-size:118px;line-height:1;letter-spacing:-2px;text-shadow:0 6px 0 rgba(0,0,0,.22)}
h1 em{font-style:normal;color:#FFD23F}
p.sub{font-weight:700;font-size:50px;line-height:1.25;margin-top:40px}
.card{background:#FFF8E7;color:#1B1B1B;border-radius:30px;padding:30px 38px;margin-top:24px;box-shadow:0 10px 0 rgba(0,0,0,.2);
 font-size:50px;font-weight:800;display:flex;gap:28px;align-items:center}
.card .tag{flex:none;width:92px;height:92px;border-radius:22px;background:#C97B3D;color:#FFF8E7;display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:900}
.cta{position:absolute;left:80px;right:80px;bottom:150px;text-align:center}
.cta .pill{display:inline-block;background:#1B1B1B;color:#FFF8E7;font-weight:900;font-size:48px;padding:24px 44px;border-radius:999px}
.cta small{display:block;margin-top:22px;font-weight:800;font-size:38px;color:#FFF8E7}
.char svg{right:110px !important;bottom:420px !important}
"""

def story(body, cta="Síguenos para más", extra=""):
    return f"""<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="chalk circle"></div><div class="chalk half"></div><div class="dirt"></div>
<div class="brand">{BALL.format(s=72)}<b>PICHANGA <span>BRAVA</span></b></div>
<div class="content">{body}</div>{extra}
<div class="cta"><span class="pill">@pichangabrava</span><small>{cta}</small></div></body></html>"""

HIST = {
 "h1_vie_cual_eres": story("""<div class="kicker">NUEVO POST</div>
<h1>¿Cuál eres <em>tú</em>?</h1>
<div class="card"><div class="tag">1</div>El comilón</div>
<div class="card"><div class="tag">2</div>El arquero volante</div>
<div class="card"><div class="tag">3</div>El que llega tarde</div>
<p class="sub">Responde con tu número por mensaje</p>""", "Mira el post completo en el perfil"),
 "h2_sab_completa": story("""<div class="kicker">COMPLETA LA FRASE</div>
<h1>En mi pichanga siempre hay <em>uno</em> que…</h1>
<p class="sub">Mándanos tu respuesta por mensaje.<br>Las mejores las publicamos.</p>""", "Síguenos para ver las respuestas"),
 "h3_dom_vof": story("""<div class="kicker">¿VERDADERO O FALSO?</div>
<h1>El dueño de la pelota <em>nunca</em> sale de la cancha</h1>
<div class="card"><div class="tag">V</div>Verdadero, es ley</div>
<div class="card"><div class="tag">F</div>Falso, en mi barrio no</div>""", "Responde con V o F por mensaje"),
 "h4_lun_pase": story("""<div class="kicker">PREGUNTA SERIA</div>
<h1>¿A quién <em>nunca</em> le pasan la pelota en tu equipo?</h1>
<p class="sub">Comparte esta historia y etiquétalo.<br>Él sabe quién es.</p>""", "Síguenos para más humor de barrio",
   extra='<div class="char">' + character("#4F6F8F", "?") + '</div>'),
 "h5_mar_grupo": story("""<div class="kicker">MÁNDALA AL GRUPO</div>
<h1>Comparte esto en el grupo de la <em>pichanga</em></h1>
<p class="sub">Y mira quién es el primero en responder…<br>y quién deja el visto.</p>""", "Síguenos para más"),
 "h6_mie_dia": story("""<div class="kicker">ENCUESTA</div>
<h1>¿Qué día es tu <em>pichanga</em>?</h1>
<div class="card"><div class="tag">A</div>Entre semana, después de la pega</div>
<div class="card"><div class="tag">B</div>Sábado o domingo</div>""", "Responde A o B por mensaje"),
 "h7_jue_pelota": story("""<div class="kicker">SE VIENE EL FINDE</div>
<h1>Mañana es viernes…<br>¿quién lleva la <em>pelota</em>?</h1>
<p class="sub">Etiqueta al que siempre dice<br>"yo la llevo" y nunca la lleva.</p>""", "Síguenos para más humor de barrio",
   extra='<div class="char">' + character("#B5584F", "9", '<circle cx="250" cy="350" r="26" fill="#FFF8E7" stroke="#1B1B1B" stroke-width="5"/>') + '</div>'),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1080,"height":1920})
        for n, h in HIST.items():
            await pg.set_content(h); await pg.wait_for_timeout(150)
            await pg.screenshot(path=str(OUT/f"{n}.png"))
        await b.close()
asyncio.run(main())
print("historias", len(HIST))
