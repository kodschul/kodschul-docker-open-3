# Lab 8.1 – Übung: Eigene Docker-Repositories erstellen und verwalten

**Dauer:** ca. 30 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — die Hello-Images liegen danach mit festen Versionen in der eigenen Registry `127.0.0.1:5001` (Ordner `playground/registry/`); Lab 8.2 startet die App von dort.

## Vorbereitung

- Docker Desktop läuft; Kurs-Shell bash ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Die Images `frontend:v1`, `frontend:v2` und `backend:v1` aus Lab 3.2 sind vorhanden: `docker images` prüfen. Fehlen sie, im Ordner `project/` `bash build-images.sh` ausführen.
- Docker-Konto mit bekannter Docker-ID ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)). In den Befehlen steht `<docker-id>` für diese ID, z. B. `maxmuster`.
- Registry-Starter in den Arbeitsbereich kopieren (im Ordner `project/`):

  ```bash
  mkdir -p playground/registry
  cp starters/m08-l01-registry-compose.yml playground/registry/compose.yml
  ```

## Aufgaben

1. Entferne den Registry-Container aus Lab 3.3 mit `docker rm -f registry`. Ergänze in `playground/registry/compose.yml` die drei TODOs (Volume, Neustart-Regel, Volume-Definition) und starte die Registry im Ordner `playground/registry` mit `docker compose up -d`.
2. Tagge die Hello-Images für die Registry und pushe sie:
   - `frontend:v1` als `127.0.0.1:5001/frontend:1.0.0`
   - `frontend:v2` als `127.0.0.1:5001/frontend:2.0.0` und zusätzlich als `127.0.0.1:5001/frontend:latest`
   - `backend:v1` als `127.0.0.1:5001/backend:1.0.0` und `127.0.0.1:5001/backend:latest`

   Prüfe danach Katalog und Tags mit `curl` (`/v2/_catalog`, `/v2/frontend/tags/list`, `/v2/backend/tags/list`).
3. Stoppe die Registry mit `docker compose down`, starte sie erneut mit `docker compose up -d` und prüfe den Katalog noch einmal. Lösche danach das lokale Image `127.0.0.1:5001/frontend:1.0.0` mit `docker rmi` und ziehe es mit `docker pull` aus der Registry zurück.
4. Lege auf Docker Hub ein privates Repository `hello-frontend` an. Erzeuge danach einen Zugangstoken mit dem Recht **Read & Write** und führe im Terminal `docker login --username <docker-id>` aus; gib bei `Password:` den Token ein.
5. Tagge `frontend:v2` als `<docker-id>/hello-frontend:2.0.0`, pushe es und prüfe auf Docker Hub unter **My Hub > Repositories > hello-frontend**, dass der Tag `2.0.0` mit dem Hinweis **Private** erscheint.

## Checkpoint

- Nach Aufgabe 1: `docker compose ps` im Ordner `registry` zeigt `registry-registry-1` mit `Up` und Port `0.0.0.0:5001->5000/tcp`.
- Nach Aufgabe 2: `curl -s http://localhost:5001/v2/_catalog` gibt `{"repositories":["backend","frontend"]}` aus.
- Nach Aufgabe 3: Der Katalog ist nach dem Neustart unverändert; `docker pull` meldet `Downloaded newer image` oder `Image is up to date`.
- Nach Aufgabe 4: `docker login` endet mit `Login Succeeded`.

## Abschlusskriterien

- Die eigene Registry enthält `frontend` mit den Tags `1.0.0`, `2.0.0`, `latest` und `backend` mit `1.0.0`, `latest`, auch nach einem Neustart.
- Das private Docker-Hub-Repository `<docker-id>/hello-frontend` enthält den Tag `2.0.0`; die Anmeldung lief mit Token, nicht mit Passwort.

## Erweiterung

- Prüfe, dass `latest` und `2.0.0` dasselbe Image sind: Vergleiche den Digest beider Tags in der Registry.

  ```bash
  for t in 2.0.0 latest; do
    curl -sI -H "Accept: application/vnd.oci.image.index.v1+json" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
      http://localhost:5001/v2/frontend/manifests/$t | grep -i docker-content-digest
  done
  ```

  Tagge danach `frontend:v1` als `127.0.0.1:5001/frontend:latest`, pushe es und vergleiche erneut: `latest` zeigt jetzt auf eine andere Version. Stelle den Stand mit `frontend:v2` als `latest` wieder her.

## Fallback

- Port 5001 belegt, obwohl `registry` gelöscht ist: `docker ps` prüfen; einen anderen Container auf 5001 stoppen oder den Port in `compose.yml` und allen Befehlen ändern (z. B. 5002).
- Ohne Docker-Konto oder ohne Internet: Aufgaben 4–5 auslassen; Lab 8.2 funktioniert mit der eigenen Registry allein.
- `denied: requested access to the resource is denied`: Docker-ID im Image-Namen prüfen (Kleinbuchstaben), neuen Token mit **Read & Write** erzeugen.
- Registry-Daten verloren (z. B. nach `docker compose down -v`): Aufgabe 2 wiederholen. Fertige `compose.yml`: `project/examples/m08-repositories/l01-own-repositories/registry/compose.yml`.
