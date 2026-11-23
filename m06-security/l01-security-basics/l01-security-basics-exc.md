# Lab 6.1 – Übung: Grundlagen der Docker-Sicherheit

**Dauer:** ca. 10 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Hello-App wird nur untersucht; die Testdatei aus Aufgabe 4 wird wieder gelöscht.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)), Ordner `project/playground/hello`. Unter Windows in Git Bash vorher `export MSYS_NO_PATHCONV=1`.
- Die Hello-App läuft mit Compose (`docker compose ps` zeigt `frontend` und `backend`); sonst `docker compose up -d`.

## Aufgaben

1. Prüfe, als welcher Benutzer das Hello-Frontend läuft: `docker compose exec frontend whoami` und `docker compose exec frontend id -u`.
2. Zeige, welcher Prozess im Frontend-Container läuft und unter welchem Benutzer: `docker compose top frontend`.
3. Starte einen Wegwerf-Container mit eingebundenem Wurzelverzeichnis und liste es auf: `docker run --rm -v /:/host alpine:3.24 ls /host`. Vergleiche mit `docker run --rm alpine:3.24 ls /`.
4. Lege aus einem Container heraus eine Datei im Wurzelverzeichnis des Hosts an und prüfe Besitzer und Inhalt mit einem zweiten Container:
   `docker run --rm -v /:/host alpine:3.24 sh -c 'echo "geschrieben von einem Container" > /host/tmp/container-war-hier.txt'`
   `docker run --rm -v /:/host alpine:3.24 ls -l /host/tmp/container-war-hier.txt`
   Lösche die Datei danach: `docker run --rm -v /:/host alpine:3.24 rm /host/tmp/container-war-hier.txt`.
5. Binde den eigenen Benutzerordner schreibgeschützt ein und versuche, dort eine Datei anzulegen: `docker run --rm -v "$HOME":/home-host:ro alpine:3.24 sh -c 'ls /home-host | head -5; touch /home-host/test.txt'`.

## Checkpoint

- Aufgabe 1: `root` und `0`.
- Aufgabe 2: Spalte `UID` zeigt `root`, Befehl `python frontend.py`.
- Aufgabe 3: `/host` zeigt Ordner wie `bin`, `etc`, `home`, `tmp`, `usr`, `var`; die Liste unterscheidet sich vom Wurzelverzeichnis des Alpine-Containers.
- Aufgabe 4: `ls -l` zeigt die Datei mit Besitzer `root`.
- Aufgabe 5: die ersten Einträge des eigenen Benutzerordners erscheinen, danach `touch: /home-host/test.txt: Read-only file system`.

## Abschlusskriterien

- Belegt: Das Hello-Frontend läuft als root.
- Belegt: Ein Container mit `-v /:/host` liest und schreibt als root im Dateisystem des Hosts (bei Docker Desktop: der Linux-VM); `:ro` verhindert das Schreiben.
- Die Testdatei `/tmp/container-war-hier.txt` ist gelöscht.

## Fallback

- `alpine:3.24` lässt sich nicht laden (`toomanyrequests`): `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)) oder `busybox:1.37` statt `alpine:3.24` verwenden.
- Unter Windows meldet Aufgabe 5 einen Pfadfehler: Git Bash mit `MSYS_NO_PATHCONV=1` nutzen; `$HOME` zeigt dort auf `C:\Users\<Name>`.
