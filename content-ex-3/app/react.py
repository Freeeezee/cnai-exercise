import argparse
import json
import re
import time
from types import SimpleNamespace

from agent import MAX_SCHRITTE, Ergebnis, alle_werkzeuge, fragen, werkzeug_ausfuehren, zeige_schritt
from llm import MODEL, client
from werkzeuge import Werkzeug

ACTION = re.compile(r"Action:\s*(\w+)\s*\((.*)\)", re.DOTALL)
FINAL = re.compile(r"Final Answer:\s*(.*)", re.DOTALL)

SYSTEM = """Du bist ein Campus-Assistent einer Hochschule. 
Du beantwortest Fragen von Studierenden auf Deutsch, kurz und freundlich, in höchstens drei Sätzen.
  
Du hast diese Werkzeuge:

{werkzeuge}

Antworte immer in genau einem dieser Formate:

Thought: was du als Nächstes tun möchtest
Action: werkzeug({{"param": "wert"}})

oder, wenn du die Antwort kennst:

Thought: ich kenne die Antwort
Final Answer: die Antwort.

Nach jeder Action bekommst du eine Observation mit dem Ergebnis. Erfinde keine
Observation. 
Findest du nichts, antworte: Final Answer: Dazu habe ich keine Information."""


def beschreibung(w: Werkzeug) -> str:
    return f"- {w.name}({json.dumps(w.parameter.get('properties', {}), ensure_ascii=False)}): {w.beschreibung}"


def react(aufgabe: str, werkzeuge: list[Werkzeug], max_schritte: int = MAX_SCHRITTE, bestaetigen=fragen,
          zeigen: bool = False) -> Ergebnis:
    verzeichnis = {w.name: w for w in werkzeuge}

    system = SYSTEM.format(werkzeuge="\n".join(beschreibung(w) for w in werkzeuge))

    nachrichten = [{"role": "system", "content": system}, {"role": "user", "content": aufgabe}]

    ergebnis = Ergebnis(antwort="")
    start = time.perf_counter()

    for _ in range(max_schritte):
        response = client.chat.completions.create(model=MODEL, messages=nachrichten, temperature=0,
                                                 max_tokens=500, stop=["Observation:"])
        ergebnis.modellaufrufe += 1
        ergebnis.eingabe_tokens += response.usage.prompt_tokens
        ergebnis.ausgabe_tokens += response.usage.completion_tokens

        text = response.choices[0].message.content or ""
        nachrichten.append({"role": "assistant", "content": text})

        if action := ACTION.search(text):
            aufruf = SimpleNamespace(function=SimpleNamespace(name=action[1], arguments=action[2].strip() or "{}"))
            schritt = werkzeug_ausfuehren(aufruf, verzeichnis, bestaetigen)
            ergebnis.schritte.append(schritt)

            if zeigen:
                zeige_schritt(schritt)

            nachrichten.append({"role": "user", "content": f"Observation: {schritt.ergebnis}"})

        elif final := FINAL.search(text):
            ergebnis.antwort = final[1].strip()
            ergebnis.sekunden = time.perf_counter() - start
            return ergebnis

        else:
            nachrichten.append({"role": "user", "content": "Observation: Ungültiges Format. Antworte mit "
                                                           "Action: werkzeug({...}) oder Final Answer: ..."})

    ergebnis.antwort = f"Abgebrochen nach {max_schritte} Modellaufrufen ohne Antwort."
    ergebnis.abgebrochen = True
    ergebnis.sekunden = time.perf_counter() - start
    return ergebnis


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Campus-Agent im ReAct-Format")
    parser.add_argument("aufgabe", nargs="?", default="Was gibt es heute in der Mensa?")
    args = parser.parse_args()

    e = react(args.aufgabe, alle_werkzeuge(not args.ohne_mcp), zeigen=True)
    print(f"\n{e.antwort}\n")
    print(f"  {len(e.schritte)} Werkzeugaufrufe · {e.modellaufrufe} Modellaufrufe · "
          f"{e.eingabe_tokens} Eingabe-Tokens · {e.sekunden:.1f} s · {MODEL}")
