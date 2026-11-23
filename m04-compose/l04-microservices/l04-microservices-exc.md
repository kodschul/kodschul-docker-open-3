# Lab 4.4 – Übung: Migration in eine Microservice-basierte Anwendung

**Dauer:** ca. 10 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Änderung an `compose.yml` wird in Aufgabe 5 zurückgenommen; danach gilt wieder der Stand aus Lab 4.3.

## Vorbereitung

- Stand aus Lab 4.3: `project/playground/hello/compose.yml` mit einem Frontend auf Port 8080 und Volume `hello-data`. Fehlt er, im Ordner `project/`:
  `cp -r examples/m04-compose/l03-volumes/hello/. playground/hello/`
- Arbeitsdatei: `playground/hello/compose.yml`; kein Starter. Alle Befehle laufen im Ordner `project/playground/hello`.

## Aufgaben

1. Starte die Hello-App mit `docker compose up -d` und notiere aus `docker compose ps` für beide Container die Spalte `CREATED` und aus `docker ps` die `CONTAINER ID`. Öffne `http://localhost:8080` und notiere Version und Frontend-ID.
2. Ändere in `compose.yml` beim Frontend das Build-Argument auf `APP_VERSION=2.1.0` und ergänze `environment` mit `APP_COLOR=lightblue`.
3. Baue und ersetze nur das Frontend mit `docker compose up -d --build --no-deps frontend` und lies die Meldungen.
4. Vergleiche mit Aufgabe 1: `docker compose ps`, `docker ps` und die Seite im Browser (Version, Farbe, Frontend-ID, Backend-Zeile, Aufrufe in access.log).
5. Nimm beide Änderungen in `compose.yml` zurück und führe `docker compose up -d --build --no-deps frontend` erneut aus.

## Checkpoint

- Aufgabe 3: Die Meldungen nennen nur das Frontend (`Image frontend:v2 Built`, `Container hello-frontend-1 Started`); das Backend erscheint nicht.
- Aufgabe 4: Das Backend hat dieselbe Container-ID und läuft länger als das Frontend; das Frontend hat eine neue ID. Die Seite ist hellblau mit „Hello World 2.1.0", die Aufrufe zählen weiter.
- Aufgabe 5: Die Seite ist wieder gelb mit „Hello World 2.0.0".

## Abschlusskriterien

- Das Frontend wurde zweimal aktualisiert, ohne dass der Backend-Container neu gestartet wurde.
- `compose.yml` entspricht wieder dem Stand aus Lab 4.3; die Hello-App läuft.

## Fallback

- Build scheitert: `docker compose logs frontend` lesen; Stand mit `cp -r examples/m04-compose/l03-volumes/hello/. playground/hello/` (im Ordner `project/`) wiederherstellen.
