# Station 30 — Sechs Nutzerrückmeldungen: Zeitanzeige, Fotos, Standardbilder, Verleih-Karte, Layout, Avatar

**Zeitraum:** 17.09.2026 (ENTSCHEIDUNGSLOG.md Phase 58)
**Mit Code-Duplikat:** Vorher-Stand in `code_stand/`.

## Auslöser

Direktes Nutzerfeedback nach Nutzung der Web-UI, sechs Punkte. Auf ausdrücklichen Wunsch erst in
klare Aufgaben gefasst und per Rückfrage bestätigt (vier echte Entscheidungsfragen), bevor
irgendetwas umgesetzt wurde.

## 1. Zeitanzeige — Ankerwort statt Uhrzeit, für alle Tage ohne bekannte Zeit

**Fund/Verlauf:** Phase 56 hatte für Tag 1/Tage ohne F20-Antwort eine "ca. HH:MM Uhr"-Anzeige
eingeführt (angenommener Standard-Tagesbeginn). Der Nutzer wollte das nicht: "nicht eine Uhrzeit
hinterschreiben, sondern einfach nach Ankunft oder sowas" — und zwar für ALLE Tage ohne bekannte
Zeit, nicht nur Tag 1 (Rückfrage-Entscheidung).

**Umsetzung:** `_zeitpunkt_text` (`src/ausgabe/reiseplan.py`) baut jetzt eine relative Dauer MIT
Ankerwort direkt am Wert: `f"{dauer} nach {anker}"` (Anker = "Ankunft" an Tag 1, "Tagesbeginn" ab
Tag 2 ohne F20-Antwort), z.B. "15min nach Ankunft" statt "ca. 09:15 Uhr" oder der alten, zweimal
missverständlichen nackten Dauer "ab 1h". `_uhrzeit_hinweis_text` erklärt das einmalig.
`EINSTELLUNGEN.standard_tagesstart_minuten`/`STANDARD_TAGESSTART_MINUTEN` (Phase 56) wurde entfernt,
da jetzt ungenutzt.

**Warum kein Rückfall in den alten Fehler:** Die Ankerwort-Variante unterscheidet sich von der
ursprünglichen, in Phase 56 verworfenen Fassung dadurch, dass JEDER einzelne Zeitwert das Wort
"nach Ankunft"/"nach Tagesbeginn" direkt trägt – die alte Fassung hatte nur EIN "nach"/"bis" als
Satzanfang, der beim isolierten Lesen eines einzelnen Werts verloren ging.

## 2. Fotos — echter Bug behoben, plus Nachlade-Fallback

**Fund:** `src/ausgabe/fotos.py::lade_fotos_fuer_plan` lud bis Stage 29 NUR Fotos für Unterkunft +
tatsächlich eingeplante Tagesrouten-POIs herunter. Alle "Vorschlag"-Karten (Markt-/Café-Beispiele,
Beispielrestaurants, Sondertage-/Touren-/Lernaktivitäts-Beispiele, generische Beispiele an leeren
Tagen) und "Weitere Empfehlungen" blieben dadurch IMMER ohne Foto — unabhängig davon, ob Google
eins geliefert hätte. Der vom Nutzer beobachtete Fischmarkt-Brügge-Fall war mit hoher
Wahrscheinlichkeit genau so eine Vorschlag-Karte.

**Umsetzung:** `lade_fotos_fuer_plan` deckt jetzt ALLE POI-Kategorien ab, die `als_kartendaten`
(reiseplan.py) als eigene Karte zeigt (`weitere_aktivitaeten_empfehlungen`, `beispielrestaurants`,
`tour_tag_beispiele`, `lernaktivitaet_tag_beispiele`, `markt_beispiele`), plus den neuen
`lokaler_verleih_poi` (siehe Punkt 4). Zusätzlich ein Nachlade-Fallback: fehlt `foto_referenz` bei
einem POI (die ursprüngliche Nearby-/Text-Search-Antwort hatte kein `photos`-Feld), versucht
`GoogleMapsClient.hole_foto_referenz` (neue Methode, `place/details/json` mit `fields=photos`) einen
zweiten, gezielten Abruf. Bewusst NUR für die kleine, bereits feststehende Menge an Karten im
FERTIGEN Reiseplan (Performance-Hinweis, CLAUDE.md), nicht für jeden rohen Suchtreffer — analog zu
`ist_barrierefrei`.

## 3. Standardbilder für Bahn/Auto/Fernbus

Hin-/Rückreise-Karten hatten `foto_url` fest auf `None` gesetzt (kein einzelner "Ort" mit Foto).
Drei neue, selbst gestaltete SVG-Icons (`static/img/bahn.svg`/`auto.svg`/`bus.svg`, schlichtes
Flat-Design in der Akzentfarbe der App, lizenzfrei) werden über die neue Funktion
`reiseplan.py::_standardbild_url` per Teilstring-Suche im Verkehrsmittel-Text zugeordnet ("bahn"/
"zug" → Bahn-Icon, "auto"/"pkw" → Auto-Icon, "bus"/"fernbus" → Bus-Icon). Ein unbekanntes/neues
Verkehrsmittel bekommt bewusst kein erzwungenes Icon (`None`), um kein irreführendes Bild zu zeigen.

**Entscheidung bei Rückfrage:** selbst gestaltete Grafik statt Nutzer-gelieferter Bilddateien.

## 4. Verleih als eigene Karte

`als_kartendaten` liefert jetzt ein neues `"verleih"`-Feld: eine POI-Karte (Name, Foto, Google-Maps-
Link) für `plan.lokaler_verleih_poi`, mit `kategorie` überschrieben zu "Verleih: <Fahrzeug>"
(`plan.lokales_leihfahrzeug_gewuenscht`). `None`, wenn kein Verleih gewünscht oder trotz Wunsch
keiner gefunden wurde — die ehrliche Fehlanzeige bleibt weiterhin NUR als Text erhalten
(`_verleih_hinweis_text`), keine "nicht gefunden"-Karte, analog zu `unterkunft`. Kein
"Vorschlag"-Label, da ein im Dialog bereits bestätigter, konkreter Fund. In `static/index.html`
direkt unter der Unterkunfts-Karte gerendert (`#verleih-bereich`).

**Entscheidung bei Rückfrage:** Position ganz oben unter der Unterkunft (statt unter der Hinreise).

## 5. Layout weiter zentrieren

Nach dem ersten Blick auf den in Stage 29 umgesetzten Zustand: der kleine Chat saß oben am Rand
(`position: sticky; top: 24px`), wirkte "in die Ecke gedrängt". Jetzt: vertikal MITTIG im
sichtbaren Bereich (`position: sticky; top: 50%; transform: translateY(-50%)` — bleibt beim
Scrollen durch einen langen Reiseplan weiterhin sichtbar, aber zentriert statt oben klebend),
schmalere Spalte (`minmax(260px, 320px)` statt `minmax(320px, 380px)`), deutlich mehr Abstand zum
Reiseplan (`column-gap: 56px` statt `24px`) und mehr Innenpolster links/rechts (`padding: 24px
48px`), damit der Reiseplan als der optisch dominante, zentrale Bereich wirkt.

## 6. Avatar

Zwei Schritte, beide noch am selben Tag:

1. Kompass-Emoji (🧭) durch ein Gesichts-Emoji (😊) ersetzt — wirkte laut Nutzer zu abstrakt/nach
   Reise-Symbol statt erkennbar nach "hier spricht eine Person", passend zur "warmherziger
   Reiseberater"-Tonalität aus `chat.py`.
2. Direktes Folge-Feedback (Nutzer schickte ein Beispielbild eines Chatbot-Charakters als
   Stilvorlage): das Emoji durch einen EIGENEN, komplett neu gezeichneten kleinen Bot-Charakter mit
   Kopf UND angedeutetem Oberkörper ersetzt (`static/img/avatar.svg`, eigenes Original – nur die
   Grundidee des Beispielbilds aufgegriffen, kein Nachbau, damit keine Urheberrechtsfrage entsteht).
   `erzeugeAvatar()` erzeugt jetzt ein `<img>` statt eines Text-Emojis; die vorherige
   Kreis-Hintergrundfarbe der `.avatar`-Regel entfällt, da die Grafik ihre Form/Farbe selbst
   mitbringt.

**Kein Code-Duplikat für Schritt 2:** Diese Anpassung wurde direkt umgesetzt, ohne vorher einen
`code_stand`-Snapshot von `static/index.html` anzulegen (wie bei den Stationen 24–27, siehe
`doku/README.md` – transparent vermerkt statt verschwiegen).

**Direkte Feinjustierung danach:** Kopf und Schultern-Ellipse hatten sichtbaren Abstand
zueinander. Erster Versuch (Ellipse `cy`/`ry` verschoben, sodass ihre Oberkante die Kopf-Unterkante
berührt) reichte nicht – beim tatsächlichen Rendern blieb eine sichtbare Naht/Kerbe an der
Übergangsstelle, weil sich Rechteck (Kopf) und Ellipse (Schultern) nur an einem einzelnen Punkt in
der Mitte berührten, an den Seiten aber weiterhin auseinanderklafften (Kopf-Eckenrundung und
Ellipsen-Rand liefen dort in unterschiedliche Richtungen auseinander). Behoben durch EINE einzige,
durchgehende Pfad-Silhouette (Kopf + Oberkörper als ein Pfad mit sanfter Taillierung dazwischen)
statt zweier separat positionierter Formen – dadurch keine Naht mehr möglich, unabhängig von der
exakten Positionierung. Per Headless-Browser-Screenshot (`msedge --headless --screenshot`) vor der
Rückmeldung an den Nutzer visuell verifiziert, nicht nur anhand der Koordinaten angenommen.

## Verifikation

Komplette Python-Testsuite grün (335/335, vorher 325). Neue/angepasste Tests in
`tests/test_reiseplan.py` (Zeitanzeige, Standardbilder, Verleih-Karte), `tests/test_fotos.py`
(erweiterter Scope, Nachlade-Fallback), `tests/test_google_maps.py` (`hole_foto_referenz`).
JS-Syntax von `static/index.html` mit Node.js geprüft (`new Function(...)` über den
`<script>`-Inhalt).

## Offene Punkte

- Layout-Feinschliff (5) ist eine erste Annäherung an eine mündlich beschriebene Vorstellung, nicht
  pixelgenau abgestimmt — nächster sinnvoller Schritt ist wieder Screenshot-Feedback wie bei
  Station 29.
- Der Foto-Nachlade-Fallback (2) wurde NICHT gegen die echte Google-API verifiziert (kein Live-Key
  in dieser Sitzung), nur die Anfragestruktur (URL, Parameter, Antwort-Parsing) getestet. Ob er in
  der Praxis tatsächlich mehr Fotos findet, zeigt erst ein echter Testlauf mit `MOCK_MODE=false`.
- Die drei SVG-Icons sind ein erster, bewusst schlichter Entwurf — falls gewünscht, später gegen
  eigene Grafiken austauschbar (gleicher Dateiname, gleicher Ort).
