"""Erzeugt alle Erklärvideos: python3 render.py [video-id ...]
Braucht: pip install piper-tts, Node 22, ffmpeg, Chrome (HYPERFRAMES_BROWSER_PATH)."""
import subprocess
import sys
import tarfile
import urllib.request
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

import engine
from skripte import VIDEOS as BASIS
from skripte_profi import VIDEOS as PROFI
from skripte_uebertrag import VIDEOS as UEBERTRAG

VIDEOS = BASIS + PROFI + UEBERTRAG

HERE = Path(__file__).parent
VOICE_DIR = HERE / ".voices"
VOICE = VOICE_DIR / "de-thorsten-low.onnx"
VOICE_URL = "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-de-thorsten-low.tar.gz"
HF = "hyperframes@0.8.147"


def ensure_voice():
    if VOICE.exists():
        return
    VOICE_DIR.mkdir(exist_ok=True)
    tgz = VOICE_DIR / "voice.tgz"
    urllib.request.urlretrieve(VOICE_URL, tgz)
    with tarfile.open(tgz) as t:
        t.extractall(VOICE_DIR, filter="data")
    tgz.unlink()


def fix_phonemes(voice):
    """Neuere espeak-Versionen zerlegen 'ç' (ich-Laut) in 'c' + Cedille. Die alte Stimme kennt nur 'ç'."""
    orig = voice.phonemize

    def phonemize(text):
        out = []
        for sent in orig(text):
            ph = []
            for p in sent:
                if p == "\u0327" and ph and ph[-1] == "c":
                    ph[-1] = "ç"
                elif p in voice.config.phoneme_id_map:
                    ph.append(p)
            out.append(ph)
        return out

    voice.phonemize = phonemize


def main(ids):
    ensure_voice()
    voice = PiperVoice.load(str(VOICE))
    fix_phonemes(voice)
    cfg = SynthesisConfig(length_scale=1.12)
    for v in VIDEOS:
        if ids and v["id"] not in ids:
            continue
        out, total = engine.build(v, HERE / "build", voice, cfg)
        print(f"{v['id']}: {total:.1f} s")
        if "--no-render" in sys.argv:
            continue
        subprocess.run(["npx", "--yes", HF, "lint"], cwd=out, check=True)
        subprocess.run(["npx", "--yes", HF, "render", "-o", str(HERE / f"{v['id']}.mp4")], cwd=out, check=True)


if __name__ == "__main__":
    main([a for a in sys.argv[1:] if not a.startswith("--")])
