# Lab 3.1 – Übung: Aufbau und Speichern von Images

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung nutzt fertige Basis-Images und ein kleines Beispiel im eigenen Ordner `playground/layers/`.

## Vorbereitung

- Docker Desktop läuft; Terminal (macOS/Linux: Terminal, Windows: Git Bash mit `MSYS_NO_PATHCONV=1`, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)) im Ordner `project/`.
- Starter: `project/starters/m03-l01-image-layers/layers/` (`Dockerfile` mit TODOs, `app.py`).
- Arbeitsordner: `project/playground/layers/`. Starter dorthin kopieren:

  ```bash
  cp -r starters/m03-l01-image-layers/. playground/
  ```

## Aufgaben

1. Lade die Basis-Images `ubuntu:24.04`, `alpine:3.24` und `python:3.13-alpine` mit `docker pull` und vergleiche ihre Größen mit `docker images` (Spalten `DISK USAGE` und `CONTENT SIZE`).
2. Lies mit `docker history python:3.13-alpine` die Bauschritte des Python-Images. Suche die unterste Schicht (Basis), die größte Schicht und einen Schritt mit `0B`.
3. Wechsle nach `playground/layers/`, ergänze das `Dockerfile` nach den drei TODOs (Vorlage: Abschnitt „Beispiel eines Dockerfiles mit Schichten" in der Theorie) und baue es als Image `layers-demo:1.0`. Starte danach einen Container daraus mit dem Befehl `python3 /app/app.py`:
   `docker run --rm layers-demo:1.0 python3 /app/app.py`
4. Zeige `docker history layers-demo:1.0` an und vergleiche die Größe von `layers-demo:1.0` mit `ubuntu:24.04` in `docker images`. Ordne die drei obersten Zeilen der History den drei Anweisungen des Dockerfiles zu.
5. Ändere den Text in `app.py`, baue erneut als `layers-demo:1.1` und beobachte, welche Schritte die Ausgabe von `docker build` als `CACHED` markiert. Starte `layers-demo:1.1` wie in Aufgabe 3.

## Checkpoint

- `docker images` listet `ubuntu:24.04`, `alpine:3.24` und `python:3.13-alpine`; Alpine ist das kleinste.
- `docker run --rm layers-demo:1.0 python3 /app/app.py` gibt `Hallo aus der Schicht COPY app.py` aus.
- `docker history layers-demo:1.0` zeigt oben die Schritte `COPY app.py …` und `RUN … apt-get install -y python3`, darunter die Schritte von Ubuntu.
- Beim Build von `layers-demo:1.1` sind `FROM` und `RUN` als `CACHED` markiert, nur `COPY` läuft neu.

## Abschlusskriterien

- Die Größen der drei Basis-Images sind verglichen, und die Schicht, die `layers-demo` größer macht als `ubuntu:24.04`, ist benannt.
- `layers-demo:1.0` und `layers-demo:1.1` existieren und geben ihren jeweiligen Text aus.

## Fallback

- `toomanyrequests` beim Pull: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
- `apt-get update` schlägt fehl (Proxy oder kein Internet): Aufgabe 3 bis 5 mit Alpine bauen; in der ersten Zeile `FROM alpine:3.24`, in der zweiten `RUN apk add --no-cache python3`. Die Schichten sind dieselben, nur kleiner.
- Dockerfile lässt sich nicht bauen: fertigen Stand kopieren mit `cp -r examples/m03-images-registries/l01-image-layers/. playground/` (im Ordner `project/`).
