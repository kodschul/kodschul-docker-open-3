# Lab 1.2 – Übung: Vergleich zur Virtualisierung

**Dauer:** ca. 5 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung startet nur kurzlebige Container, die sich selbst entfernen.

## Vorbereitung

- Docker Desktop läuft (`Engine running`), Terminal in der Kurs-Shell `bash` ist offen ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Starter und Arbeitsdatei: keine, alle Schritte sind Befehle.

## Aufgaben

1. Zeige mit `docker run --rm alpine:3.24 uname -r` die Kernel-Version, die ein Alpine-Container sieht.
2. Starte einen Container aus `ubuntu:24.04` mit demselben Befehl `uname -r` und vergleiche beide Versionen.
3. Zeige in beiden Images mit `docker run --rm <image> cat /etc/os-release` den Namen der Linux-Distribution.
4. Miss die Startzeit eines Containers mit `time docker run --rm alpine:3.24 echo hallo`; führe den Befehl zweimal aus.

## Checkpoint

- Aufgabe 1 und 2 geben dieselbe Kernel-Version aus.
- Aufgabe 3 zeigt `Alpine Linux` bzw. `Ubuntu`.
- Aufgabe 4 gibt `hallo` aus; die Zeile `real` liegt unter einer Sekunde.

## Abschlusskriterien

- Erklärt: zwei Distributionen, ein gemeinsamer Kernel.
- Gemessen: Ein Container startet, führt einen Befehl aus und endet in weniger als einer Sekunde.

## Fallback

- `toomanyrequests` beim Download: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
- Kein Download möglich (kein Netz, Proxy): Ergebnisse im Screenshot der [Lösung](l02-virtualization-sol.md) nachlesen; `hello-world` aus Lab 1.1 eignet sich nicht als Ersatz, weil es keine Befehle wie `uname` enthält.
