# Lab 3.2 – Übung: Eigene Images erstellen und verwalten

**Dauer:** ca. 60 Minuten (Einführung 15, Arbeitsphase 35, Debrief 10)
**Ändert die Hello-App-Projektbasis?** Ja — die Hello-App bekommt ihre Dockerfiles; die Images `frontend:v1`, `frontend:v2` und `backend:v1` nutzen alle folgenden Labs.

## Vorbereitung

- Docker Desktop läuft; Terminal (macOS/Linux: Terminal, Windows: Git Bash mit `MSYS_NO_PATHCONV=1`, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)) im Ordner `project/`.
- Starter: `project/starters/m03-l02-own-images/` mit `weather/`, `pizza/` und `hello/{frontend,backend}/` (je ein `Dockerfile` mit TODOs). Kopieren:

  ```bash
  cp -r starters/m03-l02-own-images/. playground/
  ```

- Arbeitsordner: `project/playground/weather/`, `project/playground/pizza/`, `project/playground/hello/backend/` und `project/playground/hello/frontend/`.
- Ablauf: Einführung mit der Theorie, Arbeitsphase mit den Aufgaben 1 bis 5 (Zwischenstand nach Aufgabe 1 im Checkpoint), Debrief: eigene Dockerfiles mit der Lösung vergleichen.

## Aufgaben

1. Ergänze in `playground/weather/` das `Dockerfile` nach den TODOs (Basis `python:3.13-alpine`, `weather.py` kopieren und beim Start ausführen). Baue es im Ordner `playground/weather` als `weather:1.0` und starte einen Container mit `docker run --rm weather:1.0`.
2. Ergänze in `playground/pizza/` das `Dockerfile` nach demselben Muster für `order_pizza.py` und baue es als `pizza:1.0`. Starte den Container zuerst mit `docker run --rm pizza:1.0`, danach mit `docker run -it --rm pizza:1.0`, und bestelle eine Pizza.
3. Ergänze in `playground/hello/backend/` und `playground/hello/frontend/` die Dockerfiles nach den TODOs. Baue im Ordner `backend` das Image `backend:v1` und im Ordner `frontend` das Image `frontend:v1` mit `--build-arg APP_VERSION=1.0.0`.
4. Baue im Ordner `frontend` zusätzlich `frontend:v2` mit `--build-arg APP_VERSION=2.0.0`. Starte es mit `docker run -d --name hello-frontend -p 8080:80 frontend:v2`, öffne `http://localhost:8080` und zeige mit `docker images` alle Images dieser Übung an.
5. Ersetze beim Start den Standardbefehl (`CMD`): Lies mit `docker run --rm frontend:v1 cat version.info` und `docker run --rm frontend:v2 cat version.info` die Versionsdatei beider Images und zeige mit `docker run --rm frontend:v2 env` die Umgebungsvariablen. Suche `APP_DISPLAY_VERSION` und `APP_VERSION`.

## Checkpoint

- Nach Aufgabe 1: `docker run --rm weather:1.0` gibt `Heute scheint die Sonne!` aus.
- Ohne `-it` endet die Pizza-App mit `EOFError`; mit `-it` fragt sie `Welche Pizza soll es sein?` und bestätigt die Eingabe.
- `docker images` listet `weather:1.0`, `pizza:1.0`, `backend:v1`, `frontend:v1` und `frontend:v2`.
- `http://localhost:8080` zeigt „Hello World 2.0.0", die Container-ID und IP des Frontends und „Backend nicht erreichbar (http://backend:80): ConnectionError". Die Fehlermeldung ist erwartet: Das Backend läuft noch nicht mit dem Frontend zusammen (Modul 4).
- `version.info` enthält `Last version updated: 1.0.0` bzw. `2.0.0`; `env` zeigt `APP_DISPLAY_VERSION=2.0.0`, aber kein `APP_VERSION`.

## Abschlusskriterien

- Fünf eigene Images sind gebaut und gestartet; der Container `hello-frontend` läuft auf Port 8080.
- Der Unterschied ist sichtbar: `ARG APP_VERSION` existiert nur beim Bauen, `ENV APP_DISPLAY_VERSION` auch im Container.

## Erweiterung

Starte das Backend allein mit `docker run -d --name hello-backend -p 8081:80 backend:v1` und rufe `http://localhost:8081` auf. Die Seite zeigt das JSON mit `hostname`, `ip` und `now`. Entferne den Container danach mit `docker rm -f hello-backend`.

## Fallback

- `toomanyrequests` beim Laden von `python:3.13-alpine`: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
- Ein Dockerfile lässt sich nicht bauen: fertigen Stand kopieren mit `cp -r examples/m03-images-registries/l02-own-images/. playground/` (im Ordner `project/`) und erneut bauen.
- Hello-Images fehlen für die nächsten Labs: `bash build-images.sh` im Ordner `project/` baut `frontend:v1`, `frontend:v2` und `backend:v1` aus den fertigen Dockerfiles.
- Port 8080 belegt: alten Container mit `docker ps` suchen und mit `docker rm -f <name>` entfernen, oder einen anderen Port wählen (z. B. `-p 8090:80`).
