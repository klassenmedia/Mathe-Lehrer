"""Baut aus einem Video-Skript (siehe skripte.py) ein HyperFrames-Projekt:
Sprachausgabe pro Satz mit Piper, Untertitel, Szenen und GSAP-Timeline."""
import html
import json
import re
import shutil
import wave
from pathlib import Path

HERE = Path(__file__).parent
ASSETS = HERE / "assets"

LEAD_IN = 0.6      # Stille am Anfang
GAP = 0.45         # Pause zwischen zwei Sätzen
SCENE_TAIL = 0.7   # Pause am Ende einer Szene
OUTRO = 1.2        # Stille am Ende
HF_CONFIG = {"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
             "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
             "media": {"autoProxy": True}}

ZAHLWORT = {1: "ein", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf", 6: "sechs", 7: "sieben",
            8: "acht", 9: "neun", 10: "zehn"}
REIHE = {2: "Zweier", 3: "Dreier", 4: "Vierer", 5: "Fünfer", 6: "Sechser", 7: "Siebener",
         8: "Achter", 9: "Neuner", 10: "Zehner"}


def sprich(text):
    """Untertitel-Text -> Text für die Sprachausgabe."""
    t = re.sub(r"\s+", " ", text.replace("☐", " Kästchen "))
    t = re.sub(r"(\d+)er\b", lambda m: REIHE.get(int(m.group(1)), m.group(0)), t)
    t = re.sub(r"(\d+)er-", lambda m: REIHE.get(int(m.group(1)), m.group(1)) + "-", t)
    t = re.sub(r"\b(\d+)-mal\b", lambda m: ZAHLWORT.get(int(m.group(1)), m.group(1)) + "mal", t)
    t = re.sub(r"(\d|Kästchen) : (\d|Kästchen)", r"\1 geteilt durch \2", t)
    t = t.replace("·", " mal ").replace("−", " minus ").replace("+", " plus ").replace("=", " gleich ")
    return re.sub(r"\s+", " ", t).strip()


def synth(voice, cfg, text, path, pitch=1.0):
    with wave.open(str(path), "wb") as w:
        voice.synthesize_wav(text, w, syn_config=cfg)
    if pitch != 1.0:
        import subprocess
        with wave.open(str(path), "rb") as r:
            sr = r.getframerate()
        tmp = path.with_suffix(".p.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path), "-af",
                        f"asetrate={int(sr * pitch)},aresample={sr},atempo={1 / pitch:.4f}", "-ac", "1", "-c:a", "pcm_s16le", str(tmp)], check=True)
        tmp.replace(path)
    with wave.open(str(path), "rb") as r:
        return r.getnframes() / r.getframerate(), r.getframerate(), r.readframes(r.getnframes())


def build(video, out_root, voice, cfg, stimmen=None):
    """stimmen: {sprecher: (PiperVoice, SynthesisConfig, tonhoehe)} für Figuren."""
    stimmen = stimmen or {}
    out = out_root / video["id"]
    if out.exists():
        shutil.rmtree(out)
    (out / "tmp").mkdir(parents=True)
    for f in ASSETS.iterdir():
        shutil.copy(f, out / f.name)

    pcm = bytearray()
    rate = None
    t = LEAD_IN
    scenes, caps, say_tl = [], [], []

    def silence(sec):
        pcm.extend(b"\x00\x00" * int(sec * rate))

    for si, sc in enumerate(video["scenes"]):
        start = t
        starts, durs = [], []
        for k, item in enumerate(sc["say"]):
            who, cap = item if isinstance(item, tuple) else (None, item)
            v, c, pitch = stimmen.get(who, (voice, cfg, 1.0))
            dur, r, frames = synth(v, c, sprich(cap), out / "tmp" / f"{si}_{k}.wav", pitch)
            if rate is None:
                rate = r
                silence(LEAD_IN)
            starts.append(round(t, 3))
            durs.append(round(dur, 3))
            pcm.extend(frames)
            t += dur
            pause = GAP if k < len(sc["say"]) - 1 else SCENE_TAIL
            silence(pause)
            caps.append(((f"{who.capitalize()}: " if who else "") + cap, starts[-1], round(dur + pause, 3)))
            say_tl.append([starts[-1], round(dur, 3), who])
            t += pause
        scenes.append(dict(i=si, html=sc["html"], js=sc.get("js", ""), start=round(start, 3),
                           end=round(t, 3), t=starts, d=durs))
    silence(OUTRO)
    total = round(t + OUTRO, 3)

    with wave.open(str(out / "voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(pcm))
    shutil.rmtree(out / "tmp")

    scene_html = "\n".join(
        f'<div id="s{s["i"]}" class="clip scene" data-start="{s["start"]}" '
        f'data-duration="{round(s["end"] - s["start"], 3)}"><div class="inner">{s["html"]}</div></div>'
        for s in scenes)
    cap_html = "\n".join(
        f'<div class="clip cap" data-start="{st}" data-duration="{du}"><div class="captext">{html.escape(c)}</div></div>'
        for c, st, du in caps)
    scene_js = "\n".join(
        f'(function(S,T0,T1,t,d){{const q=s=>S.querySelector(s),qa=s=>[...S.querySelectorAll(s)];'
        f'sceneFade(S,T0,T1);\n{s["js"]}\n}})(document.getElementById("s{s["i"]}"),{s["start"]},{s["end"]},'
        f'{json.dumps(s["t"])},{json.dumps(s["d"])});'
        for s in scenes)

    page = (HERE / "template.html").read_text(encoding="utf-8")
    if video.get("three"):
        three_canvas = '<canvas id="three-layer"></canvas>'
        three_js = ('<script>window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};'
                    'window.__hf.buildReady.figuren = new Promise(r => window.figurenFertig = r);</script>\n'
                    '<script type="module">\n' + video["three"] + '\n</script>')
    else:
        three_canvas = three_js = ""
    meta = (f"<script>window.SAY = {json.dumps(say_tl)}; window.SCN = "
            f"{json.dumps([[s['start'], s['end']] for s in scenes])}; window.renderHooks = [];</script>")
    page = (page.replace("%%TOTAL%%", str(total))
                .replace("%%THREE_CANVAS%%", three_canvas)
                .replace("%%THREE_JS%%", three_js)
                .replace("%%META%%", meta)
                .replace("%%TOPIC%%", html.escape(video["topic"]))
                .replace("%%SCENES%%", scene_html)
                .replace("%%CAPTIONS%%", cap_html)
                .replace("%%SCENE_JS%%", scene_js))
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / "hyperframes.json").write_text(json.dumps(HF_CONFIG, indent=2), encoding="utf-8")
    return out, total
