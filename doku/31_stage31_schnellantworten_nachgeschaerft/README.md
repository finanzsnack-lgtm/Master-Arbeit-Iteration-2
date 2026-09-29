# Station 31 — Schnellantworten-Anweisung nachgeschärft nach echtem Nutzertest

**Zeitraum:** 21.09.2026
**Mit Code-Duplikat:** Vorher-Stand von `src/fragekatalog/regelwerk.py` in `code_stand/`.

## Auslöser

Erster echter Blick auf Schnellantworten im laufenden Chat (Screenshot des Nutzers): Bei der Frage
"Mit wem geht's denn ans Meer – reist du allein, mit Partner/in, Familie oder Freunden?" bot das
LLM KEINE Klick-Chips an, obwohl die Frage selbst schon vier klar benennbare Optionen im Text
aufzählt und die bestehende Regelwerk-Anweisung ("Ja/Nein ODER eine kurze, feste Handvoll
Optionen") das eigentlich bereits erlaubt hätte. Nutzerwunsch: generell mehr/konsequentere
Antwortmöglichkeiten im gesamten Chatprozess.

## Einordnung

Die Technik (Parsing `zerlege_schnellantworten`, WebSocket-Übertragung, Klick-Chips im Frontend)
war bereits vollständig fertig und getestet (Stage 28). Die beobachtete Lücke war reines
LLM-Prompt-Verhalten: die Anweisung existierte, wurde aber nicht zuverlässig/konsequent
angewendet – genau der in Stage 28 als offen vermerkte Punkt ("hängt vom tatsächlichen
LLM-Verhalten ab ... noch nicht in einer echten Chat-Session beobachtet").

## Umsetzung

`src/fragekatalog/regelwerk.py`, Abschnitt SCHNELLANTWORTEN nachgeschärft:

- Ton von "darfst du optional" auf "GRUNDSÄTZLICH, der Regelfall" verschärft – weiterhin freiwillig
  im Sinne von "kein Zwang zur Nutzung des Tools", aber nicht mehr als reine Kann-Option formuliert.
- Neue, direkt auf die beobachtete Lücke zugeschnittene Regel: nennt das LLM in seiner eigenen
  Frage bereits konkrete Beispielantworten im Fließtext, MUSS es dieselben Optionen zusätzlich als
  Schnellantworten anhängen – schließt genau die im Screenshot beobachtete Inkonsistenz.
  Beispiel aus dem Fragekatalog explizit genannt: Reisebegleitung ("Allein"/"Partner/in"/
  "Familie"/"Freunde").
- Weitere konkrete Beispiele ergänzt (Ja/Nein-Fragen wie Reiseleitung/Lernaktivitäten/gesundheit-
  liche Einschränkungen, Verkehrsmittel-Präferenz), damit das LLM das Muster über den ganzen
  Fragekatalog hinweg konsistenter erkennt, statt nur den einen konkret gemeldeten Einzelfall zu
  reparieren.
- Die Ausschlussliste für echt offene Fragen (Name, E-Mail, Zielregion, Reisezeitraum, Budget-
  Betrag, Aktivitäteninteressen, freie Unterkunftswünsche) explizit ausformuliert, damit die
  Verschärfung nicht zu erfundenen Kategorien bei genuinely offenen Fragen führt.

Bewusst KEINE Code-/Architekturänderung (kein neues Tool, keine deterministische Verdrahtung) –
Grundprinzip 1 bleibt gewahrt: die Auswahl bleibt beim LLM, nur die Anweisung dazu ist klarer und
mit konkreten Beispielen unterlegt.

## Verifikation

Komplette Testsuite unverändert grün (335/335) – reiner Prompt-Text, keine der bestehenden Tests
prüft den genauen Wortlaut von `regelwerk.py` (nur `zerlege_schnellantworten`, unverändert).
Prompt-Text selbst ist naturgemäß nicht deterministisch testbar (Grundprinzip 1: das LLM steuert
den Dialog, kein fest vorhersagbarer Ablauf).

## Offene Punkte

- Ob die Nachschärfung tatsächlich zu konsequenterem Verhalten führt, zeigt sich erst im nächsten
  echten Chat-Test – Prompt-Verhalten lässt sich nicht automatisiert verifizieren.
