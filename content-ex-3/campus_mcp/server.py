"""Campus-Werkzeuge als MCP-Server.

Dieser Server läuft als eigener Container und bietet seine Werkzeuge über
das Model Context Protocol (MCP) an. Jeder MCP-Client kann sie nutzen:
unser Agent, aber genauso Claude Desktop, Cursor oder der MCP Inspector.

Transport: Streamable HTTP unter http://<host>:8000/mcp

Die Daten sind ausgedacht und liegen in belegung.json und speiseplan.json.
Buchungen landen nur im Arbeitsspeicher und sind nach einem Neustart weg.
"""

import json
import os
import re
from datetime import date, timedelta
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

HIER = Path(__file__).parent
BELEGUNG = json.loads((HIER / "belegung.json").read_text(encoding="utf-8"))
SPEISEPLAN = json.loads((HIER / "speiseplan.json").read_text(encoding="utf-8"))

# Zeitfenster, in denen Seminarräume belegt oder gebucht werden können
SLOTS = ["08:00", "09:45", "11:30", "14:00", "15:45", "17:30"]
WOCHENTAGE = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]

DATUM_FEHLER = ("Fehler: '{}' ist kein gültiges Datum. Erlaubt sind JJJJ-MM-TT, "
                "'heute', 'morgen', 'übermorgen' oder ein Wochentag wie 'montag'.")

# Buchungen von Studierenden: {(raum, datum, slot): name}
buchungen: dict[tuple[str, str, str], str] = {}

mcp = FastMCP("campus", host="0.0.0.0", port=8000)


def _wochentag(datum: str) -> str:
    return WOCHENTAGE[date.fromisoformat(datum).weekday()]


def _datum_lesen(datum: str) -> str:
    """Wandelt das Datum, das das Modell schickt in ein ISO-Datum um."""
    text = datum.strip().lower()

    iso = re.match(r"\d{4}-\d{2}-\d{2}", text)
    if iso:
        return date.fromisoformat(iso.group()).isoformat()

    woerter = re.findall(r"[a-zäöüß]+", text)
    if woerter and woerter[0] == "am":
        woerter = woerter[1:]

    wort = woerter[0] if woerter else ""
    heute = date.fromisoformat(os.environ["HEUTE"]) if os.environ.get("HEUTE") else date.today()
    relativ_zu_heute = {"heute": 0, "morgen": 1}

    if wort in relativ_zu_heute:
        return (heute + timedelta(days=relativ_zu_heute[wort])).isoformat()

    if wort in WOCHENTAGE:
        tage = (WOCHENTAGE.index(wort) - heute.weekday()) % 7
        return (heute + timedelta(days=tage)).isoformat()

    raise ValueError(datum)


def _belegt(raum: str, datum: str) -> dict[str, str]:
    """Alle belegten Slots eines Raums an einem Datum, mit Grund."""
    plan = BELEGUNG["raeume"].get(raum, {})
    belegt = dict(plan.get(_wochentag(datum), {}))
    for (r, d, slot), name in buchungen.items():
        if r == raum and d == datum:
            belegt[slot] = f"gebucht von {name}"
    return belegt


@mcp.tool()
def raeume_auflisten() -> str:
    """Listet alle Seminarräume, die Studierende zum Lernen buchen können,
    mit Gebäude und Zahl der Plätze."""
    zeilen = [f"{r}: {info['plaetze']} Plätze, {info['ausstattung']}"
              for r, info in BELEGUNG["raeume"].items()]
    return "\n".join(zeilen)


@mcp.tool()
def raum_frei(raum: str, datum: str) -> str:
    """Zeigt, in welchen Zeitfenstern ein Seminarraum an einem Tag frei ist.

    raum: Raumnummer wie O-108 (Gebäude, Bindestrich, Nummer)
    datum: Datum im Format JJJJ-MM-TT, zum Beispiel 2026-11-05. Erlaubt sind auch
           'heute', 'morgen' oder ein Wochentag wie 'montag'.
    """
    raum = raum.strip().upper()
    if raum not in BELEGUNG["raeume"]:
        return f"Fehler: Raum {raum} gibt es nicht oder er ist nicht buchbar. Nutze raeume_auflisten."
    try:
        datum = _datum_lesen(datum)
    except ValueError:
        return DATUM_FEHLER.format(datum)
    tag = _wochentag(datum)
    if tag in ("samstag", "sonntag"):
        return f"{raum} ist am {tag} geschlossen."
    belegt = _belegt(raum, datum)
    frei = [s for s in SLOTS if s not in belegt]
    return (f"{raum} am {datum} ({tag}): frei um {', '.join(frei) or 'keinem Slot'}. "
            f"Belegt: {', '.join(f'{s} ({g})' for s, g in sorted(belegt.items())) or 'nichts'}.")


# Schreibt ein Werkzeug raum_buchen(raum, datum, uhrzeit, name), das einen
# freien Slot für eine Person bucht und in `buchungen` einträgt.
#  - Prüft wie raum_frei, ob Raum und Datum gültig sind.
#  - uhrzeit muss einer der SLOTS sein, sonst Fehlermeldung mit den gültigen Slots.
#  - Ist der Slot belegt, gebt eine Fehlermeldung zurück, die sagt, was frei ist.
#  - Sonst eintragen und eine Bestätigung zurückgeben.
# Fehler gebt ihr als Text zurück, der mit "Fehler:" beginnt, statt eine
# Exception zu werfen. Das Modell liest den Text und kann sich korrigieren.
# Der Docstring ist die Beschreibung, die das Modell sieht. Schreibt ihn sorgfältig.

@mcp.tool()
def raum_buchen(raum: str, datum: str, uhrzeit: str, name: str):
    """Bucht einen freien Slot in einem Raum für eine Person.

    raum: Raumnummer wie O-108 (Gebäude, Bindestrich, Nummer)
    datum: Datum im Format JJJJ-MM-TT, zum Beispiel 2026-11-05. Erlaubt sind auch
           'heute', 'morgen' oder ein Wochentag wie 'montag'.
    uhrzeit: Uhrzeit des Slots, einer von ['08:00', '09:45', '11:30', '14:00', '15:45', '17:30']
    name: Name der Person, die den Raum bucht

    Gibt eine Bestätigung zurück oder eine Fehlermeldung, die mit "Fehler:" beginnt.
    """
    raum = raum.strip().upper()
    if raum not in BELEGUNG["raeume"]:
        return f"Fehler: Raum {raum} gibt es nicht oder er ist nicht buchbar. Nutze raeume_auflisten."

    try:
        datum = _datum_lesen(datum)
    except ValueError:
        return DATUM_FEHLER.format(datum)
    tag = _wochentag(datum)

    if tag in ("samstag", "sonntag"):
        return f"Fehler: {raum} ist am {tag} geschlossen."

    if uhrzeit not in SLOTS:
        return f"Fehler: '{uhrzeit}' ist keine gültige Uhrzeit. Gültige Slots sind: {', '.join(SLOTS)}."

    belegt = _belegt(raum, datum)

    if uhrzeit in belegt:
        frei = [s for s in SLOTS if s not in belegt]
        return (f"Fehler: {raum} ist am {datum} um {uhrzeit} belegt ({belegt[uhrzeit]}). "
                f"Frei sind nur: {', '.join(frei) or 'keine Slots'}.")

    buchungen[(raum, datum, uhrzeit)] = name

    return f"{raum} wurde am {datum} um {uhrzeit} erfolgreich für {name} gebucht."


@mcp.tool()
def mensa_speiseplan(datum: str) -> str:
    """Speiseplan der Mensa (Gebäude M) für einen Tag, mit Preisen für Studierende.

    datum: Datum im Format JJJJ-MM-TT, zum Beispiel 2026-11-05. Erlaubt sind auch
           'heute', 'morgen' oder ein Wochentag wie 'montag'.
    """
    try:
        datum = _datum_lesen(datum)
    except ValueError:
        return DATUM_FEHLER.format(datum)
    tag = _wochentag(datum)
    gerichte = SPEISEPLAN.get(tag)
    if not gerichte:
        return f"Am {tag} ({datum}) hat die Mensa geschlossen."
    return f"Mensa am {tag}, {datum}:\n" + "\n".join(f"- {g}" for g in gerichte)


@mcp.custom_route("/zuruecksetzen", methods=["POST"])
async def zuruecksetzen(request: Request) -> PlainTextResponse:
    """Kein Werkzeug, nur für messen.py: alle Buchungen löschen,
    damit jede Messung mit derselben Raumbelegung startet."""
    buchungen.clear()
    return PlainTextResponse("ok")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
