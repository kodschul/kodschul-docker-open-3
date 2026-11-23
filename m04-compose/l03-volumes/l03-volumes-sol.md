# Lab 4.3 – Lösung: Datenvolumes und Persistenz

Fertiger Stand: `project/examples/m04-compose/l03-volumes/recipe-book/` und `project/examples/m04-compose/l03-volumes/hello/compose.yml`. Getestet am 23.11.2026 mit Docker 29.9.3, Compose 5.7.0, `node:24-alpine`, `mongo:8`, Express 5 und Mongoose 9; IDs und Zeiten weichen ab.

## Aufgabe 1: Dockerfile für das Rezeptbuch

```dockerfile
# Rezeptbuch-Image: Node.js-App aus diesem Ordner
FROM node:24-alpine

WORKDIR /app

# Erst die Abhängigkeiten (Schicht bleibt im Cache, solange package.json gleich bleibt)
COPY package.json .
RUN npm install --omit=dev

# Danach den Code
COPY . .

EXPOSE 3000

# entspricht "npm start"; node direkt als Hauptprozess beendet sich bei docker stop sofort
CMD ["node", "index.js"]
```

- Reihenfolge wie bei der Hello-App (Lab 3.2): Abhängigkeiten vor dem Code, damit eine Code-Änderung `npm install` nicht wiederholt.
- `--omit=dev` installiert nur, was zur Laufzeit gebraucht wird. `app/.dockerignore` hält einen lokalen Ordner `node_modules` aus dem Image heraus.
- `npm start` als `CMD` funktioniert ebenfalls; `node index.js` startet ohne Umweg über npm.

## Aufgabe 2: Compose-Datei mit Named Volume

```yaml
# Rezeptbuch: App (eigenes Image) und Datenbank (MongoDB) mit Named Volume
services:
  recipe-app:
    build: ./app                            # Image aus app/Dockerfile bauen
    ports:
      - 3000:3000
    depends_on:
      - recipe-database                     # Datenbank-Container zuerst starten

  recipe-database:
    image: mongo:8                          # MongoDB 8 (Version 6 ohne Support seit 31.07.2025)
    volumes:
      - recipe-data:/data/db                # MongoDB speichert seine Dateien unter /data/db

volumes:
  recipe-data:                              # Named Volume; docker compose down -v löscht es
```

Der Dienstname `recipe-database` muss zur Adresse in `index.js` passen (`mongodb://recipe-database:27017/recipes`). Die Datenbank bekommt keinen Port nach außen; nur die App spricht mit ihr.

```bash
docker compose up -d --build
```

```text
[+] Building 14.2s (11/11) FINISHED
…
[+] up 5/5
 ✔ Image recipe-book-recipe-app            Built
 ✔ Network recipe-book_default             Created
 ✔ Volume recipe-book_recipe-data          Created
 ✔ Container recipe-book-recipe-database-1 Started
 ✔ Container recipe-book-recipe-app-1      Started
```

```bash
docker compose logs recipe-app
```

```text
recipe-app-1  | Recipe Book App listening on port 3000
recipe-app-1  | Mit MongoDB verbunden
```

Erscheint `MongoDB nicht erreichbar`, war die Datenbank beim ersten Versuch noch nicht bereit oder der Dienstname stimmt nicht.

## Aufgabe 3: Rezept anlegen und abrufen

```bash
curl -X POST http://localhost:3000/recipes -H "Content-Type: application/json" \
  -d '{"title":"Spaghetti Carbonara","ingredients":["Spaghetti","Eier","Speck","Parmesan"],"instructions":"Spaghetti kochen, Speck anbraten, mit Eiern und Käse mischen."}'
```

```json
{"title":"Spaghetti Carbonara","ingredients":["Spaghetti","Eier","Speck","Parmesan"],"instructions":"Spaghetti kochen, Speck anbraten, mit Eiern und Käse mischen.","_id":"6b04bca71fa2fa46dec2eeb0","__v":0}
```

```bash
curl http://localhost:3000/recipes
```

```json
[{"_id":"6b04bca71fa2fa46dec2eeb0","title":"Spaghetti Carbonara","ingredients":["Spaghetti","Eier","Speck","Parmesan"],"instructions":"Spaghetti kochen, Speck anbraten, mit Eiern und Käse mischen.","__v":0}]
```

`_id` vergibt MongoDB; `__v` ist ein Versionszähler von Mongoose und für die Übung unwichtig.

```bash
docker volume ls
docker volume inspect recipe-book_recipe-data
```

```text
DRIVER    VOLUME NAME
local     recipe-book_recipe-data
…
[
    {
        "CreatedAt": "2026-11-23T22:22:18Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.config-hash": "1a31f376…",       ← unwichtig
            "com.docker.compose.project": "recipe-book",          ← gehört zum Compose-Projekt
            "com.docker.compose.version": "5.7.0",
            "com.docker.compose.volume": "recipe-data"            ← Name in der Compose-Datei
        },
        "Mountpoint": "/var/lib/docker/volumes/recipe-book_recipe-data/_data",
        "Name": "recipe-book_recipe-data",
        "Options": null,
        "Scope": "local"
    }
]
```

## Aufgabe 4: down, up und down -v

```bash
docker compose down
docker compose up -d
curl http://localhost:3000/recipes
```

```json
[{"_id":"6b04bca71fa2fa46dec2eeb0","title":"Spaghetti Carbonara",…}]
```

`down` entfernt Container und Netzwerk, das Volume `recipe-book_recipe-data` bleibt; der neue Datenbank-Container findet seine Dateien unter `/data/db` wieder.

```bash
docker compose down -v
```

```text
[+] down 4/4
 ✔ Container recipe-book-recipe-app-1      Removed
 ✔ Container recipe-book-recipe-database-1 Removed
 ✔ Network recipe-book_default             Removed
 ✔ Volume recipe-book_recipe-data          Removed
```

```bash
docker compose up -d
curl http://localhost:3000/recipes
```

```json
[]
```

Mit `-v` ist das Volume gelöscht; Compose legt beim nächsten `up` ein leeres an. Zum Schluss `docker compose down -v`.

Alternative mit Bind Mount statt Named Volume (wie in der ursprünglichen Übungsvorlage mit Ordner `data/`): `- ./data:/data/db`. Die Dateien liegen dann sichtbar im Projektordner; unter macOS und Windows ist das langsamer, und `down -v` löscht sie nicht.

## Aufgabe 5: Hello-App mit Volume hello-data

```yaml
# Hello-App, Stand ab Lab 4.3: ein Frontend auf Port 8080, access.log im Volume hello-data
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
    ports:
      - 8080:80
    volumes:
      - hello-data:/data                    # Named Volume: access.log überlebt Container
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

volumes:
  hello-data:                               # von Docker verwaltet; docker compose down -v löscht es
```

```bash
docker compose up -d          # Seite dreimal laden: Aufrufe 1, 2, 3
docker compose down
docker compose up -d          # Seite laden: Aufrufe in access.log: 4
docker compose exec frontend cat /data/access.log
```

```text
2026-11-23 22:23:24 628a3fa0f633 2.0.0
2026-11-23 22:23:24 628a3fa0f633 2.0.0
2026-11-23 22:23:24 628a3fa0f633 2.0.0
2026-11-23 22:23:37 55cac945bf8e 2.0.0
```

Direkt nach `up -d` braucht das Frontend ein bis zwei Sekunden (es wartet auf den Healthcheck des Backends); ein sofortiger Aufruf scheitert, ein Neuladen danach klappt.

Die letzte Zeile stammt von einem neuen Container (andere ID), die Datei ist dieselbe. Ohne Volume hätte der neue Container wieder bei 1 begonnen. Die Hello-App läuft für Lab 4.4 weiter.

## Erweiterung

Docker Desktop: **Volumes** → `hello_hello-data` → Reiter **Stored data** zeigt `access.log`; ein Doppelklick öffnet den Inhalt mit denselben Zeilen wie oben. **Container in-use** zeigt `hello-frontend-1` mit Ziel `/data`.
