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

- Verbesserungen beim Prompt scheinen die Fehler etwas auszugleichen, allerdings reicht bereits der längere Docstring in dem MCP mit Fehlertoleranz aus, um die Vorteile wieder zu verlieren. 
- MCP Fehlertoleranz erzielt immerhin eine Verbesserung bei der Workflow Lösung.
- 