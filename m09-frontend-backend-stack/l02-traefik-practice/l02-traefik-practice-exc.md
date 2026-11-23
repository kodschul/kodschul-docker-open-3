# Lab 9.2 – Übung: Traefik in der Praxis

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Time-App entsteht in einem eigenen Ordner `playground/time-app/`.

## Vorbereitung

- Docker Desktop läuft; Terminal im Ordner `project/` (Windows: Git Bash, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Starter: Ordner `project/starters/m09-l02-time-app/` · Arbeitsordner: `project/playground/time-app/`.
- Im Starter fertig: `backend/backend.py` und `frontend/index.html`. Zu ergänzen (Markierung `TODO`): `backend/requirements.txt`, `backend/Dockerfile`, `frontend/Dockerfile`, `compose.yml`.
- Traefik aus Lab 9.1 gestoppt: im Ordner `playground/hello` `docker compose -f compose-traefik.yml down`.

## Aufgaben

1. Kopiere den Starter nach `playground/time-app` (`cp -r starters/m09-l02-time-app playground/time-app`) und wechsle in diesen Ordner.
2. Ergänze `backend/requirements.txt` um die drei Pakete, die `backend.py` importiert, und schreibe `backend/Dockerfile` nach den sieben TODOs.
3. Schreibe `frontend/Dockerfile` (nginx liefert `index.html` aus) und ergänze in `compose.yml` die Router-Labels für `frontend` und `backend` sowie Ports und Docker-Socket bei `traefik`.
4. Baue und starte den Stack mit `docker compose up -d --build`. Öffne `http://localhost` und klicke beide Knöpfe; rufe danach `http://localhost/api/v1/time` und `http://localhost/api/v1/last_time` direkt auf.
5. Lies den gespeicherten Wert direkt in Redis mit `docker compose exec redis redis-cli get last_time`. Starte das Backend mit `docker compose restart backend` neu und rufe `http://localhost/api/v1/last_time` erneut auf.

## Checkpoint

- `docker compose ps` zeigt vier laufende Dienste; nur `traefik` hat Ports auf dem Rechner (80, 8080).
- Der Knopf „Get current time" zeigt `Current time: <Datum Uhrzeit>`, „Get last time" danach `Last time: <dieselbe Zeit>`.
- `redis-cli get last_time` gibt dieselbe Zeit aus.
- Nach dem Neustart des Backends liefert `/api/v1/last_time` weiter den gespeicherten Wert.
- Das Dashboard `http://localhost:8080` zeigt die Router `frontend@docker` und `backend@docker`.

## Abschlusskriterien

- Traefik, Frontend, Backend und Redis laufen als ein Compose-Projekt, erreichbar nur über `http://localhost`.
- Anfragen unter `/api` landen beim Backend, alle anderen beim Frontend.

## Erweiterung

Starte drei Backend-Container mit `docker compose up -d --scale backend=3`. Rufe `/api/v1/time` und `/api/v1/last_time` abwechselnd mehrmals auf: Der gespeicherte Wert bleibt stimmig, obwohl jede Anfrage bei einem anderen Backend-Container landen kann. Prüfe im Dashboard unter **HTTP → Services** die Zahl der Server.

## Fallback

- Port 80 belegt: bei `traefik` `- 8000:80` eintragen und `http://localhost:8000` aufrufen (die Seite nutzt relative Adressen und funktioniert auch so).
- Fertiger Stand zum Vergleichen oder Weiterarbeiten: im Ordner `project/` `cp -r examples/m09-frontend-backend-stack/l02-traefik-practice/. playground/` (überschreibt `playground/time-app`).
- Fehlersuche: `docker compose logs backend` und `docker compose logs traefik` (Traefik läuft mit `--log.level=DEBUG`).
