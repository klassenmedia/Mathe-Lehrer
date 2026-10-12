"""python3 -m unittest test_engine (im Ordner videos/)"""
import unittest

from engine import HERE, figuren_fuer, seite_fuellen


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


if __name__ == "__main__":
    unittest.main()
