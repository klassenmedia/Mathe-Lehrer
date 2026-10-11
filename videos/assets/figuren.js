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
// Kugel-Texturen (Leinwand 2:1): die Vorderseite (+z) liegt bei u = .25 (Kugel) bzw. u = .5 (Lathe).
const leinwand = (w, h) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")]; };
const alsTextur = (c, wrap = true) => {
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (wrap) t.wrapS = THREE.RepeatWrapping; return t;
};
// Kleine, weiche Federn als Schuppenreihen; dichte = Abstand in Pixeln.
function federn(g, r, { x0 = 0, y0 = 0, w, h, dichte = 22, dunkel = "#3d2210", hell = "#a87a52", alpha = .5 }){
  for (let y = y0 - dichte; y < y0 + h + dichte; y += dichte * .6)
    for (let x = x0 - dichte; x < x0 + w + dichte; x += dichte){
      const px = x + ((y / dichte | 0) % 2) * dichte / 2 + (r() - .5) * dichte * .3, py = y + (r() - .5) * dichte * .2, s = dichte * (.5 + r() * .15);
      g.globalAlpha = alpha * (.5 + r() * .5); g.fillStyle = hell;
      g.beginPath(); g.ellipse(px, py - s * .25, s * .55, s * .45, 0, 0, Math.PI * 2); g.fill();
      g.globalAlpha = alpha * (.7 + r() * .3); g.strokeStyle = dunkel; g.lineWidth = Math.max(1.5, dichte * .09);
      g.beginPath(); g.arc(px, py - s * .3, s * .62, .25, Math.PI - .25); g.stroke();
    }
  g.globalAlpha = 1;
}
// Rumpf rundum braun gefiedert, unten vorne heller Verlauf bis zum fast weißen Bauch (keine Flecken)
function koerperTextur(){
  const [c, g] = leinwand(1024, 1024), r = prng(11);
  const grund = g.createLinearGradient(0, 0, 0, 1024); grund.addColorStop(0, "#6e4527"); grund.addColorStop(1, "#5e3a20");
  g.fillStyle = grund; g.fillRect(0, 0, 1024, 1024);
  federn(g, r, { w: 1024, h: 1024, dichte: 26, dunkel: "#3a200e", hell: "#80583a", alpha: .3 });
  g.save(); g.scale(1, 1.6);                                              // Verlauf wird mit gestreckt: Mitte landet bei y ≈ 960
  const hell = g.createRadialGradient(512, 600, 30, 512, 600, 230);
  hell.addColorStop(0, "#f0dcbc"); hell.addColorStop(.62, "#d9b78c"); hell.addColorStop(1, "rgba(217,183,140,0)");
  g.fillStyle = hell; g.beginPath(); g.arc(512, 600 / 1.6, 230, 0, Math.PI * 2); g.fill(); g.restore();
  const bauch = g.createRadialGradient(512, 880, 20, 512, 880, 180);
  bauch.addColorStop(0, "#fbf3e4"); bauch.addColorStop(1, "rgba(251,243,228,0)");
  g.fillStyle = bauch; g.fillRect(250, 650, 524, 374);
  federn(g, r, { x0: 330, y0: 360, w: 364, h: 600, dichte: 20, dunkel: "#b08458", hell: "#fff4e2", alpha: .2 });
  return alsTextur(c);
}
function kopfTextur(){
  const [c, g] = leinwand(1024, 512), r = prng(12);
  g.fillStyle = "#6c4528"; g.fillRect(0, 0, 1024, 512);
  federn(g, r, { w: 1024, h: 512, dichte: 18, dunkel: "#3a200e", hell: "#86603e", alpha: .3 });
  for (let i = 0; i < 260; i++){                                         // feine Strichel auf dem Scheitel
    const x = r() * 1024, y = r() * 220;
    g.globalAlpha = .35; g.strokeStyle = r() < .5 ? "#2f190b" : "#c49a6c"; g.lineWidth = 2;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - .5) * 4, y + 8 + r() * 8); g.stroke();
  }
  g.globalAlpha = 1; return alsTextur(c);
}
// Gesichtsschleier: hell, mit strahlenförmigen Federn um das Auge und dunklem Rand
function schleierTextur(){
  const [c, g] = leinwand(1024, 512), r = prng(13), cx = 256, cy = 256, grad = 512 / 180;
  g.fillStyle = "#6e4527"; g.fillRect(0, 0, 1024, 512);
  const rand = 72 * grad, innen = 64 * grad;
  g.fillStyle = "#5a3519"; g.beginPath(); g.arc(cx, cy, rand, 0, Math.PI * 2); g.fill();
  const f = g.createRadialGradient(cx, cy, 10, cx, cy, innen);
  f.addColorStop(0, "#fbefdc"); f.addColorStop(.7, "#f0dcbd"); f.addColorStop(1, "#d6b58a");
  g.fillStyle = f; g.beginPath(); g.arc(cx, cy, innen, 0, Math.PI * 2); g.fill();
  for (let i = 0; i < 220; i++){
    const a = r() * Math.PI * 2, r0 = (20 + r() * 25) * grad, r1 = r0 + (14 + r() * 18) * grad;
    g.globalAlpha = .22; g.strokeStyle = r() < .6 ? "#b48a5e" : "#ffffff"; g.lineWidth = 2.5;
    g.beginPath(); g.moveTo(cx + Math.cos(a) * r0, cy + Math.sin(a) * r0); g.lineTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1); g.stroke();
  }
  g.globalAlpha = 1; return alsTextur(c);
}
// Augapfel: großes Schwarz, Bernstein-Ring, dunkler Außenrand – dreht sich zum Blicken
function augenTextur(){
  const [c, g] = leinwand(1024, 512), cx = 256, cy = 256, grad = 512 / 180;
  g.fillStyle = "#1a0d05"; g.fillRect(0, 0, 1024, 512);
  const iris = g.createRadialGradient(cx, cy, 30 * grad, cx, cy, 56 * grad);
  iris.addColorStop(0, "#7a3a08"); iris.addColorStop(.18, "#e08a1c"); iris.addColorStop(.62, "#f7b43a"); iris.addColorStop(.86, "#c4701a"); iris.addColorStop(1, "#3a1a06");
  g.fillStyle = iris; g.beginPath(); g.arc(cx, cy, 56 * grad, 0, Math.PI * 2); g.fill();
  for (let i = 0; i < 90; i++){                                          // Iris-Fasern
    const a = i / 90 * Math.PI * 2;
    g.globalAlpha = .18; g.strokeStyle = i % 2 ? "#fff0b0" : "#8a4510"; g.lineWidth = 2;
    g.beginPath(); g.moveTo(cx + Math.cos(a) * 33 * grad, cy + Math.sin(a) * 33 * grad); g.lineTo(cx + Math.cos(a) * 52 * grad, cy + Math.sin(a) * 52 * grad); g.stroke();
  }
  g.globalAlpha = 1; g.fillStyle = "#050307"; g.beginPath(); g.arc(cx, cy, 31 * grad, 0, Math.PI * 2); g.fill();
  return alsTextur(c);
}
// Flügel: Leinwand oben = Schulter, unten = Federspitzen
function fluegelTextur(){
  const [c, g] = leinwand(512, 1024), r = prng(14);
  const grund = g.createLinearGradient(0, 0, 0, 1024); grund.addColorStop(0, "#80532f"); grund.addColorStop(1, "#5c3820");
  g.fillStyle = grund; g.fillRect(0, 0, 512, 1024);
  federn(g, r, { w: 512, h: 400, dichte: 34, dunkel: "#33190a", hell: "#a07048", alpha: .6 });
  for (let k = 0; k < 9; k++){                                           // lange Schwungfedern mit hellen Bändern
    const x0 = 10 + k * 58, top = 380 + (k % 2) * 20;
    g.fillStyle = k % 2 ? "#6a4224" : "#5e391d"; g.globalAlpha = 1;
    g.beginPath(); g.moveTo(x0, top); g.lineTo(x0 + 54, top); g.lineTo(x0 + 54, 990); g.quadraticCurveTo(x0 + 27, 1030, x0, 990); g.closePath(); g.fill();
    g.globalAlpha = .6; g.strokeStyle = "#2a1408"; g.lineWidth = 3; g.beginPath(); g.moveTo(x0 + 27, top); g.lineTo(x0 + 27, 1000); g.stroke();
    g.globalAlpha = .5; g.strokeStyle = "#e3c497"; g.lineWidth = 2.5; g.beginPath(); g.moveTo(x0 + 52, top); g.lineTo(x0 + 52, 990); g.stroke();
  }
  federn(g, r, { y0: 300, w: 512, h: 120, dichte: 40, dunkel: "#2e170a", hell: "#b48456", alpha: .7 });
  g.globalAlpha = 1; const t = alsTextur(c, false);
  t.repeat.set(1 / 1.15, 1 / 1.9); t.offset.set(.55 / 1.15, 1); return t;
}
const PM = (o) => new THREE.MeshPhysicalMaterial({ roughness: .8, metalness: 0, ...o });
const kugel = (r, ws = 64, hs = 48) => new THREE.SphereGeometry(r, ws, hs);
// Eiförmiger Drehkörper: halbe Höhe a, Radius b, unten etwas breiter (bauch > 0)
function ei(a, b, bauch = .08, seg = 96){
  const pts = [];
  for (let i = 0; i <= 48; i++){ const th = Math.PI * i / 48; pts.push(new THREE.Vector2(Math.max(b * Math.sin(th) * (1 + bauch * Math.cos(th)), 1e-4), -a * Math.cos(th))); }
  return new THREE.LatheGeometry(pts, seg, Math.PI);
}
const clamp = (x, a = -1, b = 1) => Number.isFinite(x) ? Math.min(b, Math.max(a, x)) : 0;
export function eule(){
  const root = new THREE.Group(), body = new THREE.Group(), hals = new THREE.Group(), head = new THREE.Group();
  const sprung = new THREE.Group();                                       // hebt beim Hüpfen Körper und Füße gemeinsam an
  root.add(sprung); sprung.add(body); body.add(hals); hals.add(head);
  hals.position.set(0, 2.2, .02); head.position.set(0, .58, 0); hals.rotation.order = "YXZ";
  const fK = koerperTextur(), fKopf = kopfTextur(), fFl = fluegelTextur();
  const feder = (map, extra = {}) => PM({ map, bumpMap: map, bumpScale: .9, sheen: .7, sheenRoughness: .55, sheenColor: new THREE.Color(0xffe2c0), ...extra });
  const braun = feder(fKopf), koerper = feder(fK), schleier = feder(schleierTextur(), { bumpScale: .8, roughness: .9 });
  const dunkel = feder(fKopf, { color: 0x8a6a55 });
  const lidM = PM({ color: 0xc89f74, roughness: .85, sheen: .5, sheenColor: new THREE.Color(0xffffff) });
  const augeM = PM({ map: augenTextur(), roughness: .12, clearcoat: 1, clearcoatRoughness: .04 });
  const glanz = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const schnabelM = PM({ color: 0xe8a22a, roughness: .35, clearcoat: .7, clearcoatRoughness: .2 });
  const fussM = PM({ color: 0xf2b23f, roughness: .45, clearcoat: .3 }), krallenM = PM({ color: 0x5b4a3e, roughness: .3, clearcoat: .6 });
  const hutM = PM({ color: 0x1f2b58, roughness: .6, sheen: .4, sheenColor: new THREE.Color(0x6f86d6) }), quaste = PM({ color: 0xe9b928, roughness: .45, sheen: .6, sheenColor: new THREE.Color(0xfff2a0) });
  // Rumpf: ein Ei mit heller, gefleckter Brust in der Textur
  body.add(mesh(ei(1.32, 1.3), koerper, [0, 1.42, 0], [1, 1, .93]));
  // Kopf: groß und rund, sitzt ohne Hals auf dem Rumpf
  head.add(mesh(ei(1.0, 1.16, -.04), braun, [0, 0, 0], [1, 1, .94]));
  // Gesichtsschleier und Augen
  const augen = [], lider = [], unterlider = [], brauen = [];
  [-1, 1].forEach(sd => {
    const x = sd * .43;
    const s = put(head, mesh(kugel(.54), schleier, [x, -.04, .74], [1, 1.08, .56])); s.rotation.y = sd * .22;
    const a = put(head, mesh(kugel(.34, 64, 48), augeM, [x, .02, .92], [1, 1, .75])); a.userData.ry = sd * .08; augen.push(a);
    head.add(mesh(kugel(.055, 16, 12), glanz, [x + .1, .1, 1.18]));
    head.add(mesh(kugel(.028, 12, 8), glanz, [x - .07, -.1, 1.19]));
    const lid = put(head, mesh(new THREE.SphereGeometry(.355, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), lidM, [x, .02, .92], [1, 1, .78])); lider.push(lid);
    const unterlid = put(head, mesh(new THREE.SphereGeometry(.352, 48, 24, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), lidM, [x, .02, .92], [1, 1, .78])); unterlider.push(unterlid);
    const br = put(head, mesh(new THREE.TorusGeometry(.26, .045, 12, 32, Math.PI * .7), dunkel, [x * 1.04, .3, .96], [1, 1, .6])); br.rotation.z = Math.PI * .15; brauen.push(br);   // Bogen nach oben = freundlich
  });
  head.add(mesh(kugel(.28, 32, 24), braun, [0, .26, .92], [.42, .78, .42]));   // braune Federspitze zwischen den Augen
  // Schnabel: kurz, nach unten gebogen
  const oben = put(head, mesh(new THREE.ConeGeometry(.15, .4, 32), schnabelM, [0, -.3, 1.16])); oben.rotation.x = Math.PI * .66;
  head.add(mesh(kugel(.14, 24, 16), schnabelM, [0, -.17, 1.1], [1, .8, .8]));
  const unten = put(head, mesh(new THREE.ConeGeometry(.08, .12, 24), schnabelM, [0, -.36, 1.02])); unten.rotation.x = Math.PI * .6;
  // Federohren
  [-1, 1].forEach(sd => { const o = put(head, mesh(new THREE.ConeGeometry(.2, .5, 32), braun, [sd * .74, .78, -.02], [1, 1, .6])); o.rotation.z = -sd * .45; });
  // Flügel: eine durchgehende, leicht gebogene Fläche mit gezacktem Federrand
  const fluegelMat = PM({ map: fFl, bumpMap: fFl, bumpScale: .9, roughness: .75, sheen: .6, sheenColor: new THREE.Color(0xffd5a8), side: THREE.DoubleSide });
  const fluegelGeo = (() => {
    const sh = new THREE.Shape(), tip = [.28, -1.8], end = [-.5, -.55];
    sh.moveTo(0, 0);
    sh.bezierCurveTo(.38, -.2, .52, -.95, tip[0], tip[1]);
    const n = 7, dx = end[0] - tip[0], dy = end[1] - tip[1], L = Math.hypot(dx, dy), ox = -dy / L, oy = dx / L;
    for (let i = 1; i <= n; i++){
      const ax = tip[0] + dx * (i - 1) / n, ay = tip[1] + dy * (i - 1) / n, bx = tip[0] + dx * i / n, by = tip[1] + dy * i / n;
      sh.quadraticCurveTo((ax + bx) / 2 + ox * .17, (ay + by) / 2 + oy * .17, bx, by);
    }
    sh.bezierCurveTo(-.55, -.35, -.3, -.04, 0, 0);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: .06, bevelEnabled: true, bevelThickness: .045, bevelSize: .04, bevelSegments: 4, curveSegments: 28 });
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i++) pos.setZ(i, pos.getZ(i) - .32 * pos.getX(i) * pos.getX(i));
    geo.computeVertexNormals(); return geo;
  })();
  const fluegelGruppe = sd => {
    const g = new THREE.Group(); g.position.set(sd * 1.0, 2.15, .22); body.add(g);
    const m = new THREE.Mesh(fluegelGeo, fluegelMat); m.scale.x = sd; g.add(m);
    return { g, m, sd };
  };
  const fl = fluegelGruppe(-1), fr = fluegelGruppe(1);
  const fluegelPose = (w, raise, spread, schwing) => {
    const offen = Math.min(1, raise / 1.2);
    w.g.rotation.z = w.sd * (.04 + raise + schwing);
    w.g.rotation.y = -w.sd * (.72 - .55 * offen);
    w.g.rotation.x = -.05 - offen * .1;
    w.m.scale.set(w.sd * (1 + .22 * spread), 1 + .08 * spread, 1);
  };
  // Federhosen: kurze gefiederte Beine verbinden Bauch und Füße
  const hoseM = PM({ color: 0xe9d6b6, roughness: .9, sheen: .8, sheenRoughness: .5, sheenColor: new THREE.Color(0xffffff) });
  [-.45, .45].forEach(x => sprung.add(mesh(kugel(.24, 32, 24), hoseM, [x, .3, .42], [1, 1.1, 1])));
  // Füße: drei kräftige Zehen mit dunklen Krallen
  [-.45, .45].forEach(x => [-.14, 0, .14].forEach(d => {
    const zeh = new THREE.Group(); zeh.position.set(x + d * .9, .09, .66); zeh.rotation.y = d * 1.6; sprung.add(zeh);
    const z = mesh(new THREE.CapsuleGeometry(.08, .18, 8, 16), fussM, [0, 0, .08]); z.rotation.x = Math.PI / 2; zeh.add(z);
    const k = mesh(new THREE.ConeGeometry(.04, .1, 12), krallenM, [0, -.03, .24]); k.rotation.x = Math.PI * .62; zeh.add(k);
  }));
  // Doktorhut mit Quaste
  const hut = new THREE.Group(); hut.position.set(0, .93, -.05); hut.rotation.z = -.08; head.add(hut);
  hut.add(mesh(new THREE.CylinderGeometry(.5, .56, .34, 48), hutM));
  put(hut, mesh(new THREE.BoxGeometry(1.45, .08, 1.45), hutM, [0, .2, 0])).rotation.y = Math.PI / 4;
  hut.add(mesh(kugel(.07, 16, 12), quaste, [0, .26, 0]));
  const q = new THREE.Group(); q.position.set(.64, .22, .24); hut.add(q);
  q.add(mesh(new THREE.CylinderGeometry(.022, .022, .5, 12), quaste, [0, -.25, 0]));
  q.add(mesh(kugel(.05, 12, 8), quaste, [0, -.5, 0]));
  for (let i = 0; i < 9; i++){ const a = i / 9 * Math.PI * 2; q.add(mesh(new THREE.CylinderGeometry(.012, .008, .26, 6), quaste, [Math.cos(a) * .035, -.66, Math.sin(a) * .035])); }
  root.traverse(o => { if (o.isMesh){ o.castShadow = true; o.receiveShadow = true; } });
  // Lid-Winkel: -1.75 = ganz offen, 1.45 = zu; Ruhe wach. Unterlid drückt von unten hoch = freundliche, lächelnde Augen
  const LID_OFFEN = -1.75, LID_ZU = 1.45, LID_RUHE = -1.3, UNTERLID_RUHE = .8, UNTERLID_OFFEN = 1.4;
  return { root, update(t, s = {}){
    root.scale.setScalar(Math.max(backOut(s.intro ?? 1) || 0, .001));
    const hoehe = Math.abs(Math.sin(t * 6)), hop = clamp(s.hop ?? 0, 0, 1);
    sprung.position.y = hop * hoehe * .3;
    const dehnen = hop * (hoehe - .5) * .08;                                // in der Luft gestreckt, bei der Landung gestaucht
    body.position.y = Math.sin(t * 1.9) * .035;
    body.scale.set(1 + Math.sin(t * 1.9) * .008 - dehnen * .5, 1 - Math.sin(t * 1.9) * .008 + dehnen, 1);
    body.rotation.z = clamp(s.lehnen ?? 0) * .12;
    // Kopf frei (look = alter Parameter, schwächer, damit alte Drehbücher gleich aussehen): kopf = drehen, nicken = hoch/runter, neigen = schräg (jeweils -1 … 1)
    const dreh = clamp((s.kopf ?? 0) + (s.look ?? 0) * .45), nick = clamp(s.nicken ?? 0), neig = clamp(s.neigen ?? 0);
    hals.rotation.y = dreh * .9 + Math.sin(t * .8) * .06;
    hals.rotation.x = -nick * .32 + (s.talk ?? 0) * Math.sin(t * 3.1) * .03;
    hals.rotation.z = neig * .35 + Math.sin(t * 1.3) * .04;
    // Blick: Augäpfel drehen sich, Standard folgt etwas der Kopfdrehung
    const [bx, by] = Array.isArray(s.blick) ? s.blick : [dreh * .4, 0];
    augen.forEach(a => { a.rotation.y = a.userData.ry + clamp(bx) * .38; a.rotation.x = -clamp(by) * .3; });
    const staunen = clamp(s.staunen ?? 0, 0, 1), zu = ((t + .4) % 3.6) < .16;
    const lid = zu ? LID_ZU : LID_RUHE + (LID_OFFEN - LID_RUHE) * staunen - clamp(by, -1, 0) * .3;
    lider.forEach(l => l.rotation.x = lid);
    unterlider.forEach(l => l.rotation.x = UNTERLID_RUHE + (UNTERLID_OFFEN - UNTERLID_RUHE) * staunen);
    const talk = (s.talk ?? 0) * mouthOpen(t);
    unten.rotation.x = Math.PI * (.6 + talk * .08); unten.position.y = -.33 - talk * .08;
    brauen.forEach(b => { b.position.y = .3 + staunen * .08 + (s.talk ?? 0) * .04 * Math.abs(Math.sin(t * 2.4)); });
    const w = s.wave ?? 0, pt = s.point ?? 0, rede = (s.talk ?? 0) * Math.abs(Math.sin(t * 2.2));
    fluegelPose(fr, w * 1.9 + pt * 1.35, Math.max(w, pt), w * Math.sin(t * 8) * .35 + pt * Math.sin(t * 2) * .05);
    fluegelPose(fl, rede * .25 + (s.pointL ?? 0) * 1.35, rede * .4 + (s.pointL ?? 0), 0);
    q.rotation.z = Math.sin(t * 2.6) * .2 - hals.rotation.z * .6; q.rotation.x = Math.sin(t * 1.7) * .1;
  }};
}

// ---------- Bühne ----------
// Weiches Studio-Umgebungslicht (helle Flächen in einem grauen Raum) für runde Glanzlichter
function studioLicht(renderer){
  const raum = new THREE.Scene(), box = new THREE.BoxGeometry(1, 1, 1);
  raum.add(mesh(box, new THREE.MeshBasicMaterial({ color: 0x8a8f9c, side: THREE.BackSide }), [0, 0, 0], [20, 12, 20]));
  const flaeche = (farbe, [x, y, z], [sx, sy, sz]) => raum.add(mesh(box, new THREE.MeshBasicMaterial({ color: farbe }), [x, y, z], [sx, sy, sz]));
  flaeche(0xffffff, [0, 5.8, 0], [8, .1, 8]);
  flaeche(0xfff1dc, [-9.8, 2, 2], [.1, 5, 6]);
  flaeche(0xdfe8ff, [9.8, 1, -2], [.1, 4, 5]);
  flaeche(0xffffff, [0, 1.5, 9.8], [7, 4, .1]);
  const pm = new THREE.PMREMGenerator(renderer), tex = pm.fromScene(raum, .04).texture; pm.dispose();
  box.dispose(); raum.traverse(o => o.material?.dispose()); return tex;
}
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
    scene.environment = studioLicht(renderer); scene.environmentIntensity = .35;
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
