"""Würfelmodell für das Erklärvideo: Sticker mit Position + Normale, Züge als 90°-Drehungen.
Farben: U gelb, D weiß, F blau, B grün, R rot, L orange (gelb oben, weiß unten)."""
import itertools

FARBE = {"U": "gelb", "D": "weiss", "F": "blau", "B": "gruen", "R": "rot", "L": "orange"}
# Move -> (Achse, Schichten, Winkel*90°) ; Winkel nach Rechte-Hand-Regel um +Achse
ACH = {"x": 0, "y": 1, "z": 2}
MOVES = {
    "U": ("y", (1,), -1), "D": ("y", (-1,), 1), "E": ("y", (0,), 1),
    "R": ("x", (1,), -1), "L": ("x", (-1,), 1), "M": ("x", (0,), 1),
    "F": ("z", (1,), -1), "B": ("z", (-1,), 1), "S": ("z", (0,), -1),
    "u": ("y", (0, 1), -1), "d": ("y", (-1, 0), 1),
    "r": ("x", (0, 1), -1), "l": ("x", (-1, 0), 1),
    "f": ("z", (0, 1), -1), "b": ("z", (-1, 0), 1),
    "x": ("x", (-1, 0, 1), -1), "y": ("y", (-1, 0, 1), -1), "z": ("z", (-1, 0, 1), -1),
}
NORMAL = {"U": (0, 1, 0), "D": (0, -1, 0), "R": (1, 0, 0), "L": (-1, 0, 0), "F": (0, 0, 1), "B": (0, 0, -1)}


def parse(seq):
    """'R U R\\' U2' -> [('R',1),('U',1),('R',-1),('U',2)] ; Schreibweise: ' = gegen, 2 = doppelt"""
    out = []
    for t in seq.split():
        if t.startswith("t:"):      # Sondertoken 't:1,1,1:+' = Ecke dort um 120° verdrehen
            out.append((t, 1))
            continue
        m, n = t[0], 1
        if t.endswith("'"):
            n = -1
        elif t.endswith("2"):
            n = 2
        assert m in MOVES, t
        out.append((m, n))
    return out


def inverse(seq):
    out = []
    for t in reversed(seq.split()):
        if t.startswith("t:"):
            out.append(t[:-1] + ("-" if t.endswith("+") else "+"))
        elif t.endswith("'"):
            out.append(t[0])
        elif t.endswith("2"):
            out.append(t)
        else:
            out.append(t + "'")
    return " ".join(out)


def rot(v, ax, quarter):
    """Vektor um Achse ax um quarter*90° (rechte Hand, +Achse)."""
    x, y, z = v
    for _ in range(quarter % 4):
        if ax == 0:   x, y, z = x, -z, y
        elif ax == 1: x, y, z = z, y, -x
        else:         x, y, z = -y, x, z
    return (x, y, z)


class Cube:
    def __init__(self):
        # stickers: Liste (pos, normal, farbe)
        self.s = []
        for f, n in NORMAL.items():
            for pos in itertools.product((-1, 0, 1), repeat=3):
                if sum(a * b for a, b in zip(pos, n)) == 1:
                    self.s.append([pos, n, f])

    def twist(self, pos, sign):
        S = pos
        sign = sign * S[0] * S[1] * S[2]   # Händigkeit: + = im Uhrzeigersinn von außen gesehen
        for st in self.s:
            if st[0] == pos:
                a, b, c = (st[1][i] * S[i] for i in range(3))
                a, b, c = (c, a, b) if sign > 0 else (b, c, a)
                st[1] = (a * S[0], b * S[1], c * S[2])
        return self

    def move(self, m, n=1):
        if m.startswith("t:"):
            p, s = m[2:].split(":")
            return self.twist(tuple(int(v) for v in p.split(",")), 1 if s == "+" else -1)
        ax, layers, q = MOVES[m]
        a = ACH[ax]
        for st in self.s:
            if st[0][a] in layers:
                k = q * n
                st[0] = rot(st[0], a, k)
                st[1] = rot(st[1], a, k)
        return self

    def do(self, seq):
        for m, n in parse(seq):
            self.move(m, n)
        return self

    def face_of(self, n):
        return {v: k for k, v in NORMAL.items()}[n]

    def piece(self, colors):
        """Position des Teils mit diesen Farben (Face-Buchstaben) und die Fläche je Farbe"""
        pos = {}
        for p, n, c in self.s:
            pos.setdefault(p, {})[c] = self.face_of(n)
        for p, d in pos.items():
            if set(d) == set(colors):
                return p, d

    def at(self, pos, f):
        """Farbe des Stickers an Position pos auf Fläche f"""
        for p, n, c in self.s:
            if p == pos and n == NORMAL[f]:
                return c

    def solved(self):
        for f in NORMAL:
            if len({c for p, n, c in self.s if n == NORMAL[f]}) != 1:
                return False
        # Mittelsteine bestimmen die Farbe: nach Würfeldrehung zählt nur Einfarbigkeit
        return True

    def facelets(self):
        """Kociemba-String URFDLB; Zentren definieren die Flächen (nur ohne Drehung des Würfels sinnvoll)"""
        order = []
        for r in (-1, 0, 1):          # U: hinten->vorne, links->rechts
            for c in (-1, 0, 1): order.append(((c, 1, r), "U"))
        for r in (1, 0, -1):          # R: oben->unten, vorne->hinten
            for c in (1, 0, -1): order.append(((1, r, c), "R"))
        for r in (1, 0, -1):          # F
            for c in (-1, 0, 1): order.append(((c, r, 1), "F"))
        for r in (1, 0, -1):          # D: vorne->hinten
            for c in (-1, 0, 1): order.append(((c, -1, r), "D"))
        for r in (1, 0, -1):          # L
            for c in (-1, 0, 1): order.append(((-1, r, c), "L"))
        for r in (1, 0, -1):          # B
            for c in (1, 0, -1): order.append(((c, r, -1), "B"))
        return "".join(self.at(p, f) for p, f in order)

    def diff(self, other_seq=None):
        """Anzahl Positionen (Cubies), deren Stickerfarben vom gelösten Zustand abweichen: (Ecken, Kanten)"""
        ref = Cube()
        key = lambda cube: {(p, n): c for p, n, c in cube.s}
        a, b = key(self), key(ref)
        bad = set()
        for k in a:
            if a[k] != b[k]:
                bad.add(k[0])
        corners = [p for p in bad if all(v != 0 for v in p)]
        edges = [p for p in bad if sum(1 for v in p if v == 0) == 1]
        return len(corners), len(edges)


def cube_from(seq):
    return Cube().do(seq)


if __name__ == "__main__":
    c = Cube().do("R U R' U'")
    print(c.facelets())
    assert Cube().do("R U R' U' " * 6).diff() == (0, 0)
    assert Cube().do("R U R' U' " * 6).solved()
