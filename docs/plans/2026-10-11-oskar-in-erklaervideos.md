# Oskar in den Erklärvideos 01–13

Ziel: Oskar, die Eule, steht in jedem Erklärvideo rechts neben der Rechnung, spricht mit, zeigt bei jeder neuen Szene auf den Inhalt, schaut abwechselnd zur Rechnung und zu den Kindern, winkt am Anfang, hüpft am Ende.

## Umsetzung
- Erster Ansatz (Inhalt pauschal per CSS auf 80 % skalieren) verworfen: GSAP überschreibt den Transform auf `.inner`, und viele Szenen sind breiter als der Inhaltsbereich (gemessen bis x = 1848). Jetzt misst `platzFuerOskar()` in `template.html` jede Szene über ihre Dauer und setzt Verkleinerung/Verschiebung auf `.scene` (kleinster Faktor 0,76).
- Zentral in `videos/engine.py`: Videos ohne eigenes `three`-Skript bekommen automatisch das Skript aus `videos/oskar_rand.py` (abschaltbar mit `ohne_oskar=True` im Drehbuch).
- `template.html`: `#root` bekommt Klasse `mit-oskar`; der Inhaltsbereich wird dann auf 80 % verkleinert und nach links gerückt, damit rechts Platz für Oskar ist.
- Bewegung wird nur aus `t`, `SAY` und `SCN` berechnet (kein Zustand), damit HyperFrames jedes Bild einzeln anspringen kann.

## Threat Model
(a) Angreifer: keiner realistisch – Offline-Rendering eigener Drehbücher, keine Nutzereingaben, kein Server.
(b) Untrusted Inputs: keine; Drehbücher und Assets liegen im Repo.
(c) Worst Case: kaputtes Video (Oskar verdeckt Inhalt, Absturz beim Rendern).
(d) Gegenmaßnahme: Sichtprüfung von Einzelbildern pro Video, Unit-Test für die Engine-Weiche, Review.

## Stand
- [x] Engine-Weiche + Test
- [x] Oskar-Skript, Probevideo (Punkt vor Strich, Plus mit Übertrag), Messung aller Szenen ohne Überdeckung
- [x] Alle 13 Videos rendern, komprimieren, Sichtprüfung (Kontaktbogen je 2 Zeigemomente, Messung: keine Überdeckung, 63 von 86 Szenen in voller Größe, kleinste 76 %)
- Ablage: neue Fassungen ersetzen die alten unter gleichem Namen (Entscheidung Andreas 12.10.2026); Rohvideos bleiben vorerst im Repo.
