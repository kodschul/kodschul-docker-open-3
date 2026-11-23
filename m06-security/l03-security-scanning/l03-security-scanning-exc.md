# Lab 6.3 – Übung: Docker Security Scanning und andere Tools

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — `frontend/Dockerfile` bekommt einen eigenen Benutzer (`USER app`), `frontend:v2` wird neu gebaut und läuft ab jetzt ohne root.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)), Ordner `project/playground/hello`. Unter Windows in Git Bash vorher `export MSYS_NO_PATHCONV=1`.
- Angemeldet mit dem Docker-Konto: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)). Ohne Konto: Fallback mit Trivy.
- Arbeitsdatei: `project/playground/hello/frontend/Dockerfile` (Stand Lab 3.2); die Hello-App läuft mit `compose.yml` aus Lab 6.2.
- Die Images `frontend:v1` und `frontend:v2` sind vorhanden (`docker images`); sonst im Ordner `project/` `bash build-images.sh`.

## Aufgaben

1. Zeige die Kurzfassung der Lücken von `frontend:v1` mit `docker scout quickview frontend:v1`. Lade danach `python:3.9-alpine` (`docker pull python:3.9-alpine`) und führe denselben Befehl dafür aus.
2. Liste die kritischen und hohen Lücken beider Images mit `docker scout cves --only-severity critical,high <image>` auf (`<image>` je einmal durch `frontend:v1` und `python:3.9-alpine` ersetzen).
3. Lies die Empfehlungen für `python:3.9-alpine` mit `docker scout recommendations python:3.9-alpine`.
4. Ergänze in `frontend/Dockerfile` direkt vor `CMD` einen Benutzer `app`, übergib ihm den Ordner `/data` und setze `USER app` (siehe Theorie). Baue und starte das Frontend neu mit `docker compose up -d --build frontend`.
5. Prüfe den Benutzer mit `docker compose exec frontend whoami` und öffne `http://localhost:8080`. Zeigt die Seite „Aufrufe in access.log: nicht beschreibbar", übergib den Inhalt des Volumes dem neuen Benutzer mit `docker compose exec --user root frontend chown -R app /data` und lade die Seite neu.

## Checkpoint

- Aufgabe 1: `quickview` zeigt für `frontend:v1` wenige Lücken, für `python:3.9-alpine` ein Vielfaches, darunter kritische (`C`) und hohe (`H`).
- Aufgabe 2: Tabelle je Paket mit CVE-Nummern, Schweregrad und `Fixed version`.
- Aufgabe 3: Vorschlag eines neueren Basisimages, z. B. `python:3.14-alpine`, mit weniger Lücken.
- Aufgabe 4: `docker compose up` baut `frontend:v2` neu und meldet `hello-frontend-1  Started`.
- Aufgabe 5: `whoami` zeigt `app`; die Hello-Seite zeigt „Hello World 2.0.0", die Backend-Antwort und nach `chown` wieder eine Zahl hinter „Aufrufe in access.log".

## Abschlusskriterien

- Lücken von `frontend:v1` und `python:3.9-alpine` mit `quickview` und `cves` verglichen.
- `frontend/Dockerfile` enthält `USER app`; das Hello-Frontend läuft ohne root und schreibt `access.log`.

## Erweiterung

Scanne `frontend:v2` (jetzt mit `USER`) und vergleiche es mit `frontend:v1`: `docker scout compare frontend:v2 --to frontend:v1`.

## Fallback

- Kein Docker-Konto oder `docker scout` nicht verfügbar: Aufgaben 1–2 mit Trivy (Befehl aus der Theorie), je einmal für `frontend:v1` und `python:3.9-alpine`; für nur kritische und hohe Lücken `--severity CRITICAL,HIGH` anhängen. Aufgabe 3 entfällt.
- `docker compose up --build` scheitert: `frontend/Dockerfile` mit `project/examples/m06-security/l03-security-scanning/hello/frontend/Dockerfile` vergleichen oder ihn kopieren (im Ordner `project/`: `cp -r examples/m06-security/l03-security-scanning/. playground/`).
