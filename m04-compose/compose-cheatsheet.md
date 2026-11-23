# Docker Compose Cheatsheet

Befehle und Syntax aus Modul 4. Alle `docker compose`-Befehle wirken auf das Projekt im aktuellen Ordner (Projektname = Ordnername).

## Projekt starten und stoppen

| Befehl | Wirkung |
| --- | --- |
| `docker compose up` | Dienste starten, Ausgaben im Terminal (`Strg+C` stoppt) |
| `docker compose up -d` | Dienste im Hintergrund starten; fehlende Images werden gebaut |
| `docker compose up -d --build` | Images vor dem Start neu bauen |
| `docker compose up -d --build frontend` | nur den Dienst `frontend` neu bauen und ersetzen |
| `docker compose up -d --build --no-deps frontend` | dasselbe, Dienste aus `depends_on` bleiben unberührt |
| `docker compose up -d --scale frontend=3` | Anzahl der Container eines Dienstes für diesen Aufruf festlegen |
| `docker compose up -d --remove-orphans` | Container entfernen, die nicht mehr in der Datei stehen |
| `docker compose down` | Container und Netzwerk entfernen; Images und Volumes bleiben |
| `docker compose down -v` | zusätzlich die Named Volumes des Projekts löschen |
| `docker compose -f compose-minimal.yml up -d` | andere Compose-Datei verwenden; `-f` steht vor dem Unterbefehl |

## Status, Logs und Konfiguration

| Befehl | Wirkung |
| --- | --- |
| `docker compose ps` | Container des Projekts mit Status (`healthy`) und Ports |
| `docker compose ps -a` | auch gestoppte und nur erstellte Container |
| `docker compose logs` | Ausgaben aller Dienste |
| `docker compose logs -f frontend` | Ausgaben eines Dienstes live mitlesen |
| `docker compose port --index 2 frontend 80` | Rechner-Port der zweiten Kopie für Container-Port 80 |
| `docker compose exec frontend cat /data/access.log` | Befehl in einem laufenden Dienst-Container ausführen |
| `docker compose config` | Compose-Datei mit allen eingesetzten Werten aus `.env` anzeigen |
| `docker compose version` | Compose-Version (v2/v5; `docker-compose` ist v1 und veraltet) |

## Entwicklungsmodus

| Befehl | Wirkung |
| --- | --- |
| `docker compose watch` | Dienste starten und Dateien nach `develop.watch` beobachten |
| `docker compose up --watch` | dasselbe, zusätzlich mit den Logs der Anwendung |

## Volumes

| Befehl | Wirkung |
| --- | --- |
| `docker volume create mein_db_data` | Named Volume anlegen |
| `docker volume ls` | alle Volumes auflisten |
| `docker volume inspect mein_db_data` | Details: Treiber, `Mountpoint`, Labels |
| `docker volume rm mein_db_data` | Volume löschen (kein Container darf es nutzen) |
| `docker volume prune` | alle ungenutzten Volumes löschen (Vorsicht) |
| `docker run -v mein_db_data:/var/lib/mysql …` | Named Volume einbinden |
| `docker run -v "$(pwd)/web":/usr/share/nginx/html …` | Bind Mount: Ordner des Rechners einbinden |

## Compose-Datei: Dienst-Optionen

```yaml
services:
  frontend:
    image: frontend:v2                 # Image-Name (zum Ziehen oder für das gebaute Image)
    build:
      context: ./frontend              # Ordner mit Dockerfile; Kurzform: build: frontend
      args:
        - APP_VERSION=${FE_VERSION}    # Build-Argument, Wert aus .env
    ports:
      - 8080:80                        # Rechner-Port:Container-Port; ":80" = zufälliger Rechner-Port
    volumes:
      - hello-data:/data               # Named Volume
      - ./web:/usr/share/nginx/html    # Bind Mount (Pfad beginnt mit . oder /)
    environment:
      - APP_COLOR=lightblue            # Umgebungsvariable im Container
    env_file:
      - app-config.env                 # Umgebungsvariablen aus Datei
    deploy:
      replicas: 10                     # Anzahl gleicher Container
    depends_on:
      backend:
        condition: service_healthy     # service_started | service_healthy | service_completed_successfully
    develop:
      watch:
        - path: ./frontend/frontend.py
          action: rebuild              # sync (mit target:) | rebuild | sync+restart

  backend:
    build: backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 10s
      timeout: 2s
      retries: 2
      start_period: 3s

volumes:
  hello-data:                          # Named Volumes auf oberster Ebene anlegen
```

## Werte und Variablen

| Stelle | Gelesen von | Zeitpunkt |
| --- | --- | --- |
| `.env` + `${VAR}` / `${VAR:-standard}` | Compose | beim Einlesen der Compose-Datei |
| `environment:` / `env_file:` | Container | beim Start |
| `build.args` | Dockerfile (`ARG`) | beim Bauen |

## Namen, die Compose vergibt

| Objekt | Schema | Beispiel |
| --- | --- | --- |
| Container | `<projekt>-<dienst>-<nr>` | `hello-frontend-1` |
| Netzwerk | `<projekt>_default` | `hello_default` |
| Named Volume | `<projekt>_<volume>` | `hello_hello-data` |
| gebautes Image ohne `image:` | `<projekt>-<dienst>` | `hello-frontend` |
| Hostname eines Dienstes im Projektnetzwerk | `<dienst>` | `http://backend:80` |

Dateinamen, die Compose ohne `-f` findet: `compose.yaml`, `compose.yml`, `docker-compose.yaml`, `docker-compose.yml`. Das Feld `version:` ist veraltet und wird ignoriert.
