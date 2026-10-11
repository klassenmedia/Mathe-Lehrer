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

// ---------- Bühne ----------
export function buehne(canvas, W = 1920, H = 1080){
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.setPixelRatio(1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(28, W / H, .1, 100);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a93b8, 1.7));
  const key = new THREE.DirectionalLight(0xfff3e0, 2.1); key.position.set(-4, 7, 6); scene.add(key);
  const fill = new THREE.DirectionalLight(0xffffff, .9); fill.position.set(0, 2, 10); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xbfd4ff, .9); rim.position.set(5, 3, -4); scene.add(rim);
  const schatten = (x, r = 1.1) => {
    const s = new THREE.Mesh(new THREE.CircleGeometry(r, 24), new THREE.MeshBasicMaterial({ color: 0x1c2f5e, transparent: true, opacity: .14 }));
    s.rotation.x = -Math.PI / 2; s.position.set(x, .01, 0); scene.add(s); return s;
  };
  return { renderer, scene, camera, schatten, render: () => renderer.render(scene, camera) };
}
export const helfer = { ease, backOut };
