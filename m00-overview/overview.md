# Docker Einführung – Kursüberblick

## Die Entwicklung von Docker

- Programme laufen auf jedem Rechner anders: „Works on my machine".
- 2013 macht Docker Container einfach: bauen, teilen, starten mit einem Befehl.
- 2015 folgt der offene Standard OCI: Images laufen mit vielen Werkzeugen.
- 2026: 59 % der Befragten im Stack Overflow Survey nutzen Docker intensiv.

## Was ist Docker?

- Werkzeug, das Images baut, verteilt und als Container startet.
- Container: abgeschirmter Prozess mit eigenem Dateisystem, eigener IP, begrenzten Ressourcen.
- Vergleich: der genormte Schiffscontainer – Kran, Schiff und Lkw behandeln jede Kiste gleich.

| Begriff | Bedeutung |
| --- | --- |
| Image | unveränderliche Vorlage aus Dateien und Startbefehl |
| Container | laufende Instanz eines Images |
| Dockerfile | Bauanleitung für ein Image |
| Registry | Speicher für Images, z. B. Docker Hub |
| Compose | mehrere Container aus einer YAML-Datei starten |

Details: [Lab 1.1](../m01-container-intro/l01-why-containers/l01-why-containers-thx.md)

## Warum Docker?

| Aufgabe | ohne Container | mit Docker |
| --- | --- | --- |
| neue Umgebung aufsetzen | Installationsanleitung, Stunden | `docker compose up`, Minuten |
| zwei Python-Versionen auf einem Server | Konflikt | je Container eine Version |
| gleiche Version in Test und Produktion | Hoffnung | dasselbe Image |
| Ressourcen je Anwendung | eigene VM mit eigenem Betriebssystem | geteilter Kernel, Start in Sekunden |
| Update zurücknehmen | Neuinstallation | altes Image-Tag starten |

Details: [Lab 1.2](../m01-container-intro/l02-virtualization/l02-virtualization-thx.md)

## Ziel und Ergebnis

- Container über die CLI steuern, untersuchen und mit Dateien versorgen.
- Eigene Images bauen, versionieren und in einer Registry ablegen.
- Mehrere Container mit Compose, Netzwerken und Volumes betreiben.
- Container absichern, Fehler finden, überwachen.
- Dienste hinter Traefik veröffentlichen und mit Docker Swarm orchestrieren.

## Projekt: Hello-App

- Zwei Python/Flask-Dienste: `frontend` (Webseite) und `backend` (JSON).
- Die Seite zeigt Version, Farbe, Container und IP: Replikas und Updates werden sichtbar.
- „Aufrufe in access.log" zählt mit: verlorene und dauerhafte Daten werden sichtbar.

| Tag | Stand der Hello-App am Ende |
| --- | --- |
| 1 | Images `frontend:v1`, `frontend:v2`, `backend:v1` in der lokalen Registry |
| 2 | Compose-Projekt mit Healthcheck, Watch, Volume, Limits, ohne root |
| 3 | hinter Traefik unter `app.localhost`, als Swarm-Stack mit Rolling Update |

Projektdateien: [project/README.md](../project/README.md)

## Tagesablauf

| Zeit | Tag 1 | Tag 2 | Tag 3 |
| --- | --- | --- | --- |
| 09:00–10:30 | Auftakt, Modul 1 Containertechnologie | Modul 4 Compose | Modul 7 Debugging |
| 10:30–10:45 | Pause | Pause | Pause |
| 10:45–12:15 | Modul 2 Arbeit mit Containern | Modul 4, Modul 5 Networking | Modul 8 Repositories |
| 12:15–13:15 | Mittag | Mittag | Mittag |
| 13:15–14:45 | Modul 3 Images | Modul 5, Modul 6 Sicherheit | Modul 9 Frontend-/Backend-Stack |
| 14:45–15:00 | Pause | Pause | Pause |
| 15:00–16:30 | Modul 3 Registry, Tagesabschluss | Modul 6, Tagesabschluss | Modul 10 Swarm, Kursabschluss |

Alle Labs mit Zeiten: [topics.md](topics.md)

## Arbeitsweise

- Jedes Lab: Theorie (`-thx.md`), Übung (`-exc.md`), Lösung (`-sol.md`).
- Gearbeitet wird in `project/playground/`; Startdateien liegen in `project/starters/`.
- Jeder Lab-Stand liegt fertig in `project/examples/` zum Vergleichen und Wiederherstellen.

## Voraussetzungen

- Docker Desktop (Windows mit WSL 2) und ein kostenloses Docker-Konto.
- Terminal-Grundlagen; Programmierkenntnisse sind nicht nötig.
- Anleitung: [Setup und Installation](../00-setup-and-installation.md)
