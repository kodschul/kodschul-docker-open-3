# Hello-App und Übungsprojekte

Die Hello-App besteht aus zwei kleinen Python/Flask-Diensten und wächst im Kurs vom eigenen Image bis zum Swarm-Stack. Daneben entstehen kleine Übungs-Apps (Wetter-App, Rezeptbuch, Time-App, Monitoring-Stack). Handouts: [`../README.md`](../README.md).

| Dienst | Antwort | Wichtige Umgebungsvariablen |
| --- | --- | --- |
| `backend` | JSON mit `hostname`, `ip` und `now` auf Port 80 | – |
| `frontend` | HTML-Seite mit Version, Farbe, Container, IP, Backend-Antwort und „Aufrufe in access.log" | `APP_DISPLAY_VERSION` (aus `ARG APP_VERSION`), `APP_COLOR`, `BACKEND_URL`, `DATA_DIR` |

Images im Kurs: `frontend:v1` (Version 1.0.0), `frontend:v2` (Version 2.0.0), `backend:v1`.

## Ordner

```text
project/
├── build-images.sh      baut frontend:v1, frontend:v2 und backend:v1 neu (bash build-images.sh)
├── playground/          Arbeitsbereich
│   ├── hello/           Hello-App: frontend/, backend/, web/, test.txt; ab Lab 3.2 Dockerfiles, ab Lab 4.1 Compose-Dateien
│   └── <app>/           weitere Übungs-Apps, entstehen aus den Startern
├── starters/            Startdateien der Übungen (mNN-lNN-…), mit TODO-Markierungen
├── examples/            fertiger Stand je Lab: examples/<modul>/<lab>/, Pfade wie in playground/
└── variants/            absichtlich fehlerhafte Dateien für Lab 7.1
```

## Arbeitsweise je Lab

1. Starter aus `starters/` nach `playground/` kopieren, die TODOs ergänzen.
2. Im Ordner der App arbeiten, z. B. `cd playground/hello`, dann `docker compose up -d`.
3. Mit dem fertigen Stand in `examples/<modul>/<lab>/` vergleichen.

Alle Befehle laufen in der Kurs-Shell `bash` (macOS/Linux: Terminal, Windows: Git Bash).

## Stand wiederherstellen

```bash
cd project

# Images fehlen (neuer Rechner, Speicher aufgeräumt)
bash build-images.sh

# Stand eines Labs herstellen, z. B. nach Lab 4.3
cp -r examples/m04-compose/l03-volumes/. playground/
```

## Labs, Beispiele und Starter

| Lab | Beispiel (`examples/`) | Starter (`starters/`) |
| --- | --- | --- |
| 1.1–2.3 | – (nur Befehle; Lab 2.2 nutzt `playground/hello/test.txt`) | – |
| 3.1 Aufbau und Speichern von Images | [`m03-images-registries/l01-image-layers/`](examples/m03-images-registries/l01-image-layers/) | [`m03-l01-image-layers/`](starters/m03-l01-image-layers/) |
| 3.2 Eigene Images erstellen und verwalten | [`m03-images-registries/l02-own-images/`](examples/m03-images-registries/l02-own-images/) (Wetter, Pizza, Hello-Dockerfiles) | [`m03-l02-own-images/`](starters/m03-l02-own-images/) |
| 3.3 Lokale Registry und Image-Verwaltung | [`m03-images-registries/l03-local-registry/`](examples/m03-images-registries/l03-local-registry/) | [`m03-l03-recipe-page/`](starters/m03-l03-recipe-page/) |
| 4.1 Einführung in Docker Compose | [`m04-compose/l01-compose-intro/`](examples/m04-compose/l01-compose-intro/) | [`m04-l01-compose-intro/`](starters/m04-l01-compose-intro/) |
| 4.2 Multi-Container-Anwendungen | [`m04-compose/l02-multi-container/`](examples/m04-compose/l02-multi-container/) | [`m04-l02-multi-container/`](starters/m04-l02-multi-container/) |
| 4.3 Datenvolumes und Persistenz | [`m04-compose/l03-volumes/`](examples/m04-compose/l03-volumes/) (Hello `compose.yml`, Rezeptbuch) | [`m04-l03-recipe-book/`](starters/m04-l03-recipe-book/) |
| 4.4–6.1 | – (Stand von Lab 4.3; Netzwerke per Befehl) | – |
| 6.2 Isolierung und Ressourcen | [`m06-security/l02-isolation-limits/`](examples/m06-security/l02-isolation-limits/) | – |
| 6.3 Security Scanning | [`m06-security/l03-security-scanning/`](examples/m06-security/l03-security-scanning/) | – |
| 7.1 Docker Debugging | – | Fehlerbilder in [`variants/m07-l01-debugging/`](variants/m07-l01-debugging/) |
| 7.2 Logging und Monitoring | [`m07-debugging/l02-logging-monitoring/`](examples/m07-debugging/l02-logging-monitoring/) (Monitoring-Stack, ELK-Demo) | [`m07-l02-monitoring/`](starters/m07-l02-monitoring/) |
| 8.1 Eigene Repositories | [`m08-repositories/l01-own-repositories/`](examples/m08-repositories/l01-own-repositories/) | [`m08-l01-registry-compose.yml`](starters/m08-l01-registry-compose.yml) |
| 8.2 Verteilte Anwendungen | [`m08-repositories/l02-distributed-apps/`](examples/m08-repositories/l02-distributed-apps/) | [`m08-l02-compose-registry.yml`](starters/m08-l02-compose-registry.yml) |
| 9.1 Einführung in Traefik | [`m09-frontend-backend-stack/l01-traefik-intro/`](examples/m09-frontend-backend-stack/l01-traefik-intro/) | [`m09-l01-compose-traefik.yml`](starters/m09-l01-compose-traefik.yml) |
| 9.2 Traefik in der Praxis | [`m09-frontend-backend-stack/l02-traefik-practice/`](examples/m09-frontend-backend-stack/l02-traefik-practice/) (Time-App) | [`m09-l02-time-app/`](starters/m09-l02-time-app/) |
| 9.3 Multistage Dockerfiles | [`m09-frontend-backend-stack/l03-multistage/`](examples/m09-frontend-backend-stack/l03-multistage/) (Todo-App) | [`m09-l03-multistage/`](starters/m09-l03-multistage/) |
| 10.1 Grundlagen von Docker Swarm | – (nur Befehle) | – |
| 10.3 Deployment in die Orchestrierungsplattform | [`m10-orchestration/l03-swarm-deployment/`](examples/m10-orchestration/l03-swarm-deployment/) (`stack.yml`) | – |

## Ports im Kurs

| Port | Dienst | Lab |
| --- | --- | --- |
| 8080–8082 | nginx-Übungen, Hello-Frontend | 2.1, 3.2, ab 4.1 |
| 9000 | `compose-simple.yml` | 4.1 |
| 3000 | Rezeptbuch, Todo-App, Grafana | 4.3, 9.3, 7.2 |
| 5001 | eigene Registry | 3.3, 8.1, 8.2 |
| 8701–8704 | Fehlerbilder | 7.1 |
| 8081, 9090, 9100 | cAdvisor, Prometheus, Node Exporter | 7.2 |
| 80, 8080 | Traefik und Dashboard | 9.1, 9.2 |
| 8001, 999 | Swarm-Service `web`, Hello-Stack | 10.1, 10.3 |

Vor einem neuen Lab laufende Stände mit `docker compose down` beenden, damit kein Port doppelt belegt ist.
