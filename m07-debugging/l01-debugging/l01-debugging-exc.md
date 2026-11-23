# Lab 7.1 – Übung: Docker Debugging

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Fehlerbilder sind eigene Kopien in `playground/debugging/` mit eigenen Ports (8701–8704); die Hello-App auf 8080 bleibt unverändert.

## Vorbereitung

- Docker Desktop läuft; Kurs-Shell bash ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Die Images `frontend:v2` und `backend:v1` aus Lab 3.2 sind vorhanden: `docker images` prüfen. Fehlen sie, im Ordner `project/` `bash build-images.sh` ausführen.
- Fehlerbilder in den Arbeitsbereich kopieren (im Ordner `project/`):

  ```bash
  cp -r variants/m07-l01-debugging playground/debugging
  ```

- Arbeitsordner: `project/playground/debugging/fehler1-cmd` bis `fehler4-speicher`. Jeder Ordner enthält eine `README.md` mit Startbefehl, erwartetem und beobachtetem Ergebnis.
- Ziel je Fehlerbild: Die Seite zeigt „Hello World" mit einer Backend-Antwort (Name, IP, Uhrzeit), nicht „Backend nicht erreichbar".

## Aufgaben

1. Wechsle in `fehler1-cmd`, starte das Projekt laut `README.md` und öffne `http://localhost:8701`. Finde mit Status und Logs heraus, warum die Seite nicht lädt, behebe den Fehler in den Dateien des Ordners und starte erneut.
2. Wechsle in `fehler2-copy` und starte das Projekt. Lies die Build-Ausgabe, untersuche den Build-Kontext des Frontends, behebe den Fehler, ohne Dateien zu löschen, und starte erneut. Prüfe `http://localhost:8702`.
3. Wechsle in `fehler3-netzwerk`, starte das Projekt und öffne `http://localhost:8703`. Prüfe aus dem Frontend-Container heraus, ob das Backend erreichbar ist, und untersuche die Netzwerke des Projekts. Behebe den Fehler in `compose.yml` und starte erneut.
4. Wechsle in `fehler4-speicher`, starte das Projekt und öffne `http://localhost:8704`. Finde heraus, warum das Backend nicht läuft, und belege die Ursache mit `docker inspect`. Behebe den Fehler in `compose.yml`, starte erneut und prüfe den Speicherverbrauch mit `docker stats --no-stream`.
5. Räume auf: Führe in allen vier Ordnern `docker compose down` aus und prüfe mit `docker ps -a`, dass keine Container mit `fehler` im Namen übrig sind.

## Checkpoint

- Nach Aufgabe 1: `docker compose ps` listet `frontend` mit `Up` und Port `0.0.0.0:8701->80/tcp`.
- Nach Aufgabe 2: Der Build endet ohne `failed to solve`, `http://localhost:8702` zeigt „Hello World 1.0.0".
- Nach Aufgabe 3: `docker compose exec frontend curl -sS http://backend:80` gibt JSON mit `hostname`, `ip` und `now` aus.
- Nach Aufgabe 4: `docker compose ps -a` zeigt das Backend mit `Up`; `docker stats --no-stream` zeigt für das Backend eine Grenze über dem tatsächlichen Verbrauch.

## Abschlusskriterien

- Alle vier Seiten (8701–8704) zeigten „Hello World" mit Backend-Antwort.
- Für jedes Fehlerbild ist die Gruppe (Start, Build, Netzwerk, Ressourcen) und der Befehl bekannt, der die Ursache gezeigt hat.

## Erweiterung

Baue in `fehler1-cmd` einen neuen Fehler ein: Ändere in `frontend/Dockerfile` den Programmnamen `python` in `CMD` zu `pyton`, starte mit `docker compose up -d --build` und vergleiche Exit-Code und Fehlermeldung mit Aufgabe 1. Stelle den korrekten Stand danach wieder her.

## Fallback

- Port 8701–8704 belegt: Port in der jeweiligen `compose.yml` ändern (z. B. `8711:80`).
- Ein Fehlerbild ist nach mehreren Versuchen nicht mehr im Ausgangszustand: Ordner löschen und aus `variants/m07-l01-debugging/` neu kopieren.
- Images `frontend:v2` oder `backend:v1` fehlen und der Build scheitert am Download: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
