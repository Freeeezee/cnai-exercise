import argparse
import re
import time

import rag
from wissen import Treffer, antworten, dokumente, zeigen

# regex für typische raumkennungen in der frage.
KENNUNG = re.compile(r"\b[A-Za-z]{1,3}-\d+\b")
# regex für typische paragraphschreibweisen in der frage.
PARAGRAPH = re.compile(r"(?:§|paragraph)\s*(\d+)", re.IGNORECASE)


def kennungen(frage: str) -> list[re.Pattern]:
    pattern = [re.compile(rf"\b{re.escape(k.upper())}(?!\d)") for k in KENNUNG.findall(frage)] # regex für raumsuche in dateien
    pattern += [re.compile(rf"§\s*{n}(?!\d)") for n in PARAGRAPH.findall(frage)] # regex für paragraphensuche in dateien
    return pattern


def textsuche(muster: list[re.Pattern]) -> list[Treffer]:
    if not muster:
        return []

    abschnitte = []
    for datei, text in dokumente().items():
        for abschnitt in rag.zerlege(datei, text):
            abschnitte.append(abschnitt)

    return [
        Treffer(a.datei, a.text, 1.0)
        for a in abschnitte
        if any(m.search(a.text) for m in muster)
    ]


def abrufen(frage: str, k: int = rag.K) -> tuple[list[Treffer], float]:
    start = time.perf_counter()

    exakt = textsuche(kennungen(frage))
    exakt_resultat = {t.text for t in exakt}
    rest = [t for t in rag.suche(frage, k) if t.text not in exakt_resultat]

    return (exakt + rest)[:k], time.perf_counter() - start


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("frage", nargs="+")
    parser.add_argument("-k", type=int, default=rag.K, help="Zahl der Abschnitte")

    args = parser.parse_args()
    frage = " ".join(args.frage)

    print(f"Kennungen: {[m.pattern for m in kennungen(frage)]}")

    treffer, sekunden = abrufen(frage, args.k)

    for t in treffer:
        erste_zeile = t.text.splitlines()[1] if "\n" in t.text else t.text
        print(f"  {t.wert:.3f}  {t.datei:<26} {erste_zeile[:50]}")

    print()

    zeigen(antworten(frage, treffer, sekunden))
