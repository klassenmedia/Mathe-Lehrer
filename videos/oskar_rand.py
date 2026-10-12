"""Oskar steht rechts neben der Rechnung: spricht mit, zeigt bei jeder neuen Szene auf den Inhalt,
schaut abwechselnd zur Rechnung und zu den Kindern, winkt am Anfang, hüpft am Ende.
Alles wird nur aus t, SAY und SCN berechnet, damit jedes Bild einzeln gerendert werden kann."""

OSKAR_RAND_JS = r'''
import { eule, buehne, helfer } from "./figuren.js";
const B = buehne(document.getElementById("three-layer"), 1920, 1080, { weich: true });
const oskar = eule(); B.scene.add(oskar.root);
oskar.root.position.set(7.0, 0, 0); oskar.root.rotation.y = -.22;   // x = 7 passt zu freiR = 1440 in template.html
B.scene.traverse(o => { if (o.isDirectionalLight && o.castShadow){ Object.assign(o.shadow.camera, { left: -11, right: 11 }); o.shadow.camera.updateProjectionMatrix(); } });   // Schatten auch am Rand      // rechts, etwas zur Rechnung gedreht
B.camera.position.set(0, 3.1, 20); B.camera.lookAt(0, 3.1, 0);       // Füße knapp über den Untertiteln
const E = helfer.ease;
const rampe = (t, a, b, ein = .35, aus = .45) => Math.min(E((t - a) / ein), 1 - E((t - b) / aus));
const ENDE = SCN.length ? SCN[SCN.length - 1][1] : 0;
const ZEIG_DAUER = 2.3;
function satzIndex(t){ let k = -1; SAY.forEach(([s], i) => { if (t >= s) k = i; }); return k; }
function renderAt(t){
  const spricht = SAY.some(([s, d]) => t >= s && t <= s + d) ? 1 : 0;
  let zeigen = 0;
  SCN.forEach(([a], i) => { if (i > 0) zeigen = Math.max(zeigen, rampe(t, a + .3, a + .3 + ZEIG_DAUER)); });
  const k = satzIndex(t);
  const zuKindern = (k >= 0 && k % 2 === 0 ? rampe(t, SAY[k][0], SAY[k][0] + SAY[k][1]) : 0) * (1 - zeigen);
  const zurRechnung = 1 - zuKindern;
  oskar.update(t, {
    talk: spricht,
    kopf: -.5 + .4 * zuKindern,
    blick: [-.7 * zurRechnung, -.1 * zurRechnung],
    nicken: spricht * Math.sin(t * 2.3) * .12,
    neigen: .2 * zurRechnung * Math.sin(t * .6),
    pointL: zeigen,
    lehnen: .5 * zeigen,
    staunen: .4 * zeigen,
    wave: rampe(t, .2, 2.4),
    hop: rampe(t, ENDE - 1.2, ENDE + 9),
  });
  B.render();
}
window.renderHooks.push(renderAt);
window.addEventListener("hf-seek", e => renderAt(e.detail.time));
renderAt(0);
window.figurenFertig();
'''
