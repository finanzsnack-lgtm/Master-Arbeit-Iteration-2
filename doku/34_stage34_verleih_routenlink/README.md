# Station 34 — Verleih-Karte: "Route ansehen" von der Unterkunft

**Zeitraum:** 21.09.2026
**Kein Code-Duplikat:** Direkt umgesetzt, ohne vorher einen `code_stand`-Snapshot anzulegen (wie
bei den Stationen 24–27/30/33, transparent vermerkt statt verschwiegen).

## Auslöser

Nutzerfeedback zur in Station 30 eingeführten Verleih-Karte: der Google-Maps-Link soll bleiben,
aber zusätzlich soll darunter ein "Route ansehen"-Link erscheinen, wie ihn die Tages-POI-Karten
bereits haben – bei der Verleih-Karte immer als Weg von der Unterkunft zum Verleih.

## Umsetzung

`reiseplan.py::als_kartendaten` berechnet für die Verleih-Karte jetzt zusätzlich einen
`routen_link` über die bereits bestehende `routen_link()`-Funktion (dieselbe, die auch die
Tagesrouten-Etappen und Hin-/Rückreise nutzen): Ursprung `plan.unterkunft_koordinaten`, Ziel die
Koordinaten von `plan.lokaler_verleih_poi`, Verkehrsmittel fest `"walking"` (wie bei den anderen
lokalen, kurzen Wegen im Projekt Standard – der Verleih soll laut Fragekatalog-Hintergrund
"möglichst nah an der bereits bestätigten Unterkunft" liegen). `None`, wenn keine
Unterkunfts-Koordinaten bekannt sind, statt einen geratenen Startpunkt anzunehmen (Grundprinzip 1).

Keine Frontend-Änderung nötig: `static/index.html::karteHtml()` rendert ein vorhandenes
`routen_link`-Feld bereits generisch als "Route ansehen"-Link für JEDE Kartenart – die Verleih-Karte
bekam bisher einfach nie einen Wert dafür übergeben.

## Verifikation

Neuer Test `test_als_kartendaten_verleih_karte_zeigt_route_ab_unterkunft` (prüft Ursprung, Ziel und
`travelmode=walking` im generierten Link) sowie eine ergänzte Assertion im bestehenden
Verleih-Karten-Test (kein Link ohne bekannte Unterkunfts-Koordinaten). Komplette Suite grün
(336/336).

## Offene Punkte

- Nicht in einem echten Browser geprüft, nur über die deterministischen Reiseplan-Tests.
