"""Tests für die IOKanal-Implementierungen (src/audio/kanal.py) – nur die reinen, ohne echtes
Mikrofon/Konsole testbaren Teile: `TextKanal`/`AudioKanal.zeige_karte` sind No-Ops (Fotos lassen
sich in der Konsole ohnehin nicht darstellen, siehe Moduldoku)."""
import asyncio

from src.api.typen import Unterkunft
from src.audio.kanal import TextKanal, zerlege_schnellantworten


def test_textkanal_zeige_karte_ist_no_op_und_wirft_nicht():
    kanal = TextKanal()
    unterkunft = Unterkunft(id=1, name="Hotel Zentral", x=0.0, y=0.0, preisniveau=2, zertifiziert_nachhaltig=False)
    asyncio.run(kanal.zeige_karte(unterkunft))  # darf nicht werfen


def test_textkanal_zeige_status_ist_no_op_und_wirft_nicht():
    asyncio.run(TextKanal().zeige_status("plant_reise"))  # darf nicht werfen, kein Ausgabe-Zwang


# Iteration 2 (Betreuer-Feedback: Quick Replies, siehe
# doku/28_stage28_iteration2_ux_feedback_konzepte/README.md): `zerlege_schnellantworten` trennt die
# vom LLM optional angehängte "[SCHNELLANTWORTEN: ...]"-Zeile vom eigentlichen Nachrichtentext.

def test_zerlege_schnellantworten_ohne_marker_liefert_text_unveraendert():
    text, optionen = zerlege_schnellantworten("Wie ist Ihr Name?")
    assert text == "Wie ist Ihr Name?"
    assert optionen is None


def test_zerlege_schnellantworten_trennt_marker_und_optionen():
    text, optionen = zerlege_schnellantworten(
        "Möchten Sie ein Auto mieten?\n[SCHNELLANTWORTEN: Ja | Nein]"
    )
    assert text == "Möchten Sie ein Auto mieten?"
    assert optionen == ["Ja", "Nein"]


def test_zerlege_schnellantworten_kappt_bei_vier_optionen():
    text, optionen = zerlege_schnellantworten(
        "Welches Verkehrsmittel?\n[SCHNELLANTWORTEN: Bahn | Auto | Fahrrad | Bus | Fernbus]"
    )
    assert text == "Welches Verkehrsmittel?"
    assert optionen == ["Bahn", "Auto", "Fahrrad", "Bus"]


def test_zerlege_schnellantworten_leere_klammer_liefert_keine_optionen():
    text, optionen = zerlege_schnellantworten("Alles klar?\n[SCHNELLANTWORTEN: ]")
    assert text == "Alles klar?"
    assert optionen is None
