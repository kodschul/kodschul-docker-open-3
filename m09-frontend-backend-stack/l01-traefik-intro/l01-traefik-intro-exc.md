# Lab 9.1 – Übung: Einführung in Traefik

**Dauer:** ca. 15 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — neue Datei `playground/hello/compose-traefik.yml` neben `compose.yml`; `compose.yml` aus Lab 4.3 bleibt unverändert.

## Vorbereitung

- Docker Desktop läuft; Terminal (macOS/Linux: Terminal, Windows: Git Bash, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Images `frontend:v2` und `backend:v1` vorhanden (`docker images`); falls nicht: im Ordner `project/` `bash build-images.sh`.
- Starter: `project/starters/m09-l01-compose-traefik.yml` · Arbeitsdatei: `project/playground/hello/compose-traefik.yml`.
- Port 80 frei: Kein anderes Programm (lokaler Webserver, Skype o. Ä.) belegt ihn.

## Aufgaben

1. Stoppe im Ordner `project/playground/hello` die laufende Hello-App mit `docker compose down` und kopiere den Starter als `compose-traefik.yml` in diesen Ordner.
2. Ergänze in `compose-traefik.yml` die TODOs 1–4 beim Dienst `traefik`: Docker-Provider einschalten, `exposedByDefault` auf `false`, Entrypoint `web` auf Port 80, Docker-Socket nur lesend.
3. Ergänze die TODOs 5 und 6: Labels für `frontend` (Router `app`, Host `app.localhost`) und `backend` (Router `api`, Host `api.app.localhost`), beide am Entrypoint `web`.
4. Starte den Stand mit `docker compose -f compose-traefik.yml up -d` und prüfe mit `docker compose -f compose-traefik.yml ps`, welche Dienste einen Port auf dem Rechner haben.
5. Öffne `http://app.localhost`, `http://api.app.localhost` und das Dashboard `http://localhost:8080`; suche dort unter **HTTP → Routers** die beiden Router. Rufe zum Vergleich `http://localhost` auf.

## Checkpoint

- `docker compose -f compose-traefik.yml ps` zeigt nur bei `traefik` die Ports `80` und `8080`; `frontend` und `backend` zeigen nur `80/tcp`.
- `http://app.localhost` zeigt „Hello World 2.0.0" mit Backend-Antwort und steigender Zahl „Aufrufe in access.log".
- `http://api.app.localhost` zeigt JSON mit `hostname`, `ip` und `now`.
- Das Dashboard listet `app@docker` und `api@docker` mit Status grün.
- `http://localhost` liefert `404 page not found`.

## Abschlusskriterien

- Frontend und Backend sind nur über Traefik erreichbar, jeweils unter ihrem Hostnamen.
- Im Dashboard ist für jeden Router die Rule und der Service zu sehen.

## Erweiterung

Starte drei Frontend-Container hinter demselben Router: `docker compose -f compose-traefik.yml up -d --scale frontend=3` (`--scale` startet die angegebene Anzahl Container eines Dienstes). Lade `http://app.localhost` mehrmals neu und beobachte die Frontend-IP. Öffne im Dashboard **HTTP → Services → frontend-hello** und zähle die Server.

## Fallback

- Port 80 belegt: in `compose-traefik.yml` bei `traefik` `- 8000:80` statt `- 80:80` eintragen und `http://app.localhost:8000` aufrufen.
- `app.localhost` öffnet nicht (ältere Browser, curl): `curl -H "Host: app.localhost" http://localhost`.
- Vollständiger Stand zum Vergleichen: im Ordner `project/` `cp -r examples/m09-frontend-backend-stack/l01-traefik-intro/. playground/`.
