"""Drehbuch Teil 4: Nebeneinander rechnen, wenn kein Platz zum Untereinanderschreiben ist (Video 13)."""
from skripte import merke, titel, tok

ORANGE, BLUE, GREEN, RED = "#d96a12", "#2f6fde", "#1f8a4f", "#cf3434"


def chips(*txt):
    return '<div class="jumps">' + "".join(f'<div class="jchip c{i}">{t}</div>' + ('<div class="jump"><span class="ar">→</span></div>' if i < len(txt) - 1 else "")
                                           for i, t in enumerate(txt)) + '</div>'


NEBEN = dict(id="13-nebeneinander-rechnen", topic="Nebeneinander rechnen", scenes=[
    titel("→", "Nebeneinander rechnen", "wenn kein Platz zum Untereinanderschreiben ist",
          ["Hallo! Heute lernen wir, wie man rechnet, wenn kein Platz zum Untereinanderschreiben ist."]),

    dict(say=["In der Mathearbeit stehen die Aufgaben oft nebeneinander. Und manchmal ist kein Platz zum Untereinanderschreiben.",
              "Kein Problem! Hier kommen drei Tricks, mit denen du direkt in der Zeile rechnest."],
         html='<div class="col" style="gap:50px"><div class="card c0" style="padding:30px 60px"><div class="eq">268 + 157 = <span class="box"></span></div><div class="sub">Mathearbeit, Aufgabe 3</div></div>'
              '<div class="pv" style="gap:40px"><div class="card t1"><div class="eq s b">1 Brücken</div></div><div class="card t2"><div class="eq s o">2 Zehner voll</div></div>'
              '<div class="card t3"><div class="eq s g">3 Auffüllen</div></div></div></div>',
         js='rise(q(".c0"), t[0] + .3); pop([q(".t1"), q(".t2"), q(".t3")], t[1] + 1.5, .5);'),

    dict(say=["Trick 1: Die Brücken. 268 + 157.",
              "Wir verbinden gleiche Stellen mit einem Bogen. Einer mit Einern, Zehner mit Zehnern, Hunderter mit Hundertern.",
              "Immer rechts anfangen. Einer-Brücke: 8 + 7 = 15. Die 5 kommt ganz rechts ins Ergebnis.",
              "Die kleine 1 ist der Übertrag. Die schreiben wir oben auf die nächste Brücke.",
              "Zehner-Brücke: 6 + 5 = 11, plus die 1 auf der Brücke sind 12. Die 2 ins Ergebnis, die 1 auf die nächste Brücke.",
              "Hunderter-Brücke: 2 + 1 + 1 = 4. Fertig: 425!"],
         html='<div class="col"><div class="z"></div></div>',
         js=f'''
const host = q(".z"), Z = zeile(host, ["2","6","8","+","1","5","7","=","#","#","#"], 120);
[[0,4,"{GREEN}"],[1,5,"{BLUE}"],[2,6,"{ORANGE}"]].forEach(([a,b,c]) => {{ Z.cells[a].style.color = c; Z.cells[b].style.color = c; }});
rise(Z.cells, t[0], .05);
const bE = bogen(Z.svg, Z.cx(2), Z.cx(6), 80, "{ORANGE}", t[1] + 2.4);
const bZ = bogen(Z.svg, Z.cx(1), Z.cx(5), 135, "{BLUE}", t[1] + 3.6);
const bH = bogen(Z.svg, Z.cx(0), Z.cx(4), 190, "{GREEN}", t[1] + 4.8);
blip(Z.cells[2], t[2] + 2); blip(Z.cells[6], t[2] + 2.2);
inBox(Z.cells[10], "5", t[2] + 4.6);
aufBogen(host, bZ, "1", t[3] + 2.4);
blip(Z.cells[1], t[4] + 1); blip(Z.cells[5], t[4] + 1.2);
inBox(Z.cells[9], "2", t[4] + 5.6);
aufBogen(host, bH, "1", t[4] + 7.2);
inBox(Z.cells[8], "4", t[5] + 2.6);
'''),

    dict(say=["Beim Minus geht das auch: 52 − 27.",
              "Einer-Brücke: 2 − 7 geht nicht. Bei der ersten Zahl ist zu wenig.",
              "Also machen wir bei den Zehnern einen auf. Aus der 5 wird eine 4, und aus der 2 wird eine 12. Das schreiben wir klein darunter.",
              "Jetzt rechnen wir 12 − 7 = 5.",
              "Zehner-Brücke: 4 − 2 = 2. Ergebnis: 25."],
         html='<div class="col"><div class="z"></div></div>',
         js=f'''
const host = q(".z"), Z = zeile(host, ["5","2","−","2","7","=","#","#"], 130);
[[0,3,"{BLUE}"],[1,4,"{ORANGE}"]].forEach(([a,b,c]) => {{ Z.cells[a].style.color = c; Z.cells[b].style.color = c; }});
rise(Z.cells, t[0], .05);
const bE = bogen(Z.svg, Z.cx(1), Z.cx(4), 90, "{ORANGE}", t[1]);
tl.fromTo(Z.cells[1], {{x:0}}, {{x:10, duration:.08, yoyo:true, repeat:5}}, t[1] + 2.4);
streiche(Z.cells[0], t[2] + 2.6); unterZelle(Z.cells[0], "4", t[2] + 3);
streiche(Z.cells[1], t[2] + 4); unterZelle(Z.cells[1], "12", t[2] + 4.4);
inBox(Z.cells[7], "5", t[3] + 1.8);
const bZ = bogen(Z.svg, Z.cx(0), Z.cx(3), 150, "{BLUE}", t[4]);
inBox(Z.cells[6], "2", t[4] + 1.8);
'''),

    dict(say=["Trick 2: Zehner voll machen. 47 + 38.",
              "Die 38 zerlegen wir: erst 30, dann 8.",
              "Erst die Zehner: 47 + 30 = 77.",
              "Jetzt machen wir den Zehner voll: Von 77 bis 80 sind es 3.",
              "Von den 8 sind dann noch 5 übrig: 80 + 5 = 85.",
              "In der Arbeit schreibst du nur ganz kurz daneben: 77, 80, 85."],
         html='<div class="col" style="gap:20px"><div class="eq m e0">' + tok("47 + 38") + tok("38 = 30 + 3 + 5", "o sp") + '</div><div class="zl"></div>'
              + chips("47", "77", "80", "85") + '</div>',
         js=f'''
const Z = strahl(q(".zl"), 1500, [[47,110],[77,860],[80,1010],[85,1330]]);
rise(q(".e0 .tok"), t[0]); pop(q(".sp"), t[1] + 1);
sprung(Z, 0, 1, "+30", "{BLUE}", t[2] + .4, 190);
sprung(Z, 1, 2, "+3", "{ORANGE}", t[3] + 1.6, 80);
sprung(Z, 2, 3, "+5", "{ORANGE}", t[4] + 1.6, 120);
pop(qa(".jchip"), t[5] + 1.5, .35);
'''),

    dict(say=["Trick 3 fürs Minus: Auffüllen. 52 − 27.",
              "Wir fragen: Wie weit ist es von 27 bis 52?",
              "Von 27 bis 30 sind es 3.",
              "Von 30 bis 52 sind es 22.",
              "Zusammen: 3 + 22 = 25. Also ist 52 − 27 = 25."],
         html='<div class="col" style="gap:20px"><div class="eq m e0">' + tok("52 − 27 = ?") + '</div><div class="zl"></div>'
              '<div class="eq m res">' + tok('<span class="mk"></span>3 + 22 = 25', "g") + '</div></div>',
         js=f'''
const Z = strahl(q(".zl"), 1500, [[27,130],[30,400],[52,1340]]);
rise(q(".e0"), t[0]);
tl.fromTo(Z.mk[2].g, {{opacity:.25}}, {{opacity:1, duration:.4}}, t[1] + 1.4);
sprung(Z, 0, 1, "+3", "{ORANGE}", t[2] + .6, 100);
sprung(Z, 1, 2, "+22", "{BLUE}", t[3] + .6, 190);
rise(q(".res"), t[4]); draw(q(".res .mk"), t[4] + 1.6);
'''),

    dict(say=["Auffüllen ist super, wenn Nullen im Weg sind: 403 − 158.",
              "Von 158 bis 160 sind es 2.",
              "Von 160 bis 200 sind es 40.",
              "Von 200 bis 403 sind es 203.",
              "Zusammen: 2 + 40 + 203 = 245."],
         html='<div class="col" style="gap:20px"><div class="eq m e0">' + tok("403 − 158 = ?") + '</div><div class="zl"></div>'
              '<div class="eq m res">' + tok('<span class="mk"></span>2 + 40 + 203 = 245', "g") + '</div></div>',
         js=f'''
const Z = strahl(q(".zl"), 1500, [[158,110],[160,330],[200,640],[403,1360]]);
rise(q(".e0"), t[0]);
tl.fromTo(Z.mk[3].g, {{opacity:.25}}, {{opacity:1, duration:.4}}, t[0] + 2);
sprung(Z, 0, 1, "+2", "{ORANGE}", t[1] + .4, 90);
sprung(Z, 1, 2, "+40", "{BLUE}", t[2] + .4, 140);
sprung(Z, 2, 3, "+203", "{GREEN}", t[3] + .4, 200);
rise(q(".res"), t[4]); draw(q(".res .mk"), t[4] + 2.2);
'''),

    merke(["Brücken: gleiche Stellen verbinden, rechts anfangen.",
           "Der Übertrag kommt als kleine 1 auf die nächste Brücke.",
           "Oder in Sprüngen: Zehner voll machen oder auffüllen."],
          ["Merke: Bei den Brücken verbindest du gleiche Stellen und fängst rechts an.",
           "Der Übertrag kommt als kleine 1 auf die nächste Brücke.",
           "Oder du rechnest in Sprüngen: Zehner voll machen oder auffüllen. Und mach immer einen Überschlag zur Kontrolle. Jetzt bist du dran!"]),
])

VIDEOS = [NEBEN]
