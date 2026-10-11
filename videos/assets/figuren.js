// Zahlenwerkstatt-Figuren: Low-Poly-Charaktere aus Three.js-Grundformen.
// Jede Figur hat build() -> { root, update(t, zustand) }.
// zustand: { talk: 0..1, wave: 0..1, hop: 0..1, look: -1..1, intro: 0..1 }
import * as THREE from "./three.module.js";

// ---------- Hilfen ----------
function prng(seed){ let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// Facetten-Look: gleiche Punkte bekommen dieselbe kleine Verschiebung (keine Risse)
function facet(geo, amount, seed){
  const r = prng(seed), pos = geo.attributes.position, off = new Map();
  for (let i = 0; i < pos.count; i++){
    const k = `${pos.getX(i).toFixed(3)},${pos.getY(i).toFixed(3)},${pos.getZ(i).toFixed(3)}`;
    if (!off.has(k)) off.set(k, [(r() - .5) * amount, (r() - .5) * amount, (r() - .5) * amount]);
    const o = off.get(k);
    pos.setXYZ(i, pos.getX(i) + o[0], pos.getY(i) + o[1], pos.getZ(i) + o[2]);
  }
  geo.computeVertexNormals();
  return geo;
}
const M = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: .82, metalness: 0, ...extra });
function mesh(geo, mat, [x, y, z] = [0, 0, 0], [sx, sy, sz] = [1, 1, 1]){
  const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.scale.set(sx, sy, sz); return m;
}
const put = (parent, m) => (parent.add(m), m);
const ico = (r, d = 1, j = .06, s = 1) => facet(new THREE.IcosahedronGeometry(r, d), r * j, s);
const caps = (r, l, j = .05, s = 1) => facet(new THREE.CapsuleGeometry(r, l, 3, 9), r * j, s);
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const backOut = x => { if (x <= 0) return 0; if (x >= 1) return 1; const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const blink = (t, phase) => ((t + phase) % 3.4) < .13 ? .1 : 1;
const mouthOpen = t => .35 + .65 * Math.abs(Math.sin(t * 17) * Math.sin(t * 6.1 + 1));

// ---------- Oskar: die kluge Eule mit Doktorhut ----------
export function oskar(){
  const root = new THREE.Group(), body = new THREE.Group(); root.add(body);
  const brown = M(0x8a5a3c), brown2 = M(0x6e452c), belly = M(0xe9cfa6), white = M(0xffffff), dark = M(0x1b1b22),
        beakM = M(0xf2a227), capM = M(0x22305c), tassel = M(0xf5c518);
  body.add(mesh(ico(1.25, 2, .05, 101), brown, [0, 1.55, 0], [1, 1.12, .95]));
  body.add(mesh(ico(.85, 1, .05, 102), belly, [0, 1.15, .55], [1, 1.05, .6]));
  // Gesichtsscheibe und Augen
  body.add(mesh(ico(.95, 1, .04, 103), M(0xd9b48a), [0, 2.15, .62], [1.25, .85, .45]));
  const eyes = [], pupils = [];
  [-.42, .42].forEach((x, i) => {
    const e = mesh(new THREE.CylinderGeometry(.36, .36, .12, 14), white, [x, 2.2, 1.0]); e.rotation.x = Math.PI / 2; body.add(e); eyes.push(e);
    const p = mesh(new THREE.SphereGeometry(.17, 10, 8), dark, [x, 2.2, 1.08], [1, 1, .5]); body.add(p); pupils.push(p);
    body.add(mesh(new THREE.SphereGeometry(.05, 6, 4), white, [x + .06, 2.27, 1.16]));
  });
  const beakTop = put(body, mesh(new THREE.ConeGeometry(.21, .4, 5), beakM, [0, 1.95, 1.14])); beakTop.rotation.x = Math.PI * .62;
  const beakLow = put(body, mesh(new THREE.ConeGeometry(.15, .26, 5), beakM, [0, 1.78, 1.1])); beakLow.rotation.x = Math.PI * .6;
  [-1, 1].forEach(sd => { const tf = put(body, mesh(new THREE.ConeGeometry(.2, .55, 4), brown2, [sd * .72, 3.0, .1])); tf.rotation.z = -sd * .35; });
  // Flügel (Drehpunkt oben)
  const wing = sd => { const g = new THREE.Group(); g.position.set(sd * 1.15, 1.95, 0);
    g.add(mesh(ico(.45, 1, .08, 110 + sd), brown2, [sd * .12, -.6, 0], [.45, 1.25, .8])); g.rotation.z = sd * .12; body.add(g); return g; };
  const wL = wing(-1), wR = wing(1);
  [-.4, .4].forEach((x, i) => root.add(mesh(ico(.2, 1, .1, 120 + i), beakM, [x, .1, .45], [1.2, .5, 1.3])));
  // Doktorhut
  const cap = new THREE.Group(); cap.position.set(0, 3.15, -.05); cap.rotation.z = -.12; body.add(cap);
  cap.add(mesh(new THREE.CylinderGeometry(.45, .5, .3, 8), capM));
  put(cap, mesh(new THREE.BoxGeometry(1.35, .08, 1.35), capM, [0, .18, 0])).rotation.y = Math.PI / 4;
  const tas = mesh(new THREE.CylinderGeometry(.03, .03, .5, 5), tassel, [.55, -.05, .1]); cap.add(tas);
  cap.add(mesh(ico(.08, 0, 0, 1), tassel, [.55, -.32, .1]));
  return { root, update(t, s = {}){
    root.scale.setScalar(Math.max(backOut(s.intro ?? 1), .001));
    body.position.y = Math.sin(t * 1.9) * .04 + (s.hop ?? 0) * Math.abs(Math.sin(t * 6)) * .3;
    body.rotation.y = (s.look ?? 0) * .35 + Math.sin(t * .8) * .07; body.rotation.z = Math.sin(t * 1.4) * .03;
    const b = blink(t, .4); pupils.forEach(p => p.scale.y = b); eyes.forEach(e => e.scale.z = b < 1 ? .15 : 1);
    const talk = (s.talk ?? 0) * mouthOpen(t); beakLow.position.y = 1.8 - talk * .1; beakLow.rotation.x = Math.PI * (.6 + talk * .12);
    const w = s.wave ?? 0;
    wR.rotation.z = .12 + w * (1.9 + Math.sin(t * 8) * .35);
    wL.rotation.z = -.12 - (s.talk ?? 0) * .25 * Math.abs(Math.sin(t * 2.2));
    tas.rotation.z = Math.sin(t * 3) * .2;
  }};
}

// ---------- Robbi: der Rechenroboter ----------
export function robbi(){
  const root = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); root.add(body); body.add(head);
  const teal = M(0x3fb6b9), teal2 = M(0x2c8f95), shell = M(0xe8edf5), screen = M(0x14203f), metal = M(0x9aa6bd),
        glow = M(0x6dff9e, { emissive: 0x3dff86, emissiveIntensity: .9 }), red = M(0xff4d5a, { emissive: 0xff2a3a, emissiveIntensity: .5 });
  body.add(mesh(facet(new THREE.BoxGeometry(1.7, 1.5, 1.2, 2, 2, 2), .04, 201), teal, [0, 1.15, 0]));
  put(body, mesh(new THREE.CylinderGeometry(.22, .22, .08, 10), red, [0, 1.25, .62])).rotation.x = Math.PI / 2;
  [[-.45, .95], [.45, .95]].forEach(([x, y]) => body.add(mesh(new THREE.BoxGeometry(.3, .1, .06), shell, [x, y, .61])));
  // Kopf mit Bildschirm
  head.position.set(0, 2.55, 0);
  head.add(mesh(facet(new THREE.BoxGeometry(1.9, 1.35, 1.25, 2, 2, 2), .04, 202), shell));
  head.add(mesh(new THREE.BoxGeometry(1.5, .95, .06), screen, [0, 0, .64]));
  const eyes = [-.35, .35].map(x => put(head, mesh(new THREE.BoxGeometry(.24, .3, .04), glow, [x, .12, .68])));
  const mouth = put(head, mesh(new THREE.BoxGeometry(.6, .07, .04), glow, [0, -.22, .68]));
  [-1, 1].forEach(sd => put(head, mesh(new THREE.CylinderGeometry(.18, .18, .2, 8), metal, [sd * 1.02, 0, 0])).rotation.z = Math.PI / 2);
  const ant = new THREE.Group(); ant.position.set(0, .68, 0); head.add(ant);
  ant.add(mesh(new THREE.CylinderGeometry(.04, .04, .5, 6), metal, [0, .25, 0]));
  const ball = put(ant, mesh(ico(.12, 1, 0, 1), red, [0, .55, 0]));
  // Arme und Räder
  const arm = sd => { const g = new THREE.Group(); g.position.set(sd * 1.0, 1.65, 0);
    g.add(mesh(new THREE.CylinderGeometry(.13, .13, .8, 8), metal, [0, -.4, 0]));
    g.add(mesh(ico(.2, 1, .05, 210 + sd), teal2, [0, -.85, 0])); g.rotation.z = sd * .15; body.add(g); return g; };
  const aL = arm(-1), aR = arm(1);
  [-.55, .55].forEach(x => { const w = mesh(new THREE.CylinderGeometry(.3, .3, .3, 10), screen, [x, .3, 0]); w.rotation.z = Math.PI / 2; root.add(w); });
  return { root, update(t, s = {}){
    root.scale.setScalar(Math.max(backOut(s.intro ?? 1), .001));
    body.position.y = Math.abs(Math.sin(t * 3)) * .04 + (s.hop ?? 0) * Math.abs(Math.sin(t * 6)) * .3;
    head.rotation.y = (s.look ?? 0) * .4 + Math.sin(t * .9) * .08; head.rotation.z = Math.sin(t * 1.6) * .04;
    eyes.forEach(e => e.scale.y = blink(t, 1.9));
    const talk = s.talk ?? 0; mouth.scale.set(1 - talk * .3, 1 + talk * mouthOpen(t + .5) * 3.5, 1);
    ant.rotation.z = Math.sin(t * 4) * .18; ball.scale.setScalar(1 + talk * .25 * Math.abs(Math.sin(t * 9)));
    const w = s.wave ?? 0;
    aR.rotation.z = .15 + w * (2.4 + Math.sin(t * 9) * .3);
    aL.rotation.z = -.15 - talk * .2 * Math.abs(Math.sin(t * 2.5));
  }};
}

// ---------- Zacki: der Zahlen-Dino ----------
export function zacki(){
  const root = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); root.add(body);
  const green = M(0x67c04a), green2 = M(0x4f9f37), belly = M(0xd8efa8), spike = M(0xffb02e), white = M(0xffffff), dark = M(0x1b1b22);
  body.add(mesh(ico(.95, 1, .06, 301), green, [0, 1.05, 0], [1, 1.08, .95]));
  body.add(mesh(ico(.62, 1, .05, 302), belly, [0, 1.0, .5], [1, 1.15, .62]));
  // Schwanz
  [[0, .7, -.9, .45], [0, .55, -1.45, .32], [0, .45, -1.85, .2]].forEach(([x, y, z, r], i) => body.add(mesh(ico(r, 1, .08, 310 + i), green2, [x, y, z])));
  // Kopf
  head.position.set(0, 2.1, .2); body.add(head);
  head.add(mesh(ico(.72, 1, .05, 320), green, [0, 0, 0], [1.05, .95, 1]));
  head.add(mesh(ico(.45, 1, .05, 321), green, [0, -.18, .55], [1.15, .75, .9]));
  const eyes = [], pupils = [];
  [-.3, .3].forEach(x => {
    eyes.push(put(head, mesh(new THREE.SphereGeometry(.2, 10, 8), white, [x, .22, .55])));
    pupils.push(put(head, mesh(new THREE.SphereGeometry(.1, 8, 6), dark, [x, .22, .73])));
  });
  [-.12, .12].forEach(x => head.add(mesh(new THREE.SphereGeometry(.035, 5, 4), dark, [x, -.12, .97])));
  const mouth = put(head, mesh(new THREE.BoxGeometry(.38, .05, .05), dark, [0, -.36, .88]));
  // Rückenzacken
  [[2.85, -.15, .2], [2.05, -.75, .26], [1.55, -1.0, .22], [1.05, -1.3, .17]].forEach(([y, z, r], i) => {
    const c = mesh(new THREE.ConeGeometry(r, r * 2.2, 4), spike, [0, y, z]); c.rotation.x = -.35 - i * .25; (i ? body : body).add(c); });
  const armL = put(body, mesh(caps(.13, .3, .05, 330), green2, [-.78, 1.25, .45])), armR = put(body, mesh(caps(.13, .3, .05, 331), green2, [.78, 1.25, .45]));
  [-.45, .45].forEach((x, i) => root.add(mesh(caps(.25, .2, .05, 340 + i), green2, [x, .25, .1])));
  return { root, update(t, s = {}){
    root.scale.setScalar(Math.max(backOut(s.intro ?? 1), .001));
    const hop = (s.hop ?? 0) * Math.abs(Math.sin(t * 6.5)) * .45;
    body.position.y = hop + Math.sin(t * 2.4) * .03;
    body.rotation.y = (s.look ?? 0) * .4 + Math.sin(t * 1.1) * .1;
    head.rotation.z = Math.sin(t * 1.7) * .08; head.rotation.x = -(s.talk ?? 0) * .05 * Math.abs(Math.sin(t * 3));
    pupils.forEach(p => p.scale.y = blink(t, 2.7)); eyes.forEach(e => e.scale.y = blink(t, 2.7) < 1 ? .2 : 1);
    const talk = s.talk ?? 0; mouth.scale.set(1, 1 + talk * mouthOpen(t + .2) * 2.4, 1);
    const w = s.wave ?? 0;
    armR.position.y = 1.25 + w * (.55 + Math.sin(t * 10) * .1); armR.rotation.z = -w * .8;
    armL.position.y = 1.25 + Math.sin(t * 3) * .02;
  }};
}


// ---------- Oskar (glatte Version): runde, weich beleuchtete Eule ----------
function federTextur(base, linie, seed, groesse = 34){
  const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d"), r = prng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 512, 512);
  for (let row = -1; row < 512 / (groesse * .55) + 2; row++)
    for (let col = -1; col < 512 / groesse + 2; col++){
      const x = col * groesse + (row % 2) * groesse / 2 + (r() - .5) * 5, y = row * groesse * .55;
      g.beginPath(); g.arc(x, y, groesse * .52, .15, Math.PI - .15);
      g.strokeStyle = linie; g.globalAlpha = .28 + r() * .22; g.lineWidth = 3.2; g.stroke();
    }
  g.globalAlpha = 1;
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; return t;
}
const PM = (o) => new THREE.MeshPhysicalMaterial({ roughness: .78, metalness: 0, ...o });
const kugel = (r, ws = 64, hs = 48) => new THREE.SphereGeometry(r, ws, hs);
export function eule(){
  const root = new THREE.Group(), body = new THREE.Group(), head = new THREE.Group(); root.add(body); body.add(head);
  const fBraun = federTextur("#7a4628", "#4a2814", 7), fHell = federTextur("#ecd2a8", "#b98a5c", 8, 26), fFluegel = federTextur("#5e3720", "#331a0c", 9, 40);
  fBraun.repeat.set(3, 2); fHell.repeat.set(2, 2); fFluegel.repeat.set(1, 2);
  const braun = PM({ map: fBraun, bumpMap: fBraun, bumpScale: 1.4, sheen: .6, sheenColor: new THREE.Color(0xffd9b0), sheenRoughness: .6 });
  const hell = PM({ map: fHell, bumpMap: fHell, bumpScale: 1.0, sheen: .5, sheenColor: new THREE.Color(0xffffff) });
  const fluegel = PM({ map: fFluegel, bumpMap: fFluegel, bumpScale: 1.6, sheen: .5, sheenColor: new THREE.Color(0xffc89a) });
  const gesicht = PM({ color: 0xf1dcbc, roughness: .9, sheen: .4, sheenColor: new THREE.Color(0xffffff) });
  const iris = PM({ color: 0xf5a623, roughness: .15, clearcoat: 1, clearcoatRoughness: .05 });
  const pupilleM = PM({ color: 0x111014, roughness: .1, clearcoat: 1 });
  const glanz = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const schnabelM = PM({ color: 0xd9962f, roughness: .45, clearcoat: .6 });
  const fussM = PM({ color: 0xe8a33d, roughness: .5 });
  const hutM = PM({ color: 0x1f2b55, roughness: .55, clearcoat: .3 }), quaste = PM({ color: 0xf5c518, roughness: .5 });
  // Rumpf und Bauch
  body.add(mesh(kugel(1.25), braun, [0, 1.35, 0], [1, 1.1, .95]));
  body.add(mesh(kugel(.88), hell, [0, 1.25, .68], [1, 1.08, .52]));
  // Kopf
  head.position.set(0, 2.45, .05);
  head.add(mesh(kugel(1.05), braun, [0, 0, 0], [1.1, .95, .97]));
  [-1, 1].forEach(sd => head.add(mesh(kugel(.52), gesicht, [sd * .37, 0, .74], [1, 1.02, .38])));
  head.add(mesh(kugel(.3), braun, [0, .38, .8], [.55, .5, .3]));
  // Augen mit Lidern
  const lider = [], pupillen = [], brauen = [];
  [-1, 1].forEach(sd => {
    const x = sd * .37;
    head.add(mesh(kugel(.3, 48, 32), iris, [x, .02, .9], [1, 1, .55]));
    pupillen.push(put(head, mesh(kugel(.15, 32, 24), pupilleM, [x, .02, 1.04], [1, 1, .4])));
    head.add(mesh(kugel(.05, 16, 12), glanz, [x + .08, .1, 1.1]));
    const lid = put(head, mesh(new THREE.SphereGeometry(.315, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), braun, [x, .02, .9], [1, 1, .6]));
    lid.rotation.x = -1.75; lider.push(lid);
    const br = put(head, mesh(kugel(.2, 24, 16), fluegel, [x * 1.05, .4, .86], [1.3, .28, .35])); br.rotation.z = -sd * .22; brauen.push(br);
  });
  // Schnabel
  const oben = put(head, mesh(new THREE.ConeGeometry(.19, .46, 32), schnabelM, [0, -.2, 1.02])); oben.rotation.x = Math.PI * .58;
  const unten = put(head, mesh(new THREE.ConeGeometry(.1, .16, 32), schnabelM, [0, -.3, .93])); unten.rotation.x = Math.PI * .56;
  // Federohren
  [-1, 1].forEach(sd => { const o = put(head, mesh(new THREE.ConeGeometry(.2, .55, 32), fluegel, [sd * .68, .8, .05])); o.rotation.z = -sd * .4; });
  // Flügel: eine durchgehende Flügelfläche, die an der Schulter am Körper ansetzt.
  // Unterer Rand gezackt (Federspitzen), Muster: oben Deckfedern, unten gestreifte Schwungfedern.
  const fluegelTextur = (() => {
    // Leinwand oben = Flügelansatz (Schulter), unten = Federspitzen
    const c = document.createElement("canvas"); c.width = 256; c.height = 512; const g = c.getContext("2d");
    const grad = g.createLinearGradient(0, 0, 0, 512); grad.addColorStop(0, "#7a4728"); grad.addColorStop(1, "#5a331b");
    g.fillStyle = grad; g.fillRect(0, 0, 256, 512);
    for (let row = 0; row < 13; row++) for (let col = -1; col < 10; col++){      // Deckfedern (Schuppen) oben
      const x = col * 28 + (row % 2) * 14, y = row * 15;
      g.beginPath(); g.arc(x, y, 15, .2, Math.PI - .2); g.strokeStyle = "#3b2010"; g.globalAlpha = .4; g.lineWidth = 2.5; g.stroke();
    }
    for (let k = 0; k < 8; k++){                                                // lange Schwungfedern unten
      const x0 = 16 + k * 32;
      g.globalAlpha = .55; g.strokeStyle = "#2e180a"; g.lineWidth = 2.5;
      g.beginPath(); g.moveTo(x0, 200); g.quadraticCurveTo(x0 + 6, 360, x0 + 2, 512); g.stroke();        // Federkiel
      g.globalAlpha = .35; g.strokeStyle = "#e0bd92"; g.lineWidth = 2;
      g.beginPath(); g.moveTo(x0 + 14, 210); g.quadraticCurveTo(x0 + 20, 360, x0 + 16, 512); g.stroke(); // Federkante
      for (let b = 0; b < 4; b++){ g.globalAlpha = .18; g.fillStyle = "#24120a"; g.fillRect(x0 - 12, 250 + b * 60, 28, 16); }
    }
    g.globalAlpha = .9; g.fillStyle = "#d9b98f"; g.fillRect(0, 488, 256, 24);     // helle Spitzen
    g.globalAlpha = 1;
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    t.repeat.set(1 / 1.15, 1 / 1.9); t.offset.set(.55 / 1.15, 1); return t;
  })();
  const fluegelMat = PM({ map: fluegelTextur, bumpMap: fluegelTextur, bumpScale: 1.2, roughness: .75, sheen: .5, sheenColor: new THREE.Color(0xffcf9e), side: THREE.DoubleSide });
  const fluegelGeo = (() => {
    const sh = new THREE.Shape(), tip = [.28, -1.8], end = [-.5, -.55];
    sh.moveTo(0, 0);
    sh.bezierCurveTo(.38, -.2, .52, -.95, tip[0], tip[1]);                         // Vorderkante
    const n = 6, dx = end[0] - tip[0], dy = end[1] - tip[1], L = Math.hypot(dx, dy), ox = -dy / L, oy = dx / L;
    for (let i = 1; i <= n; i++){                                                  // gezackter Federrand
      const ax = tip[0] + dx * (i - 1) / n, ay = tip[1] + dy * (i - 1) / n, bx = tip[0] + dx * i / n, by = tip[1] + dy * i / n;
      sh.quadraticCurveTo((ax + bx) / 2 + ox * .2, (ay + by) / 2 + oy * .2, bx, by);
    }
    sh.bezierCurveTo(-.55, -.35, -.3, -.04, 0, 0);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: .05, bevelEnabled: true, bevelThickness: .035, bevelSize: .035, bevelSegments: 3, curveSegments: 28 });
    const pos = geo.attributes.position;                                           // leicht um den Körper biegen
    for (let i = 0; i < pos.count; i++) pos.setZ(i, pos.getZ(i) - .32 * pos.getX(i) * pos.getX(i));
    geo.computeVertexNormals(); return geo;
  })();
  const fluegelGruppe = sd => {
    const g = new THREE.Group(); g.position.set(sd * .96, 2.1, .25); body.add(g);
    const m = new THREE.Mesh(fluegelGeo, fluegelMat); m.scale.x = sd; m.castShadow = true; g.add(m);
    return { g, m, sd };
  };
  const fl = fluegelGruppe(-1), fr = fluegelGruppe(1);
  const fluegelPose = (w, t, raise, spread, schwing) => {
    const offen = Math.min(1, raise / 1.2);
    w.g.rotation.z = w.sd * (.04 + raise + schwing);
    w.g.rotation.y = -w.sd * (.72 - .55 * offen);
    w.g.rotation.x = -.05 - offen * .1;
    w.m.scale.set(w.sd * (1 + .22 * spread), 1 + .08 * spread, 1);
  };
  // Füße
  [-.42, .42].forEach(x => [-.12, 0, .12].forEach(d => { const z = mesh(new THREE.CapsuleGeometry(.065, .16, 8, 16), fussM, [x + d, .07, .62]); z.rotation.x = Math.PI / 2; z.rotation.y = d * 2; root.add(z); }));
  // Doktorhut
  const hut = new THREE.Group(); hut.position.set(0, .95, -.05); hut.rotation.z = -.1; head.add(hut);
  hut.add(mesh(new THREE.CylinderGeometry(.48, .55, .32, 48), hutM));
  put(hut, mesh(new THREE.BoxGeometry(1.4, .07, 1.4), hutM, [0, .19, 0])).rotation.y = Math.PI / 4;
  hut.add(mesh(kugel(.06, 16, 12), quaste, [0, .24, 0]));
  const q = put(hut, mesh(new THREE.CylinderGeometry(.025, .025, .55, 12), quaste, [.6, -.06, .2]));
  hut.add(mesh(new THREE.ConeGeometry(.07, .18, 16), quaste, [.6, -.38, .2]));
  root.traverse(o => { if (o.isMesh){ o.castShadow = true; o.receiveShadow = true; } });
  return { root, update(t, s = {}){
    root.scale.setScalar(Math.max(backOut(s.intro ?? 1), .001));
    body.position.y = Math.sin(t * 1.9) * .035 + (s.hop ?? 0) * Math.abs(Math.sin(t * 6)) * .3;
    body.scale.set(1 + Math.sin(t * 1.9) * .008, 1 - Math.sin(t * 1.9) * .008, 1);
    head.rotation.y = (s.look ?? 0) * .4 + Math.sin(t * .8) * .08; head.rotation.z = Math.sin(t * 1.3) * .05;
    const zu = ((t + .4) % 3.6) < .16 ? 1 : 0;
    lider.forEach(l => l.rotation.x = zu ? 1.45 : -1.75);
    const talk = (s.talk ?? 0) * mouthOpen(t);
    unten.rotation.x = Math.PI * (.56 + talk * .08); unten.position.y = -.3 - talk * .1;
    brauen.forEach(b => b.position.y = .4 + (s.talk ?? 0) * .05 * Math.abs(Math.sin(t * 2.4)));
    const w = s.wave ?? 0, pt = s.point ?? 0, rede = (s.talk ?? 0) * Math.abs(Math.sin(t * 2.2));
    fluegelPose(fr, t, w * 1.9 + pt * 1.35, Math.max(w, pt), w * Math.sin(t * 8) * .35 + pt * Math.sin(t * 2) * .05);
    fluegelPose(fl, t, rede * .25 + (s.pointL ?? 0) * 1.35, rede * .4 + (s.pointL ?? 0), 0);
    q.rotation.z = Math.sin(t * 2.6) * .25;
  }};
}

// ---------- Bühne ----------
export function buehne(canvas, W = 1920, H = 1080, opt = {}){
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.setPixelRatio(1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  if (opt.weich){ renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15; renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; }
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(28, W / H, .1, 100);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a93b8, 1.7));
  const key = new THREE.DirectionalLight(0xfff3e0, opt.weich ? 2.6 : 2.1); key.position.set(-4, 7, 6); scene.add(key);
  if (opt.weich){
    key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 6; key.shadow.bias = -.0005;
    Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -2, near: 1, far: 30 });
    const boden = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: .18 }));
    boden.rotation.x = -Math.PI / 2; boden.receiveShadow = true; scene.add(boden);
    const warm = new THREE.DirectionalLight(0xffb070, 1.2); warm.position.set(3, 4, -6); scene.add(warm);
  }
  const fill = new THREE.DirectionalLight(0xffffff, .9); fill.position.set(0, 2, 10); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xbfd4ff, .9); rim.position.set(5, 3, -4); scene.add(rim);
  const schatten = (x, r = 1.1) => {
    const s = new THREE.Mesh(new THREE.CircleGeometry(r, 24), new THREE.MeshBasicMaterial({ color: 0x1c2f5e, transparent: true, opacity: .14 }));
    s.rotation.x = -Math.PI / 2; s.position.set(x, .01, 0); scene.add(s); return s;
  };
  return { renderer, scene, camera, schatten, render: () => renderer.render(scene, camera) };
}
export const helfer = { ease, backOut };
