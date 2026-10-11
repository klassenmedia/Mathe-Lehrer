# Zahlenwerkstatt

Mathe-Lernspiel für die 3. Klasse. Eine einzige Datei: `index.html` im Browser öffnen (auch auf Tablet/Handy).

## Stationen
- **Malreihen** – Punktefeld + Rechentricks (Kernaufgaben 2·/5·/10·, z. B. 9·6 = 10·6 − 6; 6er = doppelte 3er), auch Umkehraufgaben `☐ · 6 = 42`.
- **Teilen mit Rest** – Kekse werden animiert auf Teller verteilt, dann der schnelle Weg über die Malreihe, Regel „Rest < Teiler“ und Probe.
- **Minus-Rechenwege** – Zehnerstangen/Einerwürfel: erst Zehner weg, dann Einer (Zehner tauschen), Probe.
- **Punkt vor Strich** – Punktaufgaben markieren, zuerst rechnen, dann Strichaufgabe.
- **Fachwörter** – Faktor, Produkt, Dividend, Divisor, Quotient.

Jede Runde hat 10 Aufgaben. „Zeig mir den Weg“ erklärt jede Aufgabe Schritt für Schritt mit Bildern. Typische Fehler (z. B. Rest zu groß, Punkt-vor-Strich ignoriert) bekommen eine gezielte Rückmeldung.

## Erklärvideos
In `videos/` liegen fünf Erklärvideos mit Sprecherstimme und Untertiteln (eins pro Station). Im Spiel öffnet der Knopf „▶ Erklärvideo“ das passende Video.

Neu erzeugen (Drehbücher stehen in `videos/skripte.py`):
```bash
pip install piper-tts
export HYPERFRAMES_BROWSER_PATH=/pfad/zu/chrome   # optional, sonst lädt HyperFrames Chrome selbst
cd videos && python3 render.py            # alle Videos
python3 render.py 2-teilen-mit-rest       # nur eins
```
Die Stimme (Piper „Thorsten“, offline) wird beim ersten Lauf heruntergeladen. Gerendert wird mit [HyperFrames](https://hyperframes.heygen.com).
