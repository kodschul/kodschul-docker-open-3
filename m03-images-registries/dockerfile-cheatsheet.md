# Dockerfile-Cheatsheet (Modul 3)

Dockerfile-Anweisungen, Build-, Image- und Registry-Befehle aus Modul 3. Container-Befehle aus Modul 1 und 2: [Docker-CLI-Cheatsheet](../m02-container-basics/docker-cli-cheatsheet.md). Alle Befehle für die Kurs-Shell `bash` ([Setup](../00-setup-and-installation.md#kurs-shell-bash)). Platzhalter in spitzen Klammern ersetzen.

## Dockerfile-Anweisungen

| Anweisung | Wirkung |
| --- | --- |
| `FROM python:3.13-alpine` | Basis-Image festlegen; erste Anweisung, fester Tag statt `latest` |
| `RUN apk add --no-cache curl` | Befehl beim Bauen ausführen; Ergebnis wird eine Schicht |
| `RUN apt-get update && apt-get install -y python3` | mehrere Befehle in einer Schicht verbinden |
| `WORKDIR /app` | Arbeitsverzeichnis für folgende Anweisungen und den Container; legt es bei Bedarf an |
| `COPY requirements.txt .` | Datei aus dem Build-Kontext ins Arbeitsverzeichnis kopieren |
| `COPY . .` | ganzen Build-Kontext kopieren (ohne Einträge aus `.dockerignore`) |
| `ADD app.tar.gz /opt/app/` | wie `COPY`, entpackt zusätzlich lokale Tar-Archive und lädt URLs |
| `ARG APP_VERSION=0.0.0` | Build-Argument mit Standardwert; existiert nur beim Bauen |
| `ENV APP_DISPLAY_VERSION=$APP_VERSION` | Umgebungsvariable; bleibt im Image und gilt im Container |
| `EXPOSE 80` | dokumentiert den Port der Anwendung; veröffentlicht ihn nicht |
| `VOLUME ["/data"]` | Verzeichnis als Volume markieren |
| `USER appuser` | folgende Schritte und den Container als `appuser` ausführen |
| `CMD ["python", "app.py"]` | Standardbefehl beim Start; ein Befehl bei `docker run` ersetzt ihn |
| `ENTRYPOINT ["python"]` | fester Programmaufruf; Argumente bei `docker run` werden angehängt |
| `ENTRYPOINT ["python"]` + `CMD ["app.py"]` | startet `python app.py`; `docker run <image> other.py` startet `python other.py` |
| `# Kommentar` | Kommentarzeile |

## .dockerignore

| Eintrag | Wirkung |
| --- | --- |
| `__pycache__/` | Ordner nicht in den Build-Kontext übernehmen |
| `*.pyc` | alle Dateien mit dieser Endung ausschließen |
| `Dockerfile`, `.dockerignore` | Bauanleitung selbst nicht ins Image kopieren |
| `.env`, `*.tar` | Geheimnisse und große Dateien ausschließen |

## Images bauen

| Befehl | Wirkung |
| --- | --- |
| `docker build -t <name>:<tag> .` | Image aus dem `Dockerfile` im aktuellen Ordner bauen |
| `docker build -t frontend:v2 --build-arg APP_VERSION=2.0.0 .` | Wert für ein `ARG` übergeben |
| `docker build -f <pfad/Dockerfile> -t <name>:<tag> <kontext>` | Dockerfile mit anderem Namen oder Ort verwenden |
| `bash build-images.sh` | im Ordner `project/`: `frontend:v1`, `frontend:v2`, `backend:v1` neu bauen |

## Eigene Images starten

| Befehl | Wirkung |
| --- | --- |
| `docker run --rm weather:1.0` | Image starten, Container danach löschen |
| `docker run -it --rm pizza:1.0` | Programm mit Tastatureingabe starten |
| `docker run --rm frontend:v2 cat version.info` | `CMD` durch einen anderen Befehl ersetzen |
| `docker run --rm frontend:v2 env` | Umgebungsvariablen des Images anzeigen |
| `docker run -d --name hello-frontend -p 8080:80 frontend:v2` | Hello-Frontend im Hintergrund auf Port 8080 |
| `docker run --entrypoint sh -it --rm <image>` | `ENTRYPOINT` ersetzen, z. B. für eine Shell |

## Images und Schichten anzeigen

| Befehl | Wirkung |
| --- | --- |
| `docker images` | lokale Images mit `DISK USAGE` und `CONTENT SIZE` |
| `docker images <name>` | nur Images mit diesem Namen |
| `docker history <image>` | Bauschritte und Größe jeder Schicht |
| `docker history --no-trunc <image>` | Bauschritte ungekürzt |
| `docker system df` | Speicherverbrauch von Images, Containern, Volumes und Build-Cache |
| `docker rmi <image>` | Image-Namen entfernen; letzter Name löscht das Image |

## Registry und Tags

| Befehl | Wirkung |
| --- | --- |
| `docker run -d -p 5001:5000 --name registry registry:3` | lokale Registry auf Port 5001 starten |
| `docker tag <image> 127.0.0.1:5001/<name>:<tag>` | zweiten Namen mit Registry-Adresse vergeben |
| `docker push 127.0.0.1:5001/<name>:<tag>` | Image in die lokale Registry hochladen |
| `docker pull 127.0.0.1:5001/<name>:<tag>` | Image aus der lokalen Registry laden |
| `http://localhost:5001/v2/_catalog` | Liste der Repositories (Browser) |
| `http://localhost:5001/v2/<name>/tags/list` | Tags eines Repositories (Browser) |
| `docker login` | bei Docker Hub anmelden (Zugangstoken statt Passwort) |
| `docker tag <image> <docker-hub-name>/<name>:<tag>` | Namen für das eigene Docker-Hub-Konto vergeben |
| `docker push <docker-hub-name>/<name>:<tag>` | Image nach Docker Hub hochladen |

## Images sichern

| Befehl | Wirkung |
| --- | --- |
| `docker save -o <datei>.tar <image>` | Image mit allen Schichten in eine Datei schreiben |
| `docker save -o images.tar frontend:v1 backend:v1` | mehrere Images in eine Datei |
| `docker load -i <datei>.tar` | Image aus einer Datei laden, mit Name und Tag |

## Tag-Regeln

| Regel | Beispiel |
| --- | --- |
| semantische Version `MAJOR.MINOR.PATCH` | `recipe-page:1.0.0`, Fehlerbehebung `1.0.1`, neue Funktion `1.1.0`, Bruch `2.0.0` |
| fester Tag statt `latest` | `nginx:1.30-alpine` statt `nginx` |
| vergebene Version nie überschreiben | Änderung → neue Nummer |
| Digest für unveränderliche Auswahl | `nginx:1.30-alpine@sha256:…` |
