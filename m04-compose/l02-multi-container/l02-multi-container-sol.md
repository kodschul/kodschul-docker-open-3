# Lab 4.2 – Lösung: Multi-Container-Anwendungen erstellen

Fertiger Stand: `project/examples/m04-compose/l02-multi-container/hello/` (`compose-develop.yml`, `compose.yml`). Alle Befehle im Ordner `project/playground/hello`. Getestet am 23.11.2026 mit Docker 29.9.3 und Compose 5.7.0; IDs, Zeiten und Ports weichen ab.

## Aufgabe 1: Healthcheck und depends_on

```yaml
# Entwicklungsmodus: Backend mit Healthcheck, Frontend wartet darauf, Watch baut bei Änderungen neu
services:
  frontend:
    image: frontend:v1
    build:
      context: frontend
      args:
        - APP_VERSION=1.0.0
    depends_on:
      backend:
        condition: service_healthy          # erst starten, wenn das Backend "healthy" ist
    ports:
      - 8080:80
    develop:                                # Aufgabe 2
      watch:
        - path: ./frontend/frontend.py
          action: rebuild                   # Datei geändert -> Image neu bauen, Container ersetzen

  backend:
    image: backend:v1
    build: backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 10s                         # alle 10 Sekunden prüfen
      timeout: 2s                           # Antwort muss nach 2 Sekunden da sein
      retries: 2                            # nach 2 Fehlschlägen: unhealthy
      start_period: 3s                      # Startzeit, in der Fehlschläge nicht zählen
```

```bash
docker compose -f compose-develop.yml up -d --build
```

```text
[+] Building 3.9s (21/21) FINISHED
…
[+] up 5/5
 ✔ Image frontend:v1          Built
 ✔ Image backend:v1           Built
 ✔ Network hello_default      Created
 ✔ Container hello-backend-1  Healthy
 ✔ Container hello-frontend-1 Started
```

Während des Starts steht beim Backend zunächst `Waiting`, nach der ersten erfolgreichen Prüfung `Healthy`; erst dann startet das Frontend. `--build` baut `frontend:v1` wieder mit `APP_VERSION=1.0.0` (nach Lab 4.1 enthielt es 1.1.0).

```bash
docker compose -f compose-develop.yml ps
```

Direkt nach dem Start (im zweiten Terminal):

```text
NAME              IMAGE        COMMAND               SERVICE   CREATED        STATUS                           PORTS
hello-backend-1   backend:v1   "python backend.py"   backend   1 second ago   Up 1 second (health: starting)   80/tcp
```

Das Frontend fehlt in der Liste: Es ist nur erstellt (`Created`) und wartet; `ps -a` würde es zeigen. Einige Sekunden später:

```text
NAME               IMAGE         COMMAND                SERVICE    CREATED          STATUS                    PORTS
hello-backend-1    backend:v1    "python backend.py"    backend    14 seconds ago   Up 13 seconds (healthy)   80/tcp
hello-frontend-1   frontend:v1   "python frontend.py"   frontend   14 seconds ago   Up 10 seconds             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
```

Das Frontend lief im Test rund 4 Sekunden nach dem Backend an: so lange dauerte es bis zum ersten erfolgreichen Healthcheck. Während des Wartens zeigt `up` beim Backend `Waiting`, danach `Healthy`.

## Aufgabe 2: Compose Watch

```bash
docker compose -f compose-develop.yml watch
```

```text
[+] up 3/3
 ✔ Image frontend:v1          Built
 ✔ Container hello-frontend-1 Running
 ✔ Container hello-backend-1  Healthy
Watch enabled
```

`watch` baut die Images beim Start einmal (aus dem Cache, daher schnell) und lässt laufende Container weiterlaufen.

Änderung in `frontend/frontend.py` (Zeile mit `<h1>`):

```python
  <h1>Hallo Docker {APP_VERSION}</h1>
```

Nach dem Speichern meldet das Watch-Terminal:

```text
Rebuilding service(s) ["frontend"] after changes were detected...
Image frontend:v1 Building
Image frontend:v1 Built
service(s) ["frontend"] successfully built
Container hello-frontend-1 Recreate
Container hello-frontend-1 Recreated
```

`http://localhost:8080` zeigt „Hallo Docker 1.0.0" und eine neue Frontend-ID (neuer Container). Nach dem Rückgängigmachen (`Hello World`) baut Watch erneut, die Seite zeigt wieder „Hello World 1.0.0". `Strg+C` beendet das Beobachten; die Container laufen weiter.

## Aufgabe 3: compose.yml mit zehn Frontends

```bash
docker compose -f compose-develop.yml down
cp compose-develop.yml compose.yml
```

```yaml
# Hello-App mit 10 Frontends; jeder Container bekommt einen zufälligen freien Rechner-Port
services:
  frontend:
    image: frontend:v2
    build:
      context: frontend
      args:
        - APP_VERSION=2.0.0
    depends_on:
      backend:
        condition: service_healthy
    deploy:
      replicas: 10
    ports:
      - ":80"                               # nur Container-Port: Docker wählt den Rechner-Port
    develop:
      watch:
        - path: ./frontend/frontend.py
          action: rebuild

  backend:
    image: backend:v1
    build: backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 10s
      timeout: 2s
      retries: 2
      start_period: 3s
```

`":80"` steht in Anführungszeichen, weil ein YAML-Wert mit führendem Doppelpunkt sonst missverstanden werden kann.

## Aufgabe 4: zehn Frontends starten

```bash
docker compose up -d
docker compose ps
```

```text
NAME                IMAGE         COMMAND                SERVICE    CREATED         STATUS                   PORTS
hello-backend-1     backend:v1    "python backend.py"    backend    8 seconds ago   Up 8 seconds (healthy)   80/tcp
hello-frontend-1    frontend:v2   "python frontend.py"   frontend   8 seconds ago   Up 4 seconds             0.0.0.0:65072->80/tcp, [::]:65072->80/tcp
hello-frontend-10   frontend:v2   "python frontend.py"   frontend   8 seconds ago   Up 3 seconds             0.0.0.0:65082->80/tcp, [::]:65082->80/tcp
hello-frontend-2    frontend:v2   "python frontend.py"   frontend   8 seconds ago   Up 4 seconds             0.0.0.0:65073->80/tcp, [::]:65073->80/tcp
…
hello-frontend-9    frontend:v2   "python frontend.py"   frontend   8 seconds ago   Up 3 seconds             0.0.0.0:65081->80/tcp, [::]:65081->80/tcp
```

```bash
docker compose port --index 1 frontend 80
docker compose port --index 2 frontend 80
```

```text
0.0.0.0:65072
0.0.0.0:65073
```

`http://localhost:65072` und `http://localhost:65073` zeigen beide „Hello World 2.0.0", aber verschiedene Frontends (im Test `d647f5f89694 (172.19.0.3)` und `f410c4c3c69e (172.19.0.4)`). Die Port-Nummern vergibt Docker zufällig; sie weichen auf jedem Rechner ab.

## Aufgabe 5: auf drei Frontends verkleinern

```bash
docker compose up -d --scale frontend=3
```

```text
[+] up 11/11
 ✔ Container hello-frontend-1  Running
 ✔ Container hello-frontend-2  Running
 ✔ Container hello-frontend-3  Running
 ✔ Container hello-backend-1   Healthy
 ✔ Container hello-frontend-6  Removed
 ✔ Container hello-frontend-8  Removed
 …
 ✔ Container hello-frontend-10 Removed
```

`docker compose ps` listet danach `hello-frontend-1` bis `-3` und das Backend. `--scale` gilt nur für diesen Aufruf; ein späteres `docker compose up -d` startet wieder zehn.

```bash
docker compose down
```

## Erweiterung

Mit Port `81` im Healthcheck scheitert jede Prüfung (`curl: (7) Failed to connect to localhost:81 after 0 ms: Could not connect to server`). Nach zwei Fehlschlägen in Folge (`retries: 2`) wird das Backend `unhealthy`, im Test nach rund 13 Sekunden; das Frontend startet nicht:

```text
[+] up 3/3
 ✔ Network hello_default      Created
 ✘ Container hello-backend-1  Error dependency backend failed to start
 ✘ Container hello-frontend-1 not started: condition "service_healthy" of ...
dependency failed to start: container hello-backend-1 is unhealthy
```

`docker compose -f compose-develop.yml ps -a` zeigt `Up 13 seconds (unhealthy)` beim Backend und `Created` beim Frontend. Die letzte Prüfung liest `docker inspect --format '{{json .State.Health}}' hello-backend-1`. Mit Port `80` und `up -d` ist alles wieder `healthy`.
