"""Oskar, die Eule, stellt sich vor (3D-Figur mit Three.js, siehe assets/figuren.js -> eule())."""

FIGUREN_JS = r'''
import { eule, buehne, helfer } from "./figuren.js";
const B = buehne(document.getElementById("three-layer"), 1920, 1080, { weich: true });
const oskar = eule(); B.scene.add(oskar.root);
const spricht = t => SAY.some(([s, d]) => t >= s && t <= s + d);
const szene = t => { let i = 0; SCN.forEach(([a], k) => { if (t >= a) i = k; }); return i; };
const V = (x, y, z) => ({x, y, z});
const SHOTS = [[V(0, 2.7, 14), V(0, 1.8, 0)], [V(.8, 2.7, 9.6), V(0, 2.25, 0)], [V(-.9, 2.4, 10.5), V(0, 2.0, 0)], [V(0, 2.7, 13), V(0, 1.8, 0)]];
const mix = (a, b, k) => V(a.x + (b.x - a.x) * k, a.y + (b.y - a.y) * k, a.z + (b.z - a.z) * k);
function renderAt(t){
  const i = szene(t), cur = SHOTS[Math.min(i, SHOTS.length - 1)], prev = SHOTS[Math.max(i - 1, 0)];
  const k = helfer.ease((t - SCN[i][0] + .2) / 1.4), p = mix(prev[0], cur[0], k), l = mix(prev[1], cur[1], k);
  B.camera.position.set(p.x, p.y + Math.sin(t * .5) * .04, p.z); B.camera.lookAt(l.x, l.y, l.z);
  const s0 = SAY[0][0], letzte = SAY[SAY.length - 1];
  oskar.update(t, {
    intro: (t - .3) / .8,
    talk: spricht(t) ? 1 : 0,
    wave: (t > s0 && t < s0 + SAY[0][1]) || t > letzte[0] ? 1 : 0,
    hop: helfer.ease((t - letzte[0] - .3) / .4),
    look: i === 1 ? -.15 : i === 2 ? .2 : 0,
  });
  B.render();
}
window.renderHooks.push(renderAt);
window.addEventListener("hf-seek", e => renderAt(e.detail.time));
renderAt(0);
window.figurenFertig();
'''


def titel(text, rechts=False):
    seite = "right:40px;text-align:right" if rechts else "left:40px;text-align:left"
    return f'<div class="h" style="position:absolute;top:120px;{seite};font-size:70px;width:560px">{text}</div>'


OSKAR = dict(id="0-oskar-stellt-sich-vor", topic="Oskar, die Eule", three=FIGUREN_JS, scenes=[
    dict(say=[("oskar", "Hallo, Kinder! Ich bin Oskar, die Eule.")],
         html=titel("Hallo!"), js='rise(q(".h"), T0 + .8);'),
    dict(say=[("oskar", "Ich bin euer Mathe-Lehrer. Ich erkläre euch Schritt für Schritt, wie Rechnen funktioniert."),
              ("oskar", "Mit Bildern, Bausteinen und vielen Tricks.")],
         html=titel("Schritt für Schritt", True), js='rise(q(".h"), T0 + .8);'),
    dict(say=[("oskar", "Und denkt dran: Fehler machen gehört zum Lernen dazu. Aus jedem Fehler lernt man etwas!")],
         html=titel("Fehler sind okay!"), js='rise(q(".h"), T0 + .8);'),
    dict(say=[("oskar", "Also: Los geht's!")],
         html=titel("Los geht's!", True), js='rise(q(".h"), T0 + .4);'),
])

VIDEOS = [OSKAR]
