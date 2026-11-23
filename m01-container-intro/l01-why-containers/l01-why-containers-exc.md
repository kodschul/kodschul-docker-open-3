# Lab 1.1 – Übung: Warum Container?

**Dauer:** ca. 5 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung prüft nur die Docker-Installation.

## Vorbereitung

- Docker Desktop ist installiert ([Setup](../../00-setup-and-installation.md)).
- Terminal in der Kurs-Shell `bash` ist offen (macOS/Linux: Terminal, Windows: Git Bash, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Starter und Arbeitsdatei: keine, alle Schritte sind Befehle.

## Aufgaben

1. Starte Docker Desktop und warte, bis die Statusleiste unten links `Engine running` zeigt.
2. Starte im Terminal den ersten Container mit `docker run hello-world`.
3. Ordne die vier nummerierten Schritte der Ausgabe den Beteiligten zu: Terminal (Docker Client), Docker im Hintergrund (Docker Daemon), Docker Hub, Container.
4. Führe `docker run hello-world` ein zweites Mal aus und vergleiche die ersten Zeilen mit dem ersten Lauf.

## Checkpoint

- Die Ausgabe enthält `Hello from Docker!` und `This message shows that your installation appears to be working correctly.`
- Beim ersten Lauf stehen davor die Zeilen `Unable to find image 'hello-world:latest' locally` und `Pull complete`.
- Beim zweiten Lauf fehlen diese Zeilen.

## Abschlusskriterien

- `docker run hello-world` läuft ohne Fehlermeldung.
- Der Unterschied zwischen erstem und zweitem Lauf ist erklärt.

## Fallback

- `Cannot connect to the Docker daemon`: Docker Desktop läuft noch nicht; Statusleiste abwarten und Befehl wiederholen.
- `toomanyrequests` beim Download: `docker login` ausführen ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)) und Befehl wiederholen.
- Ohne funktionierende Installation: Ausgabe im Screenshot von [Lab 1.1](l01-why-containers-thx.md#der-erste-container-mit-hello-world) lesen und Aufgabe 3 daran lösen; Installation in der Pause mit dem Setup nachholen.
