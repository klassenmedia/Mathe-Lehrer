"""Drehbuch + Sprachausgabe für das Zauberwürfel-Erklärvideo.
python3 script.py  ->  build/scenes.json + build/audio/*.wav + build/audio_all.wav
Alle Zugfolgen und Ausgangsstellungen werden mit cube.py/cases.py gegen das Würfelmodell geprüft."""
import json
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

import cases
from cube import Cube, cube_from, inverse

HERE = Path(__file__).parent
BUILD = HERE / "build"
SR = 22050

# --- geprüfte Zugfolgen ------------------------------------------------------------------------
TRIG = "R U R' U'"
MID_R = "U R U' R' U' F' U F"
MID_L = "U' L' U L U F U' F'"
SUNE = "R U R' U R U2 R'"
KANTEN = "R U R' U R U2 R' U"
ECKEN_PLATZ = "U R U' L' U R' U' L"
TPERM = "R U R' U' R' F R2 U' R' U' R U R' F'"
YPERM = "F R U' R' U' R U R' F' R U R' U' R' F R F'"
UPERM = "R U' R U R U R U' R' U' R2"
F2L_BSP = "U R U' R'"
ROUX_BSP = "M' U M' U2 M U M'"
WORT = {1: "einmal", 3: "dreimal", 5: "fünfmal"}


def piece_ok(c, colors, pos, **faces):
    r = c.piece(colors)
    return r and r[0] == pos and all(r[1][k] == v for k, v in faces.items())


def pruefe():
    """Fehlerhafte Annahmen fallen hier auf, nicht erst im Video."""
    for name, sol in [("Trigger3", TRIG * 1), ("Mitte rechts", MID_R), ("Mitte links", MID_L), ("Sune", SUNE), ("Kanten", KANTEN),
                      ("Ecken", ECKEN_PLATZ), ("T", TPERM), ("Y", YPERM), ("U", UPERM), ("F2L", F2L_BSP), ("Roux", ROUX_BSP)]:
        assert cube_from(inverse(sol) + " " + sol).diff() == (0, 0), name
    # Weiße Ecke: Ausrichtung -> Anzahl Wiederholungen
    ori = {}
    for n in (1, 3, 5):
        c = cube_from(inverse(" ".join([TRIG] * n)))
        p, d = c.piece("DFR")
        assert p == (1, 1, 1)
        ori[n] = d["D"]
        assert cube_from(inverse(" ".join([TRIG] * n)) + " " + " ".join([TRIG] * n)).diff() == (0, 0)
    assert ori == {1: "R", 3: "U", 5: "F"}, ori
    # Mittlere Schicht: Kante liegt über der Front und die Frontfarbe passt
    assert piece_ok(cube_from(inverse(MID_R)), "FR", (0, 1, 1), F="F"), "mid R"
    assert piece_ok(cube_from(inverse(MID_L)), "FL", (0, 1, 1), F="F"), "mid L"
    # OLL/PLL-Behauptungen
    assert cube_from(TPERM).diff() == (2, 2) and cube_from(YPERM).diff() == (2, 2) and cube_from(UPERM).diff() == (0, 3)
    assert cube_from(ECKEN_PLATZ).diff() == (3, 0)
    # Sune: Kanten oben bleiben gelb, drei Ecken verdreht
    c = cube_from(SUNE)
    assert all(c.at(p, "U") == "U" for p in cases.UP.values())
    # F2L-Beispiel: Ecke und Kante liegen nach dem Aufbau beide oben (Paar) und nur der Platz FR ist unten falsch
    c = cube_from(inverse(F2L_BSP))
    assert c.piece("DFR")[0][1] == 1 and c.piece("FR")[0][1] == 1, (c.piece("DFR"), c.piece("FR"))


pruefe()
KREUZ_SOL, _ = cases.gelbes_kreuz()
ECK_SETUP, ECK_SOL = cases.ecken_drehen()
C1 = cases.find_scramble(lambda c: piece_ok(c, "DF", (0, 1, 1), D="U", F="F"))
C2 = cases.find_scramble(lambda c: piece_ok(c, "DF", (1, 1, 0), D="U"))
INTRO_SCRAMBLE = cases.scramble(11)
FINAL_SCRAMBLE = cases.scramble(2024)


def volle_loesung(scr):
    import twophase.solver as sv
    f = cube_from(scr).facelets()
    sol = sv.solve(f, 22, 5)
    sol = re.sub(r"\(\d+f\)", "", sol).replace("1", "").strip()
    sol = " ".join(t.replace("3", "'") for t in sol.split())
    assert cube_from(scr + " " + sol).solved() and cube_from(scr + " " + sol).diff() == (0, 0), sol
    return sol


# --- Drehbuch (Deutsche Buchstaben: V vorne, H hinten, O oben, U unten, L links, R rechts) -----------
DE = {"U": "O", "D": "U", "F": "V", "B": "H", "u": "o", "d": "u", "f": "v", "b": "h"}


def de_seq(s):
    return " ".join(DE.get(t[0], t[0]) + t[1:] for t in s.split())


def fmt(s):
    """{R U R' U'} -> deutsche Buchstaben (O/U/V/H), sonst Text unverändert"""
    return re.sub(r"\{([^}]*)\}", lambda m: de_seq(m.group(1)), s)


def moved(alg):
    """Steine (Farbkennung), die sich durch die Zugfolge von ihrem Platz bewegen oder verdrehen"""
    c = cube_from(alg)
    ref = {(p, n): col for p, n, col in Cube().s}
    pos = {p for p, n, col in c.s if ref[(p, n)] != col}
    ids = set()
    for p in pos:
        ids.add("".join(sorted({col for q, n, col in c.s if q == p})))
    return sorted(ids)


S = []


def sc(**kw):
    for k in ("title", "kicker", "algname"):
        if k in kw:
            kw[k] = fmt(kw[k])
    kw["bullets"] = [fmt(b) for b in kw.get("bullets", [])]
    S.append(kw)


N_MOVED = len(moved(TRIG))

# 1 Einführung
sc(chap="Einführung", kicker="Zauberwürfel für alle", title="So löst du den Würfel",
   bullets=["Jeder Stein hat <b>seinen Platz</b>", "Wir bringen ihn <b>Schritt für Schritt</b> dorthin", "Mit Tricks, die andere Steine <b>nicht kaputt machen</b>"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Hallo! Heute lernst du, wie man einen Zauberwürfel löst. Das ist keine Zauberei, sondern Logik. Jeder Stein hat einen Platz, und wir bringen die Steine nacheinander dorthin. "
        "Du lernst für jeden Stein einen kleinen Trick: Wenn ich diesen Stein dorthin haben will, dann drehe ich so. Und du erfährst auch, was dabei mit den anderen Steinen passiert.")

sc(chap="Grundlagen", kicker="Grundlagen", title="Aus welchen Steinen besteht er?",
   bullets=["<b>6 Mittelsteine</b>: bewegen sich nie, sie bestimmen die Farbe der Seite", "<b>12 Kanten</b>: 2 Farben", "<b>8 Ecken</b>: 3 Farben", "Weiß gegenüber Gelb · Blau gegenüber Grün · Rot gegenüber Orange"],
   setup="", moves="", az=35, el=28, spin=14,
   narr="Der Würfel hat sechs Mittelsteine. Sie haben nur eine Farbe und bewegen sich nie. Sie sagen dir, welche Farbe auf diese Seite gehört. Dazu kommen zwölf Kanten mit zwei Farben und acht Ecken mit drei Farben. "
        "Ein Stein gehört immer dorthin, wo seine Farben zu den Mittelsteinen passen. Eine Ecke mit Weiß, Blau und Rot gehört also zwischen die weiße, die blaue und die rote Seite.")

sc(chap="Grundlagen", kicker="Grundlagen", title="Die Seiten und ihre Buchstaben",
   bullets=["<b>V</b> vorne · <b>H</b> hinten", "<b>O</b> oben · <b>U</b> unten", "<b>L</b> links · <b>R</b> rechts", "Buchstabe = <b>eine Viertel-Drehung</b> im Uhrzeigersinn (Blick auf die Seite)", "<b>’</b> Strich = zurück (andersherum)", "<b>2</b> = halbe Drehung"],
   setup="", moves="R R' U U' F F' L L' D D' B B' R2 U2", labels=True, az=35, el=28, sway=28, algname="Jede Seite einmal",
   narr="Jede Seite bekommt einen Buchstaben: V wie vorne, H wie hinten, O wie oben, U wie unten, L wie links und R wie rechts. Ein Buchstabe allein heißt: Drehe diese Seite eine Viertel-Drehung im Uhrzeigersinn, so als würdest du direkt auf die Seite schauen. "
        "Ein Strich heißt: andersherum, also zurück. Eine Zwei heißt: halbe Drehung. Schau dir an, wie sich die Seiten drehen.")

sc(chap="Grundlagen", kicker="Grundlagen", title="So hältst du den Würfel",
   bullets=["<b>Gelb</b> oben, <b>Weiß</b> unten", "<b>Blau</b> vorne, Grün hinten", "Rot rechts, Orange links", "Den ganzen Würfel kippen: <b>x, y, z</b>"],
   setup="", moves="x x' y y' z z'", az=35, el=28, spin=0, algname="Den ganzen Würfel kippen",
   narr="Wir halten den Würfel immer gleich: Gelb oben, Weiß unten, Blau vorne, Rot rechts.",
   narr2="Wenn du den ganzen Würfel kippen willst, nennen wir das x, y oder z. Dabei ändert sich nichts am Würfel, nur dein Blickwinkel.")

sc(chap="Grundlagen", kicker="Die Grundidee", title="Ein Trick bewegt nur wenige Steine",
   bullets=[f"Folge {{R U R' U'}}", f"Nur <b>{N_MOVED} von 20</b> Steinen wandern", "Alle anderen bleiben genau, wo sie sind", "Unser Werkzeug: kleine Folgen, die <b>wenig</b> verändern"],
   setup="", moves=TRIG, hl=moved(TRIG), az=35, el=28, spin=0, algname="Nur die hellen Steine wandern", mstep=0.7,
   narr="Hier kommt die wichtigste Idee. Wir drehen die Seiten nicht wild herum. Wir nutzen kleine Folgen, die nur ein paar Steine bewegen und den Rest in Ruhe lassen. "
        f"Diese Folge hier bewegt nur {N_MOVED} von zwanzig beweglichen Steinen. Die hellen Steine wandern, alle dunklen bleiben da, wo sie waren.",
   narr2="Rechts, oben, rechts zurück, oben zurück.")

sc(chap="Anfänger-Methode", kicker="Der Plan", title="7 Schritte, Schicht für Schicht",
   bullets=["1  Kreuz unten (weiß)", "2  Ecken unten", "3  Kanten in der Mitte", "4  Kreuz oben (gelb)", "5  Kanten oben richtig stellen", "6  Ecken oben an ihren Platz", "7  Ecken oben drehen"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=14,
   narr="Wir lösen den Würfel Schicht für Schicht. Erst das weiße Kreuz unten. Dann die weißen Ecken. Dann die mittlere Schicht. Danach oben das gelbe Kreuz, die gelben Kanten, die gelben Ecken an ihren Platz und zum Schluss die gelben Ecken drehen. "
        "Zu jedem Schritt zeige ich dir: Was will ich erreichen, wo liegt der Stein gerade, und welcher Trick bringt ihn dorthin.")

# Schritt 1
sc(chap="Schritt 1", kicker="Schritt 1 · Kreuz unten", title="Ich will: eine weiße Kante nach unten",
   bullets=["Kante liegt oben, Weiß zeigt <b>nach oben</b>", "Die andere Farbe passt zum Mittelstein (hier Blau)", "Dann: <b>V2</b> – Kante springt nach unten"],
   setup=C1, moves="F2", hl=["DF"], az=35, el=28, spin=0, elto=-32, algname="{F2}",
   narr="Schritt eins: das weiße Kreuz unten. Dafür gibt es keine feste Zugfolge, hier musst du mitdenken. Die vier weißen Kanten sollen unten sitzen, und ihre zweite Farbe soll zum Mittelstein der Seite passen. "
        "Hier liegt die weiß-blaue Kante oben, Weiß zeigt nach oben und Blau passt schon zum blauen Mittelstein.",
   narr2="Jetzt reicht V zwei, also die vordere Seite halb herum. Die Kante rutscht nach unten.")

sc(chap="Schritt 1", kicker="Schritt 1 · Kreuz unten", title="Ich will: die Kante erst richtig hinstellen",
   bullets=["Kante liegt oben, aber an der falschen Stelle", "Obere Schicht drehen, bis die Seitenfarbe zum Mittelstein passt", "Dann wieder <b>V2</b>"],
   setup=C2, moves="U F2", hl=["DF"], az=35, el=28, spin=0, elto=-32, algname="{U F2}",
   narr="Liegt die Kante oben, aber an der falschen Stelle, drehst du zuerst nur die obere Schicht, bis die Seitenfarbe zu ihrem Mittelstein passt.",
   narr2="Hier reicht einmal O. Danach wieder V zwei.")

sc(chap="Schritt 1", kicker="Schritt 1 · Kreuz unten", title="So sieht das fertige Kreuz aus",
   bullets=["4 weiße Kanten unten", "Ihre Seitenfarben passen zu den Mittelsteinen", "Steckt eine Kante woanders: erst nach oben holen, dann wie eben"],
   setup="", moves="", hl=["D", "DF", "DR", "DB", "DL"], az=35, el=-32, spin=18,
   narr="Steckt eine Kante noch woanders, holst du sie zuerst nach oben, ohne die fertigen Kanten zu zerstören, und löst sie dann wie eben. Wenn alle vier sitzen, ist das Kreuz fertig. Die Seitenfarben passen zu den Mittelsteinen.")

# Schritt 2
sc(chap="Schritt 2", kicker="Schritt 2 · Ecken unten", title="Ich will: eine weiße Ecke nach unten",
   bullets=["Ecke mit Weiß oben suchen", "Oben drehen, bis sie <b>rechts vorne</b> über ihrem Platz steht", "Dann wiederholen: <b>{R U R' U'}</b>", "Das Kreuz unten bleibt am Ende heil"],
   setup=inverse(TRIG), moves=TRIG, hl=["DFR"], az=35, el=28, spin=0, elto=-32, algname="{R U R' U'}  – einmal",
   narr="Schritt zwei: die weißen Ecken. Suche oben eine Ecke mit Weiß. Drehe oben, bis sie rechts vorne über ihrem Platz steht. Dann wiederholst du R, O, R Strich, O Strich, bis die Ecke unten richtig sitzt. "
        "Zwischendurch wackeln andere Steine, am Ende sind sie wieder da. Wie oft du wiederholen musst, hängt davon ab, wohin das Weiß zeigt.")

for n, wo in ((1, "nach rechts"), (3, "nach oben"), (5, "nach vorne")):
    sc(chap="Schritt 2", kicker="Schritt 2 · Ecken unten", title=f"Weiß zeigt {wo}: {n}× wiederholen",
       bullets=[f"Weiß zeigt <b>{wo}</b>", f"<b>{{R U R' U'}}</b> genau <b>{n}×</b>", "Die Ecke dreht sich bei jeder Runde ein Stück weiter"],
       setup=inverse(" ".join([TRIG] * n)), moves=" ".join([TRIG] * n), hl=["DFR"], az=35, el=28, spin=0, elto=-32, algname=f"{{R U R' U'}}  ×{n}", mstep=0.42,
       narr=f"Zeigt Weiß {wo}, wiederholst du die Folge genau {WORT[n]}.")

# Schritt 3
sc(chap="Schritt 3", kicker="Schritt 3 · Mitte", title="Ich will: eine Kante nach rechts in die Mitte",
   bullets=["Kante <b>ohne Gelb</b> oben suchen", "Oben drehen, bis ihre Vorderfarbe zum Mittelstein <b>vorne</b> passt", "Soll sie nach rechts: <b>{U R U' R' U' F' U F}</b>", "Unten bleibt alles ganz"],
   setup=inverse(MID_R), moves=MID_R, hl=["FR"], az=35, el=28, spin=0, algname="Kante nach rechts", mstep=0.5,
   narr="Schritt drei: die mittlere Schicht. Suche oben eine Kante ohne Gelb. Drehe oben, bis ihre vordere Farbe zum Mittelstein vorne passt. Soll die Kante nach rechts in die Mitte, nimmst du diese Folge. Die untere Schicht bleibt dabei ganz.",
   narr2="O, R, O Strich, R Strich. Dann O Strich, V Strich, O, V.")

sc(chap="Schritt 3", kicker="Schritt 3 · Mitte", title="Ich will: eine Kante nach links in die Mitte",
   bullets=["Gleicher Trick, spiegelverkehrt", "Soll sie nach links: <b>{U' L' U L U F U' F'}</b>"],
   setup=inverse(MID_L), moves=MID_L, hl=["FL"], az=35, el=28, spin=0, algname="Kante nach links", mstep=0.5,
   narr="Soll die Kante nach links, spiegelst du die Folge.",
   narr2="O Strich, L Strich, O, L. Dann O, V, O Strich, V Strich. Steckt eine Kante in der Mitte falsch, holst du sie mit demselben Trick heraus.")

# Schritt 4 bis 7
sc(chap="Schritt 4", kicker="Schritt 4 · Kreuz oben", title="Ich will: das gelbe Kreuz oben",
   bullets=["Gelbe Kanten oben zählen: <b>Punkt, L oder Linie</b>", "<b>{F R U R' U' F'}</b> macht aus Punkt ein L, aus L eine Linie, aus Linie ein Kreuz", "L: hinten links halten · Linie: waagerecht"],
   setup=inverse(KREUZ_SOL), moves=KREUZ_SOL, hl=moved("F R U R' U' F'") + ["U"], az=35, el=28, spin=0, algname="Punkt → L → Linie → Kreuz", mstep=0.4, mat=0,
   narr="Schritt vier: das gelbe Kreuz oben. Schau, wie viele gelbe Kanten oben liegen. Das ist ein Punkt, ein L oder eine Linie. Die Folge V, R, O, R Strich, O Strich, V Strich macht aus dem Punkt ein L, aus dem L eine Linie und aus der Linie ein Kreuz. "
        "Das L hältst du hinten links, die Linie liegt waagerecht.")

sc(chap="Schritt 5", kicker="Schritt 5 · Kanten oben", title="Ich will: die gelben Kanten richtig stellen",
   bullets=["Oben drehen, bis mindestens <b>2 Kanten</b> zu ihren Mittelsteinen passen", "Zwei nebeneinander: hinten und rechts halten", "<b>{R U R' U R U2 R' U}</b> wiederholen", "Es wandern nur die Steine oben"],
   setup=inverse(KANTEN), moves=KANTEN, hl=moved(KANTEN), az=35, el=28, spin=0, algname="Kanten oben richtig stellen", mstep=0.5,
   narr="Schritt fünf: die gelben Kanten richtig stellen. Drehe oben, bis mindestens zwei Kanten zu ihren Mittelsteinen passen. Passen zwei nebeneinander, hältst du sie hinten und rechts und machst diese Folge. Wiederhole sie, bis alle vier stimmen. "
        "In unserem Beispiel sind die Ecken zufällig schon fertig. Bei dir kommen sie in den nächsten Schritten.",
   narr2="R, O, R Strich, O, R, O zwei, R Strich, O.")

sc(chap="Schritt 6", kicker="Schritt 6 · Ecken oben", title="Ich will: die Ecken an ihren Platz",
   bullets=["Eine Ecke steht richtig, wenn ihre 3 Farben zu den 3 Mittelsteinen drumherum passen", "Diese Ecke <b>rechts vorne oben</b> halten", "<b>{U R U' L' U R' U' L}</b>: drei Ecken wandern im Kreis, die vierte bleibt"],
   setup=inverse(ECKEN_PLATZ), moves=ECKEN_PLATZ, hl=moved(ECKEN_PLATZ), az=35, el=28, spin=0, algname="Ecken oben platzieren", mstep=0.5,
   narr="Schritt sechs: die gelben Ecken an ihren Platz bringen. Hier geht es noch nicht um die Drehung, nur um den Ort. Eine Ecke sitzt richtig, wenn ihre drei Farben zu den drei Mittelsteinen drumherum gehören. Halte so eine Ecke rechts vorne oben. "
        "Die Folge lässt diese Ecke in Ruhe und lässt die anderen drei im Kreis wandern. Gibt es keine richtige Ecke, machst du die Folge einmal und schaust neu.",
   narr2="O, R, O Strich, L Strich, O, R Strich, O Strich, L.")

sc(chap="Schritt 7", kicker="Schritt 7 · Ecken drehen", title="Ich will: die Ecken richtig drehen",
   bullets=["Falsch gedrehte Ecke <b>rechts vorne oben</b>", "<b>{R' D' R D}</b> wiederholen, bis Gelb oben ist", "Dabei nur oben die nächste Ecke holen", "Unten wackelt es kurz – am Ende ist wieder alles da"],
   setup=ECK_SETUP, moves=ECK_SOL, hl=["U", "FRU", "FLU", "BRU", "BLU"], az=35, el=28, spin=0, algname="Ecken drehen", mstep=0.34, mgap=0.07,
   narr="Schritt sieben: die gelben Ecken drehen. Jetzt stimmt der Platz, nur die Drehung nicht. Halte eine falsch gedrehte Ecke rechts vorne oben. Wiederhole R Strich, U Strich, R, U so lange, bis das Gelb oben ist. "
        "Dabei sieht der Würfel kurz durcheinander aus. Das ist normal. Dann drehst du nur die obere Schicht, bis die nächste Ecke vorne rechts oben steht, und machst weiter. Am Ende drehst du oben zurecht.")

sc(chap="Schritt 7", kicker="Geschafft", title="Der Würfel ist gelöst!",
   bullets=["1 Kreuz unten · 2 Ecken unten · 3 Mitte", "4 Kreuz oben · 5 Kanten oben", "6 Ecken platzieren · 7 Ecken drehen"],
   setup="", moves="", az=35, el=28, spin=20,
   narr="Das war's! Mit etwas Übung schaffst du das in zwei bis drei Minuten. Wer schneller werden will, lernt jetzt die Methoden der Profis.")

# Profis
sc(chap="Profi-Methoden", kicker="Schneller werden", title="Die Methoden der Profis",
   bullets=["<b>CFOP</b> (Fridrich) – am weitesten verbreitet, ca. 55 Züge", "<b>Roux</b> – Blöcke und mittlere Schicht, ca. 45 Züge", "<b>ZZ</b> – erst alle Kanten richtig drehen", "<b>Petrus</b> – Blöcke Stück für Stück aufbauen", "Alle: Muster erkennen + Folgen auswendig kennen"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Profis lösen den Würfel in wenigen Sekunden, der Weltrekord liegt unter vier Sekunden. Dafür nutzen sie klügere Methoden. C F O P von Jessica Fridrich braucht im Schnitt etwa fünfundfünfzig Züge. "
        "Roux von Gilles Roux arbeitet mit Blöcken und der mittleren Schicht. Z Z von Zbigniew Zborowski dreht zuerst alle Kanten richtig. Petrus von Lars Petrus baut Blöcke nach und nach auf. Gemeinsam ist allen: Man erkennt Muster und kennt viele Folgen auswendig.")

sc(chap="CFOP", kicker="CFOP", title="Cross · F2L · OLL · PLL",
   bullets=["<b>Cross</b>: Kreuz unten, ca. 8 Züge", "<b>F2L</b>: Ecke + Kante als Paar einsetzen · 41 Fälle", "<b>OLL</b>: oben alles gelb machen · 57 Fälle", "<b>PLL</b>: oben alles an den Platz · 21 Fälle"],
   setup="", moves="", hl=["D", "DF", "DR", "DB", "DL"], az=35, el=-32, spin=18,
   narr="C F O P heißt Cross, F zwei L, O L L und P L L. Zuerst das Kreuz unten, in höchstens acht Zügen. Dann F zwei L: Ecke und Kante der unteren zwei Schichten werden als Paar gemeinsam eingesetzt, dafür gibt es einundvierzig Fälle. "
        "Dann O L L: Alle gelben Aufkleber drehen nach oben, siebenundfünfzig Fälle. Zuletzt P L L: Alle Steine kommen an ihren Platz, einundzwanzig Fälle.")

sc(chap="CFOP", kicker="CFOP · F2L", title="Ein Paar gemeinsam einsetzen",
   bullets=["Ecke und Kante liegen oben als <b>Paar</b>", "Zusammen in den Platz rechts vorne", "<b>{U R U' R'}</b>"],
   setup=inverse(F2L_BSP), moves=F2L_BSP, hl=["DFR", "FR"], az=35, el=28, spin=0, algname="Paar einsetzen", mstep=0.6,
   narr="Beim F zwei L suchst du eine Ecke und eine Kante, die zusammenpassen, und setzt beide in einem Rutsch ein. Hier liegt das Paar oben und wird mit O, R, O Strich, R Strich in den Platz rechts vorne geschoben.")

sc(chap="CFOP", kicker="CFOP · OLL", title="Sune: oben Ecken drehen",
   bullets=["Dreht drei Ecken, die gelben Kanten bleiben oben", "<b>{R U R' U R U2 R'}</b>", "Gespiegelt: Anti-Sune"],
   setup=inverse(SUNE), moves=SUNE, hl=moved(SUNE), az=35, el=28, spin=0, algname="Sune", mstep=0.5,
   narr="Beim O L L brauchst du für jedes Muster oben eine Folge. Eine der bekanntesten heißt Sune.",
   narr2="R, O, R Strich, O, R, O zwei, R Strich. Sie dreht drei Ecken und lässt die gelben Kanten oben liegen.")

sc(chap="CFOP", kicker="CFOP · PLL", title="T-Perm: zwei Ecken, zwei Kanten tauschen",
   bullets=["Tauscht <b>zwei Ecken</b> und <b>zwei Kanten</b>", "Ecken: rechts vorne ↔ rechts hinten", "Kanten: links ↔ rechts"],
   setup=inverse(TPERM), moves=TPERM, hl=moved(TPERM), az=35, el=28, spin=0, algname="T-Perm", mstep=0.5,
   narr="Beim P L L ist oben schon alles gelb, aber die Steine sind noch vertauscht. Die T-Perm tauscht zwei benachbarte Ecken und zwei Kanten. Alle anderen Steine bleiben.")

sc(chap="CFOP", kicker="CFOP · PLL", title="Y-Perm: Ecken diagonal tauschen",
   bullets=["Tauscht <b>zwei diagonale Ecken</b> und <b>zwei Kanten</b>"],
   setup=inverse(YPERM), moves=YPERM, hl=moved(YPERM), az=35, el=28, spin=0, algname="Y-Perm", mstep=0.46,
   narr="Die Y-Perm tauscht zwei Ecken, die sich diagonal gegenüberliegen, und zwei Kanten.")

sc(chap="CFOP", kicker="CFOP · PLL", title="U-Perm: drei Kanten im Kreis",
   bullets=["Dreht <b>drei Kanten</b> im Kreis", "Die Ecken bleiben"],
   setup=inverse(UPERM), moves=UPERM, hl=moved(UPERM), az=35, el=28, spin=0, algname="U-Perm", mstep=0.5,
   narr="Die U-Perm lässt drei Kanten im Kreis wandern und die Ecken in Ruhe. Mit den anderen neunzehn Fällen löst man damit jede letzte Schicht.")

sc(chap="Roux", kicker="Roux", title="Blöcke und die Mitte",
   bullets=["1  Block aus 1×2×3 links", "2  Zweiter Block rechts", "3  CMLL: letzte 4 Ecken", "4  LSE: Rest nur mit <b>M</b> (Mitte) und <b>O</b>"],
   setup=inverse(ROUX_BSP), moves=ROUX_BSP, az=35, el=28, spin=0, algname="Beispiel: nur M und O", mstep=0.55,
   narr="Roux löst zuerst links einen Block aus ein mal zwei mal drei Steinen und dann rechts einen zweiten. Danach kommen die letzten vier Ecken. Den Rest löst man nur mit M, der mittleren Schicht, und O, der oberen Seite. Dafür braucht man im Schnitt nur etwa fünfundvierzig Züge.",
   narr2="So sieht eine Folge nur aus M und O aus.")

sc(chap="ZZ und Petrus", kicker="ZZ · Petrus", title="Erst Kanten, erst Blöcke",
   bullets=["<b>ZZ</b>: alle Kanten richtig herum drehen, dann nur mit R, O, L weiter", "<b>Petrus</b>: Block 2×2×2 → 2×2×3 → Kanten drehen → untere 2 Schichten → oben"],
   setup=INTRO_SCRAMBLE, moves="", az=215, el=28, spin=16,
   narr="Bei Z Z drehst du zuerst alle Kanten richtig herum. Danach brauchst du für die unteren Schichten nur noch Züge mit R, O und L, man muss den Würfel kaum umgreifen. "
        "Bei Petrus baust du erst einen Block aus zwei mal zwei mal zwei Steinen, dann zwei mal zwei mal drei, drehst alle Kanten richtig und löst zuletzt die obere Schicht.")

sc(chap="Mehr", kicker="Spezial", title="Blind lösen",
   bullets=["Stellung merken, Augen zu, blind lösen", "Old Pochmann: <b>T-Perm</b> für Kanten, <b>Y-Perm</b> für Ecken", "Profis: unter einer Minute"],
   setup=inverse(TPERM), moves=TPERM, hl=moved(TPERM), az=35, el=28, spin=0, algname="T-Perm als Blind-Werkzeug", mstep=0.4, mat=0.8,
   narr="Beim Blindlösen merkt man sich die ganze Stellung, verbindet sich die Augen und löst den Würfel, ohne hinzusehen. Anfänger nutzen die Methode Old Pochmann: Mit der T-Perm tauscht man Kanten, mit der Y-Perm Ecken, immer gegen einen festen Pufferstein. Profis schaffen Merken und Lösen in unter einer Minute.")

sc(chap="Mehr", kicker="Spezial", title="Andere Würfel",
   bullets=["<b>2×2</b>: nur Ecken", "<b>4×4, 5×5</b>: erst Mitten bilden, Kanten paaren, dann wie 3×3", "Megaminx, Pyraminx, Skewb: eigene Methoden"],
   setup="", moves="", az=35, el=28, spin=14,
   narr="Auch größere und kleinere Würfel folgen diesen Ideen. Beim zwei mal zwei gibt es nur Ecken. Bei vier mal vier und fünf mal fünf bildest du erst die Mitten, paarst die Kanten und löst dann wie einen normalen Würfel. Auch für Megaminx, Pyraminx und Skewb gibt es eigene Methoden.")

sc(chap="Mehr", kicker="Computer", title="Gottes Zahl: 20",
   bullets=["2010 bewiesen: <b>20 Züge</b> reichen immer", "Kociemba-Zwei-Phasen-Algorithmus", "Ein Computer löst jeden Würfel in Sekunden"],
   setup=FINAL_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Wie viele Züge braucht man höchstens? Im Jahr zweitausendzehn wurde bewiesen: Zwanzig Züge reichen immer. Diese Zahl heißt Gottes Zahl. Computerprogramme wie der Zwei-Phasen-Algorithmus von Herbert Kociemba finden kurze Lösungen in Sekunden. Sieh dir ein Beispiel an.")


SOL_FINAL = None  # später gesetzt


def final_scene():
    return dict(chap="Komplettlösung", kicker="Computer-Lösung", title="Verdreht → gelöst",
                bullets=["Verdrehte Stellung (20 Zufallszüge)", f"Lösung in <b>{len(SOL_FINAL.split())} Zügen</b>"],
                setup=FINAL_SCRAMBLE, moves=SOL_FINAL, az=35, el=28, sway=30, algname="Computer-Lösung", mstep=0.4, mgap=0.06,
                narr="Der Würfel ist mit zwanzig Zufallszügen verdreht. Der Computer findet eine Lösung mit nur wenigen Zügen. Schau zu, wie sich alles ordnet.", mat=0.0)


def ende_scene():
    return dict(chap="Fazit", kicker="Tipps", title="So wirst du besser",
                bullets=["Anfänger-Methode zuerst, jeden Schritt einzeln üben", "Dann Kreuz ohne Hinsehen, F2L, OLL, PLL", "Fingertricks statt Kraft, Würfel gut schmieren", "Geduld: Jeder Rekord beginnt langsam"],
                setup="", moves="", az=35, el=28, spin=20,
                narr="Zum Schluss ein paar Tipps. Lerne zuerst die Anfänger-Methode und übe jeden Schritt einzeln. Danach kommen das Kreuz ohne Hinsehen, F zwei L, O L L und P L L. Dreh mit den Fingern statt mit Kraft und schmiere den Würfel, damit er flüssig läuft. Viel Spaß beim Drehen!")


# --- Sprache ---------------------------------------------------------------------------------------
TTS_REPL = [("C F O P", "Zeh eff oh peh"), ("O L L", "Oh ell ell"), ("P L L", "Peh ell ell"), ("F zwei L", "eff zwei ell"),
            ("Z Z", "Zett zett"), ("E O Line", "Eh oh lain"), ("C M L L", "Zeh em ell ell"), ("L S E", "ell ess eh"),
            ("Roux", "Ruh"), ("Fridrich", "Fridrich"), ("Zbigniew Zborowski", "Sbigniew Sboroffski"), ("Kociemba", "Kozjemba"),
            ("Pochmann", "Pochmann"), ("Megaminx", "Mega minks"), ("Pyraminx", "Pyra minks"), ("Skewb", "Skjuhb"), ("3-Style", "Drei-Stail"),
            ("T-Perm", "Teh Perm"), ("Y-Perm", "Ypsilon Perm"), ("U-Perm", "Uh Perm"), ("L Strich", "ell Strich"), ("L,", "ell,"), ("L.", "ell."),
            ("zwei mal zwei mal drei", "zwei mal zwei mal drei"), ("Jessica", "Dschessika"), ("Gilles", "Schil"), ("Lars", "Larss")]


def tts(text, path):
    t = text
    for a, b in TTS_REPL:
        t = t.replace(a, b)
    subprocess.run(["espeak-ng", "-v", "de", "-s", "152", "-p", "40", "-g", "6", "-w", str(path), t], check=True)
    w = wave.open(str(path))
    n, sr = w.getnframes(), w.getframerate()
    data = np.frombuffer(w.readframes(n), dtype=np.int16)
    assert sr == SR, sr
    return data


def saetze(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for p in parts:
        while len(p) > 120:
            cut = p.rfind(", ", 0, 120)
            if cut < 40:
                cut = p.rfind(" ", 0, 120)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        out.append(p)
    return out


def timed(text, dur, start):
    """Untertitel-Zeitfenster: Zeichenanteil je Satz"""
    s = saetze(text)
    tot = sum(len(x) for x in s)
    res, t = [], start
    for x in s:
        d = dur * len(x) / tot
        res.append([round(t, 3), round(t + d, 3), x])
        t += d
    return res


def build():
    global SOL_FINAL
    (BUILD / "audio").mkdir(parents=True, exist_ok=True)
    try:
        import os
        SOL_FINAL = inverse(FINAL_SCRAMBLE) if os.environ.get("NO_SOLVE") else volle_loesung(FINAL_SCRAMBLE)
    except Exception as e:
        raise SystemExit(f"Computer-Lösung nicht möglich: {e!r}")
    scenes = S + [final_scene(), ende_scene()]
    chunks, gstart = [], 0.0
    for i, sc_ in enumerate(scenes):
        a1 = tts(sc_["narr"], BUILD / "audio" / f"{i:02d}a.wav")
        d1 = len(a1) / SR
        a2 = tts(sc_["narr2"], BUILD / "audio" / f"{i:02d}b.wav") if sc_.get("narr2") else None
        d2 = len(a2) / SR if a2 is not None else 0
        toks = [t for t in sc_.get("moves", "").split()]
        mstep = sc_.setdefault("mstep", 0.55)
        mgap = sc_.setdefault("mgap", 0.12)
        mdur = sum((1.55 if t.endswith("2") else 1) * mstep + mgap for t in toks)
        lead = 0.5
        if toks:
            if sc_.get("mat") is not None and sc_["mat"] == 0.0:
                sc_["mstart"] = lead + d1 * 0.55    # Bewegung läuft schon während der Erklärung
            else:
                sc_["mstart"] = lead + d1 + 0.5
        else:
            sc_["mstart"] = 9999
        mstart_audio2 = (sc_["mstart"] + 0.1) if toks else lead + d1 + 0.5
        sc_["mstart_real"] = sc_["mstart"]
        end_audio = max(lead + d1, mstart_audio2 + d2) if a2 is not None else lead + d1
        end_moves = sc_["mstart"] + mdur if toks else 0
        dur = max(end_audio, end_moves) + 1.2
        sc_["dur"] = round(dur, 3)
        subs = timed(sc_["narr"], d1, lead)
        if a2 is not None:
            subs += timed(sc_["narr2"], d2, mstart_audio2)
        sc_["subs"] = subs
        k = len(sc_["bullets"])
        sc_["btimes"] = [round(lead + (0.1 + 0.8 * j / max(k, 1)) * d1, 3) for j in range(k)]
        if not toks:
            sc_["mstart"] = 9999
        sc_["gstart"] = round(gstart, 3)
        gstart += dur
        buf = np.zeros(int(dur * SR), dtype=np.int16)
        buf[int(lead * SR):int(lead * SR) + len(a1)] = a1
        if a2 is not None:
            o = int(mstart_audio2 * SR)
            buf[o:o + len(a2)] = a2[:len(buf) - o]
        chunks.append(buf)
    for sc_ in scenes:
        sc_["total"] = round(gstart, 3)
    audio = np.concatenate(chunks)
    with wave.open(str(BUILD / "audio_all.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes())
    (BUILD / "scenes.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=1))
    print(f"{len(scenes)} Szenen, {gstart:.1f} s ({gstart / 60:.1f} min); Lösung: {SOL_FINAL}")


if __name__ == "__main__":
    build()
