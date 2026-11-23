# Lab 3.3 – Übung: Lokale Registry und Image-Verwaltung

**Dauer:** ca. 60 Minuten (Einführung 15, Arbeitsphase 35, Debrief 10)
**Ändert die Hello-App-Projektbasis?** Nein — `frontend:v1` aus Lab 3.2 wird nur zusätzlich in die lokale Registry kopiert; die Rezeptseite ist eine eigene kleine App.

## Vorbereitung

- Docker Desktop läuft; Terminal (macOS/Linux: Terminal, Windows: Git Bash mit `MSYS_NO_PATHCONV=1`, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)) im Ordner `project/`.
- `frontend:v1` aus Lab 3.2 ist gebaut (`docker images frontend`).
- Starter: `project/starters/m03-l03-recipe-page/recipe-page/` (`index.html` mit Beispielrezept, `Dockerfile` mit TODOs). Kopieren:

  ```bash
  cp -r starters/m03-l03-recipe-page/. playground/
  ```

- Arbeitsordner: `project/playground/recipe-page/`.
- Ports: Registry 5001, Rezeptseite 8081 (8080 belegt das Hello-Frontend aus Lab 3.2).

## Aufgaben

1. Ersetze in `playground/recipe-page/index.html` das Beispielrezept durch das eigene Lieblingsrezept (Titel, Zutaten, Zubereitung). Ergänze das `Dockerfile` nach den TODOs, baue es im Ordner `playground/recipe-page` als `recipe-page:1.0.0` und starte es mit `docker run -d --name recipe-page -p 8081:80 recipe-page:1.0.0`. Öffne `http://localhost:8081`.
2. Starte die lokale Registry mit `docker run -d -p 5001:5000 --name registry registry:3`. Tagge `frontend:v1` als `127.0.0.1:5001/frontend:v1` und `recipe-page:1.0.0` als `127.0.0.1:5001/recipe-page:1.0.0` und pushe beide Images.
3. Öffne im Browser `http://localhost:5001/v2/_catalog` und danach die Tag-Listen `http://localhost:5001/v2/frontend/tags/list` und `http://localhost:5001/v2/recipe-page/tags/list`.
4. Lösche die Rezeptseite lokal: Entferne den Container `recipe-page` und beide Image-Namen `recipe-page:1.0.0` und `127.0.0.1:5001/recipe-page:1.0.0` mit `docker rmi`. Ziehe das Image mit `docker pull 127.0.0.1:5001/recipe-page:1.0.0` aus der Registry und starte es wieder als Container `recipe-page` auf Port 8081.
5. Sichere das Image mit `docker save -o recipe-page.tar 127.0.0.1:5001/recipe-page:1.0.0` im Ordner `playground/recipe-page` und prüfe die Datei mit `ls -lh recipe-page.tar`. Entferne Container und Image erneut, lade es mit `docker load -i recipe-page.tar` und zeige es mit `docker images` an.

## Checkpoint

- `http://localhost:8081` zeigt das eigene Rezept.
- `docker push` endet mit einer Zeile `1.0.0: digest: sha256:… size: …` bzw. `v1: digest: …`.
- Der Katalog zeigt `{"repositories":["frontend","recipe-page"]}`, die Tag-Liste der Rezeptseite `{"name":"recipe-page","tags":["1.0.0"]}`.
- Nach dem Löschen fehlt `recipe-page` in `docker images`; nach `docker pull` ist es wieder da, und die Seite unter `http://localhost:8081` funktioniert.
- `docker load` meldet `Loaded image: 127.0.0.1:5001/recipe-page:1.0.0`.

## Abschlusskriterien

- `frontend:v1` und `recipe-page:1.0.0` liegen in der lokalen Registry und lassen sich daraus ziehen und starten.
- `recipe-page.tar` existiert und lässt sich wieder als Image laden.

## Erweiterung

Lade die Rezeptseite zusätzlich nach Docker Hub: Führe `docker login` aus, tagge das Image als `<docker-hub-name>/recipe-page:1.0.0` (eigener Docker-Hub-Benutzername) und pushe es. Prüfe auf `https://hub.docker.com` unter „My Hub" (bzw. „Repositories"), dass das Repository mit dem Tag `1.0.0` erscheint. Das Repository ist öffentlich; danach in den Repository-Einstellungen löschen oder auf privat stellen (Gratis-Konto: bis zu 1 privates Repository).

## Fallback

- `Bind for 0.0.0.0:5001 failed: port is already allocated`: alte Registry mit `docker rm -f registry` entfernen oder einen anderen Port wählen (z. B. `-p 5002:5000`, dann überall `127.0.0.1:5002`).
- `frontend:v1` fehlt: `bash build-images.sh` im Ordner `project/`.
- Dockerfile der Rezeptseite lässt sich nicht bauen: fertigen Stand kopieren mit `cp -r examples/m03-images-registries/l03-local-registry/. playground/` (im Ordner `project/`). Das Skript `playground/registry/registry.sh` führt danach Aufgabe 2 bis 4 in einem Durchlauf aus: `bash registry.sh` im Ordner `playground/registry`; es entfernt dabei einen laufenden Container `hello-frontend` und startet `127.0.0.1:5001/frontend:v1` auf Port 8080.
- `toomanyrequests` beim Laden von `registry:3` oder `nginx:1.30-alpine`: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
