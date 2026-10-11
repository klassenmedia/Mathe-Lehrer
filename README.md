# Zahlenwerkstatt

Mathe-Lernspiel für die 3. Klasse. Eine einzige Datei: `index.html` im Browser öffnen (auch auf Tablet/Handy).

## Stationen
- **Malreihen** – Punktefeld + Rechentricks (Kernaufgaben 2·/5·/10·, z. B. 9·6 = 10·6 − 6; 6er = doppelte 3er), auch Umkehraufgaben `☐ · 6 = 42`.
- **Teilen mit Rest** – Kekse werden animiert auf Teller verteilt, dann der schnelle Weg über die Malreihe, Regel „Rest < Teiler“ und Probe.
- **Minus-Rechenwege** – Zehnerstangen/Einerwürfel: erst Zehner weg, dann Einer (Zehner tauschen), Probe.
- **Punkt vor Strich** – Punktaufgaben markieren, zuerst rechnen, dann Strichaufgabe.
- **Fachwörter** – Faktor, Produkt, Dividend, Divisor, Quotient.

### Profi-Tricks für große Zahlen
- **Zahlen bis 1000** – Hunderterplatten, Zehnerstangen, Einerwürfel in der Stellentafel; die Null als Platzhalter; Übergänge (395 + 10).
- **Plus & Minus groß** – Überschlag, stellenweise rechnen, fast runde Zahlen (463 − 198 = 463 − 200 + 2).
- **Kleine Aufgabe hilft** – 3 · 40 → 3 · 4, 120 : 4 → 12 : 4, Nullen anhängen.
- **Große Malaufgaben** – 7 · 16 = 7 · 10 + 7 · 6 mit Rechteck und Malkreuz.
- **Rechentricks & Muster** – Tauschaufgabe, Zahlenhaus (Umkehraufgaben), Nachbaraufgaben, Halbieren und Verdoppeln.
- **Übertrag** – Plus und Minus mit 2–4 Stellen: Aufgabe steht nebeneinander, wird untereinander gedacht, Stelle für Stelle von rechts. Übertrag (10 Einer → 1 Zehner) und Aufmachen/Tauschen beim Minus, auch über eine 0 hinweg. Video 13 zeigt, wie man ohne Platz direkt in der Zeile rechnet (Brücken-Trick, Zehner voll machen, Auffüllen am leeren Zahlenstrahl).

Jede Runde hat 10 Aufgaben. „Zeig mir den Weg“ erklärt jede Aufgabe Schritt für Schritt mit Bildern. Typische Fehler (z. B. Rest zu groß, Punkt-vor-Strich ignoriert) bekommen eine gezielte Rückmeldung.

## Erklärvideos
In `videos/` liegen dreizehn Erklärvideos (mit 3D-Bausteinen) mit Sprecherstimme und Untertiteln (eins pro Station). Im Spiel öffnet der Knopf „▶ Erklärvideo“ das passende Video.

Neu erzeugen (Drehbücher stehen in `videos/skripte.py` `videos/skripte_profi.py` `videos/skripte_uebertrag.py` und `videos/skripte_nebeneinander.py`):
```bash
pip install piper-tts
export HYPERFRAMES_BROWSER_PATH=/pfad/zu/chrome   # optional, sonst lädt HyperFrames Chrome selbst
cd videos && python3 render.py            # alle Videos
python3 render.py 2-teilen-mit-rest       # nur eins
```
Die Stimme (Piper „Thorsten“, offline) wird beim ersten Lauf heruntergeladen. Gerendert wird mit [HyperFrames](https://hyperframes.heygen.com).

## Videos auf den eigenen Rechner holen
- Im Browser: GitHub → Repo `klassenmedia/mathe-lehrer` → Branch `claude/mathe-lernspiel-grundschule-wwonn7` → Ordner `Erklaervideos` → Video anklicken → Download-Knopf.
- Oder alles auf einmal: auf GitHub „Code“ → „Download ZIP“ (bei ausgewähltem Branch).
- Oder per Git: `git clone -b claude/mathe-lernspiel-grundschule-wwonn7 https://github.com/klassenmedia/mathe-lehrer.git`

## 3D-Figuren (aktueller Stand: nur Oskar, die Eule)
**Neueste Version:** `eule()` in `videos/assets/figuren.js` – runde Eule im Pixar-Stil: eiförmiger Körper mit heller, gefleckter Brust, großer Kopf mit hellem Gesichtsschleier, glänzende Bernstein-Augen (Augäpfel drehen sich zum Blicken, Lider leicht verschlafen, blinzeln), kurzer gebogener Schnabel, Krallenfüße, Doktorhut mit Quaste, Flügel aus einem Stück, die beim Zeigen/Winken aufklappen. Weiches Studio-Umgebungslicht in `buehne(…, { weich: true })`.
- Posen über `update(t, {talk, wave, point, pointL, hop, look, intro, kopf, nicken, neigen, blick, staunen, lehnen})`. `kopf`/`nicken`/`neigen`/`lehnen` jeweils −1 … 1, `blick: [x, y]` (−1 … 1, ohne Angabe folgt der Blick der Kopfdrehung), `staunen` 0 … 1 (Augen weit auf, Brauen hoch).
- Vorschau ohne Video: `cd videos/assets && python3 -m http.server 8765`, dann `http://localhost:8765/eule-vorschau.html#point:1` (oder `#rest:1`, `#wave:1`, `#links:1`, `#hoch:1`, `#schraeg:1`, `#live` = Kopf und Augen bewegen sich dauernd).
- Bühne mit weichen Schatten: `buehne(canvas, 1920, 1080, { weich: true })`.
- Video-Drehbuch mit der Eule: `videos/skripte_figuren.py` (Video `0-oskar-stellt-sich-vor`, gerendert: `Erklaervideos/00 Oskar stellt sich vor.mp4`, fürs Spiel `videos/0-oskar-stellt-sich-vor.mp4`). Neu: `cd videos && python3 render.py 0-oskar-stellt-sich-vor`.
- Offen: Flügel noch feiner (Form/Muster), Oskar in die Erklärvideos einbauen (z. B. am Rand, zeigt auf die Rechnung), bessere Stimme.

### Ältere Low-Poly-Figuren
`videos/assets/figuren.js` baut drei eigene Low-Poly-Figuren mit Three.js: **Oskar** (Eule, Erklärer), **Robbi** (Rechenroboter), **Zacki** (Zahlen-Dino). Sie können sprechen (Mund synchron zur Stimme), blinzeln, winken, hüpfen und schauen. Jede Figur hat eine eigene Stimme (Tonhöhe). Ein Video mit Figuren bekommt im Drehbuch ein `three`-Skript und Sätze als `("oskar", "Text")` – Beispiel: `videos/skripte_figuren.py` (Video 00).

## Videos auf den eigenen Rechner holen
- GitHub → Repo `klassenmedia/mathe-lehrer` → Branch `claude/mathe-lernspiel-grundschule-wwonn7` → Ordner `Erklaervideos` → Video anklicken → Download.
- Oder „Code“ → „Download ZIP“ (mit ausgewähltem Branch).

## Stand und nächste Ideen (für eine neue Session)
- Branch: `claude/mathe-lernspiel-grundschule-wwonn7`. Spiel = `index.html`, Videos-Quellcode = `videos/`, fertige Videos in voller Qualität = `Erklaervideos/`, komprimierte Kopien fürs Spiel = `videos/*.mp4` (CRF 28).
- Neu rendern: `cd videos && python3 render.py [video-id …]`, danach für das Spiel mit ffmpeg komprimieren (`-crf 28 -tune animation`).
- Offen: bessere Stimme. Kostenlos ist aktuell Piper „Thorsten low“. Besser wäre ElevenLabs (z. B. über Higgsfield, ca. 100–150 Credits für alle Videos) oder Piper „thorsten high“ (braucht Zugriff auf huggingface.co).
