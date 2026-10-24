"""Berechnet (und prüft mit dem Würfelmodell) alle Stellungen und Zugfolgen, die im Video vorkommen."""
import random
from cube import *

UP = {"UF": (0, 1, 1), "UR": (1, 1, 0), "UB": (0, 1, -1), "UL": (-1, 1, 0)}
FACES = "UDRLFB"


def scramble(seed, n=20):
    rng = random.Random(seed)
    out, last = [], ""
    while len(out) < n:
        f = rng.choice(FACES)
        if f == last:
            continue
        last = f
        out.append(f + rng.choice(["", "'", "2"]))
    return " ".join(out)


def find_scramble(pred, seed0=1):
    for seed in range(seed0, seed0 + 20000):
        s = scramble(seed)
        c = cube_from(s)
        if pred(c):
            return s
    raise RuntimeError("keine Stellung gefunden")


def top_edges(c):
    return {k for k, p in UP.items() if c.at(p, "U") == "U"}


def kind(c):
    t = top_edges(c)
    if len(t) == 4: return "kreuz"
    if len(t) == 0: return "punkt"
    if len(t) == 2: return "linie" if t in ({"UL", "UR"}, {"UF", "UB"}) else "L"
    return "?"


A1 = "F R U R' U' F'"
A2 = "F U R U' R' F'"


def gelbes_kreuz():
    """Punkt -> L -> Linie -> Kreuz: Zugfolge + Zwischenmuster, gefunden mit dem Modell."""
    for a in (A1, A2):
        for b in (A1, A2):
            for cc in (A1, A2):
                for k1 in range(4):
                    for k2 in range(4):
                        u1 = " ".join(["U"] * k1) if k1 < 3 else "U'"
                        u2 = " ".join(["U"] * k2) if k2 < 3 else "U'"
                        sol = f"{a} {u1} {b} {u2} {cc}".replace("  ", " ").strip()
                        c = cube_from(inverse(sol))
                        if kind(c) != "punkt": continue
                        c.do(a)
                        if kind(c) != "L": continue
                        c.do(u1)
                        if top_edges(c) != {"UB", "UL"}: continue
                        c.do(b)
                        if kind(c) != "linie": continue
                        c.do(u2)
                        if top_edges(c) != {"UL", "UR"}: continue
                        c.do(cc)
                        if c.diff()[1] == 0 and kind(c) == "kreuz":
                            return sol, (a, u1, b, u2, cc)
    raise RuntimeError("kein gelbes Kreuz")


def ecken_drehen():
    """Zwei verdrehte gelbe Ecken (+ und -), gelöst mit R' D' R D; Rückgabe: Aufbau, Zugfolge."""
    alg = "R' D' R D"
    setup = "t:1,1,1:+ t:1,1,-1:-"
    c = cube_from(setup)
    toks = []
    for i in range(2):
        reps = 0
        while c.at((1, 1, 1), "U") != "U":
            c.do(alg); toks.append(alg); reps += 1
            assert reps < 6
        if i == 0:
            c.do("U"); toks.append("U")
    c.do("U'"); toks.append("U'")
    assert c.diff() == (0, 0) and c.solved(), c.diff()
    return setup, " ".join(toks)


if __name__ == "__main__":
    s, parts = gelbes_kreuz(); print("kreuz", s, parts)
    print(ecken_drehen())
    for name, pred in [("c1", lambda c: (lambda r: r and r[0] == (0, 1, 1) and r[1]["D"] == "U" and r[1]["F"] == "F")(c.piece("DF"))),
                       ("c2", lambda c: (lambda r: r and r[0] == (1, 1, 0) and r[1]["D"] == "U")(c.piece("DF")))]:
        print(name, find_scramble(pred))
