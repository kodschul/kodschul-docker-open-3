# Lab 4.4 – Lösung: Migration in eine Microservice-basierte Anwendung

Ausgangs- und Endstand: `project/examples/m04-compose/l03-volumes/hello/compose.yml`. Alle Befehle im Ordner `project/playground/hello`. Getestet am 23.11.2026 mit Docker 29.9.3 und Compose 5.7.0; IDs und Zeiten weichen ab.

## Aufgabe 1: Ausgangszustand notieren

```bash
docker compose up -d
docker compose ps
docker ps
```

```text
NAME               IMAGE         COMMAND                SERVICE    CREATED          STATUS                    PORTS
hello-backend-1    backend:v1    "python backend.py"    backend    29 seconds ago   Up 28 seconds (healthy)   80/tcp
hello-frontend-1   frontend:v2   "python frontend.py"   frontend   4 seconds ago    Up 3 seconds              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

CONTAINER ID   IMAGE         …   NAMES
d73f6dbde9ad   frontend:v2   …   hello-frontend-1
21dafd851204   backend:v1    …   hello-backend-1
```

Die Seite zeigt „Hello World 2.0.0" auf gelbem Grund, Frontend `d73f6dbde9ad`.

## Aufgabe 2: Frontend-Version und Farbe ändern

```yaml
  frontend:
    image: frontend:v2
    build:
      context: frontend
      args:
        - APP_VERSION=2.1.0                 # vorher 2.0.0
    environment:
      - APP_COLOR=lightblue                 # neu
    depends_on:
      backend:
        condition: service_healthy
    …                                       # Rest unverändert
```

## Aufgabe 3: nur das Frontend neu bauen und ersetzen

```bash
docker compose up -d --build --no-deps frontend
```

```text
[+] Building 1.9s (14/14) FINISHED
…
[+] up 2/2
 ✔ Image frontend:v2          Built
 ✔ Container hello-frontend-1 Started
```

Nur `frontend` wird gebaut und durch einen neuen Container ersetzt; das Backend kommt in der Ausgabe nicht vor.

Ohne `--no-deps` (`docker compose up -d --build frontend`) baut Compose zusätzlich `backend:v1` neu und meldet `Container hello-backend-1 Healthy`. Der Backend-Container lief im Test danach meist weiter, wurde in einem Durchlauf aber ebenfalls ersetzt; `--no-deps` schließt das aus.

## Aufgabe 4: vorher und nachher vergleichen

```text
NAME               IMAGE         …   CREATED          STATUS                    PORTS
hello-backend-1    backend:v1    …   42 seconds ago   Up 41 seconds (healthy)   80/tcp
hello-frontend-1   frontend:v2   …   3 seconds ago    Up 2 seconds              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

CONTAINER ID   IMAGE         …   NAMES
6be94db379e9   frontend:v2   …   hello-frontend-1
21dafd851204   backend:v1    …   hello-backend-1
```

| | Frontend | Backend |
| --- | --- | --- |
| Container-ID | neu (`d73f6dbde9ad` → `6be94db379e9`) | gleich (`21dafd851204`) |
| Laufzeit | Sekunden | läuft weiter seit dem Start in Aufgabe 1 |
| Seite | hellblau, „Hello World 2.1.0" | Backend-Zeile zeigt weiterhin `21dafd851204` |

„Aufrufe in access.log" zählt weiter (im Test 4 → 5), weil `access.log` im Volume `hello-data` liegt und nicht im ersetzten Container. Genau so wird in einer Microservice-Anwendung ein Dienst ausgeliefert, ohne die anderen anzuhalten.

## Aufgabe 5: Änderung zurücknehmen

`APP_VERSION=2.0.0` wiederherstellen, den Block `environment` löschen, dann:

```bash
docker compose up -d --build --no-deps frontend
```

Die Seite ist wieder gelb mit „Hello World 2.0.0"; `frontend:v2` enthält wieder Version 2.0.0. `compose.yml` entspricht `examples/m04-compose/l03-volumes/hello/compose.yml`.
