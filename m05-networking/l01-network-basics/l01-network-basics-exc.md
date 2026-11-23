# Lab 5.1 – Übung: Netzwerkverwaltung in Containern

**Dauer:** ca. 15 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung liest nur das Netzwerk der laufenden Hello-App; Dateien bleiben unverändert.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)), Ordner `project/playground/hello`.
- Die Hello-App läuft im Stand von Lab 4.3 (`compose.yml` mit Frontend auf Port 8080 und Backend mit Healthcheck):

  ```bash
  docker compose up -d
  docker compose ps        # beide Dienste "Up", backend "(healthy)"
  ```

- Stand fehlt: im Ordner `project/` zuerst `cp -r examples/m03-images-registries/l02-own-images/. playground/` und `cp -r examples/m04-compose/l03-volumes/. playground/`; fehlen die Images `frontend:v2` oder `backend:v1`, dort `bash build-images.sh`.

## Aufgaben

1. Zeige alle Netzwerke mit `docker network ls` an. Suche das Netzwerk der Hello-App und die drei Netzwerke, die Docker selbst anlegt.
2. Lies das Projektnetzwerk mit `docker network inspect hello_default`. Suche Treiber, Subnetz, Gateway und die beiden Container mit ihren IP-Adressen. Öffne danach `http://localhost:8080` und vergleiche die IPs auf der Seite mit der Ausgabe.
3. Rufe aus dem Frontend-Container das Backend per Namen auf: `docker compose exec frontend curl -s http://backend`. Zeige danach mit `docker compose exec frontend getent hosts backend`, welche IP hinter dem Namen steht, und mit `docker compose exec frontend cat /etc/resolv.conf`, welcher DNS-Server den Namen auflöst.
4. Starte einen Einzelcontainer ohne Netzwerkangabe und versuche dasselbe:
   `docker run --rm busybox:1.37 wget -qO- -T 3 http://backend`
   Wiederhole den Befehl mit `--network hello_default` vor dem Image-Namen. (`wget -qO-` ist der `curl`-Ersatz in busybox: lädt die Adresse und gibt den Inhalt aus, `-T 3` bricht nach 3 Sekunden ab.)
5. Rufe `curl http://backend` auf dem eigenen Rechner (außerhalb von Docker) auf und danach `curl http://localhost:8080`.

## Checkpoint

- `docker network ls` zeigt `bridge`, `host`, `none` und `hello_default`.
- `inspect` listet `hello-frontend-1` und `hello-backend-1` mit IPs aus demselben Subnetz; dieselben IPs stehen auf der Hello-Seite.
- `curl -s http://backend` im Frontend-Container liefert JSON mit `hostname`, `ip` und `now`; `getent` zeigt dieselbe IP wie `inspect`; `resolv.conf` nennt `nameserver 127.0.0.11`.
- Der Einzelcontainer ohne Netzwerkangabe meldet `bad address 'backend'`, mit `--network hello_default` liefert er das JSON.
- Auf dem eigenen Rechner ist `backend` unbekannt, `localhost:8080` liefert die HTML-Seite.

## Abschlusskriterien

- Beobachtet: Der Name `backend` funktioniert nur innerhalb des Netzwerks `hello_default`, weil Compose den Dienst dort einträgt und der DNS-Server `127.0.0.11` ihn auflöst.
- Die Hello-App läuft unverändert weiter.

## Fallback

- `busybox:1.37` lässt sich nicht laden (`toomanyrequests`): `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)) oder für Aufgabe 4 das vorhandene Image nutzen: `docker run --rm --entrypoint curl backend:v1 -s -m 3 http://backend`.
- Unter Windows meldet Git Bash bei `/etc/resolv.conf` einen Pfad wie `C:/Program Files/Git/etc/…`: `export MSYS_NO_PATHCONV=1` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
