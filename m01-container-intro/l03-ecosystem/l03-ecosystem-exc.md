# Lab 1.3 – Übung: Container-Ökosystem kennenlernen

**Dauer:** ca. 5 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung liest nur Informationen aus.

## Vorbereitung

- Docker Desktop läuft (`Engine running`), Terminal in der Kurs-Shell `bash` ist offen ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Container aus Lab 1.1 und 1.2 sind vorhanden (die `hello-world`-Läufe).

## Aufgaben

1. Zeige mit `docker version` Client und Server an und lies je Version und `OS/Arch` ab.
2. Lies mit `docker info` die Zeilen `Operating System`, `Kernel Version`, `CPUs`, `Total Memory` und `Images` ab.
3. Öffne Docker Desktop und finde in der Ansicht **Containers** die Container der `hello-world`-Läufe aus Lab 1.1.
4. Öffne in Docker Desktop die Ansichten **Images** und **Volumes** und vergleiche die Image-Liste mit der Zahl `Images` aus Aufgabe 2.

## Checkpoint

- `docker version` zeigt zwei Abschnitte: `Client` mit dem eigenen Betriebssystem (`darwin`, `windows` oder `linux`) und `Server` mit `linux`.
- `Kernel Version` aus `docker info` ist dieselbe wie `uname -r` im Container aus Lab 1.2.
- **Containers** listet mindestens zwei beendete Container aus dem Image `hello-world`; **Images** enthält `hello-world`, `alpine` und `ubuntu`.

## Abschlusskriterien

- Client- und Server-Version sind abgelesen.
- Erklärt: Der Server läuft unter Linux, auch wenn der Rechner macOS oder Windows nutzt.

## Fallback

- `Server` fehlt in `docker version`, stattdessen `Cannot connect to the Docker daemon`: Docker Desktop starten und `Engine running` abwarten.
- Docker Desktop lässt sich nicht öffnen (z. B. Linux mit Docker Engine ohne Desktop): Aufgabe 3 und 4 entfallen; dieselben Listen zeigt Lab 2.1 im Terminal.
