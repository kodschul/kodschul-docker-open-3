# Lab 4.2 – Übung: Multi-Container-Anwendungen erstellen

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — `playground/hello/` erhält `compose-develop.yml` und `compose.yml`; Lab 4.3 baut auf `compose.yml` auf.

## Vorbereitung

- Stand aus Lab 4.1 in `project/playground/hello/`; alle Container der Hello-App gestoppt (`docker compose -f compose-with-config.yml down`). Fehlt der Stand, im Ordner `project/`:
  `cp -r examples/m03-images-registries/l02-own-images/. playground/ && cp -r examples/m04-compose/l01-compose-intro/. playground/`
- Starter kopieren (im Ordner `project/`):
  `cp -r starters/m04-l02-multi-container/. playground/`
  Arbeitsdateien: `playground/hello/compose-develop.yml` (mit `TODO`) und die in Aufgabe 3 neu entstehende `playground/hello/compose.yml`.
- Alle Befehle laufen im Ordner `project/playground/hello`; zwei Terminalfenster sind praktisch (eines für `watch`).

## Aufgaben

1. Ergänze in `compose-develop.yml` die `TODO`: den Healthcheck des Backends und die Bedingung `service_healthy` beim Frontend. Starte die Datei mit `docker compose -f compose-develop.yml up -d --build`, lies die Startmeldungen und rufe zweimal im Abstand von einigen Sekunden `docker compose -f compose-develop.yml ps` auf.
2. Ergänze das letzte `TODO` (`develop.watch` mit `rebuild` für `./frontend/frontend.py`) und starte im zweiten Terminal `docker compose -f compose-develop.yml watch`. Ändere in `frontend/frontend.py` die Überschrift `Hello World` in `Hallo Docker`, speichere, warte auf die Meldungen im Watch-Terminal und lade `http://localhost:8080` neu. Mache die Änderung danach rückgängig, warte auf den nächsten Neubau und beende Watch mit `Strg+C`.
3. Entferne die Container mit `docker compose -f compose-develop.yml down`. Kopiere `compose-develop.yml` nach `compose.yml` und ändere darin: Frontend-Image `frontend:v2` mit `APP_VERSION=2.0.0`, zehn Replikas für das Frontend und nur den Container-Port `":80"`.
4. Starte `compose.yml` mit `docker compose up -d` (ohne `-f`, weil `compose.yml` der Standardname ist). Zeige die Container mit `docker compose ps` an, hole mit `docker compose port --index 1 frontend 80` und `--index 2` zwei Ports und öffne beide Adressen im Browser.
5. Verkleinere mit `docker compose up -d --scale frontend=3` auf drei Frontends, prüfe mit `ps` und entferne danach alles mit `docker compose down`.

## Checkpoint

- Aufgabe 1: `up` meldet für das Backend `Waiting` und `Healthy`, erst danach `Started` für das Frontend; `ps` zeigt erst `(health: starting)`, dann `(healthy)`.
- Aufgabe 2: Das Watch-Terminal meldet einen Neubau des Frontends; die Seite zeigt „Hallo Docker 1.0.0", nach dem Rückgängigmachen wieder „Hello World 1.0.0".
- Aufgabe 4: `ps` listet `hello-frontend-1` bis `hello-frontend-10` mit verschiedenen Rechner-Ports und `hello-backend-1 … (healthy)`; beide Browser-Seiten zeigen „Hello World 2.0.0" mit verschiedener Frontend-ID und IP.
- Aufgabe 5: `ps` listet nur noch `hello-frontend-1` bis `hello-frontend-3`.

## Abschlusskriterien

- `compose-develop.yml` startet das Frontend erst nach einem `healthy` Backend und baut bei Änderungen an `frontend.py` selbst neu.
- `compose.yml` startet zehn Frontends ohne Port-Konflikt.
- `frontend/frontend.py` ist wieder im Ausgangszustand; am Ende läuft kein Container der Hello-App.

## Erweiterung

Ändere im Healthcheck von `compose-develop.yml` den Port auf `81`, starte die Datei mit `up -d`, warte, bis `up` nach einigen Sekunden abbricht, und lies die Meldung sowie `docker compose -f compose-develop.yml ps -a`. Stelle Port `80` wieder her und entferne die Container mit `down`.

## Fallback

- Watch startet nicht oder Docker Desktop ist zu alt: Änderung speichern und `docker compose -f compose-develop.yml up -d --build` von Hand ausführen; die Wirkung ist dieselbe.
- Zu wenig Speicher für zehn Frontends: `replicas: 5` verwenden.
- Dateien kaputt: fertigen Stand kopieren (`cp -r examples/m04-compose/l02-multi-container/. playground/` im Ordner `project/`).
