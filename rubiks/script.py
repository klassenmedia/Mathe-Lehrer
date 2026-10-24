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


# --- Drehbuch --------------------------------------------------------------------------------------
S = []


def sc(**kw):
    S.append(kw)


def seq(*a):
    return " ".join(a)


# Kapitel 1: Grundlagen
sc(chap="Einführung", kicker="Zauberwürfel", title="Würfel lösen – alle Methoden",
   bullets=["<b>43 Trillionen</b> Stellungen", "Jede lösbar in <b>höchstens 20 Zügen</b>", "Anfänger-Methode, Profi-Methoden, Computer"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Willkommen! Heute lernst du, einen Zauberwürfel zu lösen. Zuerst kommen die Grundlagen und die Schreibweise der Züge. Dann die Anfänger-Methode, Schritt für Schritt und mit allen Zügen. Danach die Methoden der Profis, dazu Blindlösen und Computer-Lösungen. "
        "Ein Würfel hat über dreiundvierzig Trillionen Stellungen, und jede davon lässt sich in höchstens zwanzig Zügen lösen.")

sc(chap="Grundlagen", kicker="Grundlagen", title="Aufbau des Würfels",
   bullets=["<b>6 Mittelsteine</b>: fest, sie bestimmen die Farbe der Seite", "<b>12 Kanten</b>: je 2 Farben", "<b>8 Ecken</b>: je 3 Farben",
            "Gegenüber: Gelb–Weiß, Blau–Grün, Rot–Orange"],
   setup="", moves="", az=35, el=28, spin=14,
   narr="Ein Würfel besteht aus sechsundzwanzig sichtbaren Teilen. Sechs Mittelsteine haben nur eine Farbe und bewegen sich nie. Sie legen fest, welche Farbe zu welcher Seite gehört. "
        "Dazu kommen zwölf Kanten mit zwei Farben und acht Ecken mit drei Farben. Gegenüber liegen immer Gelb und Weiß, Blau und Grün, Rot und Orange.")

sc(chap="Grundlagen", kicker="Grundlagen", title="So halten wir den Würfel",
   bullets=["<b>Gelb</b> oben, <b>Weiß</b> unten", "<b>Blau</b> vorne, Grün hinten", "Rot rechts, Orange links", "Ganzer Würfel drehen: <b>x, y, z</b>"],
   setup="", moves="x x' y y' z z'", az=35, el=28, spin=0, algname="Drehungen des ganzen Würfels",
   narr="Wir halten den Würfel immer gleich: Gelb oben, Weiß unten, Blau vorne und Rot rechts.",
   narr2="Den ganzen Würfel drehen wir mit x, y und z. x dreht wie die rechte Seite, y wie die obere und z wie die vordere. Ein Strich dreht in die Gegenrichtung.")

sc(chap="Notation", kicker="Zugschreibweise", title="Die sechs Seiten",
   bullets=["<b>R</b> rechts, <b>L</b> links", "<b>U</b> oben, <b>D</b> unten", "<b>F</b> vorne, <b>B</b> hinten", "ohne Zeichen: ¼ Drehung im Uhrzeigersinn", "<b>’</b> Strich: gegen den Uhrzeigersinn", "<b>2</b>: halbe Drehung"],
   setup="", moves="R R' L L' U U' D D' F F' B B' R2 U2 F2", labels=True, az=35, el=28, sway=28, algname="Seitenzüge",
   narr="Jede Seite hat einen Buchstaben: R wie rechts, L links, U oben, D unten, F vorne und B hinten. Ein Buchstabe allein bedeutet eine Vierteldrehung im Uhrzeigersinn, wenn du direkt auf diese Seite schaust. "
        "Ein Strich bedeutet gegen den Uhrzeigersinn. Eine Zwei bedeutet eine halbe Drehung.")

sc(chap="Notation", kicker="Zugschreibweise", title="Mittlere Schichten und breite Züge",
   bullets=["<b>M</b> wie L, <b>E</b> wie D, <b>S</b> wie F (mittlere Schicht)", "<b>r, l, u, d, f, b</b>: zwei Schichten zugleich", "Zugfolgen von <b>links nach rechts</b> lesen"],
   setup="", moves="M M' E E' S S' r r' u u' f f'", az=35, el=28, sway=25, algname="Mittlere Schichten und breite Züge",
   narr="Dazu kommen die mittleren Schichten. M liegt zwischen links und rechts und dreht wie L. E liegt zwischen oben und unten und dreht wie D. S liegt zwischen vorne und hinten und dreht wie F. "
        "Kleine Buchstaben wie r, u oder f drehen zwei Schichten zugleich. Eine Zugfolge liest du immer von links nach rechts.")

# Kapitel 3: Anfänger-Methode
sc(chap="Anfänger-Methode", kicker="Anfänger-Methode", title="Schicht für Schicht in 7 Schritten",
   bullets=["1  Weißes Kreuz", "2  Weiße Ecken", "3  Mittlere Kanten", "4  Gelbes Kreuz", "5  Gelbe Kanten ausrichten", "6  Gelbe Ecken platzieren", "7  Gelbe Ecken drehen"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=14,
   narr="Die Anfänger-Methode löst den Würfel Schicht für Schicht in sieben Schritten. Erstens das weiße Kreuz. Zweitens die weißen Ecken. Drittens die mittlere Schicht. Viertens das gelbe Kreuz. "
        "Fünftens die gelben Kanten ausrichten. Sechstens die gelben Ecken an ihren Platz bringen. Und siebtens die gelben Ecken drehen. Dafür braucht man oft über hundert Züge, aber jeder Schritt ist einfach.")

sc(chap="Schritt 1", kicker="Schritt 1 · Weißes Kreuz", title="Kante nach unten bringen",
   bullets=["Weiße Kanten nach <b>unten</b>", "Zweite Farbe passt zum <b>Mittelstein</b>", "Hier: Weiß-Blau liegt oben und passt"],
   setup=C1, moves="F2", hl=["DF"], az=35, el=28, spin=0, elto=-32, algname="Kante einsetzen",
   narr="Schritt eins: das weiße Kreuz auf der unteren Seite. Dafür gibt es keinen festen Algorithmus, hier denkst du mit. Alle vier weißen Kanten sollen unten sitzen, und ihre zweite Farbe soll zum Mittelstein der Seite passen. "
        "In diesem Beispiel liegt die weiß-blaue Kante oben, Weiß zeigt nach oben, und Blau passt schon zum blauen Mittelstein.",
   narr2="Dann reicht F zwei.")

sc(chap="Schritt 1", kicker="Schritt 1 · Weißes Kreuz", title="Erst oben ausrichten",
   bullets=["Seitenfarbe passt noch nicht", "Obere Schicht drehen, bis sie passt", "Dann <b>zweimal</b> nach unten"],
   setup=C2, moves="U F2", hl=["DF"], az=35, el=28, spin=0, elto=-32, algname="Ausrichten, dann einsetzen",
   narr="Liegt die Kante oben, aber an der falschen Stelle, drehst du zuerst die obere Schicht, bis die Seitenfarbe zu ihrem Mittelstein passt.",
   narr2="Hier reicht einmal U. Danach wieder F zwei.")

sc(chap="Schritt 1", kicker="Schritt 1 · Weißes Kreuz", title="Das fertige Kreuz",
   bullets=["4 weiße Kanten unten", "Seitenfarben = Mittelsteine", "Weiter mit den Ecken"],
   setup="", moves="", hl=["D", "DF", "DR", "DB", "DL"], az=35, el=-32, spin=18,
   narr="Steckt eine Kante woanders, holst du sie erst nach oben, ohne die schon fertigen Kanten zu zerstören, und führst sie auf einen dieser Fälle zurück. Wenn alle vier sitzen, ist das Kreuz fertig, und die Seitenfarben passen zu den Mittelsteinen.")

sc(chap="Schritt 2", kicker="Schritt 2 · Weiße Ecken", title="Die Folge R U R’ U’",
   bullets=["Ecke mit Weiß oben suchen", "Oben drehen, bis sie <b>rechts vorne</b> über ihrem Platz steht", "<b>R U R’ U’</b> wiederholen, bis Weiß unten ist"],
   setup=inverse(TRIG), moves=TRIG, hl=["DFR"], az=35, el=28, spin=0, elto=-32, algname="Eine Wiederholung",
   narr="Schritt zwei: die weißen Ecken. Suche in der oberen Schicht eine Ecke mit Weiß. Drehe oben, bis sie rechts vorne über ihrem Platz steht. Dann wiederholst du R, U, R Strich, U Strich so lange, bis die Ecke unten richtig sitzt. "
        "Wie oft, hängt davon ab, wohin das Weiß zeigt.")

for n, wo in ((1, "nach rechts"), (3, "nach oben"), (5, "nach vorne")):
    sc(chap="Schritt 2", kicker="Schritt 2 · Weiße Ecken", title=f"Weiß zeigt {wo}",
       bullets=[f"Weiß zeigt <b>{wo}</b>", f"<b>R U R’ U’</b> genau <b>{n}×</b>"],
       setup=inverse(" ".join([TRIG] * n)), moves=" ".join([TRIG] * n), hl=["DFR"], az=35, el=28, spin=0, elto=-32, algname=f"R U R’ U’  ×{n}", mstep=0.42,
       narr=f"Zeigt Weiß {wo}, brauchst du die Folge genau {WORT[n]}.")

sc(chap="Schritt 3", kicker="Schritt 3 · Mittlere Kanten", title="Kante nach rechts einsetzen",
   bullets=["Kante <b>ohne Gelb</b> oben suchen", "Frontfarbe = Mittelstein vorne", "Soll sie nach rechts: <b>U R U’ R’ U’ F’ U F</b>"],
   setup=inverse(MID_R), moves=MID_R, hl=["FR"], az=35, el=28, spin=0, algname="Mittlere Kante nach rechts", mstep=0.5,
   narr="Schritt drei: die mittlere Schicht. Suche oben eine Kante ohne Gelb. Drehe oben, bis ihre Frontfarbe zum Mittelstein vorne passt. Soll die Kante nach rechts, nimmst du diese Folge.",
   narr2="U, R, U Strich, R Strich. Dann U Strich, F Strich, U, F.")

sc(chap="Schritt 3", kicker="Schritt 3 · Mittlere Kanten", title="Kante nach links einsetzen",
   bullets=["Gleiche Idee, spiegelverkehrt", "Soll sie nach links: <b>U’ L’ U L U F U’ F’</b>"],
   setup=inverse(MID_L), moves=MID_L, hl=["FL"], az=35, el=28, spin=0, algname="Mittlere Kante nach links", mstep=0.5,
   narr="Soll die Kante nach links, spiegelst du die Folge.",
   narr2="U Strich, L Strich, U, L. Dann U, F, U Strich, F Strich. Liegt eine Kante in der Mitte, aber falsch, setzt du irgendeine Kante oben ein und holst sie so heraus.")

sc(chap="Schritt 4", kicker="Schritt 4 · Gelbes Kreuz", title="Punkt, L, Linie, Kreuz",
   bullets=["Gelbe Kanten oben zählen: Punkt, L oder Linie", "<b>F R U R’ U’ F’</b>", "L: hinten links halten · Linie: waagerecht"],
   setup=inverse(KREUZ_SOL), moves=KREUZ_SOL, az=35, el=28, spin=0, algname="Punkt → L → Linie → Kreuz", mstep=0.4,
   narr="Schritt vier: das gelbe Kreuz oben. Schau, wie viele gelbe Kanten schon oben liegen. Das ist entweder nur ein Punkt, ein L oder eine Linie. Die Folge F, R, U, R Strich, U Strich, F Strich verwandelt einen Punkt in ein L, das L in eine Linie und die Linie in ein Kreuz. "
        "Das L hältst du dabei hinten links, die Linie liegt waagerecht.",
   mat=0)

sc(chap="Schritt 5", kicker="Schritt 5 · Gelbe Kanten", title="Kanten ausrichten",
   bullets=["Oben drehen, bis mindestens <b>2 Kanten</b> zu ihren Mittelsteinen passen", "Zwei benachbarte: hinten und rechts halten", "<b>R U R’ U R U2 R’ U</b> wiederholen"],
   setup=inverse(KANTEN), moves=KANTEN, hl=["U", "UF", "UR", "UB", "UL"], az=35, el=28, spin=0, algname="Gelbe Kanten ausrichten", mstep=0.5,
   narr="Schritt fünf: die gelben Kanten ausrichten. Drehe oben, bis mindestens zwei Kanten zu ihren Mittelsteinen passen. Passen zwei benachbarte, hältst du sie hinten und rechts und machst diese Folge. Das wiederholst du, bis alle vier Kanten stimmen. "
        "In unserem Beispiel sind die Ecken zufällig schon fertig, bei dir kommen sie in den nächsten Schritten.",
   narr2="R, U, R Strich, U, R, U zwei, R Strich, U.")

sc(chap="Schritt 6", kicker="Schritt 6 · Gelbe Ecken", title="Ecken an den richtigen Platz",
   bullets=["Eine Ecke ist richtig, wenn ihre 3 Farben zu den 3 Mittelsteinen passen", "Diese Ecke <b>rechts vorne oben</b> halten", "<b>U R U’ L’ U R’ U’ L</b>"],
   setup=inverse(ECKEN_PLATZ), moves=ECKEN_PLATZ, hl=["U", "FRU", "FLU", "BRU", "BLU"], az=35, el=28, spin=0, algname="Gelbe Ecken platzieren", mstep=0.5,
   narr="Schritt sechs: die gelben Ecken an den richtigen Platz bringen. Dabei geht es noch nicht um die Drehung, nur um den Platz. Eine Ecke sitzt richtig, wenn ihre drei Farben zu den drei umliegenden Mittelsteinen gehören. Halte so eine Ecke rechts vorne oben. "
        "Gibt es keine, machst du die Folge einmal und suchst neu.",
   narr2="U, R, U Strich, L Strich, U, R Strich, U Strich, L.")

sc(chap="Schritt 7", kicker="Schritt 7 · Gelbe Ecken", title="Ecken drehen: R’ D’ R D",
   bullets=["Falsch gedrehte Ecke <b>rechts vorne oben</b>", "<b>R’ D’ R D</b> wiederholen, bis Gelb oben ist", "Nur <b>oben</b> drehen, nächste Ecke holen", "Zum Schluss die obere Schicht zurechtdrehen"],
   setup=ECK_SETUP, moves=ECK_SOL, hl=["U", "FRU", "FLU", "BRU", "BLU"], az=35, el=28, spin=0, algname="Ecken drehen", mstep=0.34, mgap=0.07,
   narr="Schritt sieben: die gelben Ecken drehen. Jetzt stimmt der Platz, nur die Drehung nicht. Halte eine falsch gedrehte Ecke rechts vorne oben. Wiederhole R Strich, D Strich, R, D so lange, bis das Gelb oben ist. "
        "Dabei sieht der Würfel kurz durcheinander aus, das ist normal. Dann drehst du nur die obere Schicht, bis die nächste Ecke rechts vorne oben steht, und machst weiter. Am Ende drehst du die obere Schicht zurecht.")

sc(chap="Schritt 7", kicker="Geschafft", title="Der Würfel ist gelöst",
   bullets=["1 Kreuz · 2 Ecken · 3 Mitte", "4 Gelbes Kreuz · 5 Kanten", "6 Ecken platzieren · 7 Ecken drehen"],
   setup="", moves="", az=35, el=28, spin=20,
   narr="Das war die Anfänger-Methode. Mit etwas Übung schaffst du den Würfel damit in zwei bis drei Minuten. Wer schneller werden will, lernt jetzt effizientere Methoden.")

# Kapitel 4: Profi-Methoden
sc(chap="Profi-Methoden", kicker="Schneller werden", title="Die großen Methoden",
   bullets=["<b>CFOP</b> (Fridrich) – am weitesten verbreitet, ca. 55 Züge", "<b>Roux</b> – Blöcke, mittlere Schicht, ca. 45 Züge", "<b>ZZ</b> – erst alle Kanten orientieren", "<b>Petrus</b> – Blockbau 2×2×2 → 2×2×3", "Alle: Muster erkennen + Algorithmen lernen"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Speedcuber lösen den Würfel in wenigen Sekunden, der Weltrekord liegt unter vier Sekunden. Dafür nutzen sie effizientere Methoden. C F O P von Jessica Fridrich braucht im Schnitt etwa fünfundfünfzig Züge. "
        "Roux von Gilles Roux arbeitet mit Blöcken und der mittleren Schicht. Z Z von Zbigniew Zborowski richtet zuerst alle Kanten aus. Petrus von Lars Petrus baut Blöcke nach und nach auf. Allen gemeinsam: Du musst Muster erkennen und Algorithmen kennen.")

sc(chap="CFOP", kicker="CFOP", title="Cross · F2L · OLL · PLL",
   bullets=["<b>Cross</b>: Kreuz unten, ca. 8 Züge", "<b>F2L</b>: Ecke + Kante als Paar · 41 Fälle", "<b>OLL</b>: letzte Schicht orientieren · 57 Fälle", "<b>PLL</b>: letzte Schicht platzieren · 21 Fälle"],
   setup="", moves="", hl=["D", "DF", "DR", "DB", "DL"], az=35, el=-32, spin=18,
   narr="C F O P steht für Cross, F zwei L, O L L und P L L. Zuerst das Kreuz, meist unten und in höchstens acht Zügen. Dann F zwei L: Ecke und Kante der ersten zwei Schichten werden gemeinsam als Paar eingesetzt, dafür gibt es einundvierzig Fälle. "
        "Danach O L L: Alle gelben Steine drehen nach oben, siebenundfünfzig Fälle. Zuletzt P L L: Alle Steine kommen an ihren Platz, einundzwanzig Fälle.")

sc(chap="CFOP", kicker="CFOP · F2L", title="Ein F2L-Paar einsetzen",
   bullets=["Ecke und Kante liegen oben als <b>Paar</b>", "Gemeinsam in den Platz rechts vorne", "<b>U R U’ R’</b>"],
   setup=inverse(F2L_BSP), moves=F2L_BSP, hl=["DFR", "FR"], az=35, el=28, spin=0, algname="F2L-Paar", mstep=0.6,
   narr="Beim F zwei L suchst du Ecke und Kante, die zusammenpassen, und setzt beide in einem Rutsch ein. Hier ein einfacher Fall: Das Paar liegt oben und wird mit U, R, U Strich, R Strich in den Platz rechts vorne geschoben.")

sc(chap="CFOP", kicker="CFOP · OLL", title="Sune: ein bekannter OLL-Fall",
   bullets=["Dreht Ecken, Kanten oben bleiben gelb", "<b>R U R’ U R U2 R’</b>", "Der Spiegel heißt Anti-Sune"],
   setup=inverse(SUNE), moves=SUNE, hl=["U", "FRU", "FLU", "BRU", "BLU"], az=35, el=28, spin=0, algname="Sune", mstep=0.5,
   narr="Beim O L L brauchst du für jedes Bild der oberen Seite eine Zugfolge. Eine der bekanntesten heißt Sune.",
   narr2="R, U, R Strich, U, R, U zwei, R Strich. Sie dreht drei Ecken, ohne die gelben Kanten oben zu stören.")

sc(chap="CFOP", kicker="CFOP · PLL", title="T-Perm",
   bullets=["Tauscht <b>zwei Ecken</b> und <b>zwei Kanten</b>", "Ecken: rechts vorne ↔ rechts hinten", "Kanten: links ↔ rechts"],
   setup=inverse(TPERM), moves=TPERM, hl=["U", "FRU", "FLU", "BRU", "BLU", "UF", "UR", "UB", "UL"], az=35, el=28, spin=0, algname="T-Perm", mstep=0.5,
   narr="Beim P L L sind alle Steine oben schon gelb, aber noch vertauscht. Die T-Perm tauscht zwei benachbarte Ecken und zwei Kanten.")

sc(chap="CFOP", kicker="CFOP · PLL", title="Y-Perm",
   bullets=["Tauscht <b>zwei diagonale Ecken</b>", "und <b>zwei Kanten</b>"],
   setup=inverse(YPERM), moves=YPERM, hl=["U", "FRU", "FLU", "BRU", "BLU", "UF", "UR", "UB", "UL"], az=35, el=28, spin=0, algname="Y-Perm", mstep=0.46,
   narr="Die Y-Perm tauscht zwei diagonal gegenüberliegende Ecken und zwei Kanten.")

sc(chap="CFOP", kicker="CFOP · PLL", title="U-Perm",
   bullets=["Dreht <b>drei Kanten</b> im Kreis", "Ecken bleiben unberührt"],
   setup=inverse(UPERM), moves=UPERM, hl=["U", "UF", "UR", "UB", "UL"], az=35, el=28, spin=0, algname="U-Perm", mstep=0.5,
   narr="Die U-Perm dreht drei Kanten im Kreis und lässt die Ecken in Ruhe. Zusammen mit den anderen neunzehn Fällen löst man damit jede letzte Schicht.")

sc(chap="Roux", kicker="Roux", title="Blöcke und die mittlere Schicht",
   bullets=["1  Erster Block 1×2×3 links", "2  Zweiter Block 1×2×3 rechts", "3  CMLL: letzte 4 Ecken", "4  LSE: Rest nur mit <b>M</b> und <b>U</b>"],
   setup=inverse(ROUX_BSP), moves=ROUX_BSP, az=35, el=28, spin=0, algname="Beispiel: nur M und U", mstep=0.55,
   narr="Roux löst zuerst links einen Block aus ein mal zwei mal drei Steinen und danach rechts einen zweiten. Es folgen die letzten vier Ecken, C M L L genannt. Den Rest, die letzten sechs Kanten und die Mitte, löst man nur mit M und U Zügen, das heißt L S E. "
        "Dadurch braucht man im Schnitt nur etwa fünfundvierzig Züge.",
   narr2="So sieht eine Folge aus M und U Zügen aus.")

sc(chap="ZZ", kicker="ZZ", title="Erst die Kanten, dann der Rest",
   bullets=["<b>EOLine</b>: alle Kanten richtig orientieren + 2 Kanten unten", "<b>F2L</b> links und rechts nur mit <b>R, U, L</b>", "Letzte Schicht: OLL/PLL oder ZBLL"],
   setup=INTRO_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Bei Z Z drehst du zuerst alle Kanten richtig herum und legst zwei Kanten unten fest. Das heißt E O Line. Danach brauchst du für die ersten zwei Schichten nur noch Züge mit R, U und L. Man muss den Würfel kaum umgreifen, und die Züge laufen flüssig.")

sc(chap="Petrus", kicker="Petrus", title="Blockbau",
   bullets=["1  Block 2×2×2", "2  Erweitern auf 2×2×3", "3  Alle Kanten orientieren", "4  Erste zwei Schichten fertig", "5  Letzte Schicht"],
   setup=INTRO_SCRAMBLE, moves="", az=215, el=28, spin=16,
   narr="Bei Petrus baust du zuerst einen Block aus zwei mal zwei mal zwei Steinen und erweiterst ihn auf zwei mal zwei mal drei. Dann orientierst du alle Kanten, beendest die ersten zwei Schichten und löst zuletzt die letzte Schicht. Die Methode braucht wenige Züge und viel Überblick.")

# Kapitel 5: mehr
sc(chap="Mehr", kicker="Spezial", title="Blindlösen",
   bullets=["Stellung merken, Augen zu, blind lösen", "Old Pochmann: <b>T-Perm</b> für Kanten, <b>Y-Perm</b> für Ecken", "Profis: 3-Style, unter einer Minute"],
   setup=inverse(TPERM), moves=TPERM, hl=["UL", "UR", "FRU", "BRU"], az=35, el=28, spin=0, algname="T-Perm als Blind-Werkzeug", mstep=0.4,
   narr="Beim Blindlösen merkt man sich die ganze Würfelstellung, verbindet sich die Augen und löst den Würfel, ohne hinzusehen. Anfänger nutzen die Methode Old Pochmann: Mit der T-Perm tauscht man Kanten, mit der Y-Perm Ecken, immer gegen einen festen Pufferstein. "
        "Profis verwenden 3-Style und schaffen Merken und Lösen in unter einer Minute.", mat=0.8)

sc(chap="Mehr", kicker="Spezial", title="Andere Würfel",
   bullets=["<b>2×2</b>: nur Ecken, Anfänger-Methode ohne Kanten", "<b>4×4, 5×5</b>: Reduktion – Mitten bilden, Kanten paaren, dann wie 3×3", "4×4 hat zusätzlich Parität-Fälle", "Megaminx, Pyraminx, Skewb: eigene Methoden"],
   setup="", moves="", az=35, el=28, spin=14,
   narr="Auch größere und kleinere Würfel folgen diesen Ideen. Beim zwei mal zwei gibt es nur Ecken, die löst du wie beim dreier. Bei vier mal vier und fünf mal fünf bildest du erst die Mitten, paarst die Kanten und löst dann wie einen normalen Würfel. "
        "Beim vier mal vier kommen zusätzlich Paritätsfälle dazu. Auch für Megaminx, Pyraminx und Skewb gibt es eigene Methoden.")

sc(chap="Mehr", kicker="Computer", title="Gottes Zahl: 20",
   bullets=["2010 bewiesen: <b>20 Züge</b> reichen immer", "Kociemba-Zwei-Phasen-Algorithmus", "Computer lösen in Sekunden"],
   setup=FINAL_SCRAMBLE, moves="", az=35, el=28, spin=16,
   narr="Wie viele Züge braucht man höchstens? Im Jahr zweitausendzehn wurde bewiesen: Zwanzig Züge reichen immer. Diese Zahl heißt Gottes Zahl. Computer-Programme wie der Zwei-Phasen-Algorithmus von Herbert Kociemba finden solche kurzen Lösungen in Sekunden. "
        "Sieh dir ein Beispiel an.")

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
