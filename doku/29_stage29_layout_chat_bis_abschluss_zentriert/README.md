# Station 29 — Layout-Korrektur: Chat bleibt zentriert bis zum Abschluss

**Zeitraum:** 17.09.2026 (ENTSCHEIDUNGSLOG.md Phase 57)
**Mit Code-Duplikat:** Vorher-Stand von `static/index.html` in `code_stand/`.

## Auslöser

Erster echter Browser-Test von Station 28 (Layout, Konzept 1) durch den Nutzer, mit Screenshot
belegt: Das Zwei-Spalten-Layout (Chat klein links, Reiseplan-Platzhalter rechts) war von Anfang an
sichtbar, sobald das Browserfenster breit genug war – also schon WÄHREND des laufenden Gesprächs,
nicht erst nach Abschluss. Der Nutzer wollte das nicht: Während des Gesprächs soll der Chat wie
ursprünglich groß und zentriert bleiben, ohne jede Andeutung, wo/wie der Reiseplan später
erscheint. Erst NACH der letzten Antwort soll der Chat klein werden, an die Seite rücken, und der
fertige Reiseplan groß in die Mitte kommen.

## Umsetzung

Aus Station 28 war das Layout rein breitenabhängig (`@media (min-width: 980px)` griff sofort,
unabhängig vom Gesprächsstand). Jetzt zusätzlich zustandsabhängig:

- `<main>` bekommt eine neue `id="app"`. Das Zwei-Spalten-Grid in `static/index.html` greift jetzt
  NUR noch für `main.abgeschlossen` (zusätzlich zur Mindestbreite) – ohne diese Klasse bleibt es
  bei der ursprünglichen, einspaltigen, zentrierten `main`-Regel von vor Iteration 2.
  `zeigeErgebnis()` setzt diese Klasse genau in dem Moment, in dem die echte "ergebnis"-Nachricht
  vom Server ankommt – nicht früher.
  Kleinere Anpassung dabei: die Chat-Spalte ist im abgeschlossenen Zustand schmaler
  (`minmax(320px, 380px)` statt vorher `minmax(360px, 480px)`) und `#verlauf` bekommt eine
  reduzierte `max-height` (45vh), damit der Chat wirklich sichtbar kompakt wirkt, wie im
  Referenz-Screenshot.
- Der bisherige `#ergebnis-platzhalter` (Platzhaltertext + der davon abhängige
  `zeigePlanungsStatus`-Mechanismus aus Station 28) wurde entfernt. Das Status-Signal
  "Reiseroute wird berechnet ..." erscheint jetzt als eigene Sprechblase IM CHAT (mit Avatar,
  ersetzt die generische Tipp-Animation für diesen Moment), statt den bis dahin unsichtbaren
  Reiseplan-Bereich vorzeitig aufzudecken.

## Verifikation

JS-Syntax mit Node.js geprüft (`new Function(...)` über den `<script>`-Inhalt, keine
Laufzeitprüfung im Browser). Komplette Python-Testsuite weiterhin grün (325/325, unverändert –
diese Korrektur betrifft ausschließlich `static/index.html`, keine Python-Logik). Noch NICHT in
einem echten Browser gegen den tatsächlichen Chat-Ablauf verifiziert (offener Punkt, wie schon in
Station 28 vermerkt).

## Offene Punkte

- Echter Browser-Test des korrigierten Übergangs (Chat groß → Ergebnis-Nachricht → Layoutwechsel)
  steht noch aus.
- Die schmalere Chat-Spalte/reduzierte `max-height` im abgeschlossenen Zustand sind eine erste
  Annäherung an den vom Nutzer gezeigten Screenshot, nicht pixelgenau abgeglichen.
