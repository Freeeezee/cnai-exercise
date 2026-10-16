# Exercise 1

## 2

### 2-1

| Frage                                   | Modell       | TTFT (ms) | Gesamt (ms) | Antwort brauchbar? |
| --------------------------------------- | ------------ | --------- | ----------- | ------------------ |
| Wie viele Semester hat ein AIN-Studium? | llama3.2:3b  | 9418 ms   | 12644 ms    | N                  |
| Wie viele Semester hat ein AIN-Studium? | qwen2.5:0.5b | 5572 ms   | 5904 ms     | N                  |
| Wo liegt Konstanz?                      | llama3.2:3b  | 1346 ms   | 5795 ms     | (N)                |
| Wo liegt Konstanz?                      | qwen2.5:0.5b | 1111 ms   | 2192 ms     | N                  |
| Wann wurde die HTWG gegründet?          | llama3.2:3b  | 1355 ms   | 3323 ms     | N                  |
| Wann wurde die HTWG gegründet?          | qwen2.5:0.5b | 402 ms    | 1150 ms     | N                  |

### 2-2

*Ist die HTWG Konstanz eine private oder eine staatliche Hochschule?*

**qwen2.5:0.5b:** Eine HTWG Konstanz ist stattdessen öffentlich und staatlicher Hochschule.

**llama3.2:3b:** Die Hochschule für Technologie, Wirtschaft und Geosciences (HTWG) Konstanz ist eine staatliche Hochschule im sinngeräumigen Staat Bayern, aber der Campus liegt in Baden-Württemberg.

→ llama3.2:3b ist generell meistens näher dran, wobei beide eigentlich nie eine 100% richtige Antwort liefern.

## 3 — Sampling

### 3-1

*Wie viele verschiedene Antworten bekommt ihr bei jeder Temperature?*

| Temperature | Anzahl Antworten |
| ----------- | ---------------- |
| 0.0         | 1                |
| 0.7         | 4                |
| 1.2         | 5                |

### 3-2

*Liefert Temperature 0 wirklich fünfmal dieselbe Antwort? Wenn nicht: Woran könnte das liegen?*

In diesem Fall ja. Es könnte allerdings abhängig von Hardware- oder Softwareunterschieden und -optimierungen zu Abweichungen kommen.

### 3-3

*Welche Fehler kommen schon bei Temperature 0 vor, welche erst bei höheren Werten? Was sagt das über die Ursache (Sampling oder Trainingsdaten)?*

Bei Temperature 0 ist die Kernantwort *(staatlich)* faktisch richtig, allerdings wird die HTWG als "Hochschule für Technik und Wirtschaft" bezeichnet, also "Gestaltung" vergessen. Abgesehen davon ist die Antwort allerdings zufriedenstellend.

Erhöht man die Temperature auf 0.7 beginnt das Modell *staatlich* und *staatlich anerkannt* zu vermischen, was impliziert, dass die HTWG nur eine private Hochschule ist. Außerdem wird hier erstmalig das "G" zwar berücksichtigt, allerdings mit "Geisteswissenschaften" falsch übersetzt.

Bei Temperature 1.2 gibt es zwar ein mal die einzige wirklich richtige Antwort ("Die HTWG Konstanz ist eine staatliche Hochschule."), das ist allerdings vor allem dem geschuldet, dass die Antwort kürzer ausfällt und nicht versucht die Abkürzung aufzulösen.
Ansonsten treten die gleichen Vermischungsfehler wie bei 0.7 auf, und die Abkürzung wird jetzt vor allem durch zusammengewürfelt erscheinende Stadt-Namen aufgelöst, die nichts mit der HTWG zu tun haben. Auch wird die HTWG einmal als "Berufsakademie" bezeichnet.

→ Die Trainingsdaten enthalten offenbar mit genügend Sicherheit die richtige Antwort *staatlich*, und Abweichungen hier sind vor allem der Temperature geschuldet. Die Nähe des der Kombination "staatlich anerkannt" zu "staatlich" macht dem Modell aber Schwierigkeiten — "privat" taucht nie auf, der Fehler entsteht eher durch die Neigung "anerkannt" auf "staatlich" folgen zu lassen. 
Über die Abkürzung der HTWG kann man das allerdings nicht sagen, diese ist offenbar in den Trainingsdaten zu wenig vorhanden um eine korrekte Antwort zu ermöglichen.

## 3 — Tokens

### 3-1

Deutsch    63 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 14 Tokens mehr (+29%).

### 3-2

Deutsch    68 Tokens für 21 Wörter
Englisch   49 Tokens für 21 Wörter

Deutsch braucht 19 Tokens mehr (+39%).

→ Der Unterschied wird größer. Tokenization ist generell eher abhängig von der Zeichenanzahl als der Anzahl der Wörter.

## 4

### 4-1

qwen2.5:0.5b hat **4** richtig eingeordnet, llama3.2:3b hat **8** richtig erkannt.

### 4-2

| Model        | Anliegen Falsch | Studiengang Falsch | Frist Falsch |
| ------------ | --------------- | ------------------ | ------------ |
| llama3.2:3b  | 0               | 2                  | 4            |
| qwen2.5:0.5b | 4               | 4                  | 5            |

Bei den gemeldeten Fehlern ist das Anliegen falsch, allerdings ist bei den gleichen oder auch anderen Antworten mit richtigem Anliegen oft die Frist oder der Studiengang falsch.

### 4-3

Das Schema überprüft nur das Antwortformat. Und da weder `studiengang` noch `frist` ein standartisiertes Format haben, sondern beliebige *Strings* oder *null* sein dürfen ist das Schema erfüllt, auch wenn der Inhalt nicht korrekt oder null ist.

### 4-4

Beide Modelle sind zwar verwirrt und geben unlogische Antworten aus, das Schema behalten Sie aber bei und versuchen weiterhin die E-Mails einzuordnen, es klappt also nicht, das Modell seinen System-Prompt damit vergessen zu lassen.

### 4-5

Auch wenn Sie weiterhin versuchen Json auszugeben, halten sich die Modelle nicht mehr ans vorgegebene Schema, und die Antworten können nicht mehr in das vorgegebene Objekt umgewandelt werden, weshalb die Einordnung misslingt. Temperature 0 macht das ganze nur schwieriger, da auch erneute Versuche den gleichen Output produzieren und ebenfalls nicht gelesen werden können.

Mit einem besseren/ausführlicheren System prompt mit dem genauen Schema lässt sich das Problem allerdings eindämmen:

```
SYSTEM_PROMPT = (
    "Du ordnest Mails von Studierenden an die HTWG Konstanz ein. "
    "Antworte ausschließlich mit JSON der Form {anliegen: pruefung | mensa | bibliothek | sonstiges, studiengang: string | null, frist: string | null}. "
    "anliegen ist pruefung, mensa, bibliothek oder sonstiges. "
    "studiengang ist das Kürzel (z. B. AIN, WIN, MSI) oder null. "
    "frist ist die Frist aus der Mail, so wie sie dort steht, oder null."
)
```

