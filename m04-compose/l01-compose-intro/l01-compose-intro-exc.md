# Lab 4.1 – Übung: Einführung in Docker Compose

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — `playground/hello/` erhält vier Compose-Dateien sowie `.env` und `app-config.env`; Lab 4.2 baut darauf auf.

## Vorbereitung

- Docker Desktop läuft; Terminal mit bash ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Arbeitsordner: `project/playground/hello/` mit den Dockerfiles aus Lab 3.2 (`frontend/Dockerfile`, `backend/Dockerfile`). Fehlen sie, im Ordner `project/` den Stand herstellen:
  `cp -r examples/m03-images-registries/l02-own-images/. playground/`
- Starter kopieren (im Ordner `project/`):
  `cp -r starters/m04-l01-compose-intro/. playground/`
  Danach liegen in `playground/hello/`: `compose-simple.yml` und `compose-with-custom-image.yml` (fertig), `compose-minimal.yml` und `compose-with-config.yml` (mit `TODO`), `.env` und `app-config.env`.
- Alle Befehle laufen im Ordner `project/playground/hello`. Container aus Tag 1 auf Port 8080 oder 9000 vorher entfernen (`docker ps`, `docker rm -f <name>`).

## Aufgaben

1. Lies `compose-simple.yml`, starte sie mit `docker compose -f compose-simple.yml up -d` und öffne `http://localhost:9000`. Zeige die Container mit `docker compose -f compose-simple.yml ps` an und entferne alles wieder mit `docker compose -f compose-simple.yml down`.
2. Ergänze in `compose-minimal.yml` die drei `TODO`: beide Dienste werden aus ihrem Ordner gebaut, das Frontend ist auf Port 8080 erreichbar. Starte die Datei mit `up -d`, öffne `http://localhost:8080`, lies die Ausgaben mit `logs` und zeige die neuen Images mit `docker images`. Entferne die Container danach mit `down`.
3. Starte `compose-with-custom-image.yml` mit `up -d`, öffne `http://localhost:8080` und lade die Seite mehrmals neu. Vergleiche Farbe, Version und die Backend-Zeile mit Aufgabe 2 und zeige mit `ps` die Container an. Entferne sie danach mit `down`.
4. Ergänze in `compose-with-config.yml` die fünf `TODO` mit den Werten aus `.env` und `app-config.env`. Prüfe das Ergebnis mit `docker compose -f compose-with-config.yml config` und starte die Datei danach mit `up -d --build`.
5. Ändere in `.env` den Port auf `8081` und die Anzahl der Backends auf `2`, führe `up -d` erneut aus und öffne `http://localhost:8081`. Entferne zum Schluss alles mit `docker compose -f compose-with-config.yml down`.

## Checkpoint

- Aufgabe 1: Port 9000 zeigt „Willkommen"; `ps` listet `hello-web-1`, `hello-extra-1` und `hello-extra-2`.
- Aufgabe 2: Die Hello-Seite zeigt unter **Backend** eine Container-ID, eine IP und eine Uhrzeit statt „Backend nicht erreichbar"; `docker images` listet `hello-frontend` und `hello-backend`.
- Aufgabe 3: Die Seite ist hellblau mit „Hello World 1.0.0"; `ps` zeigt zwei Backend-Container.
- Aufgabe 4: `config` zeigt `APP_VERSION: 1.1.0`, `published: "8080"`, `replicas: 3` und `APP_COLOR: lightgreen`; die Seite ist hellgrün mit „Hello World 1.1.0".
- Aufgabe 5: Die Seite ist nur noch auf Port 8081 erreichbar; `ps` zeigt zwei Backends.

## Abschlusskriterien

- Alle vier Compose-Varianten sind gestartet und wieder entfernt; `docker compose ps` ist leer.
- `compose-minimal.yml` und `compose-with-config.yml` sind vollständig und starten ohne Fehler.

## Erweiterung

Starte `compose-with-config.yml` ohne Datei `.env` (umbenennen in `env.bak`) mit `config` und lies die Warnungen. Benenne die Datei danach zurück.

## Fallback

- Port 8080, 8081 oder 9000 belegt: in der Compose-Datei bzw. `.env` einen freien Port eintragen.
- Starter-Dateien kaputt: fertigen Stand aus `examples/m04-compose/l01-compose-intro/` kopieren (`cp -r examples/m04-compose/l01-compose-intro/. playground/`).
- `toomanyrequests` beim Download von `nginx`: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
