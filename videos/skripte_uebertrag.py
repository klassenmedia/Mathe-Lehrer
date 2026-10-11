"""Drehbücher Teil 3: Plus und Minus mit Übertrag (Videos 11 und 12)."""
from skripte import merke, titel, tok

# Positionen in der Baustein-Bühne (1150 x 530): links Zehner, rechts Einer
BLOCK_JS = '''
const BX = i => [40 + i*60, 120];                                  // Zehnerstange i
const CX = k => [660 + (k % 5)*62, 130 + Math.floor(k / 5)*62];     // Einerwürfel k
const SX = j => [1060, 120 + j*36];                                 // Würfel j im Turm (= eine Stange)
'''


def colored(n):
    """Zahl mit farbigen Stellen (Einer orange, sonst blau)."""
    s = str(n)
    return "".join(f'<span class="{"o" if i == len(s) - 1 else "b"}">{c}</span>' for i, c in enumerate(s))


def sortieren(a, op, b, cols, say):
    """Szene: Aufgabe steht nebeneinander und wird untereinander sortiert."""
    return dict(
        say=say,
        html=f'<div class="col" style="gap:40px"><div class="hz-row h0">{colored(a)}<span>{op}</span>{colored(b)}</div>'
             f'<div class="h ar" style="font-size:56px">↓ untereinander ↓</div><div class="w"></div></div>',
        js=f'''
const R = written(q(".w"), {cols!r}, "{a}", "{b}", "{op}");
rise(q(".h0"), t[0]);
pop(q(".ar"), t[1]);
rise(R.hd, t[1] + .6, .2);
R.a.forEach((c, i) => drop(c, t[1] + 1.4 + (R.a.length - 1 - i)*.25));
R.b.forEach((c, i) => drop(c, t[1] + 2.4 + (R.b.length - 1 - i)*.25));
''')


def schriftlich(a, op, b, cols, say, steps, fin_at, fin):
    """Szene: schriftliches Rechnen Stelle für Stelle. steps: Liste von JS-Schnipseln, die R benutzen."""
    return dict(
        say=say,
        html=f'<div class="colL" style="align-items:center;gap:40px"><div class="w"></div><div class="eq m fin">{tok(fin, "g")}</div></div>',
        js=f'const R = written(q(".w"), {cols!r}, "{a}", "{b}", "{op}");\nrise(q(".w"), T0 + .2);\n'
           + "\n".join(steps) + f'\nrise(q(".fin"), {fin_at});')


def ersetze(R_i, at, neu, row="a"):
    return f'strikeCell(R.{row}[{R_i}], {at}); pop(put(R.{row}[{R_i}], "{neu}", "sm"), {at} + .4);'


# ---------------------------------------------------------------- 11 Plus mit Übertrag
PLUS = dict(id="11-plus-mit-uebertrag", topic="Plus mit Übertrag", scenes=[
    titel("+1", "Plus mit Übertrag", "wenn 10 voll sind, wird getauscht",
          ["Hallo! Heute lernen wir, was ein Übertrag beim Plus ist."], symsize=120),

    sortieren(47, "+", 38, ["Z", "E"],
              ["In deinem Heft stehen die Aufgaben nebeneinander: 47 + 38.",
               "Der Trick: Wir schreiben sie untereinander. Einer unter Einer, Zehner unter Zehner."]),

    dict(say=["So sieht 47 mit Bausteinen aus: 4 Zehnerstangen und 7 Einerwürfel.",
              "Dazu kommen 38: 3 Zehnerstangen und 8 Einerwürfel.",
              "Wir fangen immer rechts an, bei den Einern: 7 + 8 = 15.",
              "15 Würfel! Das sind mehr als 10. Also kleben wir 10 Würfel zu einer Zehnerstange zusammen.",
              "Die neue Stange wandert zu den Zehnern. Das ist der Übertrag. Wir schreiben eine kleine 1 über die Zehner.",
              "Bei den Einern bleiben 5 Würfel. Wir schreiben 5.",
              "Jetzt die Zehner: 4 + 3 = 7. Plus der Übertrag 1, das sind 8 Zehner.",
              "Also: 47 + 38 = 85."],
         html='<div class="bstage"><div class="div"></div><div class="blab b" style="left:0;width:600px">Zehner</div><div class="blab o" style="left:604px;width:546px">Einer</div></div>'
              '<div class="colL" style="align-items:center;gap:30px"><div class="w"></div><div class="eq m fin">' + tok("47 + 38 = 85", "g") + '</div></div>',
         js=BLOCK_JS + '''
const B = q(".bstage"), R = written(q(".w"), ["Z","E"], "47", "38", "+");
const bars = [0,1,2,3,4,5,6].map(i => klotz(B, "st", ...BX(i)));
const cubes = Array.from({length:15}, (_, k) => klotz(B, "", ...CX(k)));
drop(bars.slice(0,4), t[0] + .8, .15); drop(cubes.slice(0,7), t[0] + 2.4, .08);
drop(bars.slice(4), t[1] + .8, .15);   drop(cubes.slice(7), t[1] + 2.4, .08);
tl.fromTo([R.a[0], R.a[1]], {opacity:0}, {opacity:1, duration:.4}, t[0]);
tl.fromTo([R.b[0], R.b[1]], {opacity:0}, {opacity:1, duration:.4}, t[1]);
// Einer
markAt(R.res[1], t[2], 4);
tl.fromTo(cubes, {filter:"brightness(1)"}, {filter:"brightness(1.35)", duration:.3, yoyo:true, repeat:1}, t[2] + 1);
// 10 Würfel zum Turm
for (let k = 0; k < 10; k++) moveTo(cubes[k], CX(k), SX(k), t[3] + 2.4 + k*.08, .6);
const nb = klotz(B, "st", ...SX(0));
tl.fromTo(nb, {opacity:0}, {opacity:1, duration:.4}, t[3] + 3.6);
tl.to(cubes.slice(0,10), {opacity:0, duration:.3}, t[3] + 3.8);
// Übertrag: Stange wandert zu den Zehnern
moveTo(nb, SX(0), BX(7), t[4] + .6, 1.1, "power3.inOut");
tl.fromTo(nb, {rotationY:0}, {rotationY:360, duration:1.1, ease:"power2.inOut"}, t[4] + .6);
pop(put(R.cr[0], "1"), t[4] + 3.4);
// restliche Würfel aufrücken
for (let k = 10; k < 15; k++) moveTo(cubes[k], CX(k), CX(k - 10), t[5], .6);
pop(put(R.res[1], "5", "g"), t[5] + 2);
// Zehner
markAt(R.res[0], t[6], 5);
tl.fromTo([...bars, nb], {filter:"brightness(1)"}, {filter:"brightness(1.35)", duration:.3, yoyo:true, repeat:1, stagger:.1}, t[6] + 2);
pop(put(R.res[0], "8", "g"), t[6] + 4);
rise(q(".fin"), t[7] + .3);
'''),

    dict(say=["Ein häufiger Fehler: Man vergisst den Übertrag.",
              "Dann kommt 75 heraus. Das ist falsch! Die kleine 1 muss immer mitgezählt werden."],
         html='<div class="pv"><div class="card c1"><div class="big r tok">75<span class="strike"></span></div><div class="sub">Übertrag vergessen</div></div>'
              '<div class="card c2"><div class="big g">85</div><div class="sub">mit Übertrag</div></div></div>',
         js='pop(q(".c1"), t[1]); draw(q(".c1 .strike"), t[1] + 1.8); pop(q(".c2"), t[1] + 3);'),

    schriftlich("268", "+", "157", ["H", "Z", "E"],
                ["Bei großen Zahlen geht es genauso: 268 + 157.",
                 "Einer: 8 + 7 = 15. Schreibe 5, die 1 wandert als Übertrag zu den Zehnern.",
                 "Zehner: 6 + 5 = 11, plus Übertrag 1 sind 12. Schreibe 2, die 1 wandert zu den Hundertern.",
                 "Hunderter: 2 + 1 = 3, plus Übertrag 1 sind 4.",
                 "Ergebnis: 268 + 157 = 425."],
                ['plus_step(R, 2, t[1], "5", 1, t[1] + 3.2);',
                 'plus_step(R, 1, t[2], "2", 0, t[2] + 4.4);',
                 'plus_step(R, 0, t[3], "4");'],
                "t[4]", "268 + 157 = 425"),

    schriftlich("2475", "+", "1368", ["T", "H", "Z", "E"],
                ["Und sogar mit Tausendern: 2475 + 1368.",
                 "Einer: 5 + 8 = 13. Schreibe 3, merke 1.",
                 "Zehner: 7 + 6 + 1 = 14. Schreibe 4, merke 1.",
                 "Hunderter: 4 + 3 + 1 = 8.",
                 "Tausender: 2 + 1 = 3. Ergebnis: 3843."],
                ['plus_step(R, 3, t[1], "3", 2, t[1] + 2.2);',
                 'plus_step(R, 2, t[2], "4", 1, t[2] + 2.4);',
                 'plus_step(R, 1, t[3], "8");',
                 'plus_step(R, 0, t[4], "3");'],
                "t[4] + 2.6", "2475 + 1368 = 3843"),

    merke(["Untereinander schreiben: Einer unter Einer.",
           "Immer rechts bei den Einern anfangen.",
           "10 oder mehr? Die 1 wandert als Übertrag nach links."],
          ["Merke: Schreib die Zahlen untereinander. Einer unter Einer, Zehner unter Zehner.",
           "Fang immer rechts bei den Einern an.",
           "Sind es 10 oder mehr, wandert die 1 als Übertrag eine Stelle nach links. Und den Übertrag nie vergessen! Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 12 Minus mit Übertrag
MINUS = dict(id="12-minus-mit-uebertrag", topic="Minus mit Übertrag", scenes=[
    titel("−1", "Minus mit Übertrag", "einen Zehner aufmachen",
          ["Hallo! Heute lernen wir, was man beim Minus macht, wenn es nicht reicht."], symsize=120),

    sortieren(52, "−", 27, ["Z", "E"],
              ["Wir rechnen 52 − 27.",
               "Wieder schreiben wir untereinander. Einer unter Einer, Zehner unter Zehner. Die größere Zahl steht oben."]),

    dict(say=["52, das sind 5 Zehnerstangen und 2 Einerwürfel.",
              "Wir fangen rechts an, bei den Einern: 2 − 7. Das geht nicht! Wir haben nur 2 Würfel.",
              "Also machen wir eine Zehnerstange auf und tauschen sie in 10 Einerwürfel.",
              "Jetzt sind es nur noch 4 Zehner. Bei den Einern haben wir 12.",
              "12 − 7 = 5. Wir nehmen 7 Würfel weg.",
              "Jetzt die Zehner: 4 − 2 = 2.",
              "Also: 52 − 27 = 25."],
         html='<div class="bstage"><div class="div"></div><div class="blab b" style="left:0;width:600px">Zehner</div><div class="blab o" style="left:604px;width:546px">Einer</div></div>'
              '<div class="colL" style="align-items:center;gap:30px"><div class="w"></div><div class="eq m fin">' + tok("52 − 27 = 25", "g") + '</div></div>',
         js=BLOCK_JS + '''
const B = q(".bstage"), R = written(q(".w"), ["Z","E"], "52", "27", "−");
const bars = [0,1,2,3,4].map(i => klotz(B, "st", ...BX(i)));
const cubes = [0,1].map(k => klotz(B, "", ...CX(k)));
const neu = Array.from({length:10}, (_, j) => klotz(B, "", ...SX(j)));
drop(bars, t[0] + .6, .15); drop(cubes, t[0] + 2.6, .15);
tl.fromTo([R.a[0], R.a[1], R.b[0], R.b[1]], {opacity:0}, {opacity:1, duration:.4}, t[0]);
markAt(R.res[1], t[1], 4);
tl.fromTo(cubes, {x:0}, {x:12, duration:.08, yoyo:true, repeat:5}, t[1] + 3);
// Stange aufmachen
moveTo(bars[4], BX(4), SX(0), t[2] + 1, 1, "power3.inOut");
tl.to(bars[4], {opacity:0, duration:.2}, t[2] + 2.2);
tl.fromTo(neu, {opacity:0}, {opacity:1, duration:.2}, t[2] + 2.2);
for (let j = 0; j < 10; j++) moveTo(neu[j], SX(j), CX(j + 2), t[2] + 2.8 + j*.07, .6);
strikeCell(R.a[0], t[3]); pop(put(R.a[0], "4", "sm"), t[3] + .5);
strikeCell(R.a[1], t[3] + 1.6); pop(put(R.a[1], "12", "sm"), t[3] + 2.1);
// 7 Würfel weg
tl.to(neu.slice(3), {y:"+=220", opacity:0, duration:.6, stagger:.12, ease:"power2.in"}, t[4] + 2);
pop(put(R.res[1], "5", "g"), t[4] + 3.4);
// Zehner
markAt(R.res[0], t[5], 3.5);
tl.to([bars[3], bars[2]], {y:-200, opacity:0, duration:.6, stagger:.2, ease:"power2.in"}, t[5] + 1.2);
pop(put(R.res[0], "2", "g"), t[5] + 2.4);
rise(q(".fin"), t[6] + .3);
'''),

    dict(say=["Achtung, typischer Fehler: Manche rechnen bei den Einern einfach 7 − 2 = 5, also von unten nach oben.",
              "Dann kommt 35 heraus. Das ist falsch! Wir nehmen immer von der oberen Zahl weg.",
              "Probe mit Plus: 25 + 27 = 52. Stimmt!"],
         html='<div class="col"><div class="pv"><div class="card c1"><div class="big r tok">35<span class="strike"></span></div><div class="sub">von unten gerechnet</div></div>'
              '<div class="card c2"><div class="big g">25</div><div class="sub">richtig</div></div></div>'
              '<div class="eq m pr">' + tok("Probe: 25 + 27 = 52 ✓", "g") + '</div></div>',
         js='pop(q(".c1"), t[1]); draw(q(".c1 .strike"), t[1] + 2.4); pop(q(".c2"), t[1] + 3.4); rise(q(".pr"), t[2]);'),

    schriftlich("403", "−", "158", ["H", "Z", "E"],
                ["Schwieriger: 403 − 158.",
                 "Einer: 3 − 8 geht nicht. Wir brauchen einen Zehner. Aber bei den Zehnern steht eine 0!",
                 "Also gehen wir weiter nach links und machen einen Hunderter auf. Aus 4 Hundertern werden 3, und wir bekommen 10 Zehner.",
                 "Jetzt machen wir einen Zehner auf. Es bleiben 9 Zehner, und wir haben 13 Einer.",
                 "13 − 8 = 5.",
                 "Zehner: 9 − 5 = 4.",
                 "Hunderter: 3 − 1 = 2. Ergebnis: 245."],
                ['markAt(R.res[2], t[1], 14);',
                 ersetze(0, "t[2] + 2.6", "3") + 'const z10 = put(R.a[1], "10", "sm"); strikeCell(R.a[1], t[2] + 4.6); pop(z10, t[2] + 5);',
                 'tl.to(z10, {opacity:0, duration:.3}, t[3] + 1.2); pop(put(R.a[1], "9", "sm"), t[3] + 1.5);' + ersetze(2, "t[3] + 3.4", "13"),
                 'pop(put(R.res[2], "5", "g"), t[4] + 1);',
                 'markAt(R.res[1], t[5], 3); pop(put(R.res[1], "4", "g"), t[5] + 1.6);',
                 'markAt(R.res[0], t[6], 3); pop(put(R.res[0], "2", "g"), t[6] + 1.4);'],
                "t[6] + 2.8", "403 − 158 = 245"),

    schriftlich("5230", "−", "1415", ["T", "H", "Z", "E"],
                ["Auch bei Tausendern geht es genauso: 5230 − 1415.",
                 "Einer: 0 − 5 geht nicht. Wir machen einen Zehner auf: 10 − 5 = 5.",
                 "Zehner: Jetzt sind es nur noch 2. 2 − 1 = 1.",
                 "Hunderter: 2 − 4 geht nicht. Wir machen einen Tausender auf: 12 − 4 = 8.",
                 "Tausender: Jetzt sind es nur noch 4. 4 − 1 = 3. Ergebnis: 3815."],
                [ersetze(2, "t[1] + 2.4", "2") + ersetze(3, "t[1] + 3", "10") + 'markAt(R.res[3], t[1], 5.5); pop(put(R.res[3], "5", "g"), t[1] + 4.4);',
                 'markAt(R.res[2], t[2], 3.5); pop(put(R.res[2], "1", "g"), t[2] + 2.4);',
                 ersetze(0, "t[3] + 2.6", "4") + ersetze(1, "t[3] + 3.2", "12") + 'markAt(R.res[1], t[3], 5.5); pop(put(R.res[1], "8", "g"), t[3] + 4.6);',
                 'markAt(R.res[0], t[4], 3.5); pop(put(R.res[0], "3", "g"), t[4] + 2.6);'],
                "t[4] + 4", "5230 − 1415 = 3815"),

    merke(["Untereinander schreiben, rechts anfangen.",
           "Oben zu wenig? Beim linken Nachbarn einen aufmachen und in 10 tauschen.",
           "Immer von oben nach unten rechnen."],
          ["Merke: Schreib untereinander und fang rechts an.",
           "Ist oben zu wenig, machst du beim linken Nachbarn einen auf und tauschst ihn in 10.",
           "Rechne immer von oben nach unten. Und am Ende die Probe mit Plus. Jetzt bist du dran!"]),
])

VIDEOS = [PLUS, MINUS]
