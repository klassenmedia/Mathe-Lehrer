"""Erzeugt alle Erklärvideos: python3 render.py [video-id ...]
Braucht: pip install piper-tts, Node 22, ffmpeg, Chrome (HYPERFRAMES_BROWSER_PATH)."""
import hashlib
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

import engine
from skripte import VIDEOS as BASIS
from skripte_profi import VIDEOS as PROFI
from skripte_uebertrag import VIDEOS as UEBERTRAG
from skripte_nebeneinander import VIDEOS as NEBEN
from skripte_figuren import VIDEOS as FIGUREN

VIDEOS = BASIS + PROFI + UEBERTRAG + NEBEN + FIGUREN

HERE = Path(__file__).parent
VOICE_DIR = HERE / ".voices"
VOICE = VOICE_DIR / "de_DE-thorsten-high.onnx"
VOICE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx"
TEMPO = 1.3   # length_scale > 1 = langsamer; für Kinder deutlich ruhiger als Piper-Standard
HF = "hyperframes@0.8.147"


# SHA-256 der offiziellen Dateien (Modell laut Hugging-Face-LFS); schützt vor still ausgetauschten Dateien hinter dem Tag
VOICE_SHA256 = {"onnx": "9df1c43c61149ef9b39e618e2b861fbe41e1fcea9390b2dac62e8761573ea4f1",
                "json": "6de734444e4c3f9e33b7ebe2746dbc19b71e85f613e79c65acf623200b99a76a"}


def laden_und_pruefen(ziel, url, sha256):
    """Lädt erst in eine .part-Datei und legt sie nur bei passender Prüfsumme ab; ein Abbruch hinterlässt nichts."""
    teil = ziel.with_name(ziel.name + ".part")
    try:
        urllib.request.urlretrieve(url, teil)
        ist = hashlib.sha256(teil.read_bytes()).hexdigest()
        if ist != sha256:
            raise RuntimeError(f"Prüfsumme falsch für {url}: {ist}")
        os.replace(teil, ziel)
    finally:
        teil.unlink(missing_ok=True)


def ensure_voice(path=VOICE, url=VOICE_URL):
    """Lädt die Stimme (Modell + Konfiguration) einmalig von den offiziellen Piper-Stimmen (CC0)."""
    VOICE_DIR.mkdir(exist_ok=True)
    for ziel, quelle, sha in [(path, url, VOICE_SHA256["onnx"]), (Path(f"{path}.json"), f"{url}.json", VOICE_SHA256["json"])]:
        if not ziel.exists():
            laden_und_pruefen(ziel, quelle, sha)


def main(ids):
    ensure_voice()
    voice = PiperVoice.load(str(VOICE))
    cfg = SynthesisConfig(length_scale=TEMPO)
    stimmen = {"oskar": (voice, cfg, 1.0),
               "robbi": (voice, SynthesisConfig(length_scale=TEMPO * .91), 1.14),
               "zacki": (voice, SynthesisConfig(length_scale=TEMPO * .89), 1.38)}
    for v in VIDEOS:
        if ids and v["id"] not in ids:
            continue
        out, total = engine.build(v, HERE / "build", voice, cfg, stimmen)
        print(f"{v['id']}: {total:.1f} s")
        if "--no-render" in sys.argv:
            continue
        subprocess.run(["npx", "--yes", HF, "lint"], cwd=out, check=True)
        subprocess.run(["npx", "--yes", HF, "render", "-o", str(HERE / f"{v['id']}.mp4")], cwd=out, check=True)


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
