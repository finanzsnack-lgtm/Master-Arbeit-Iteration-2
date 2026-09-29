# Station 33 — Chat-Verlauf: horizontales Scrollen behoben

**Zeitraum:** 21.09.2026
**Kein Code-Duplikat:** Direkt umgesetzt, ohne vorher einen `code_stand`-Snapshot von
`static/index.html` anzulegen (wie bei den Stationen 24–27/30, transparent vermerkt statt
verschwiegen).

## Auslöser

Screenshot des Nutzers: im Chatverlauf war trotz bereits schmal umgebrochenem Text zusätzlich ein
horizontaler Scrollbalken sichtbar. Anforderung: der Chat soll in der Breite IMMER vollständig
passen, vertikales Scrollen ist ausdrücklich in Ordnung.

## Fund

Drei zusammenwirkende Ursachen, nicht nur eine:

1. **Hauptursache:** `#verlauf` setzte nur `overflow-y: auto`, nie `overflow-x`. Nach CSS-
   Spezifikation wird eine Achse, die auf "visible" steht, automatisch auf "auto" hochgestuft,
   sobald die ANDERE Achse einen Wert ungleich "visible" bekommt – dadurch war `overflow-x`
   effektiv ebenfalls `auto`, nicht `hidden`/`visible` wie beabsichtigt. Erklärt den Scrollbalken
   unabhängig davon, wie schmal der Text bereits umbrach.
2. `.nachricht` hatte kein `overflow-wrap`/`word-break` – ein einzelnes langes, leerzeichenloses
   Wort oder ein langer Link in einer Bot-Antwort hätte die Sprechblase in die Breite gedrückt statt
   umzubrechen.
3. `.hotel-karte-wrapper` hatte eine feste Breite (`width: 220px`) – im schmalen Chat des
   Abschluss-Zustands (`main.abgeschlossen`, Spalte ab 260px minus Innenabstand) reichte der
   verfügbare Platz teils nicht mehr aus.

## Umsetzung

- `#verlauf`: explizit `overflow-x: hidden` ergänzt (behebt Ursache 1, vertikales Scrollen bleibt
  über `overflow-y: auto` unverändert erhalten).
- `.nachricht`: `overflow-wrap: break-word; word-break: break-word;` ergänzt (behebt Ursache 2).
- `.nachricht-zeile`: `min-width: 0` ergänzt (Flex-Kinder schrumpfen sonst nie unter ihre eigene
  Inhaltsbreite – zusätzliche Absicherung, nicht die Hauptursache).
- `.hotel-karte-wrapper`: `width: 220px` auf `width: 100%` (mit weiterhin `max-width: 220px`)
  geändert – schrumpft jetzt mit, statt Overflow zu erzwingen (behebt Ursache 3).

## Verifikation

Eigene Testseite mit Original-CSS aus `static/index.html`, einer Chat-Nachricht mit einem extrem
langen, leerzeichenlosen Testwort UND einem langen Link, im schmalen `main.abgeschlossen`-Layout,
per Headless-Browser (`msedge --headless --screenshot`) gerendert: nur noch ein vertikaler
Scrollbalken sichtbar, kein horizontaler mehr. Komplette Python-Testsuite unverändert grün
(335/335, reine CSS-Änderung). JS-Syntax mit Node.js geprüft.

## Offene Punkte

- Nicht in einem echten Browser mit echten, langen LLM-Antworten (statt einer synthetischen
  Testnachricht) geprüft.
