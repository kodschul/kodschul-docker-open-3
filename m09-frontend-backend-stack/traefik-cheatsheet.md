# Traefik und Multistage – Cheatsheet (Modul 9)

## Traefik starten (Compose, `command:`)

| Option | Wirkung |
| --- | --- |
| `image: traefik:v3.8` | Traefik v3, fester Tag |
| `--providers.docker=true` | Docker-Provider: Container und Labels über den Docker-Socket lesen |
| `--providers.docker.exposedByDefault=false` | nur Container mit `traefik.enable=true` veröffentlichen (Standard: `true`) |
| `--entryPoints.web.address=:80` | Entrypoint `web` auf Port 80 |
| `--api.insecure=true` | Dashboard und API auf Port 8080 ohne Anmeldung (nur lokal) |
| `--log.level=DEBUG` | ausführliche Logs |
| `- 80:80` und `- 8080:8080` unter `ports:` | Webverkehr und Dashboard auf dem Rechner |
| `- /var/run/docker.sock:/var/run/docker.sock:ro` | Docker-Socket nur lesend einbinden |

## Labels an Diensten (Traefik v3)

| Label | Wirkung |
| --- | --- |
| `traefik.enable=true` | Container veröffentlichen |
| ``traefik.http.routers.<router>.rule=Host(`app.localhost`)`` | Router nach Hostname |
| ``traefik.http.routers.<router>.rule=Host(`localhost`) && PathPrefix(`/api`)`` | Router nach Hostname und Pfad |
| `traefik.http.routers.<router>.entrypoints=web` | Router an Entrypoint `web` binden |
| `traefik.http.services.<service>.loadbalancer.server.port=5000` | Zielport im Container festlegen (bei mehreren Ports) |
| `traefik.http.routers.<router>.middlewares=<mw>` | Middleware an Router hängen |
| `traefik.http.middlewares.<mw>.stripprefix.prefixes=/api` | Pfad-Präfix vor dem Weiterleiten entfernen |
| `traefik.docker.network=<netz>` | Netzwerk zum Container wählen |

## Rules für Router

| Rule | passt auf |
| --- | --- |
| ``Host(`app.localhost`)`` | genau diesen Hostnamen |
| ``PathPrefix(`/api`)`` | Pfade, die mit `/api` beginnen |
| `A && B` / `A \|\| B` | beide / eine der Bedingungen |
| Priorität | längere Rule gewinnt (Standard) |

## Befehle und Adressen

| Befehl | Wirkung |
| --- | --- |
| `docker compose -f compose-traefik.yml up -d` | Hello-App hinter Traefik starten (Lab 9.1) |
| `docker compose -f compose-traefik.yml down` | wieder stoppen, Ports 80 und 8080 frei |
| `docker compose up -d --build` | Time-App bauen und starten (Lab 9.2) |
| `docker compose up -d --scale backend=3` | drei Container eines Dienstes hinter einem Router |
| `docker compose logs traefik` | Logs von Traefik |
| `docker compose exec redis redis-cli get last_time` | Wert direkt in Redis lesen |
| `curl -H "Host: app.localhost" http://localhost` | Router testen, ohne dass der Name aufgelöst wird |
| `http://localhost:8080` | Dashboard: Entrypoints, Routers, Services, Middlewares |

## Multistage-Dockerfile

| Anweisung / Befehl | Wirkung |
| --- | --- |
| `FROM node:24-alpine AS base` | Stufe mit Namen beginnen |
| `FROM base AS builder` | Stufe auf einer früheren Stufe aufbauen |
| `COPY --from=builder /usr/src/app/server.js ./` | Datei aus früherer Stufe übernehmen |
| `RUN npm ci` | alle Pakete aus `package-lock.json` (inkl. devDependencies) |
| `RUN npm ci --omit=dev && npm cache clean --force` | nur Laufzeitpakete, npm-Cache löschen |
| `docker build -f app/Dockerfile.prod -t todo-app:prod app` | Dockerfile mit anderem Namen bauen |
| `docker build --build-arg NODE_VERSION=24 -t todo-app:dev app` | Build-Argument überschreiben |
| `docker images todo-app` | Größen der Tags vergleichen |
| `docker history todo-app:prod` | Schichten und ihre Größe anzeigen |
