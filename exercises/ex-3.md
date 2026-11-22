# Exercise 3

## 1

### 1-1, 1-2

#### *Was gibt es heute in der Mensa?*

```
  → mensa_speiseplan(datum='heute')  [wert]
  ← Fehler: 'heute' ist kein Datum im Format JJJJ-MM-TT.

Entschuldigung! Ich habe keine Informationen über das spezifische Datum "heute". Dazu habe ich keine Information.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 940 Eingabe-Tokens · 47.2 s · llama3.2:3b
```

→ Versucht den Mensa-Speiseplan mit 'heute' aufzurufen, was nicht klappt weil das kein Datum ist. Das Modell müsste vorher mit dem `heute` Tool das aktuelle Datum bestimmen. Die Antwort ist also falsch, da es die Information theoretisch hat.

**Fehlermodus:** Falsche Werte, Falsche Reflexion

#### *Ich bin am Tag meiner Klausur krank. Was muss ich tun?*

```
	→ suche_wissen(begriff='Klausur')
  ← pruefungsordnung.md (1 Treffer): § 9 Prüfungsformen. Prüfungen sind Klausuren, mündliche Prüfungen,

Wenn du am Tag deiner Klausur krank bist, solltest du dich von deinem Arzt beraten lassen und eine ärztliche Attestation erhalten. Dann kannst du dich bei der Hochschule um eine Verschiebung oder eine Aussetzung deiner Klausur bitten.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 969 Eingabe-Tokens · 11.5 s · llama3.2:3b
```

→ Sucht nach dem Eintrag zu Klausuren im Wissensbereich und gibt darauf basierend die richtige Antwort.

#### *Ist O-108 am Donnerstag um 14 Uhr frei?*

```
  → raum_frei(raum='O-108', datum='2026-11-04')
  ← O-108 am 2026-11-04 (mittwoch): frei um 08:00, 09:45, 11:30, 15:45, 17:30. Belegt: 14:00 (Datenbanken).

O-108 ist am Donnerstag um 14 Uhr nicht frei.

  1 Werkzeugaufrufe · 2 Modellaufrufe · 998 Eingabe-Tokens · 9.9 s · llama3.2:3b
```

→ Inkorrekt. Das Modell sucht zwar nach dem richtigen Raum um die Richtige Uhrzeit, und wertet das Ergebnis auch korrekt aus, das gewählte Datum ist allerdings weder ein Donnerstag, noch der Kommende.

**Fehlermodus:** Falsche Werte, Ziel verfehlt

### 1-3

```
Modell: llama3.2:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               3/13    9/13          0       4        0        1.1       1.9       968    10.8s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    1/4         1/1         1/4         0/1         0/1         0/1         0/1
```

### 1-4

Weil bei jedem Schritt die gesamte Historie mitgesendet wird, auch die neuesten Werkzeugaufrufe.

### 1-5

Die Anfrage wird abgebrochen. Ein Limit ist trotzdem notwendig, da das LLM sich sonst für unbestimmte Zeit im Kreis drehen kann, was sowohl für den Nutzer eine schlechte Erfahrung bildet als auch immense Kosten mit sich ziehen kann.

## 2

### 2-1

```
  → tage_bis(datum='heute')  [wert]
  ← Fehler: 'heute' ist kein gültiges Datum im Format JJJJ-MM-TT.
```

Er scheitert bereits am ersten Aufruf, möchte aus irgendwelchen Gründen die Tage bis heute wissen.

### 2-3

#### 2-3-1

```
  ? Soll ich raum_buchen(datum='2026-11-05', uhrzeit='09:45', name='Kim', raum='O-108') ausführen? [j/N] N
  → raum_buchen(datum='2026-11-05', uhrzeit='09:45', name='Kim', raum='O-108')  [abgelehnt]
  ← Abgelehnt.

Dazu habe ich keine Information.
```

→ Bricht ab. Die Nachricht ist etwas unscharf, aber das Verhalten ist korrekt.

```
  ? Soll ich raum_buchen(datum='2026-11-05', uhrzeit='09:45', name='Kim', raum='O-108') ausführen? [j/N] j
  → raum_buchen(datum='2026-11-05', uhrzeit='09:45', name='Kim', raum='O-108')  [wert]
  ← Fehler: O-108 ist am 2026-11-05 um 09:45 belegt (Webapplikationen). Frei sind nur: 11:30, 15:45, 17:30.

Entschuldigung, ich habe keine Informationen über die Verfügbarkeit des Raumes O-108 am Freitag um 9:45 Uhr.
```

#### 2-3-2

Es ist ein simpler check ob der Name des Tools mit einem bestimmten Wort beginnt. Da diese Liste vom Konsumenten des MCP verwaltet wird, und damit unter normalen Umständen nicht vom Ersteller des MCP, könnte es hier schnell passieren, dass der MCP Tools anbietet, die zwar destruktiv sind, vom Agent aber nicht als solche erkannt werden, und daher auch keine Anfrage provozieren. MCP Tool Annotations wären ein Weg, wie MCPs direkt in ihren Tool Definitionen angeben können, wie destruktiv die Tools sind, bzw. welche anderen Side-Effects auftreten können. Der Agent muss dann natürlich trotzdem entscheiden, wie er damit umgeht, allerdings sind die möglichen Werte hier standartisiert und werden sich nicht einfach so ändern.

## 3

### 3-1

Ohne MCP Fehlertoleranz:
```
Modell: llama3.2:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               2/13    9/13          0       5        0        0.8       1.8      1220    10.2s
agent.v2.yaml               4/13    9/13          0       1        0        1.0       1.9      1723    14.2s
workflow                    5/13    7/13          0       3        0        0.7       2.0       447     7.0s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    1/4         1/1         0/4         0/1         0/1         0/1         0/1
agent.v2.yaml                    2/4         1/1         0/4         0/1         1/1         0/1         0/1
workflow                         2/4         0/1         1/4         0/1         0/1         1/1         1/1
```

```
Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               5/13    8/13          0       0        0        0.6       1.6      1647     3.4s
agent.v2.yaml               4/13    8/13          0       1        0        0.5       1.5      1949     3.8s
workflow                    3/13    8/13          0       0        0        0.8       2.0       436     3.1s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    2/4         1/1         0/4         0/1         1/1         0/1         1/1
agent.v2.yaml                    2/4         1/1         0/4         0/1         0/1         0/1         1/1
workflow                         1/4         1/1         0/4         0/1         0/1         0/1         1/1
```

Mit MCP Fehlertoleranz:

```
Modell: llama3.2:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               2/13    9/13          0       4        0        0.8       1.8      1310    19.9s
agent.v2.yaml               2/13    8/13          0       1        0        0.9       1.9      1804    23.8s
workflow                    6/13    7/13          0       1        0        0.7       2.0       452     6.3s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    1/4         1/1         0/4         0/1         0/1         0/1         0/1
agent.v2.yaml                    1/4         1/1         0/4         0/1         0/1         0/1         0/1
workflow                         3/4         0/1         1/4         0/1         0/1         1/1         1/1
```

```
Modell: qwen2.5:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               6/13    8/13          0       1        0        0.8       1.8      1958     5.2s
agent.v2.yaml               5/13    8/13          0       0        0        0.5       1.5      2066     4.2s
workflow                    3/13    8/13          0       0        0        0.8       2.0       436     3.5s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    3/4         1/1         0/4         0/1         1/1         0/1         1/1
agent.v2.yaml                    2/4         1/1         0/4         0/1         1/1         0/1         1/1
workflow                         1/4         1/1         0/4         0/1         0/1         0/1         1/1
```

**Erkenntnisse:**

- Verbesserungen beim Prompt scheinen die Fehler bei `llama3.2:3b` etwas auszugleichen, allerdings reicht bereits der längere Docstring in dem MCP mit Fehlertoleranz aus, um die Vorteile wieder zu verlieren. `qwen2.5:3b` hingegen schaden Sie eher.
- MCP Fehlertoleranz erzielt bei `llama3.2:3b` nur eine leichte Verbesserung bei der Workflow Lösung, `qwen2.5:3b` profitiert bei beiden Agent Prompts. 
- Der Workflow kann gut sagen, wenn ihm das Wissen fehlt, und beantwortet Fragen, die im Vorhinein erwartet wurden, und einen klaren Ablauf haben am besten. Das kann aber auch dazu führen, dass Fragen, auf die er eine Antwort hat, die allerdings keinen weiteren Kontext benötigt (wie zb. "Wie viel ist 17 mal 23?") abgelehnt werden, da die Information über den Mangel an Kontext überwiegt. Außerdem können Nuancen verloren gehen, da durch die strikte Kategorisierung am Anfang falsche Tool-Aufrufe gemacht werden, obwohl das Modell alles richtig eingeschätzt hat ("Hat die Mensa am Samstag offen?" → ruft `mensa_speiseplan` auf, da es als `mensa` kategorisiert wurde, obwohl die Antwort da nicht zu finden ist).
- Insgesamt scheint `llama3.2:3b` aber vom strikten Workflow zu profitieren, `qwen2.5:3b` schadet er eher.

## 4

### 4-1

#### 4-1-1

Zuerst kommt der System prompt mit der Rolle `system`, dann der User mit `user`. Tool calls und Antwortenhaben die Rolle `assistant` und die Antworten der Tools die Rolle `tool`. Der System Prompt steht nur am Anfang, ab dann folgt die Konveration dem Schema `user` → beliebige Anzahl `assistant` tool calls, die mit `tool` beantwortet werden → `assistant` antwort → `user`.

Tools werden immer mit einer ID aufgerufen, die auch in der Tool Antwort steht. Damit können Sie zueinander zugeordnet werden.

#### 4-1-2

```
  ? Soll ich raum_buchen(raum='O-108', datum='2026-11-05', uhrzeit='09:45', name='Studierender') ausführen? [j/N] N
  → raum_buchen(raum='O-108', datum='2026-11-05', uhrzeit='09:45', name='Studierender')  [abgelehnt]
  ← Abgelehnt.

Dazu habe ich keine Information.
```

→ Der Agent versucht diese unvollständige Frage zu interpretieren, kann aber nur raten, welchen Raum der Fragesteller meint, welches Datum, welchen Namen er hat und was er eigentlich erreichen will. Es fehlt die vorangegangene Frage. Stattdessen nimmt das Modell einfach die Beispielwerte aus der Toolbeschreibung.

#### 4-1-3

Frage 1: 1642 Eingabe-Tokens gesamt.
Frage 2: 3560 Eingabe-Tokens gesamt.

→ Mehr als die Doppelte Menge Eingabe Tokens, da bei der zweiten Frage auch die gesamte Historie mitgesendet wird. 

Mit Fenster hat Frage 2 3221 Eingabe-Tokens, versucht aber auch den Raum zu buchen, wie der Agent ohne Historie zuvor. 

→ Die vorangegangene Frage wurde abgeschnitten. Es wird immer bei der Nachricht einer Person abgeschnitten, da die Konversation andernfalls mit einem Tool-Call oder dessen Resultat beginnen würde, was das Modell verwirren könnte.

#### 4-1-4

Direkt nachdem der Schritt gemacht wurde, und bevor er ausgegeben wird, damit die Ausgabe immer nur sicher gespeicherten Output anzeigt. Zwischen jedem Schritt damit möglichst wenig verloren geht. Das Schlimmste was hier passieren könnte wäre ein crash nach einem Tool-Call, bevor gespeichert wurde, da dann der Tool-Call erneut ausgeführt wird, was bei destruktiven Operationen problematisch sein kann. 

### 4-2

#### 4-2-1

```json
"status": "wartet_auf_bestaetigung",
"offene_aktion": {
  "id": "call_w5ou058i",
  "function": {
    "arguments": "{\"uhrzeit\":\"14:00\",\"name\":\"Kim\",\"raum\":\"O-108\",\"datum\":\"2026-11-05\"}",
    "name": "raum_buchen"
  },
  "type": "function",
  "index": 0
},
```

→ Alles außer Datum stimmen, die Probleme mit dem Datum sind allerdings die Bekannten, und bereits früher im Chat falsch gewesen. Die Bestätigung ist soweit sinnvoll.

#### 4-2-2

```
Es tut mir leid, aber die Person hat diese Aktion nicht bestätigt. Ich kann den Raum nicht für dich buchen.
```

→ Es entschuldigt sich und führt es nicht aus.

#### 4-2-3

```
Sitzung kim wartet auf keine Bestätigung (Status: fertig).
```

→ In der Sitzung ist kein offener Tool-Call gespeichert, also passiert nichts. Wenn ein Fehler während, bzw. direkt nach dem Tool-Call auftritt, kann wie oben beschrieben eine destruktive Operation durchlaufen, ohne, dass der erfolgreiche Aufruf gespeichert wurde und damit würde es nochmal ausgeführt werden. Damit dabei kein Schaden angerichtet wird muss das Tool idempotent sein.

#### 4-2-4

- Zwischen der Frage und der Antwort kann sehr viel Zeit liegen, während der die blockierende Variante durchgehend aktiv sein müsste, und damit Ressourcen unnötig verschwenden würde.
- Jede Instanz des Agents wäre gebunden an eine bestimmte Session und es kann nicht zwischen Replicas nach Bedarf umhergeschaltet werden.

### 4-3

#### 4-3-1

```
  → merken(fakt='Die Person isst vegetarisch.')
  ← Gespeichert: Die Person isst vegetarisch.

Ich habe es aufgezeichnet.
```

→ Wird in der dritten Person aufgerufen. Das ist wichtig, da die nächste Session nur diesen Satz sieht. Das Wort "ich" wäre hier zb. missverständlich, da es für das Modell nicht klar ist, wer in diesem Fall "ich" ist. Auch darf es nicht wörtlich aufgeschrieben werden, da das ebenfalls vom Kontext abhängen könnte, der dann fehlt.

#### 4-3-2

```
Modell: llama3.2:3b · 6 Aufgaben · Fenster 20 Nachrichten

Variante       Typ         Treffer  Werkz.  Aufrufe Σ  Tokens Σ  Dauer Σ
mit Memory     kurzzeit      2/6     6/6           12     10672      70s
mit Memory     langzeit      1/3     4/6           10      8890      61s
ohne Memory    kurzzeit      1/6     6/6           12      8561      69s
ohne Memory    langzeit      0/3     3/6           12      7493      57s
```

```
Modell: qwen2.5:3b · 6 Aufgaben · Fenster 20 Nachrichten

Variante       Typ         Treffer  Werkz.  Aufrufe Σ  Tokens Σ  Dauer Σ
mit Memory     kurzzeit      4/6     5/6            9     12048      44s
mit Memory     langzeit      1/3     6/6           11     13963      62s
ohne Memory    kurzzeit      2/6     5/6            9      9805      34s
ohne Memory    langzeit      0/3     3/6            8      8105      21s
```

→ Fragen nach einer Information die Zuvor bewusst genannt wurde (bspw. nach dem Namen) werden erst durch Memory möglich. Fragen wie die nach dem Essen in der Mensa und den Lerngruppen sind ebenfalls abhängig vom Memory, scheitern aber trotzdem an anderen Stellen und Aufrufen. Die übrigen scheitern vor allem an falschen Werten (Datum), die Memory nicht behebt.

Fehlermodi mit Memory (ohne Memory kommt bei Langzeit-Aufgaben ein Werkzeugfehler dazu, da `merken` fehlt):

| Aufgabe | llama3.2:3b | qwen2.5:3b |
|---|---|---|
| raum_von_vorhin | Falsche Werte (Freitag → `2026-11-05`), Ziel verfehlt | - |
| mensa_folgefrage | Falsche Werte (Donnerstag → `2026-11-04`), Ineffizienz | - |
| campuskarte | - | Falsche Reflexion (antwortet ohne zu suchen) |
| vegetarisch | Ziel verfehlt (`merken` als Text statt Aufruf), Falsche Werte (morgen → `2026-11-05`) | Falsche Werte (morgen → `2026-11-05`), Ziel verfehlt (Fakt nicht genutzt) |
| lerngruppe | Ziel verfehlt (`merken` als Text), Falsche Werte, Falsche Reflexion | Falsche Werte (`2023-04-14`, `name='Lerngruppe'`), Falsche Reflexion |

#### 4-3-3

Jeder Fakt wird direkt in den System-Prompt geschrieben und kostet damit so viele Input-Tokens wie er lang ist. Bei vielen Fakten kann das dann bei kleinen Modellen schnell den gesamten Kontext ausfüllen und sinnvolle Antworten unmöglich machen. Hier wäre dann wieder eine Vorauswahl oder eine Retrieval Lösung sinnvoll, oder ein regelmäßiges Aufräumen des Memory. 

#### 4-3-4

Beide Modelle lassen sich davon nicht austricksen und beantworten einfach nur die Frage nach einem freien Raum.

#### 4-3-5

Neben der `memory.json` datei müssten auch alle Sessions der Person gelöscht werden.

### 4-4

#### 4-4-1

```
Modell: llama3.2:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               2/13    9/13          0       5        0        0.8       1.8      1220     9.3s
supervisor                  1/13   10/13          0       6        0        1.3       3.2      1285    11.0s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    1/4         1/1         0/4         0/1         0/1         0/1         0/1
supervisor                       0/4         1/1         0/4         0/1         0/1         0/1         0/1
```

```
Modell: qwen2.5:3b · 13 Aufgaben

Variante                  Antwort  Werkz.  ungültig  Fehler  Abbruch  Aufrufe Ø  Modell Ø  Tokens Ø  Dauer Ø
agent.v1.yaml               5/13    8/13          0       0        0        0.6       1.6      1647     4.5s
supervisor                  3/13    9/13          0       2        0        1.1       2.8      1493     9.2s

Richtige Antworten nach Typ:
Variante                       datum      direkt      wissen mehrschritt  schreibend        ohne       fehlt
agent.v1.yaml                    2/4         1/1         0/4         0/1         1/1         0/1         1/1
supervisor                       1/4         1/1         0/4         1/1         0/1         0/1         0/1
```

→ Der Supervisor scheint tendenziell etwas günstiger in tokens, auch wenn er mehr Modellaufrufe durchführt. Trotzdem ist der Effekt nicht signifikant, während die Dauer auffällig steigt und die Antworten des Supervisors öfter falsch sind.

#### 4-4-2

**Planung:** „Klausur krank“ (`llama3.2:3b`) → verwendet unnötigerweise zusätzlich `raum_agent` und `mensa_agent`

**Übergabe:** "Klausur krank" (`llama3.2:3b`), `wissen_agent` erhält „Wo kann ich mich aufhalten, wenn ich krank bin?“, was nicht viel mit der Originalfrage zu tun hat.

**Spezialist:** „O-108 am Donnerstag“ (`qwen2.5:3b`), Auftrag wird wörtlich übernommen, aber Spezialist wählt `datum='2023-11-10'`

#### 4-4-3

Um einen eventuell faireren Vergleich zu machen müsste der Agent prompt mit den gleichen Regeln ausgestattet und getestet werden. Allerdings kann das auch durch das limitiertere Kontextfenster zu Verschlechterungen führen, was wiederum unfair wäre, da gerade die Stärke des Supervisors in detaillierteren Prompts liegen kann. Wirklich 1:1 vergleichen ist schwierig, am Ende müsste man beide Typen so weit optimieren, wie möglich und dann die besten Ergebnisse vergleichen.
