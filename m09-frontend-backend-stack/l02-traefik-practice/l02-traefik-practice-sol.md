# Lab 9.2 – Lösung: Traefik in der Praxis

Fertiger Stand: `project/examples/m09-frontend-backend-stack/l02-traefik-practice/time-app/`.

## Aufgabe 1: Starter kopieren

```bash
cd ~/kurs/kodschul-docker-open-3/project      # Pfad an den eigenen Kursordner anpassen
cp -r starters/m09-l02-time-app playground/time-app
cd playground/time-app
ls -R
```

```text
backend  compose.yml  frontend

./backend:
Dockerfile  backend.py  requirements.txt

./frontend:
Dockerfile  index.html
```

## Aufgabe 2: Backend-Abhängigkeiten und Dockerfile

`backend/requirements.txt`:

```text
flask>=3.1,<4
flask-cors>=6,<7
redis>=8,<9
```

Die Paketnamen sind die Namen auf PyPI (`flask-cors` mit Bindestrich); im Code heißt das Modul `flask_cors`. Die Versionsbereiche erlauben Fehlerbehebungen, aber keinen Sprung auf die nächste Hauptversion.

`backend/Dockerfile`:

```dockerfile
FROM python:3.13-alpine
WORKDIR /code
ENV FLASK_APP=backend.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--debug"]
```

## Aufgabe 3: Frontend-Dockerfile und Compose

`frontend/Dockerfile`:

```dockerfile
FROM nginx:1.30-alpine
COPY index.html /usr/share/nginx/html/index.html
```

`compose.yml` (ergänzte Stellen markiert):

```yaml
services:
  frontend:
    build: ./frontend
    labels:
      - traefik.enable=true
      - traefik.http.routers.frontend.rule=Host(`localhost`) && PathPrefix(`/`)     # TODO 1
      - traefik.http.routers.frontend.entrypoints=web                               # TODO 1

  backend:
    build: ./backend
    depends_on:
      - redis
    labels:                                                                         # TODO 2
      - traefik.enable=true
      - traefik.http.routers.backend.rule=Host(`localhost`) && PathPrefix(`/api`)
      - traefik.http.routers.backend.entrypoints=web

  redis:
    image: redis:8-alpine

  traefik:
    image: traefik:v3.8
    command:
      - --log.level=DEBUG
      - --api.insecure=true
      - --providers.docker=true
      - --providers.docker.exposedByDefault=false
      - --entryPoints.web.address=:80
    ports:                                                                          # TODO 3
      - 80:80
      - 8080:8080
    volumes:                                                                        # TODO 3
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## Aufgabe 4: Bauen, starten, testen

```bash
docker compose up -d --build
docker compose ps
```

```text
NAME                  IMAGE                COMMAND                  SERVICE    CREATED          STATUS          PORTS
time-app-backend-1    time-app-backend     "flask run --debug"      backend    12 seconds ago   Up 10 seconds   5000/tcp
time-app-frontend-1   time-app-frontend    "/docker-entrypoint.…"   frontend   12 seconds ago   Up 10 seconds   80/tcp
time-app-redis-1      redis:8-alpine       "docker-entrypoint.s…"   redis      12 seconds ago   Up 11 seconds   6379/tcp
time-app-traefik-1    traefik:v3.8         "/entrypoint.sh --lo…"   traefik    12 seconds ago   Up 11 seconds   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
```

Ohne `image:` benennt Compose die gebauten Images `<Projekt>-<Dienst>`, hier `time-app-backend` und `time-app-frontend`.

<img src="../../assets/images/m09/time-app.png" alt="Browser mit http://localhost: Time-App mit den Knöpfen Get current time und Get last time, darunter die Antworten Current time und Last time mit Datum und Uhrzeit" width="520">

_Quelle: eigener Screenshot, Time-App hinter Traefik, 23.11.2026._

```bash
curl http://localhost/api/v1/time
curl http://localhost/api/v1/last_time
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/
```

```text
Current time: 2026-11-23 22:28:08
Last time: 2026-11-23 22:28:08
200
```

- `/` liefert die Seite aus nginx, `/api/…` das Backend; beide Router passen auf `/api/v1/time`, die längere Backend-Regel gewinnt.
- Die Zeit ist UTC (im Winter eine Stunde hinter der deutschen Uhrzeit), weil im Image keine Zeitzone gesetzt ist.
- Vor dem ersten Aufruf von `/api/v1/time` liefert `/api/v1/last_time` eine leere Antwort (`""`), weil in Redis noch nichts steht.

## Aufgabe 5: Wert in Redis, Neustart des Backends

```bash
docker compose exec redis redis-cli get last_time
```

```text
"2026-11-23 22:28:08"
```

```bash
docker compose restart backend
curl http://localhost/api/v1/last_time
```

```text
Last time: 2026-11-23 22:28:08
```

Der Wert liegt im Redis-Container, nicht im Backend; der Neustart ändert nichts daran. Würde `redis` neu erstellt (`docker compose down`, `up`), wäre er weg: Redis hält die Daten hier nur im Arbeitsspeicher, ohne Volume (Lab 4.3).

## Erweiterung: drei Backend-Container

```bash
docker compose up -d --scale backend=3
for i in 1 2 3; do curl -s http://localhost/api/v1/time; echo; curl -s http://localhost/api/v1/last_time; echo; done
```

```text
Current time: 2026-11-23 22:28:27
Last time: 2026-11-23 22:28:27
Current time: 2026-11-23 22:28:27
Last time: 2026-11-23 22:28:27
Current time: 2026-11-23 22:28:27
Last time: 2026-11-23 22:28:27
```

Traefik verteilt die Anfragen reihum auf drei Backend-Container; alle lesen und schreiben denselben Redis. **HTTP → Services → backend-time-app** zeigt drei Server. Aufräumen am Ende: `docker compose down`.
