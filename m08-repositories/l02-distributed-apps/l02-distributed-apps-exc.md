# Lab 8.2 – Übung: Verteilte und containerisierte Anwendungen mit Docker

**Dauer:** ca. 25 Minuten (Paarübung; Einzel-Fallback unten)
**Ändert die Hello-App-Projektbasis?** Ja — neue Datei `playground/hello/compose-registry.yml`, die die Hello-App aus der Registry startet; `compose.yml` bleibt der Hauptstand.

## Vorbereitung

- Lab 8.1 ist abgeschlossen: Die Registry läuft (`curl -s http://localhost:5001/v2/_catalog` zeigt `backend` und `frontend`), und `docker login` mit Token ist aktiv.
- Im Ordner `playground/hello/frontend` liegt das Dockerfile aus Lab 3.2. Fehlt es, im Ordner `project/`:

  ```bash
  cp -r examples/m03-images-registries/l02-own-images/hello/. playground/hello/
  ```

- Starter kopieren (im Ordner `project/`):

  ```bash
  cp starters/m08-l02-compose-registry.yml playground/hello/compose-registry.yml
  ```

- Mit der Partnerperson die Docker-IDs austauschen. In den Befehlen steht `<docker-id>` für die eigene, `<partner-id>` für die der Partnerperson.
- Arbeitsordner: `project/playground/hello`.

## Aufgaben

1. Lege auf Docker Hub ein **öffentliches** Repository `hello-web` an (**My Hub > Repositories > Create repository**, Visibility **Public**). Baue danach im Ordner `hello` das Frontend für zwei Plattformen und pushe es:

   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 --build-arg APP_VERSION=2.0.0 \
     -t <docker-id>/hello-web:2.0.0 --push frontend
   ```

2. Zeige mit `docker buildx imagetools inspect <docker-id>/hello-web:2.0.0`, für welche Plattformen das Image vorliegt, und mit `docker version --format '{{.Server.Os}}/{{.Server.Arch}}'`, welche der eigene Rechner nutzt.
3. Ziehe das Image der Partnerperson und starte es auf Port 8090:

   ```bash
   docker run -d --name partner-web -p 8090:80 <partner-id>/hello-web:2.0.0
   ```

   Öffne `http://localhost:8090` und vergleiche die angezeigte Container-ID mit `docker ps`.
4. Ergänze in `compose-registry.yml` die beiden TODOs: Frontend `2.0.0` und Backend `1.0.0` aus der Registry `127.0.0.1:5001`. Starte die Hello-App damit:

   ```bash
   docker compose -f compose-registry.yml pull
   docker compose -f compose-registry.yml up -d
   ```

   Prüfe mit `docker compose -f compose-registry.yml images`, woher die Images kommen, und öffne `http://localhost:8080`.
5. Stelle den Hauptstand wieder her: Starte die Hello-App mit `docker compose up -d` (ohne `-f`) und entferne den Container der Partnerperson mit `docker rm -f partner-web`.

## Checkpoint

- Nach Aufgabe 2: Die Ausgabe von `imagetools inspect` enthält `Platform: linux/amd64` und `Platform: linux/arm64`.
- Nach Aufgabe 3: `http://localhost:8090` zeigt „Hello World 2.0.0"; die Zeile zum Backend meldet „Backend nicht erreichbar", weil nur das Frontend läuft.
- Nach Aufgabe 4: `docker compose -f compose-registry.yml images` zeigt `127.0.0.1:5001/frontend` und `127.0.0.1:5001/backend`; `http://localhost:8080` zeigt „Hello World 2.0.0" mit Backend-Antwort.

## Abschlusskriterien

- Das eigene Image `<docker-id>/hello-web:2.0.0` liegt für `linux/amd64` und `linux/arm64` auf Docker Hub; die Partnerperson hat es gestartet.
- Die Hello-App lief aus der Registry, ohne `build:` in der Compose-Datei.

## Erweiterung

Starte das Image der Partnerperson zusätzlich in der jeweils anderen Plattform und vergleiche die Architektur im Container:

```bash
docker run --rm --platform linux/amd64 <partner-id>/hello-web:2.0.0 uname -m
docker run --rm --platform linux/arm64 <partner-id>/hello-web:2.0.0 uname -m
```

## Fallback

- **Einzeln statt im Paar:** In Aufgabe 3 das eigene Image nutzen. Vorher die lokale Kopie löschen, damit es wirklich von Docker Hub kommt: `docker rmi <docker-id>/hello-web:2.0.0` (meldet `No such image`, wenn es nur in der Registry liegt), danach `docker run … <docker-id>/hello-web:2.0.0`.
- **Ohne Docker-Konto:** Aufgaben 1–3 mit der eigenen Registry: `-t 127.0.0.1:5001/hello-web:2.0.0` statt `<docker-id>/hello-web:2.0.0`, Prüfung mit `curl -s http://localhost:5001/v2/hello-web/tags/list`.
- **Multi-Plattform-Build bricht ab** (`Multi-platform build is not supported for the docker driver`): in Docker Desktop unter **Settings > General** „Use containerd for pulling and storing images" einschalten, oder nur für die eigene Plattform bauen (ohne `--platform`).
- **Build dauert sehr lange** (Emulation der anderen Plattform): auf das Ende warten oder Aufgabe 1 mit `--platform linux/amd64,linux/arm64` als Erweiterung behandeln und einfach bauen.
- Fertige Datei: `project/examples/m08-repositories/l02-distributed-apps/hello/compose-registry.yml`.
