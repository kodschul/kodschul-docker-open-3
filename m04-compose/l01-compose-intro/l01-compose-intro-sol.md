# Lab 4.1 – Lösung: Einführung in Docker Compose

Fertiger Stand: `project/examples/m04-compose/l01-compose-intro/hello/`. Alle Befehle im Ordner `project/playground/hello`. Getestet am 23.11.2026 mit Docker 29.9.3 und Compose 5.7.0; IDs, Zeiten und IP-Adressen weichen ab.

## Aufgabe 1: compose-simple.yml starten

```bash
docker compose -f compose-simple.yml up -d
```

```text
[+] up 4/4
 ✔ Network hello_default   Created
 ✔ Container hello-web-1   Started
 ✔ Container hello-extra-2 Started
 ✔ Container hello-extra-1 Started
```

```bash
docker compose -f compose-simple.yml ps
```

```text
NAME            IMAGE               COMMAND                  SERVICE   CREATED        STATUS                  PORTS
hello-extra-1   nginx:1.30-alpine   "/docker-entrypoint.…"   extra     1 second ago   Up Less than a second   80/tcp
hello-extra-2   nginx:1.30-alpine   "/docker-entrypoint.…"   extra     1 second ago   Up Less than a second   80/tcp
hello-web-1     nginx:1.30-alpine   "/docker-entrypoint.…"   web       1 second ago   Up Less than a second   0.0.0.0:9000->80/tcp, [::]:9000->80/tcp
```

`http://localhost:9000` zeigt „Willkommen – Diese Seite liefert nginx aus dem Ordner web/ aus." aus dem Bind Mount `./web`. Die beiden `extra`-Container haben keinen veröffentlichten Port (`80/tcp` ohne Pfeil).

```bash
docker compose -f compose-simple.yml down
```

```text
[+] down 4/4
 ✔ Container hello-extra-1 Removed
 ✔ Container hello-extra-2 Removed
 ✔ Container hello-web-1   Removed
 ✔ Network hello_default   Removed
```

## Aufgabe 2: compose-minimal.yml vervollständigen

```yaml
# Kleinste Compose-Datei der Hello-App: beide Images aus den Dockerfiles bauen
services:
  frontend:
    build: frontend                         # Ordner mit Dockerfile (Build-Kontext)
    ports:
      - 8080:80

  backend:
    build: backend                          # kein Port nach außen: nur das Frontend fragt das Backend
```

```bash
docker compose -f compose-minimal.yml up -d
```

```text
[+] Building 6.4s (21/21) FINISHED
…
[+] up 5/5
 ✔ Image hello-frontend       Built
 ✔ Image hello-backend        Built
 ✔ Network hello_default      Created
 ✔ Container hello-frontend-1 Started
 ✔ Container hello-backend-1  Started
```

Die Images fehlen noch, deshalb baut `up` sie zuerst. `http://localhost:8080` zeigt „Hello World 0.0.0" (kein Build-Argument, also der Standardwert aus dem Dockerfile) und unter **Backend** z. B. `0fdea9fe53cc (172.19.0.2) um 22:16:14` (siehe Bild in der Theorie). Das Frontend erreicht `http://backend:80` über den Dienstnamen im Projektnetzwerk.

```bash
docker compose -f compose-minimal.yml logs
```

```text
backend-1  | Hello-Backend auf Port 80
backend-1  |  * Serving Flask app 'backend'
backend-1  |  * Debug mode: off
backend-1  |  * Running on all addresses (0.0.0.0)
backend-1  |  * Running on http://127.0.0.1:80
backend-1  |  * Running on http://172.19.0.2:80
backend-1  | Press CTRL+C to quit
backend-1  | 172.19.0.3 - - [23/Nov/2026 22:16:14] "GET / HTTP/1.1" 200 -
frontend-1  | Hello-Frontend 0.0.0 auf Port 80
frontend-1  |  * Serving Flask app 'frontend'
…
```

Jede Seite im Frontend erzeugt eine Anfrage im Backend; Flask-Warnungen zum Entwicklungsserver sind hier unwichtig.

```bash
docker images
```

```text
IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
backend:v1              8286084874f1        103MB           25MB   U
frontend:v1             cbf0f67e6ffb        108MB         26.1MB
frontend:v2             6b7c18dbc0fa        108MB         26.1MB
hello-backend:latest    0b737b4cfa4f        103MB           25MB   U
hello-frontend:latest   1ead2bd5cb53        108MB         26.1MB   U
…
```

Docker 29 zeigt `docker images` in dieser Form; `U` in `EXTRA` bedeutet: ein Container nutzt das Image.

Ohne `image:` heißen die Images `<projekt>-<dienst>` mit Tag `latest`. Danach `docker compose -f compose-minimal.yml down`.

## Aufgabe 3: compose-with-custom-image.yml

```bash
docker compose -f compose-with-custom-image.yml up -d
docker compose -f compose-with-custom-image.yml ps
```

```text
NAME               IMAGE         COMMAND                SERVICE    CREATED        STATUS                  PORTS
hello-backend-1    backend:v1    "python backend.py"    backend    1 second ago   Up Less than a second   80/tcp
hello-backend-2    backend:v1    "python backend.py"    backend    1 second ago   Up Less than a second   80/tcp
hello-frontend-1   frontend:v1   "python frontend.py"   frontend   1 second ago   Up Less than a second   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
```

- `frontend:v1` und `backend:v1` existieren seit Lab 3.2, deshalb baut `up` nicht, sondern startet die vorhandenen Images.
- Die Seite ist hellblau (`APP_COLOR=lightblue` aus `environment`, wirkt beim Start) und zeigt „Hello World 1.0.0".
- Beim Neuladen wechselt die Backend-Zeile zwischen zwei Container-IDs (im Test `0419a0114090` und `ef672e91dd59`): Der Name `backend` führt im Projektnetzwerk zu beiden Kopien.

Danach `docker compose -f compose-with-custom-image.yml down`.

## Aufgabe 4: compose-with-config.yml vervollständigen

```yaml
# Werte aus .env (Platzhalter ${...}) und aus app-config.env (env_file)
services:
  frontend:
    image: frontend:v1
    build:
      context: ./frontend
      args:
        - APP_VERSION=${FE_VERSION}         # aus .env, nur beim Bauen
    ports:
      - ${FE_PORT}:80                       # aus .env
    env_file:
      - app-config.env                      # Laufzeit-Variablen für den Container

  backend:
    image: backend:v1
    build: backend
    env_file:
      - app-config.env
    deploy:
      replicas: ${BE_REPLICAS}              # aus .env
```

```bash
docker compose -f compose-with-config.yml config
```

```text
name: hello
services:
  backend:
    build:
      context: …/playground/hello/backend
      dockerfile: Dockerfile
    deploy:
      replicas: 3
    environment:
      APP_COLOR: lightgreen
    image: backend:v1
    networks:
      default: null
  frontend:
    build:
      context: …/playground/hello/frontend
      dockerfile: Dockerfile
      args:
        APP_VERSION: 1.1.0
    environment:
      APP_COLOR: lightgreen
    image: frontend:v1
    networks:
      default: null
    ports:
      - mode: ingress
        target: 80
        published: "8080"
        protocol: tcp
networks:
  default:
    name: hello_default
```

`config` zeigt alle eingesetzten Werte, macht aus `env_file` die Einträge unter `environment` und ergänzt Standardwerte wie das Netzwerk `default`.

```bash
docker compose -f compose-with-config.yml up -d --build
```

```text
[+] up 6/6
 ✔ Image backend:v1          Built
 ✔ Image frontend:v1         Built
 ✔ Container hello-backend-1  Started
 ✔ Container hello-backend-2  Started
 ✔ Container hello-backend-3  Started
 ✔ Container hello-frontend-1 Started
```

Ohne `--build` startet Compose das vorhandene `frontend:v1`: Die Seite ist zwar hellgrün (`env_file` wirkt beim Start), zeigt aber „Hello World 1.0.0". Mit `--build` entsteht das Image neu mit `APP_VERSION=1.1.0`; die Seite ist hellgrün und zeigt „Hello World 1.1.0", `ps` listet `hello-backend-1` bis `hello-backend-3`.

Das Image `frontend:v1` enthält danach Version 1.1.0. Lab 4.2 baut es mit `APP_VERSION=1.0.0` neu (`up -d --build`); alternativ stellt `bash build-images.sh` im Ordner `project/` alle drei Hello-Images wieder her.

## Aufgabe 5: Werte in .env ändern

```bash
# .env
FE_PORT=8081
FE_VERSION=1.1.0
BE_REPLICAS=2
```

```bash
docker compose -f compose-with-config.yml up -d
```

```text
[+] up 4/4
 ✔ Container hello-backend-1  Running
 ✔ Container hello-backend-2  Running
 ✔ Container hello-backend-3  Removed
 ✔ Container hello-frontend-1 Started
```

Compose vergleicht den gewünschten mit dem laufenden Zustand: Ein Backend wird entfernt, das Frontend mit neuem Port neu erstellt, die übrigen Container bleiben. `http://localhost:8081` zeigt die Seite, `http://localhost:8080` antwortet nicht mehr.

```bash
docker compose -f compose-with-config.yml down
docker compose -f compose-with-config.yml ps      # leer
```

## Erweiterung

```bash
mv .env env.bak
docker compose -f compose-with-config.yml config
```

```text
WARN[0000] The "FE_VERSION" variable is not set. Defaulting to a blank string.
WARN[0000] The "FE_PORT" variable is not set. Defaulting to a blank string.
WARN[0000] The "BE_REPLICAS" variable is not set. Defaulting to a blank string.
error while interpolating services.backend.deploy.replicas: failed to cast to expected type: strconv.Atoi: parsing "": invalid syntax
```

Ein leerer Text ist keine Zahl, deshalb bricht Compose bei `replicas` ab. Danach `mv env.bak .env`.
