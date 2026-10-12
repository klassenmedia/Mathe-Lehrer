"""python3 -m unittest test_engine (im Ordner videos/)"""
import unittest

from engine import HERE, figuren_fuer, seite_fuellen, sprich, zahlwort


class FigurenWeiche(unittest.TestCase):
    def test_video_ohne_eigene_figuren_bekommt_oskar(self):
        js, klasse = figuren_fuer({"id": "x", "scenes": []})
        self.assertIn("eule()", js)
        self.assertEqual(klasse, "mit-oskar")

    def test_eigenes_three_skript_bleibt_unveraendert(self):
        self.assertEqual(figuren_fuer({"three": "EIGEN"}), ("EIGEN", ""))

    def test_oskar_abschaltbar(self):
        self.assertEqual(figuren_fuer({"ohne_oskar": True}), ("", ""))


class Seitenvorlage(unittest.TestCase):
    WERTE = dict.fromkeys(["TOTAL", "THREE_CANVAS", "THREE_JS", "META", "TOPIC", "SCENES", "CAPTIONS", "SCENE_JS"], "x")

    def test_vorlage_wird_vollstaendig_gefuellt_und_bekommt_oskar_klasse(self):
        page = seite_fuellen((HERE / "template.html").read_text(encoding="utf-8"), {**self.WERTE, "ROOT_CLASS": "mit-oskar"})
        self.assertNotIn("%%", page)
        self.assertIn('<div id="root" class="mit-oskar"', page)

    def test_fehlender_platzhalter_wird_gemeldet(self):
        with self.assertRaises(ValueError):
            seite_fuellen((HERE / "template.html").read_text(encoding="utf-8"), self.WERTE)


class Zahlwoerter(unittest.TestCase):
    def test_zahlwoerter(self):
        faelle = {0: "null", 1: "eins", 7: "sieben", 11: "elf", 12: "zwölf", 16: "sechzehn", 17: "siebzehn", 20: "zwanzig",
                  21: "ein-und-zwanzig", 30: "dreißig", 44: "vier-und-vierzig", 99: "neun-und-neunzig", 100: "hundert",
                  101: "hundert-eins", 158: "hundert-acht-und-fünfzig", 200: "zwei-hundert", 347: "drei-hundert-sieben-und-vierzig",
                  1000: "tausend", 1368: "tausend-drei-hundert-acht-und-sechzig", 2001: "zwei-tausend-eins",
                  5813: "fünf-tausend-acht-hundert-dreizehn", 21000: "ein-und-zwanzig-tausend", 101000: "hundert-ein-tausend"}
        for zahl, wort in faelle.items():
            self.assertEqual(zahlwort(zahl), wort, zahl)

    def test_zu_grosse_zahl_bleibt_ziffer(self):
        self.assertEqual(zahlwort(1_000_000), "1000000")

    def test_sprich_schreibt_zahlen_aus(self):
        self.assertEqual(sprich("Probe: 44 + 26 = 70. Richtig!"), "Probe: vier-und-vierzig plus sechs-und-zwanzig gleich siebzig. Richtig!")
        self.assertEqual(sprich("Schreibe 2, die 1 wandert."), "Schreibe zwei, die eins wandert.")
        self.assertNotRegex(sprich("Ohne die 0 stünde da 68. 403 − 158 und 3 · 40 = 120"), r"\d")

    def test_kommazahl_und_ueberlange_ziffern(self):
        self.assertEqual(sprich("Das sind 3,5 Kekse."), "Das sind drei Komma fünf Kekse.")
        self.assertEqual(sprich("Code " + "9" * 5000), "Code " + "9" * 5000)

    def test_bestehende_umschreibungen_bleiben(self):
        self.assertEqual(sprich("die 6er-Reihe, 10-mal"), "die Sechser-Reihe, zehnmal")
        self.assertEqual(sprich("☐ · 6 = 42"), "Kästchen mal sechs gleich zwei-und-vierzig")


class StimmenDownload(unittest.TestCase):
    def test_falsche_pruefsumme_bricht_ab_und_hinterlaesst_nichts(self):
        import tempfile
        from pathlib import Path
        from unittest import mock
        import render
        with tempfile.TemporaryDirectory() as tmp:
            ziel = Path(tmp) / "stimme.onnx"
            def falsch_laden(url, pfad):
                Path(pfad).write_bytes(b"manipuliert")
            with mock.patch("urllib.request.urlretrieve", falsch_laden):
                with self.assertRaises(RuntimeError):
                    render.laden_und_pruefen(ziel, "https://example.invalid/x", "0" * 64)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_richtige_pruefsumme_legt_datei_ab(self):
        import hashlib, tempfile
        from pathlib import Path
        from unittest import mock
        import render
        with tempfile.TemporaryDirectory() as tmp:
            ziel = Path(tmp) / "stimme.onnx"
            with mock.patch("urllib.request.urlretrieve", lambda url, pfad: Path(pfad).write_bytes(b"echt")):
                render.laden_und_pruefen(ziel, "https://example.invalid/x", hashlib.sha256(b"echt").hexdigest())
            self.assertEqual(ziel.read_bytes(), b"echt")


if __name__ == "__main__":
    unittest.main()
