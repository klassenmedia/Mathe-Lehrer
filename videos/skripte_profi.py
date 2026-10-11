"""Drehbücher Teil 2: Profi-Tricks für große Zahlen (Videos 6–10)."""
from skripte import merke, titel, tok


def blocks(h, z, e, extra_cls=""):
    """Inhalt der drei Spalten einer Stellentafel."""
    return ("".join(f'<div class="hplate p{i}"></div>' for i in range(h)),
            "".join(f'<div class="sbar z{i}"></div>' for i in range(z)),
            "".join(f'<div class="scube e{i}"></div>' for i in range(e)))


def tafel(h, z, e, digits=None, cls=""):
    H, Z, E = blocks(h, z, e)
    d = digits or (str(h), str(z), str(e))
    return (f'<div class="tafel {cls}"><div class="th b">H</div><div class="th b">Z</div><div class="th o">E</div>'
            f'<div class="tc cH">{H}</div><div class="tc cZ">{Z}</div><div class="tc cE">{E}</div>'
            f'<div class="td dH">{d[0]}</div><div class="td dZ">{d[1]}</div><div class="td dE">{d[2]}</div></div>')


# ---------------------------------------------------------------- 6 Zahlen bis 1000
STELLEN = dict(id="6-zahlen-bis-1000", topic="Zahlen bis 1000", scenes=[
    titel("HZE", "Zahlen bis 1000", "Hunderter, Zehner, Einer",
          ["Hallo! Heute lernen wir, wie große Zahlen gebaut sind."], symsize=80),

    dict(say=["Das ist ein Einerwürfel. Er ist 1.",
              "10 Einer legen wir zu einer Zehnerstange zusammen. Das sind 10.",
              "Und 10 Zehnerstangen werden zu einer Hunderterplatte. Das sind 100.",
              "Jede Stelle ist also 10-mal so viel wie die Stelle davor."],
         html='<div class="col" style="gap:50px">'
              '<div class="trow r1"><div class="row1" style="display:flex;gap:10px">'
              + "".join(f'<div class="scube big c{i}"></div>' for i in range(10)) +
              '</div><div class="eqs">=</div><div class="sbar big rb" style="height:44px;width:220px;background-size:22px 100%;'
              'background-image:linear-gradient(90deg,rgba(255,255,255,.6) 2px,transparent 2px)"></div><div class="lab2">10 Einer = 1 Zehner</div></div>'
              '<div class="trow r2"><div style="display:flex;gap:10px">'
              + "".join(f'<div class="sbar big b{i}"></div>' for i in range(10)) +
              '</div><div class="eqs">=</div><div class="hplate big rp"></div><div class="lab2">10 Zehner = 1 Hunderter</div></div></div>',
         js='''
pop(q(".c0"), t[0] + .3);
pop(qa(".row1 .scube").slice(1), t[1], .12);
pop(q(".rb"), t[1] + 2.4); rise(q(".r1 .lab2"), t[1] + 2.8);
pop(qa(".r2 .sbar").filter(e => !e.classList.contains("rp")), t[2], .1);
pop(q(".rp"), t[2] + 2.6); rise(q(".r2 .lab2"), t[2] + 3);
'''),

    dict(say=["Jetzt bauen wir die Zahl 347.",
              "3 Hunderterplatten. Das sind 300.",
              "4 Zehnerstangen. Das sind 40.",
              "Und 7 Einer.",
              "300 + 40 + 7 = 347."],
         html='<div class="col" style="gap:30px">' + tafel(3, 4, 7) + '<div class="eq m res">' + tok('<span class="mk"></span>300 + 40 + 7 = 347') + '</div></div>',
         js='''
rise(q(".tafel"), t[0]);
pop(qa(".cH > div"), t[1], .2); pop(q(".dH"), t[1] + 1);
pop(qa(".cZ > div"), t[2], .15); pop(q(".dZ"), t[2] + 1);
pop(qa(".cE > div"), t[3], .1); pop(q(".dE"), t[3] + .8);
rise(q(".res"), t[4]); draw(q(".res .mk"), t[4] + 1.2);
'''),

    dict(say=["Ganz wichtig ist die Null. Schau dir 608 an.",
              "6 Hunderter, 0 Zehner, 8 Einer.",
              "Die 0 sagt: Hier gibt es keine Zehner. Sie hält den Platz frei.",
              "Ohne die 0 stünde da 68. Das ist eine ganz andere Zahl!"],
         html='<div class="col" style="gap:30px">' + tafel(6, 0, 8, ("6", '<span class="r">0</span>', "8"))
              + '<div class="eq m wr">' + tok("608", "g") + tok("nicht") + tok('68<span class="strike"></span>', "r") + '</div></div>',
         js='''
rise(q(".tafel"), t[0]);
pop(qa(".cH > div"), t[1], .1); pop(q(".dH"), t[1] + .4); pop(q(".dZ"), t[1] + 1.4);
pop(qa(".cE > div"), t[1] + 2, .08); pop(q(".dE"), t[1] + 2.4);
tl.fromTo(q(".cZ"), {backgroundColor:"rgba(255,227,110,0)"}, {backgroundColor:"rgba(255,227,110,.6)", duration:.5}, t[2]);
rise(q(".wr"), t[3]); draw(q(".wr .strike"), t[3] + 1.6);
'''),

    dict(say=["Was ist 395 + 10?",
              "Ein Zehner kommt dazu. Jetzt haben wir 10 Zehnerstangen.",
              "10 Zehner tauschen wir in einen Hunderter.",
              "Jetzt sind es 4 Hunderter, 0 Zehner und 5 Einer. Also 405."],
         html='<div class="col" style="gap:24px"><div class="eq m e0">' + tok("395 + 10 = ?") + '</div>'
              + tafel(3, 10, 5, ('<span class="o1">3</span><span class="n1">4</span>', '<span class="o2">9</span><span class="n2">0</span>', "5"))
              + '</div>',
         js='''
const Z = qa(".cZ .sbar"), P = document.createElement("div"); P.className = "hplate"; q(".cH").append(P);
tl.fromTo(Z[9], {opacity:0, y:-120}, {opacity:1, y:0, duration:.6, ease:"back.out(1.6)"}, t[1] + .6);
tl.fromTo(P, {opacity:0, scale:0}, {opacity:1, scale:1, duration:.5, ease:"back.out(2)"}, t[2] + 1.6);
tl.to(Z, {opacity:0, x:-300, duration:.6, ease:"power2.in", stagger:.03}, t[2] + .6);
tl.fromTo([q(".n1"), q(".n2")], {opacity:0}, {opacity:1, duration:.4}, t[3]);
tl.fromTo([q(".o1"), q(".o2")], {opacity:1}, {opacity:0, duration:.4}, t[3]);
rise(q(".e0"), t[0]);
'''),

    merke(["Jede Stelle ist 10-mal so viel wie die rechts daneben.",
           "Die Null hält einen Platz frei."],
          ["Merke: Jede Stelle ist 10-mal so viel wie die Stelle rechts daneben.",
           "Und die Null hält einen Platz frei. Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 7 Plus und Minus mit großen Zahlen
def jumps(start, steps):
    out = f'<div class="jumps"><div class="jchip j0">{start}</div>'
    for i, (lab, val, cls) in enumerate(steps, 1):
        out += f'<div class="jump a{i} {cls}"><span>{lab}</span><span class="ar">→</span></div><div class="jchip j{i}">{val}</div>'
    return out + "</div>"


GROSS = dict(id="7-plus-minus-gross", topic="Plus & Minus groß", scenes=[
    titel("+−", "Große Zahlen", "plus und minus mit Tricks",
          ["Hallo! Heute rechnen wir plus und minus mit großen Zahlen."], symsize=110),

    dict(say=["Bevor wir rechnen, schätzen wir. Das heißt Überschlag.",
              "345 + 238. 345 ist ungefähr 300. 238 ist ungefähr 200.",
              "Das Ergebnis ist also ungefähr 500."],
         html='<div class="col"><div class="h hh">Überschlag</div><div class="eq e0">' + tok("345 + 238") + '</div>'
              '<div class="eq m e1">' + tok("≈ 300 + 200 = 500", "o") + '</div></div>',
         js='rise(q(".hh"), t[0]); rise(q(".e0"), t[1]); rise(q(".e1"), t[1] + 2.4);'),

    dict(say=["Jetzt rechnen wir genau, Stelle für Stelle.",
              "Hunderter: 300 + 200 = 500.",
              "Zehner: 40 + 30 = 70.",
              "Einer: 5 + 8 = 13.",
              "Alles zusammen: 500 + 70 + 13 = 583.",
              "583 passt gut zu unserem Überschlag. Wäre 5813 herausgekommen, wüssten wir sofort: Da stimmt etwas nicht!"],
         html='<div class="colL"><div class="eq l0">' + tok("345 + 238") + '</div>'
              '<div class="eq m l1">' + tok("H:", "b") + tok("300 + 200 = 500") + '</div>'
              '<div class="eq m l2">' + tok("Z:", "b") + tok("40 + 30 = 70") + '</div>'
              '<div class="eq m l3">' + tok("E:", "o") + tok("5 + 8 = 13") + '</div>'
              '<div class="eq l4">' + tok('<span class="mk"></span>500 + 70 + 13 = 583') + '</div></div>',
         js='rise(q(".l0"), t[0]); rise(q(".l1"), t[1]); rise(q(".l2"), t[2]); rise(q(".l3"), t[3]); rise(q(".l4"), t[4]); draw(q(".l4 .mk"), t[4]+1.5);'),

    dict(say=["Jetzt ein Trick für Minus: 463 − 198.",
              "198 ist fast 200. Also rechnen wir erst minus 200: 463 − 200 = 263.",
              "Aber wir haben 2 zu viel weggenommen. Die geben wir zurück: 263 + 2 = 265.",
              "Also ist 463 − 198 = 265."],
         html='<div class="col" style="gap:60px"><div class="eq e0">' + tok("463 − 198 = ?") + '</div>'
              + jumps(463, [("− 200", 263, "r"), ("+ 2", 265, "g")]) + '</div>',
         js='''
rise(q(".e0"), t[0]); pop(q(".j0"), t[1]);
pop(q(".a1"), t[1] + 2); pop(q(".j1"), t[1] + 3.6);
pop(q(".a2"), t[2] + 2.4); pop(q(".j2"), t[2] + 4);
tl.fromTo(q(".j2"), {scale:1}, {scale:1.15, duration:.3, yoyo:true, repeat:1}, t[3] + 1);
'''),

    dict(say=["Das klappt auch beim Plus: 356 + 99.",
              "99 ist fast 100. 356 + 100 = 456.",
              "Das war 1 zu viel. 456 − 1 = 455."],
         html='<div class="col" style="gap:60px"><div class="eq e0">' + tok("356 + 99 = ?") + '</div>'
              + jumps(356, [("+ 100", 456, "g"), ("− 1", 455, "r")]) + '</div>',
         js='rise(q(".e0"), t[0]); pop(q(".j0"), t[1]); pop(q(".a1"), t[1]+1.2); pop(q(".j1"), t[1]+2.2); pop(q(".a2"), t[2]+.8); pop(q(".j2"), t[2]+2);'),

    merke(["Erst schätzen, dann rechnen.",
           "Stelle für Stelle: Hunderter, Zehner, Einer.",
           "Fast runde Zahl? Runde Zahl nehmen, dann ausgleichen."],
          ["Merke: Erst schätzen, dann rechnen.",
           "Rechne Stelle für Stelle: Hunderter, Zehner, Einer.",
           "Und bei fast runden Zahlen: Nimm die runde Zahl und gleiche dann aus. Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 8 Kleine Aufgabe hilft
def bar_groups(groups, per):
    return ('<div style="display:flex;gap:46px;align-items:flex-end">'
            + "".join('<div class="grp" style="display:flex;gap:10px">' + "".join(f'<div class="sbar big g{g}"></div>' for _ in range(per)) + '</div>'
                      for g in range(groups)) + '</div>')


ZEHNER = dict(id="8-kleine-aufgabe-hilft", topic="Kleine Aufgabe hilft", scenes=[
    titel("·0", "Mal mit Zehnern", "die kleine Aufgabe hilft",
          ["Hallo! Heute lernen wir, wie eine kleine Aufgabe bei großen Zahlen hilft."], symsize=110),

    dict(say=["Wie viel ist 3 · 40?",
              "Das sieht schwer aus. Aber 40, das sind 4 Zehner.",
              "3 · 4 Zehner sind 12 Zehner.",
              "Und 12 Zehner sind 120."],
         html='<div class="col" style="gap:40px"><div class="eq e0">' + tok("3 · 40 = ?") + '</div>' + bar_groups(3, 4)
              + '<div class="eq m e1">' + tok("12 Zehner = 120", "g") + '</div></div>',
         js='rise(q(".e0"), t[0]); pop(qa(".sbar"), t[1] + 1.5, .08); tl.fromTo(qa(".grp"), {y:0}, {y:-16, duration:.3, yoyo:true, repeat:1, stagger:.4}, t[2]); rise(q(".e1"), t[3]);'),

    dict(say=["Der Trick: Verstecke die Null und rechne die kleine Aufgabe.",
              "3 · 4 = 12.",
              "Dann hängst du die Null wieder an: 120."],
         html='<div class="col" style="gap:50px"><div class="eq e0">' + tok("3 · 4") + tok('<span class="z0">0</span>', "zz") + '</div>'
              '<div class="eq e1">' + tok("3 · 4 = 12") + '</div><div class="eq e2">' + tok("3 · 40 = 12") + tok("0", "o nul") + '</div></div>',
         js='''
rise(q(".e0"), t[0]);
tl.to(q(".zz"), {opacity:.15, y:30, duration:.5}, t[0] + 1.5);
rise(q(".e1"), t[1]);
rise(q(".e2"), t[2]); tl.fromTo(q(".nul"), {y:-60, opacity:0}, {y:0, opacity:1, duration:.5, ease:"bounce.out"}, t[2] + 1.6);
'''),

    dict(say=["Das klappt auch mit Hundertern: 3 · 200.",
              "Kleine Aufgabe: 3 · 2 = 6.",
              "200 hat zwei Nullen. Also hängen wir zwei Nullen an: 600."],
         html='<div class="col" style="gap:50px"><div class="eq e0">' + tok("3 · 200 = ?") + '</div>'
              '<div class="eq e1">' + tok("3 · 2 = 6") + '</div><div class="eq e2">' + tok("3 · 200 = 6") + tok("00", "o nul") + '</div></div>',
         js='rise(q(".e0"), t[0]); rise(q(".e1"), t[1]); rise(q(".e2"), t[2]); tl.fromTo(q(".nul"), {y:-60, opacity:0}, {y:0, opacity:1, duration:.5, ease:"bounce.out"}, t[2]+3);'),

    dict(say=["Und beim Teilen: 120 : 4.",
              "120, das sind 12 Zehner.",
              "12 Zehner verteilen wir auf 4 Gruppen. Jede Gruppe bekommt 3 Zehner.",
              "3 Zehner sind 30. Also ist 120 : 4 = 30."],
         html='<div class="col" style="gap:40px"><div class="eq e0">' + tok("120 : 4 = ?") + '</div>' + bar_groups(4, 3)
              + '<div class="eq m e1">' + tok("12 : 4 = 3") + tok("→", "") + tok("120 : 4 = 30", "g") + '</div></div>',
         js='''
rise(q(".e0"), t[0]);
pop(qa(".sbar"), t[1], .08);
tl.fromTo(qa(".grp"), {x:(i) => (1.5 - i) * 46}, {x:0, duration:.8, ease:"power2.inOut"}, t[2] + 1.2);
rise(q(".e1"), t[3]);
'''),

    merke(["Nullen weglassen, klein rechnen, Nullen wieder anhängen.",
           "Zähle genau, wie viele Nullen es sind."],
          ["Merke: Lass die Nullen weg und rechne die kleine Aufgabe.",
           "Dann hängst du die Nullen wieder an. Zähle genau, wie viele es sind. Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 9 Große Malaufgaben
def kreuz(a, t_, e, cls=""):
    return (f'<div class="kreuz {cls}"><div class="hd">·</div><div class="hd k1">{t_}</div><div class="hd k2">{e}</div>'
            f'<div class="hd k3">{a}</div><div class="k4 b">{a*t_}</div><div class="k5 o">{a*e}</div></div>')


MALKREUZ = dict(id="9-grosse-malaufgaben", topic="Große Malaufgaben", scenes=[
    titel("7·16", "Große Malaufgaben", "zerlegen macht es leicht",
          ["Hallo! Heute lernen wir, wie man große Malaufgaben leicht rechnet."], symsize=76),

    dict(say=["Wie viel ist 7 · 16? Das steht in keiner Malreihe.",
              "Aber die 16 können wir zerlegen: 16 = 10 + 6.",
              "Das Punktefeld hat 7 Reihen mit je 16 Punkten. Wir teilen es in zwei Teile.",
              "Links: 7 · 10 = 70.",
              "Rechts: 7 · 6 = 42.",
              "Zusammen: 70 + 42 = 112."],
         html='<div class="col" style="gap:34px"><div class="eq m e0" style="gap:70px">' + tok("7 · 16 = ?") + tok("16 = 10 + 6", "o sp") + '</div><div class="f"></div>'
              '<div class="eq m e1" style="gap:70px">' + tok("7 · 10 = 70", "b x1") + tok("7 · 6 = 42", "o x2") + '</div>'
              '<div class="eq e2">' + tok('<span class="mk"></span>70 + 42 = 112') + '</div></div>',
         js='''
const R = field(q(".f"), 7, 16, 34, (r, c) => c < 10 ? "" : "o");
R.forEach(r => { r.dots[5].style.marginLeft = "0"; r.dots[10].style.marginLeft = "48px"; });
rise(q(".e0 .tok"), t[0]); pop(q(".sp"), t[1] + 1.4);
pop(R.flatMap(r => r.dots), t[2], .006);
rise(q(".x1"), t[3]); rise(q(".x2"), t[4]);
rise(q(".e2"), t[5]); draw(q(".e2 .mk"), t[5] + 1.2);
'''),

    dict(say=["Man kann das kurz in einem Malkreuz aufschreiben.",
              "Oben stehen die Teile 10 und 6. Links steht die 7.",
              "In die Kästchen kommen 7 · 10 = 70 und 7 · 6 = 42.",
              "Dann zählen wir zusammen: 112."],
         html='<div class="col" style="gap:40px">' + kreuz(7, 10, 6) + '<div class="eq e2">' + tok('<span class="mk"></span>70 + 42 = 112') + '</div></div>',
         js='rise(q(".kreuz"), t[0]); pop([q(".k1"), q(".k2"), q(".k3")], t[1] + .4, .5); pop(q(".k4"), t[2] + .6); pop(q(".k5"), t[2] + 2.6); rise(q(".e2"), t[3]); draw(q(".e2 .mk"), t[3] + .8);'),

    dict(say=["Noch eins: 4 · 23.",
              "Zerlegen: 23 = 20 + 3.",
              "4 · 20 = 80. 4 · 3 = 12.",
              "80 + 12 = 92."],
         html='<div class="col" style="gap:40px"><div class="eq m e0">' + tok("4 · 23 = ?") + '</div>' + kreuz(4, 20, 3)
              + '<div class="eq e2">' + tok('<span class="mk"></span>80 + 12 = 92') + '</div></div>',
         js='rise(q(".e0"), t[0]); rise(q(".kreuz"), t[1]); pop(q(".k4"), t[2] + .4); pop(q(".k5"), t[2] + 2); rise(q(".e2"), t[3]); draw(q(".e2 .mk"), t[3] + .8);'),

    merke(["Zerlege die große Zahl in Zehner und Einer.",
           "Nimm beide Teile mal und zähle zusammen."],
          ["Merke: Zerlege die große Zahl in Zehner und Einer.",
           "Nimm beide Teile mal und zähle sie zusammen. Vergiss die Einer nicht! Jetzt bist du dran!"]),
])

# ---------------------------------------------------------------- 10 Rechentricks & Muster
TRICKS = dict(id="10-rechentricks-muster", topic="Rechentricks & Muster", scenes=[
    titel("3·5", "Rechentricks", "Zahlen gehören zusammen",
          ["Hallo! Heute lernen wir Rechentricks. Mit ihnen siehst du, wie Zahlen zusammengehören."], symsize=84),

    dict(say=["Schau dir dieses Punktefeld an: 3 Reihen mit je 5 Punkten. 3 · 5 = 15.",
              "Jetzt drehen wir das Feld.",
              "Jetzt sind es 5 Reihen mit je 3 Punkten. 5 · 3 = 15.",
              "Es sind dieselben Punkte! Beim Malnehmen darfst du tauschen. Das ist die Tauschaufgabe."],
         html='<div class="f" style="width:420px;height:420px;justify-content:center;align-items:center"></div><div class="colL">'
              '<div class="eq m l1">' + tok("3 · 5 = 15", "b") + '</div><div class="eq m l2">' + tok("5 · 3 = 15", "o") + '</div></div>',
         js='''
const R = field(q(".f"), 3, 5, 60);
pop(R.flatMap(r => r.dots), t[0], .04); rise(q(".l1"), t[0] + 2);
tl.fromTo(q(".f"), {rotation:0}, {rotation:90, duration:1.2, ease:"power2.inOut"}, t[1] + .3);
rise(q(".l2"), t[2] + 1);
'''),

    dict(say=["Die Zahlen 3, 5 und 15 sind eine Familie. Sie wohnen in einem Zahlenhaus.",
              "Zu der Familie gehören vier Aufgaben:",
              "3 · 5 = 15 und 5 · 3 = 15.",
              "15 : 3 = 5 und 15 : 5 = 3.",
              "Wenn du eine Aufgabe kannst, kannst du alle vier!"],
         html='<div class="house"><div class="roof">15</div><div class="floor"><div>3</div><div>5</div></div>'
              '<div class="rooms"><div class="m1 b">3 · 5 = 15</div><div class="m2 b">5 · 3 = 15</div>'
              '<div class="m3 o">15 : 3 = 5</div><div class="m4 o">15 : 5 = 3</div></div></div>',
         js='rise(q(".roof"), t[0]); rise(q(".floor"), t[0] + 1); pop([q(".m1"), q(".m2")], t[2], 1.2); pop([q(".m3"), q(".m4")], t[3], 1.4);'),

    dict(say=["Der Nachbar-Trick: Du weißt 6 · 7 = 42.",
              "Was ist 6 · 8? Das ist nur eine 6 mehr!",
              "42 + 6 = 48."],
         html='<div class="f"></div><div class="colL"><div class="eq m l1">' + tok("6 · 7 = 42", "b") + '</div>'
              '<div class="eq m l2">' + tok("+ 6", "o") + '</div><div class="eq l3">' + tok('<span class="mk"></span>6 · 8 = 48') + '</div></div>',
         js='''
const R = field(q(".f"), 6, 8, 54, (r, c) => c < 7 ? "" : "o");
pop(R.flatMap(r => r.dots.slice(0, 7)), t[0], .01); rise(q(".l1"), t[0] + 1);
pop(R.map(r => r.dots[7]), t[1] + 1, .12); rise(q(".l2"), t[1] + 2);
rise(q(".l3"), t[2]); draw(q(".l3 .mk"), t[2] + 1);
'''),

    dict(say=["Ein Profi-Trick: 4 · 35.",
              "Wir schneiden das Rechteck in der Mitte durch und legen die Hälften nebeneinander.",
              "Jetzt ist es halb so hoch, aber doppelt so lang: 2 · 70.",
              "Halbieren und verdoppeln. Das Ergebnis bleibt gleich: 140."],
         html='<div class="col" style="gap:30px"><div class="area"><div class="half h1"></div><div class="half h2"></div></div>'
              '<div class="eq m l1">' + tok("4 · 35") + tok("=", "q1") + tok("2 · 70", "q2") + tok("= 140", "g q3") + '</div></div>',
         js='''
rise(q(".area"), t[0]); rise(q(".l1 .tok"), t[0] + .4);
tl.to(q(".h2"), {x:770, y:-80, duration:1.4, ease:"power2.inOut"}, t[1] + 2.4);
pop([q(".q1"), q(".q2")], t[2] + .4, .3);
pop(q(".q3"), t[3] + 2);
'''),

    dict(say=["Mathe ist voller Muster. Schau dir die 9er-Reihe an.",
              "9, 18, 27, 36, 45.",
              "Die Zehner werden immer eins mehr. Die Einer werden immer eins weniger.",
              "Wer Muster sieht, findet Fehler ganz schnell."],
         html='<div class="muster">' + "".join(
             f'<div class="mu{i}"><span>9 · {i} =</span><span><span class="b">{(9*i)//10 if 9*i >= 10 else ""}</span><span class="o">{(9*i)%10}</span></span></div>'
             for i in range(1, 6)) + '</div><div class="colL"><div class="eq s z1 b">' + tok("Zehner: +1") + '</div><div class="eq s z2 o">' + tok("Einer: −1") + '</div></div>',
         js='for (let i = 1; i <= 5; i++) rise(q(".mu"+i), t[1] + (i-1)*.6); rise(q(".z1"), t[2] + .3); rise(q(".z2"), t[2] + 2.4);'),

    merke(["Tauschen ist erlaubt: 3 · 5 = 5 · 3.",
           "Eine Aufgabe kennen heißt vier Aufgaben kennen.",
           "Nutze Nachbaraufgaben und Muster."],
          ["Merke: Beim Malnehmen darfst du tauschen.",
           "Wenn du eine Aufgabe kennst, kennst du die ganze Familie.",
           "Und nutze Nachbaraufgaben und Muster. Jetzt bist du dran!"]),
])

VIDEOS = [STELLEN, GROSS, ZEHNER, MALKREUZ, TRICKS]
