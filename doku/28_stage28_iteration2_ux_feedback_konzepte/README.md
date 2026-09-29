# Station 28 — Iteration 2 beginnt: Web-UI-Feedback der Betreuer umgesetzt

**Zeitraum:** 09.09.2026 (ENTSCHEIDUNGSLOG.md Phase 56)
**Markiert den Beginn von Iteration 2.** Iteration 1 wurde am 07.09.2026 abgeschlossen
(Dokumentation dazu im projektübergreifenden `Iteration 1/`-Ordner: `Doku_Iteration_1.md`,
`Doku_Iteration_1.docx`, Demo-Screenshots). Der komplette Code-Stand von Iteration 1 wurde am
09.09.2026 zusätzlich als privates GitHub-Repo gesichert
(`https://github.com/finanzsnack-lgtm/Master-Arbeit-`).
**Mit Code-Duplikat:** Vorher-Stand aller betroffenen Dateien in `code_stand/` (siehe unten),
Konzeptphase und Umsetzung erfolgten in einem Zug nach Abstimmung mit dem Product Owner.

## Auslöser

Echtes Feedback der Betreuer aus der Iteration-1-Demo (`Iteration 1/DEMO Feedbag.txt`,
"Demo-Feedbag 1"), fünf Punkte zur Web-Oberfläche (`static/index.html`, `webapp.py`):

1. Layout/Anordnung — Reiseplan soll neben dem Chat stehen, nicht darunter.
2. Darstellung — Zeiten und Beschreibungen besser strukturieren.
3. Chat-Funktionalität — Schnellantworten (Quick Replies).
4. Performance-Feedback — visueller Ladeindikator bei längeren Wartezeiten.
5. Bot-Persönlichkeit — Avatar für den Bot.

## Konzept und Umsetzung

### 1. Layout — Reiseplan neben dem Chat

Ab einer Mindestbreite `main` auf ein Zwei-Spalten-Layout umstellen (Chat links, `#ergebnis`
rechts), unterhalb eines Breakpoints (Smartphone) bleibt es bei der bisherigen gestapelten
Darstellung. Die rechte Spalte zeigt von Beginn an einen Platzhaltertext statt leer zu bleiben,
das bereitet Konzept 4 mit vor.

**Umgesetzt in:** `static/index.html` (CSS-Grid-Media-Query ab 980px, `#ergebnis-platzhalter`).

### 2. Zeitanzeige — real wirkende Uhrzeit statt missverständlicher Dauer, klar als Annahme markiert

**Fund:** `src/ausgabe/reiseplan.py:151-158` (`_zeitpunkt_text`) hat zwei Anzeigemodi. Ab Tag 2
mit beantworteter Tagesablauf-Frage (F20, `tagesstart_minuten` gesetzt) wird bereits heute die
echte Uhrzeit gezeigt ("14:00 Uhr – 15:00 Uhr"). An Tag 1 (immer) und an jedem Tag ohne
F20-Antwort wird stattdessen eine relative Dauer seit Tagesbeginn gezeigt ("ab 1h – bis 2h",
`_format_dauer`, Zeilen 94–104) — das liest sich wie eine Aufenthaltsdauer von 1–2 Stunden, gemeint
ist aber "eine Stunde nach Tagesbeginn bis zwei Stunden nach Tagesbeginn". Bewusst so gebaut, weil
eine echte Uhrzeit dort erfunden wäre (kein reales Ticket für die Hinreise, keine bekannte
Tagesstart-Präferenz) — Verstoß gegen Grundprinzip 1.

**Konzept (mit Product Owner abgestimmt, 09.09.2026):** Für Tag 1 und Tage ohne F20-Antwort einen
festen, klar als Annahme gekennzeichneten Standard-Tagesbeginn verwenden (09:00 Uhr, neue Konstante
analog `STANDARD_TAGESBUDGET_MINUTEN` in `src/config.py`) und daraus eine Uhrzeit im selben Format
wie die echten Zeiten berechnen, aber mit dem "ca."-Präfix markieren, das die App bereits für die
Kostenschätzung verwendet ("ca. X € / Nacht"): also "ca. 14:00 Uhr" statt "ab 1h". Zusätzlich EINE
erklärende Zeile analog zur bestehenden `_uhrzeit_hinweis_text`-Funktion, die einmalig erläutert,
dass "ca."-Zeiten auf einem angenommenen Tagesbeginn beruhen, keine feste Angabe sind. Betrifft
`_zeitpunkt_text`/`_format_dauer`/`_uhrzeit_hinweis_text` in `reiseplan.py` — wirkt dadurch
einheitlich sowohl auf die Web-Karten (`als_kartendaten`) als auch auf den Text-/HTML-Reiseplan
(`als_text`), eine einzige Quelle für beide Ausgabeformen.

**Umgesetzt in:** `src/config.py` (neue Konstante `standard_tagesstart_minuten`, `.env.example`),
`src/ausgabe/reiseplan.py` (`_zeitpunkt_text`, `_uhrzeit_hinweis_text`, Doku am Feld
`tagesstart_minuten`). Drei bestehende Tests in `tests/test_reiseplan.py` an das neue Format
angepasst (alte Tests prüften explizit das Fehlen von Uhrzeit-Mustern, das war der alte, jetzt
bewusst geänderte Zustand).

### 3. Chat — Quick Replies als reine Eingabehilfe, LLM-gesteuert

Klarstellung nach Rückfrage beim Product Owner: Die Auswahl der Kurzantworten bleibt bewusst beim
LLM, NICHT im deterministischen Layer verdrahtet — passend zu Grundprinzip 1 (LLM führt den Dialog
eigenverantwortlich). Zwei harte Vorgaben:

- Die Chips sind reine Eingabehilfe. Das Textfeld bleibt IMMER zusätzlich nutzbar, die Eingabe wird
  NIE auf die angebotenen Optionen beschränkt.
- Bei Ja/Nein-artigen Fragen kann das LLM Chips anbieten; braucht es danach mehr Information, stellt
  es einfach eine normale Rückfrage — kein separater Mechanismus nötig, das kann das LLM ohnehin
  schon.

**Technische Anknüpfung:** Kein sechstes Tool, die dokumentierte "fünf Werkzeuge"-Architektur bleibt
unangetastet. Stattdessen eine Konvention in der Systemanweisung: Das LLM darf seiner Textnachricht
optional eine strukturierte letzte Zeile anhängen (`[SCHNELLANTWORTEN: Ja | Nein]`, max. 4
Optionen), die `bot_sagt` herausparst, aus dem angezeigten Text entfernt und separat als Chips
mitschickt. Rein additiv, kein Eingriff in die Tool-Architektur.

**Umgesetzt in:** `src/fragekatalog/regelwerk.py` (neuer "SCHNELLANTWORTEN"-Abschnitt in
`_TOOL_ANLEITUNG`), `src/audio/kanal.py` (neue Funktion `zerlege_schnellantworten`, angewendet in
`TextKanal`/`AudioKanal.bot_sagt`, dort werden die Optionen nur verworfen), `webapp.py`
(`WebIOKanal.bot_sagt` schickt `schnellantworten` zusätzlich im WebSocket-JSON), `static/index.html`
(Klick-Chips unter der jeweils letzten Bot-Nachricht, Textfeld bleibt immer parallel nutzbar, alte
Chips verschwinden bei der nächsten gesendeten Nachricht). Neue Tests in `tests/test_kanal.py` und
`tests/test_webapp.py`.

### 4. Performance — Ladeindikator (vereinfachte Erklärung)

Zwei getrennte Situationen:

- **Normales Warten:** Nach "Senden" sofort eine kurze Animation ("Bot schreibt …", drei Punkte)
  im Chatverlauf zeigen, bis irgendeine Antwort ankommt. Reine Frontend-Änderung, kein
  Server-Eingriff nötig.
- **Der eine Sonderfall, der wirklich wehtut:** Beim finalen Planungsschritt kann es laut
  CLAUDE.md ("Performance-Hinweis") und einem dokumentierten Live-Vorfall (ENTSCHEIDUNGSLOG.md
  Phase 44) wirklich lange dauern, weil für "mittel"/"stark" Barrierefreiheit jeder Kandidat
  einzeln bei Google geprüft wird. Die normale "Bot schreibt"-Animation sieht dann genauso aus wie
  eine kurze, normale Denkpause — der Nutzer kann nicht unterscheiden, ob die App noch arbeitet
  oder eingefroren ist. Deshalb für GENAU diesen einen Moment (kurz bevor die Reise geplant wird)
  eine eigene, deutlichere Meldung einblenden: "Reiseroute wird berechnet – kann bei vielen
  Kandidaten etwas dauern." Der Server muss dafür nur EIN zusätzliches Signal schicken, kurz bevor
  er mit dem eigentlichen Planen anfängt.

**Umgesetzt in:** `static/index.html` (`.tippt`-Animation, `zeigeTippt`/`entferneTippt`,
`zeigePlanungsStatus`), `src/audio/kanal.py` (`IOKanal.zeige_status`, No-Op-Konsolenzeile in
`TextKanal`/`AudioKanal`), `webapp.py` (`WebIOKanal.zeige_status` sendet `{typ:"status", phase}`),
`src/fragekatalog/agent_tools.py` (`AgentSessionState.io_kanal`, Aufruf in
`plane_reise_und_abschliessen` VOR dem blockierenden `plane_reise`-Aufruf), `chat.py` (übergibt den
Kanal an den Session-State). Neue Tests in `tests/test_kanal.py`, `tests/test_agent_tools.py`,
`tests/test_webapp.py`.

### 5. Bot-Avatar

Kleines rundes Icon links neben jeder Bot-Sprechblase, Akzentfarbe der App, bewusst schlicht (kein
Name/Charakter — das wäre eine größere, eigene Entscheidung für später).

**Umgesetzt in:** `static/index.html` (`.avatar`/`.nachricht-zeile`, `erzeugeAvatar()`, angewendet
in `anhaengen()` und `zeigeTippt()`).

## Verifikation

Komplette Test-Suite grün (325/325, vorher 291 vor Iteration 2 laut `doku/README.md`-Übersicht).
Konzept 1 (Layout) und Konzept 5 (Avatar) sind reine CSS-/DOM-Änderungen ohne Pytest-Abdeckung
(kein Browser-Test in dieser Suite) – noch nicht gegen einen echten Browser verifiziert. Konzept 3
(Schnellantworten) ist auf Code-Ebene getestet (Parsing, WebSocket-Übertragung), aber NICHT, ob das
LLM der neuen Regelwerk-Anweisung in einer echten Session zuverlässig folgt – das lässt sich nur in
einem echten Chat-Test beobachten, nicht deterministisch testen.

## Offene Punkte / nächste Schritte

- Layout (1), Avatar (5) und das tatsächliche LLM-Verhalten bei Schnellantworten (3) noch nicht in
  einem echten Browser/einer echten Chat-Session beobachtet.
- Falls sich das LLM nicht zuverlässig an das Schnellantworten-Format hält (z.B. falsche Syntax,
  zu häufiger/seltener Einsatz): Regelwerk-Text in `regelwerk.py` nachschärfen, kein struktureller
  Umbau nötig (reine Prompt-Iteration).
