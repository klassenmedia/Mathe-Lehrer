"""Drehbücher der fünf Erklärvideos. Jede Szene: say (Sätze = Untertitel + Sprache), html, js.
Im js stehen zur Verfügung: S (Szene), T0/T1 (Start/Ende), t[i]/d[i] (Start/Dauer von Satz i),
q/qa (Selektoren in der Szene) und die Helfer aus template.html (pop, rise, draw, fadeTo, field, cookies)."""


def titel(sym, h1, p, say, symsize=150):
    return dict(
        say=say,
        html=f'<div class="title"><div class="sym" style="font-size:{symsize}px">{sym}</div><h1>{h1}</h1><p>{p}</p></div>',
        js='pop(q(".sym"), T0+.2); rise(q("h1"), T0+.5); rise(q("p"), T0+.8);',
    )


def merke(zeilen, say, schluss="Jetzt bist du dran!"):
    items = "".join(f'<div class="rule r{i}"><span class="k">Merke</span>{z}</div>' if i == 0 else
                    f'<div class="rule r{i}">{z}</div>' for i, z in enumerate(zeilen))
    return dict(
        say=say,
        html=f'<div class="col">{items}<div class="h go">{schluss}</div></div>',
        js="".join(f'rise(q(".r{i}"), t[{min(i, len(say) - 1)}]+.1);' for i in range(len(zeilen)))
           + 'pop(q(".go"), t[t.length-1]+.2);',
    )


def tok(txt, cls=""):
    return f'<span class="tok {cls}">{txt}</span>'


# ---------------------------------------------------------------- 1 Malreihen
MAL = dict(id="1-malreihen", topic="Malreihen", scenes=[
    titel("3·6", "Malreihen", "mit Tricks schnell rechnen",
          ["Hallo! Heute lernen wir Tricks für die Malreihen."], symsize=84),

    dict(say=["Was heißt eigentlich 4 · 6?",
              "Das heißt: 4-mal die 6.",
              "Also 4 Reihen mit je 6 Punkten.",
              "6, 12, 18, 24. Also ist 4 · 6 = 24."],
         html='<div class="eq e1">' + tok("4 · 6") + tok("= 24", "g res") + '</div><div class="f"></div>',
         js='''
const R = field(q(".f"), 4, 6, 64, null, r => String((r+1)*6));
rise(q(".e1 .tok"), t[0]);
pop(R.flatMap(r => r.dots), t[2], .04);
R.forEach((r, i) => pop(r.lab, t[3] + i*.6));
pop(q(".res"), t[3] + 2.6);
'''),

    dict(say=["Manche Aufgaben sind ganz leicht. Das sind die Kernaufgaben.",
              "1-mal ist einfach die Zahl selbst.",
              "2-mal ist das Doppelte: 6 + 6 = 12.",
              "10-mal: Hänge eine Null an. Das sind 60.",
              "Und 5-mal ist die Hälfte von 10-mal. Die Hälfte von 60 ist 30."],
         html='<div class="col"><div class="h hh" style="font-size:64px">Kernaufgaben</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:28px 40px">'
              '<div class="card c1"><div class="eq">1 · 6 = 6</div><div class="sub">die Zahl selbst</div></div>'
              '<div class="card c2"><div class="eq">2 · 6 = 12</div><div class="sub">das Doppelte</div></div>'
              '<div class="card c3"><div class="eq">10 · 6 = 60</div><div class="sub">Null anhängen</div></div>'
              '<div class="card c4"><div class="eq">5 · 6 = 30</div><div class="sub">Hälfte von 10 ·</div></div>'
              '</div></div>',
         js='rise(q(".hh"), t[0]); [1,2,3,4].forEach(i => pop(q(".c"+i), t[i]+.2));'),

    dict(say=["Jetzt eine schwere Aufgabe: 9 · 6.",
              "Wir fangen bei 10 · 6 an. Das ist leicht: 60.",
              "Aber wir wollen nur 9 Reihen. Eine Reihe ist zu viel.",
              "Die nehmen wir weg: 60 − 6 = 54.",
              "Also ist 9 · 6 = 54."],
         html='<div class="f"></div><div class="colL">'
              '<div class="eq m l0">' + tok("9 · 6 = ?") + '</div>'
              '<div class="eq m l1 b">' + tok("10 · 6 = 60") + '</div>'
              '<div class="eq m l2">' + tok("60 − 6 = 54") + '</div>'
              '<div class="eq l3">' + tok('<span class="mk"></span>9 · 6 = 54') + '</div></div>',
         js='''
const R = field(q(".f"), 10, 6, 46);
const st = document.createElement("div"); st.className = "fstrike"; R[9].row.append(st);
rise(q(".l0"), t[0]);
pop(R.flatMap(r => r.dots), t[1], .012);
rise(q(".l1"), t[1] + 1.2);
fadeTo(R[9].dots, t[2] + 1.2); draw(st, t[2] + 1.4);
rise(q(".l2"), t[3]);
rise(q(".l3"), t[4]); draw(q(".l3 .mk"), t[4] + .6);
'''),

    dict(say=["Und 7 · 6?",
              "Wir nehmen erst 5 · 6. Das sind 30.",
              "Dann fehlen noch 2 Reihen: 2 · 6 = 12.",
              "Zusammen: 30 + 12 = 42."],
         html='<div class="f"></div><div class="colL">'
              '<div class="eq m l0">' + tok("7 · 6 = ?") + '</div>'
              '<div class="eq m l1 b">' + tok("5 · 6 = 30") + '</div>'
              '<div class="eq m l2 o">' + tok("2 · 6 = 12") + '</div>'
              '<div class="eq l3">' + tok('<span class="mk"></span>30 + 12 = 42') + '</div></div>',
         js='''
const R = field(q(".f"), 7, 6, 54, r => r < 5 ? "" : "o");
rise(q(".l0"), t[0]);
pop(R.slice(0,5).flatMap(r => r.dots), t[1], .02); rise(q(".l1"), t[1] + 1);
pop(R.slice(5).flatMap(r => r.dots), t[2] + .8, .03); rise(q(".l2"), t[2] + 1.4);
rise(q(".l3"), t[3]); draw(q(".l3 .mk"), t[3] + .7);
'''),

    dict(say=["Noch ein Trick: Die 6er-Reihe ist das Doppelte der 3er-Reihe.",
              "8 · 3 = 24.",
              "Das Doppelte von 24 ist 48.",
              "Also ist 8 · 6 = 48."],
         html='<div class="f"></div><div class="colL">'
              '<div class="eq m l1 b">' + tok("8 · 3 = 24") + '</div>'
              '<div class="eq m l2 o">' + tok("24 + 24 = 48") + '</div>'
              '<div class="eq l3">' + tok('<span class="mk"></span>8 · 6 = 48') + '</div></div>',
         js='''
const R = field(q(".f"), 8, 6, 50, (r, c) => c < 3 ? "" : "o");
R.forEach(r => r.dots[3].style.marginLeft = "40px");
pop(R.flatMap(r => r.dots.slice(0,3)), t[1], .02); rise(q(".l1"), t[1] + .6);
pop(R.flatMap(r => r.dots.slice(3)), t[2], .02); rise(q(".l2"), t[2] + .8);
rise(q(".l3"), t[3]); draw(q(".l3 .mk"), t[3] + .6);
'''),

    merke(["Fang bei einer leichten Aufgabe an: 2-mal, 5-mal oder 10-mal.",
           "Dann rechne dazu oder ziehe ab."],
          ["Merke: Fang bei einer leichten Aufgabe an. 2-mal, 5-mal oder 10-mal.",
           "Dann rechnest du dazu oder ziehst ab.",
           "Jetzt bist du dran! Viel Spaß in der Zahlenwerkstatt."]),
])

# ---------------------------------------------------------------- 2 Teilen mit Rest
TEILEN = dict(id="2-teilen-mit-rest", topic="Teilen mit Rest", scenes=[
    titel(":", "Teilen mit Rest", "gerecht verteilen, was übrig bleibt",
          ["Hallo! Heute lernen wir, wie man mit Rest teilt."]),

    dict(say=["Wir haben 14 Kekse.",
              "Die wollen wir gerecht auf 4 Teller verteilen. Jeder Teller soll gleich viele bekommen.",
              "Runde 1: Jeder Teller bekommt einen Keks.",
              "Runde 2: Wieder bekommt jeder einen.",
              "Runde 3: Und noch einmal.",
              "Jetzt sind noch 2 Kekse übrig. Für 4 Teller reicht das nicht mehr.",
              "Diese 2 Kekse sind der Rest.",
              "Jeder Teller hat 3 Kekse. Also: 14 : 4 = 3 Rest 2."],
         html='<div class="cstage"><div class="ceq"><div class="eq">' + tok("14 : 4 =") + tok("3", "b")
              + tok('<span class="mk"></span>Rest 2', "r") + '</div></div></div>',
         js='''
const C = cookies(q(".cstage"), 14, 4, (i, a) => a.pile(i));
pop(C.ck, t[0], .05);
pop(C.plates, t[1] + .3, .15);
tl.fromTo(C.restbox, {opacity:0}, {opacity:1, duration:.4}, t[5]);
for (let k = 0; k < 3; k++) for (let p = 0; p < 4; p++) C.move(k*4 + p, C.plate(p, k), t[2+k] + .4 + p*.3);
C.move(12, C.rest(0), t[6]); C.move(13, C.rest(1), t[6] + .3);
const L = [0,1,2,3].map(p => C.plabel(p, "3")); pop(L, t[7], .1);
rise(q(".ceq .eq"), t[7] + .4); draw(q(".ceq .mk"), t[7] + 2.4);
'''),

    dict(say=["Ganz wichtig: Der Rest ist immer kleiner als die Zahl, durch die du teilst.",
              "Schau mal: 14 : 4 = 2 Rest 6. Stimmt das?",
              "Nein! Von den 6 Keksen kann jeder Teller noch einen bekommen.",
              "Dann bleiben nur 2 übrig. Richtig ist: 3 Rest 2.",
              "Merke: Ist der Rest zu groß, passt noch einer rein!"],
         html='<div class="col" style="gap:10px"><div class="rule rr" style="font-size:44px;padding:18px 36px">Der Rest ist immer <u>kleiner</u> als die Zahl, durch die du teilst.</div>'
              '<div class="cstage" style="height:640px;margin-top:-120px">'
              '<div class="ceq" style="top:530px;gap:60px"><div class="eq m wrong">' + tok('14 : 4 = 2 Rest 6<span class="strike"></span>', "r")
              + '</div><div class="eq m right">' + tok("14 : 4 = 3 Rest 2", "g") + '</div></div></div></div>',
         js='''
const C = cookies(q(".cstage"), 14, 4, (i, a) => i < 8 ? a.plate(i % 4, Math.floor(i / 4)) : a.rest(i - 8));
rise(q(".rr"), t[0]);
pop([...C.plates, ...C.ck], t[1], .02); tl.fromTo(C.restbox, {opacity:0}, {opacity:1, duration:.4}, t[1]);
rise(q(".wrong"), t[1] + .4);
draw(q(".wrong .strike"), t[2]);
for (let p = 0; p < 4; p++) C.move(8 + p, C.plate(p, 2), t[2] + 1 + p*.35);
for (let k = 0; k < 2; k++) C.move(12 + k, C.rest(k), t[2] + 2.6);
rise(q(".right"), t[3]);
tl.fromTo(q(".rr"), {scale:1}, {scale:1.06, duration:.3, yoyo:true, repeat:1}, t[4]);
'''),

    dict(say=["Mit großen Zahlen dauert das Verteilen zu lange. Schneller geht es mit der Malreihe.",
              "Beispiel: 29 : 5.",
              "Wir gehen die 5er-Reihe entlang: 5, 10, 15, 20, 25.",
              "30 ist schon zu groß! Das ist mehr als 29.",
              "Also nehmen wir 5 · 5 = 25.",
              "Von 25 bis 29 fehlen noch 4. Das ist der Rest.",
              "29 : 5 = 5 Rest 4."],
         html='<div class="col"><div class="eq e0">' + tok("29 : 5 = ?") + '</div><div class="series">'
              + "".join(f'<span class="chip ch{i}{" hit" if i == 5 else ""}{" over" if i == 6 else ""}">{i} · 5 = {i*5}'
                        + ('<span class="strike"></span>' if i == 6 else "") + '</span>' for i in range(1, 7))
              + '</div><div class="eq m e1">' + tok("25 + ") + tok("4", "r") + tok(" = 29") + '</div>'
              + '<div class="eq e2">' + tok('<span class="mk"></span>29 : 5 = 5 Rest 4') + '</div></div>',
         js='''
rise(q(".e0"), t[1]);
for (let i = 1; i <= 5; i++) pop(q(".ch"+i), t[2] + 1.7 + (i-1)*.62);
pop(q(".ch6"), t[3]); draw(q(".ch6 .strike"), t[3] + .8);
tl.fromTo(q(".ch5"), {scale:1}, {scale:1.15, duration:.35, yoyo:true, repeat:1}, t[4]);
rise(q(".e1"), t[5]);
rise(q(".e2"), t[6]); draw(q(".e2 .mk"), t[6] + .5);
'''),

    dict(say=["Zum Schluss machen wir die Probe. Wir rechnen rückwärts.",
              "5 · 5 = 25. Dazu der Rest 4: 25 + 4 = 29.",
              "Das ist genau unsere Zahl. Alles richtig!"],
         html='<div class="col"><div class="h hh">Probe</div><div class="eq m p1">' + tok("5 · 5 = 25") + '</div>'
              '<div class="eq m p2">' + tok("25 + 4 = 29") + '</div><div class="check">✓</div></div>',
         js='rise(q(".hh"), t[0]); rise(q(".p1"), t[1]); rise(q(".p2"), t[1] + 1.8); pop(q(".check"), t[2]);'),

    merke(["Suche in der Malreihe die größte Zahl, die passt.",
           "Der Rest ist immer kleiner als die Zahl, durch die du teilst.",
           "Mach am Ende die Probe."],
          ["Merke: Suche in der Malreihe die größte Zahl, die passt.",
           "Der Rest ist immer kleiner als die Zahl, durch die du teilst.",
           "Und mach am Ende die Probe. Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 3 Minus
def bars(n, cls="bar"):
    return "".join(f'<div class="{cls} k{i}"></div>' for i in range(n))


MINUS = dict(id="3-minus-rechenwege", topic="Minus-Rechenwege", scenes=[
    titel("−", "Minus rechnen", "erst die Zehner, dann die Einer",
          ["Hallo! Heute lernen wir einen Rechenweg für Minus-Aufgaben."]),

    dict(say=["Wir rechnen 70 − 26.",
              "Zuerst zerlegen wir die 26 in Zehner und Einer.",
              "26 = 20 + 6."],
         html='<div class="col"><div class="eq e0">' + tok("70 − 26") + '</div><div class="split">'
              '<div class="pbox p0">26</div><div class="arrows"><span class="a1 tok">↙</span><span class="a2 tok">↘</span></div>'
              '<div class="parts"><div class="pbox bl p1">20</div><div class="pbox or p2">6</div></div></div></div>',
         js='rise(q(".e0"), t[0]); pop(q(".p0"), t[1]); pop(qa(".arrows .tok"), t[1]+1.2, .2); pop(q(".p1"), t[2]+.3); pop(q(".p2"), t[2]+1);'),

    dict(say=["70, das sind 7 Zehnerstangen.",
              "Erst nehmen wir die Zehner weg. 20, das sind 2 Stangen.",
              "70 − 20 = 50."],
         html='<div class="b10">' + bars(7) + '</div><div class="eq m e1">' + tok('<span class="mk"></span>70 − 20 = 50') + '</div>',
         js='''
pop(qa(".bar"), t[0], .12);
tl.to([q(".k5"), q(".k6")], {y:-140, opacity:0, duration:.7, ease:"power2.in", stagger:.2}, t[1] + 2);
rise(q(".e1"), t[2]); draw(q(".e1 .mk"), t[2] + .8);
'''),

    dict(say=["Jetzt müssen noch 6 Einer weg.",
              "Aber wir haben nur Zehnerstangen! Was nun?",
              "Wir tauschen eine Stange in 10 Einerwürfel.",
              "Jetzt nehmen wir 6 Würfel weg.",
              "Es bleiben 4 Stangen und 4 Würfel. Das sind 44."],
         html='<div class="b10">' + bars(5) + '<div class="cubes">' + "".join(f'<div class="cube u{i}"></div>' for i in range(10))
              + '</div></div><div class="colL"><div class="eq m e0">' + tok("50 − 6 = ?") + '</div>'
              '<div class="eq e1">' + tok('<span class="mk"></span>50 − 6 = 44') + '</div></div>',
         js='''
rise(q(".e0"), t[0]);
tl.fromTo(qa(".cube"), {opacity:0, scale:0}, {opacity:1, scale:1, duration:.35, stagger:.06, ease:"back.out(2)"}, t[2] + 1.6);
tl.to(q(".k4"), {opacity:0, scaleY:.2, duration:.6}, t[2] + 1.2);
tl.to([4,5,6,7,8,9].map(i => q(".u"+i)), {y:160, opacity:0, duration:.6, stagger:.15, ease:"power2.in"}, t[3] + .8);
rise(q(".e1"), t[4] + .4); draw(q(".e1 .mk"), t[4] + 1.4);
'''),

    dict(say=["So schreibst du es auf:",
              "70 − 20 = 50.",
              "50 − 6 = 44.",
              "Und die Probe: 44 + 26 = 70. Richtig!"],
         html='<div class="colL"><div class="eq l0">' + tok("70 − 26 = 44", "b") + '</div><div class="eq m l1">' + tok("70 − 20 = 50")
              + '</div><div class="eq m l2">' + tok("50 − 6 = 44") + '</div><div class="eq m l3 g">' + tok("Probe: 44 + 26 = 70 ✓") + '</div></div>',
         js='rise(q(".l0"), t[0]); rise(q(".l1"), t[1]); rise(q(".l2"), t[2]); rise(q(".l3"), t[3]);'),

    dict(say=["Ein Tipp: Pass auf die Reihenfolge der Ziffern auf.",
              "50 − 4 ist 46. Nicht 64!",
              "Vorne stehen die Zehner, hinten die Einer."],
         html='<div class="pv"><div class="card c1"><div class="big g">46</div><div class="sub">4 Zehner, 6 Einer</div></div>'
              '<div class="card c2"><div class="big r tok">64<span class="strike"></span></div><div class="sub">falsch herum</div></div></div>',
         js='pop(q(".c1"), t[1]); pop(q(".c2"), t[1]+1.4); draw(q(".c2 .strike"), t[1]+2); tl.fromTo(q(".c1"), {scale:1}, {scale:1.08, duration:.3, yoyo:true, repeat:1}, t[2]);'),

    merke(["Erst die Zehner weg, dann die Einer.",
           "Am Ende die Probe mit Plus."],
          ["Merke: Erst die Zehner weg, dann die Einer.",
           "Und am Ende machst du die Probe mit Plus. Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 4 Punkt vor Strich
PUNKT = dict(id="4-punkt-vor-strich", topic="Punkt vor Strich", scenes=[
    titel("·+", "Punkt vor Strich", "was rechnet man zuerst?",
          ["Hallo! Heute lernen wir die Regel Punkt vor Strich."]),

    dict(say=["Schau dir diese Aufgabe an: 6 · 5 + 8 · 3.",
              "Da stehen Mal und Plus in einer Aufgabe.",
              "Was rechnen wir zuerst?"],
         html='<div class="col"><div class="eq e0">' + tok("6 · 5 + 8 · 3") + '</div><div class="big qm o">?</div></div>',
         js='rise(q(".e0"), t[0]); pop(q(".qm"), t[2]);'),

    dict(say=["Dafür gibt es eine Regel: Punkt vor Strich.",
              "Mal und geteilt sind Punktrechnungen. Die rechnen wir zuerst.",
              "Plus und minus sind Strichrechnungen. Die kommen danach."],
         html='<div class="col"><div class="h hh">Punkt vor Strich</div><div class="pv">'
              '<div class="card c1"><div class="sub">1. zuerst</div><div class="big b">·  :</div><div class="sub">Punktrechnung</div></div>'
              '<div class="card c2"><div class="sub">2. danach</div><div class="big o">+  −</div><div class="sub">Strichrechnung</div></div></div></div>',
         js='rise(q(".hh"), t[0]); pop(q(".c1"), t[1]); pop(q(".c2"), t[2]);'),

    dict(say=["Wir markieren die Punktaufgaben gelb.",
              "6 · 5 = 30.",
              "8 · 3 = 24.",
              "Jetzt bleibt nur noch eine leichte Aufgabe: 30 + 24.",
              "30 + 24 = 54."],
         html='<div class="col" style="gap:50px"><div class="eq e0">' + tok('<span class="mk m1"></span>6 · 5') + tok("+")
              + tok('<span class="mk m2"></span>8 · 3') + '</div><div class="eq e1">' + tok("30", "b r1") + tok("+", "pl")
              + tok("24", "b r2") + tok("= 54", "res g") + '</div></div>',
         js='''
draw(q(".m1"), t[0] + .6); draw(q(".m2"), t[0] + 1);
rise(q(".r1"), t[1]); rise(q(".r2"), t[2]);
rise(q(".pl"), t[3]);
pop(q(".res"), t[4] + .8);
'''),

    dict(say=["Was passiert, wenn man einfach von links nach rechts rechnet?",
              "6 · 5 = 30. Plus 8 sind 38. Mal 3 sind 114.",
              "114 ist falsch! Denk immer daran: Punkt vor Strich."],
         html='<div class="col"><div class="eq m w0">' + tok("6 · 5 = 30") + '</div><div class="eq m w1">' + tok("30 + 8 = 38")
              + '</div><div class="eq m w2">' + tok("38 · 3 = 114") + '</div><div class="eq w3">' + tok('114<span class="strike"></span>', "r") + tok("54 ✓", "g ok") + '</div></div>',
         js='rise(q(".w0"), t[1]); rise(q(".w1"), t[1]+1.8); rise(q(".w2"), t[1]+3.4); rise(q(".w3 .tok"), t[2]); draw(q(".w3 .strike"), t[2]+.6); pop(q(".ok"), t[2]+2);'),

    dict(say=["Noch ein Beispiel: 25 − 36 : 6.",
              "Erst die Punktaufgabe: 36 : 6 = 6.",
              "Dann die Strichaufgabe: 25 − 6 = 19."],
         html='<div class="col" style="gap:50px"><div class="eq e0">' + tok("25 −") + tok('<span class="mk"></span>36 : 6') + '</div>'
              '<div class="eq e1">' + tok("25 − 6", "b") + tok("= 19", "g res") + '</div></div>',
         js='rise(q(".e0"), t[0]); draw(q(".e0 .mk"), t[1]); rise(q(".e1 .b"), t[1]+1.6); pop(q(".res"), t[2]+1);'),

    merke(["Punkt vor Strich: Erst · und :, dann + und −."],
          ["Merke: Punkt vor Strich. Erst mal und geteilt, dann plus und minus.",
           "Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 5 Fachwörter
def labeled(cells):
    out = ""
    for v, lab, cls in cells:
        if lab is None:
            out += tok(v)
        else:
            out += f'<div class="cell {cls}"><span class="tok">{v}</span><span class="lab">{lab}</span></div>'
    return f'<div class="eq" style="align-items:flex-start">{out}</div>'


BOX = '<span class="box"></span>'

BEGRIFFE = dict(id="5-fachwoerter", topic="Fachwörter", scenes=[
    titel("Aa", "Fachwörter", "Faktor, Produkt, Quotient und Co.",
          ["Hallo! Heute lernen wir die Namen der Zahlen beim Malnehmen und Teilen."]),

    dict(say=["Beim Malnehmen haben die Zahlen eigene Namen.",
              "3 · 4 = 12.",
              "Die 3 und die 4 heißen Faktoren.",
              "Das Ergebnis, die 12, heißt Produkt."],
         html='<div class="col"><div class="h hh">Malnehmen</div>'
              + labeled([("3", "Faktor", "f1"), ("·", None, ""), ("4", "Faktor", "f2"), ("=", None, ""), ("12", "Produkt", "f3")]) + '</div>',
         js='rise(q(".hh"), t[0]); rise(q(".eq"), t[1]); pop([q(".f1 .lab"), q(".f2 .lab")], t[2]+.4, .3); pop(q(".f3 .lab"), t[3]+.6);'),

    dict(say=["Beim Teilen gibt es andere Namen.",
              "12 : 4 = 3.",
              "Die 12 wird geteilt. Sie heißt Dividend.",
              "Die 4 ist die Zahl, durch die geteilt wird. Sie heißt Divisor.",
              "Das Ergebnis, die 3, heißt Quotient."],
         html='<div class="col"><div class="h hh">Teilen</div>'
              + labeled([("12", "Dividend", "f1"), (":", None, ""), ("4", "Divisor", "f2"), ("=", None, ""), ("3", "Quotient", "f3")]) + '</div>',
         js='rise(q(".hh"), t[0]); rise(q(".eq"), t[1]); pop(q(".f1 .lab"), t[2]+.6); pop(q(".f2 .lab"), t[3]+1); pop(q(".f3 .lab"), t[4]+.6);'),

    dict(say=["Merke dir:",
              "Das Produkt ist das Ergebnis beim Malnehmen.",
              "Der Quotient ist das Ergebnis beim Teilen."],
         html='<div class="pv"><div class="card c1"><div class="eq">3 · 4 = <span class="o">12</span></div><div class="sub">Produkt = Mal-Ergebnis</div></div>'
              '<div class="card c2"><div class="eq">12 : 4 = <span class="o">3</span></div><div class="sub">Quotient = Geteilt-Ergebnis</div></div></div>',
         js='pop(q(".c1"), t[1]); pop(q(".c2"), t[2]);'),

    dict(say=["Jetzt ein Rätsel: Ein Faktor ist 6, das Produkt ist 36.",
              "Wir schreiben: 6 · ☐ = 36.",
              "Welche Zahl passt? 6 · 6 = 36.",
              "Der andere Faktor ist 6."],
         html='<div class="col"><div class="rule rr">Ein Faktor ist 6, das Produkt ist 36.</div>'
              + labeled([("6", "Faktor", "f1"), ("·", None, ""), (BOX, "Faktor", "f2"), ("=", None, ""), ("36", "Produkt", "f3")])
              + '<div class="eq m sol">' + tok('<span class="mk"></span>6 · 6 = 36') + '</div></div>',
         js='rise(q(".rr"), t[0]); rise(q(".col > .eq"), t[1]); rise(q(".sol"), t[2]+1.4); draw(q(".sol .mk"), t[3]);'),

    dict(say=["Noch ein Rätsel: Der Divisor ist 3, der Quotient ist 5.",
              "Wir schreiben: ☐ : 3 = 5.",
              "Wir rechnen rückwärts mit Mal: 5 · 3 = 15.",
              "Der Dividend ist 15."],
         html='<div class="col"><div class="rule rr">Der Divisor ist 3, der Quotient ist 5.</div>'
              + labeled([(BOX, "Dividend", "f1"), (":", None, ""), ("3", "Divisor", "f2"), ("=", None, ""), ("5", "Quotient", "f3")])
              + '<div class="eq m sol">' + tok('<span class="mk"></span>5 · 3 = 15') + '</div></div>',
         js='rise(q(".rr"), t[0]); rise(q(".col > .eq"), t[1]); rise(q(".sol"), t[2]+1.6); draw(q(".sol .mk"), t[3]);'),

    merke(["Faktor · Faktor = Produkt", "Dividend : Divisor = Quotient"],
          ["Merke: Faktor mal Faktor gleich Produkt.",
           "Dividend geteilt durch Divisor gleich Quotient. Jetzt bist du dran!"]),
])

VIDEOS = [MAL, TEILEN, MINUS, PUNKT, BEGRIFFE]
