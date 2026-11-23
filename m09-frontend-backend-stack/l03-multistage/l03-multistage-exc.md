# Lab 9.3 – Übung: Multistage Dockerfiles

**Dauer:** ca. 15 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung nutzt die Todo-App im Ordner `playground/todo-app/`.

## Vorbereitung

- Docker Desktop läuft; Terminal im Ordner `project/playground` (Windows: Git Bash, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Todo-App aus Lab 4.2 im Ordner `playground/todo-app`; falls nicht vorhanden, in Aufgabe 1 holen. Läuft sie noch per Compose: im Ordner `playground/todo-app` `docker compose down`.
- Starter: `project/starters/m09-l03-multistage/Dockerfile.prod` (mit TODOs) und `project/starters/m09-l03-multistage/server.js` (fertig angepasst) · Arbeitsdateien: `playground/todo-app/app/Dockerfile.prod`, `playground/todo-app/app/server.js`.
- Port 3000 frei (Grafana aus Lab 7.2 und Rezeptbuch gestoppt).

## Aufgaben

1. Hole die Todo-App nach `playground/todo-app`, falls sie fehlt:
   - mit git: `git clone https://github.com/docker/multi-container-app.git todo-app`
   - ohne git: [ZIP herunterladen](https://github.com/docker/multi-container-app/archive/refs/heads/main.zip), nach `playground/` entpacken und den Ordner `multi-container-app-main` in `todo-app` umbenennen.
2. Baue im Ordner `playground/todo-app` das bisherige Image mit aktuellem Node: `docker build --build-arg NODE_VERSION=24 -t todo-app:dev app`. Prüfe, dass nodemon darin steckt: `docker run --rm todo-app:dev nodemon --version`.
3. Kopiere beide Starterdateien nach `app/` (`cp ../../starters/m09-l03-multistage/Dockerfile.prod ../../starters/m09-l03-multistage/server.js app/`) und ergänze in `app/Dockerfile.prod` die TODOs der Stufe `production`.
4. Baue das Multistage-Image mit `docker build -f app/Dockerfile.prod -t todo-app:prod app`. Vergleiche die Größen mit `docker images todo-app` und prüfe nodemon erneut mit `docker run --rm todo-app:prod nodemon --version`.
5. Starte das Produktions-Image mit Datenbank in einem eigenen Netzwerk und lege im Browser unter `http://localhost:3000` zwei Aufgaben an:
   ```bash
   docker network create todo-net
   docker run -d --name todo-database --network todo-net mongo:8
   docker run -d --name todo-app --network todo-net -p 3000:3000 todo-app:prod
   ```
   Räume danach mit `docker rm -f todo-app todo-database` und `docker network rm todo-net` auf.

## Checkpoint

- `docker images todo-app` zeigt zwei Tags; `prod` ist rund 50 MB kleiner als `dev`.
- `nodemon --version` gibt bei `todo-app:dev` eine Versionsnummer aus, bei `todo-app:prod` den Fehler `Cannot find module '/usr/src/app/nodemon'`.
- `docker logs todo-app` zeigt `Live-Reload aus …`, `Server listening on port 3000` und `Mongodb Connected`.
- Die Todo-Liste unter `http://localhost:3000` speichert neue Einträge.

## Abschlusskriterien

- `app/Dockerfile.prod` hat drei Stufen; die letzte enthält nur Laufzeitpakete und die Dateien `server.js`, `config`, `models`, `routes`, `views`.
- Das Produktions-Image läuft ohne Entwicklungsabhängigkeiten und ist kleiner als das Entwicklungs-Image.

## Erweiterung

Zeige mit `docker history todo-app:dev` und `docker history todo-app:prod` die Schichten beider Images. Suche die Schichten von `npm install -g nodemon` und `chown -R` im Entwicklungs-Image und vergleiche ihre Größe mit der größten Schicht des Produktions-Images.

## Fallback

- Fertiger Stand der beiden Dateien: `project/examples/m09-frontend-backend-stack/l03-multistage/todo-app/app/` (im Ordner `project/`: `cp -r examples/m09-frontend-backend-stack/l03-multistage/. playground/`, setzt eine geholte Todo-App voraus).
- `toomanyrequests` beim Laden von `node:24-alpine` oder `mongo:8`: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
