"""Vorstellungsvideo der Mathe-Freunde (3D-Figuren mit Three.js, siehe assets/figuren.js)."""

FIGUREN_JS = r'''
import { oskar, robbi, zacki, buehne, helfer } from "./figuren.js";
const B = buehne(document.getElementById("three-layer"));
const F = { oskar: [oskar(), -3.6], robbi: [robbi(), 0], zacki: [zacki(), 3.6] };
for (const [f, x] of Object.values(F)) { f.root.position.x = x; B.scene.add(f.root); B.schatten(x); }
const spricht = (who, t) => SAY.some(([s, d, w]) => w === who && t >= s && t <= s + d);
const satz = (who, t) => SAY.filter(([s, d, w]) => w === who).findIndex(([s, d]) => t >= s && t <= s + d);
const szene = t => { let i = 0; SCN.forEach(([a], k) => { if (t >= a) i = k; }); return i; };
const V = (x, y, z) => ({x, y, z});
const TOTALE = [V(0, 2.9, 15.5), V(0, 1.7, 0)];
const nah = x => [V(x * .8, 2.5, 11.5), V(x, 2.05, 0)];
const SHOTS = [TOTALE, nah(-3.6), nah(0), nah(3.6), TOTALE];
const mix = (a, b, k) => V(a.x + (b.x - a.x) * k, a.y + (b.y - a.y) * k, a.z + (b.z - a.z) * k);
function kamera(t){
  const i = szene(t), cur = SHOTS[Math.min(i, SHOTS.length - 1)], prev = SHOTS[Math.max(i - 1, 0)];
  const k = helfer.ease((t - SCN[i][0] + .2) / 1.3);
  const p = mix(prev[0], cur[0], k), l = mix(prev[1], cur[1], k);
  B.camera.position.set(p.x, p.y + Math.sin(t * .5) * .05, p.z); B.camera.lookAt(l.x, l.y, l.z);
}
function renderAt(t){
  kamera(t);
  const i = szene(t), sprecher = Object.keys(F).find(w => spricht(w, t));
  Object.entries(F).forEach(([w, [f, x]], n) => {
    const intro = (t - SCN[0][0] - .4 - n * .55) / .7;
    const zielX = sprecher ? F[sprecher][1] : 0;
    f.update(t, {
      intro,
      talk: spricht(w, t) ? 1 : 0,
      wave: (w === "oskar" && satz("oskar", t) === 1) || (w === "robbi" && satz("robbi", t) === 0) || (i === 4 && t > SAY[SAY.length - 1][0]) ? 1 : 0,
      hop: (w === "zacki" && spricht("zacki", t)) || (i === 4 && t > SAY[SAY.length - 1][0]) ? 1 : 0,
      look: w === sprecher ? 0 : Math.max(-1, Math.min(1, (zielX - x) / 4)),
    });
  });
  B.render();
}
window.renderHooks.push(renderAt);
window.addEventListener("hf-seek", e => renderAt(e.detail.time));
renderAt(0);
window.figurenFertig();
'''


def chip(text):
    return f'<div class="h" style="position:absolute;top:-20px;left:0;right:0;font-size:64px">{text}</div>'


FREUNDE = dict(id="0-mathe-freunde", topic="Mathe-Freunde", three=FIGUREN_JS, scenes=[
    dict(say=[("oskar", "Hallo, Kinder! Darf ich vorstellen? Das sind eure Mathe-Freunde.")],
         html=chip("Deine Mathe-Freunde"), js='rise(q(".h"), T0 + .2);'),
    dict(say=[("oskar", "Ich bin Oskar, die Eule. Ich erkläre euch Schritt für Schritt, wie Mathe funktioniert."),
              ("oskar", "Und denkt dran: Fehler machen gehört zum Lernen dazu!")],
         html=chip("Oskar · die kluge Eule"), js='rise(q(".h"), T0 + .6);'),
    dict(say=[("robbi", "Hallo! Ich bin Robbi, der Rechenroboter. Ich rechne blitzschnell."),
              ("robbi", "Und ich zeige euch die besten Rechentricks. Piep, piep!")],
         html=chip("Robbi · der Rechenroboter"), js='rise(q(".h"), T0 + .6);'),
    dict(say=[("zacki", "Und ich bin Zacki, der Zahlen-Dino! Ich zähle alles, was ich sehe."),
              ("zacki", "Eins, zwei, drei, vier, fünf! Kekse, Würfel, Punkte. Einfach alles!")],
         html=chip("Zacki · der Zahlen-Dino"), js='rise(q(".h"), T0 + .6);'),
    dict(say=[("oskar", "Zusammen schaffen wir jede Aufgabe."), ("zacki", "Los geht's!")],
         html=chip("Los geht's!"), js='rise(q(".h"), t[1]);'),
])

VIDEOS = [FREUNDE]
