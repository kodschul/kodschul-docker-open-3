# Lab 7.1 – Lösung: Docker Debugging

Alle Befehle laufen im jeweiligen Ordner unter `project/playground/debugging/`. Compose benennt Container nach dem Muster `<ordner>-<dienst>-1`.

## Aufgabe 1: Fehlerbild 1, falscher Dateiname im CMD

**Gruppe:** Start. Das Image wird gebaut, der Container beendet sich sofort.

```bash
cd fehler1-cmd
docker compose up -d --build
docker compose ps
docker compose ps -a
```

```text
NAME                     IMAGE                  COMMAND               SERVICE   CREATED         STATUS         PORTS
fehler1-cmd-backend-1    backend:v1             "python backend.py"   backend   4 seconds ago   Up 3 seconds   80/tcp

NAME                     IMAGE                  COMMAND               SERVICE    CREATED         STATUS                     PORTS
fehler1-cmd-backend-1    backend:v1             "python backend.py"   backend    4 seconds ago   Up 3 seconds               80/tcp
fehler1-cmd-frontend-1   fehler1-frontend:1.0   "python fronted.py"   frontend   4 seconds ago   Exited (2) 3 seconds ago
```

`docker compose ps` zeigt das Frontend gar nicht, erst `ps -a` zeigt `Exited (2)`. Die Spalte `COMMAND` verrät den Fehler bereits; die Logs bestätigen ihn:

```bash
docker compose logs frontend
```

```text
frontend-1  | python: can't open file '/app/fronted.py': [Errno 2] No such file or directory
```

Gegenprobe im Image mit einer Shell als Entrypoint:

```bash
docker run --rm --entrypoint sh fehler1-frontend:1.0 -c 'pwd; ls'
```

```text
/app
frontend.py
requirements.txt
version.info
```

**Ursache:** `CMD ["python", "fronted.py"]` in `frontend/Dockerfile`; die Datei heißt `frontend.py`.

**Behebung:** in `frontend/Dockerfile`

```dockerfile
CMD ["python", "frontend.py"]
```

```bash
docker compose up -d --build
docker compose ps
```

```text
NAME                     IMAGE                  COMMAND                SERVICE    CREATED          STATUS          PORTS
fehler1-cmd-backend-1    backend:v1             "python backend.py"    backend    13 seconds ago   Up 12 seconds   80/tcp
fehler1-cmd-frontend-1   fehler1-frontend:1.0   "python frontend.py"   frontend   2 seconds ago    Up 2 seconds    0.0.0.0:8701->80/tcp, [::]:8701->80/tcp
```

`http://localhost:8701` zeigt „Hello World 1.0.0" und die Backend-Antwort. Ohne `--build` würde Compose das alte, fehlerhafte Image weiterverwenden.

## Aufgabe 2: Fehlerbild 2, fehlende Datei im COPY

**Gruppe:** Build. Es entsteht kein Image, daher startet kein Container.

```bash
cd ../fehler2-copy
docker compose up -d --build
```

```text
 > [4/7] COPY requirements.txt .:
------
Dockerfile:8
--------------------
   6 |     WORKDIR /app
   7 |
   8 | >>> COPY requirements.txt .
   9 |     RUN pip install --no-cache-dir -r requirements.txt
--------------------
failed to solve: failed to compute cache key: failed to calculate checksum of ref …: "/requirements.txt": not found
```

Die Datei liegt aber im Ordner:

```bash
ls frontend
cat frontend/.dockerignore
```

```text
Dockerfile  frontend.py  notizen.txt  requirements.txt

__pycache__/
*.pyc
Dockerfile
.dockerignore
# Notizen und Textdateien nicht ins Image
*.txt
```

**Ursache:** Die Regel `*.txt` in `frontend/.dockerignore` schließt auch `requirements.txt` aus dem Build-Kontext aus. `COPY` sieht nur den Build-Kontext, nicht den Ordner auf der Festplatte.

**Behebung:** Ausnahme für `requirements.txt` in `frontend/.dockerignore` ergänzen (eine Zeile mit `!` hebt eine vorherige Regel auf):

```text
# Notizen und Textdateien nicht ins Image
*.txt
!requirements.txt
```

```bash
docker compose up -d --build
docker run --rm --entrypoint ls fehler2-frontend:1.0
```

```text
frontend.py
requirements.txt
version.info
```

`notizen.txt` bleibt wie beabsichtigt draußen, `http://localhost:8702` zeigt „Hello World 1.0.0" mit Backend-Antwort. Ebenso gültig: die Regel `*.txt` durch `notizen.txt` ersetzen.

## Aufgabe 3: Fehlerbild 3, Backend in anderem Netzwerk

**Gruppe:** Netzwerk. Beide Container laufen, das Frontend findet das Backend nicht.

```bash
cd ../fehler3-netzwerk
docker compose up -d
docker compose ps
```

```text
NAME                          IMAGE         COMMAND                SERVICE    CREATED         STATUS         PORTS
fehler3-netzwerk-backend-1    backend:v1    "python backend.py"    backend    4 seconds ago   Up 3 seconds   80/tcp
fehler3-netzwerk-frontend-1   frontend:v2   "python frontend.py"   frontend   4 seconds ago   Up 3 seconds   0.0.0.0:8703->80/tcp, [::]:8703->80/tcp
```

`http://localhost:8703` zeigt „Backend: Backend nicht erreichbar (http://backend:80): ConnectionError". Test aus dem Frontend heraus:

```bash
docker compose exec frontend curl -sS http://backend:80
docker compose exec frontend ping -c 1 backend
```

```text
curl: (6) Could not resolve host: backend (Domain name not found)
ping: bad address 'backend'
```

Der Name ist unbekannt, die URL selbst (`BACKEND_URL=http://backend:80`) stimmt. Netzwerke prüfen:

```bash
docker network ls --filter name=fehler3
docker network inspect fehler3-netzwerk_front --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
docker network inspect fehler3-netzwerk_back --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
```

```text
NETWORK ID     NAME                     DRIVER    SCOPE
00043842c53c   fehler3-netzwerk_back    bridge    local
0a55e916f91d   fehler3-netzwerk_front   bridge    local

fehler3-netzwerk-frontend-1 172.23.0.2/16

fehler3-netzwerk-backend-1 172.24.0.2/16
```

**Ursache:** Das Frontend hängt nur in `front`, das Backend nur in `back`. Namensauflösung funktioniert nur innerhalb desselben Netzwerks.

**Behebung:** Backend zusätzlich in `front` aufnehmen (`compose.yml`):

```yaml
  backend:
    image: backend:v1
    networks:
      - back
      - front
```

```bash
docker compose up -d
docker compose exec frontend curl -sS http://backend:80
```

```text
{"hostname":"097659f58a19","ip":["172.24.0.2","172.23.0.3"],"now":"09:42:19"}
```

Das Backend hat jetzt eine IP in jedem Netzwerk; `http://localhost:8703` zeigt die Backend-Antwort. Gleichwertig: `networks:` bei beiden Diensten entfernen, dann hängen beide im Netzwerk `default`.

Schneller Test ohne Neustart (nicht dauerhaft): `docker network connect --alias backend fehler3-netzwerk_front fehler3-netzwerk-backend-1`. Ohne `--alias` bleibt `backend` unbekannt, weil der Container im neuen Netzwerk nur unter seinem Containernamen erreichbar ist.

## Aufgabe 4: Fehlerbild 4, zu kleines Memory-Limit

**Gruppe:** Ressourcen. Das Frontend läuft, das Backend ist sofort beendet.

```bash
cd ../fehler4-speicher
docker compose up -d
docker compose ps -a
docker compose logs backend
```

```text
NAME                          IMAGE         COMMAND                SERVICE    CREATED         STATUS                       PORTS
fehler4-speicher-backend-1    backend:v1    "python backend.py"    backend    5 seconds ago   Exited (137) 4 seconds ago
fehler4-speicher-frontend-1   frontend:v2   "python frontend.py"   frontend   5 seconds ago   Up 5 seconds                 0.0.0.0:8704->80/tcp, [::]:8704->80/tcp
```

Die Logs sind leer: Python wurde beendet, bevor es etwas ausgeben konnte. Exit-Code `137` heißt `SIGKILL`; `docker inspect` zeigt den Grund:

```bash
docker inspect -f 'status={{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}} mem={{.HostConfig.Memory}}' fehler4-speicher-backend-1
```

```text
status=exited exit=137 oom=true mem=8388608
```

**Ursache:** `memory: 8M` unter `deploy.resources.limits`; Python mit Flask braucht beim Start gut 20 MB. Der OOM-Killer beendet den Prozess.

**Behebung:** Grenze in `compose.yml` erhöhen:

```yaml
    deploy:
      resources:
        limits:
          memory: 64M
          cpus: "0.5"
```

```bash
docker compose up -d
docker stats --no-stream fehler4-speicher-backend-1 fehler4-speicher-frontend-1
```

```text
CONTAINER ID   NAME                          CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O    PIDS
e4a9b57e9a30   fehler4-speicher-backend-1    0.02%     22.39MiB / 64MiB      34.99%    1.52kB / 737B    0B / 0B      1
5a5c03ed996d   fehler4-speicher-frontend-1   0.03%     27.18MiB / 7.65GiB    0.35%     3.5kB / 2.65kB   0B / 176kB   1
```

Das Backend nutzt etwa ein Drittel seiner Grenze; `http://localhost:8704` zeigt die Backend-Antwort. Das Frontend hat keine Grenze, daher steht dort der gesamte Speicher von Docker (bei Docker Desktop: der Linux-VM).

## Aufgabe 5: Aufräumen

```bash
cd ..
for d in fehler1-cmd fehler2-copy fehler3-netzwerk fehler4-speicher; do (cd $d && docker compose down); done
docker ps -a --filter name=fehler
```

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Die Liste ist leer. Die Images `fehler1-frontend:1.0` und `fehler2-frontend:1.0` bleiben; bei Bedarf `docker image rm fehler1-frontend:1.0 fehler2-frontend:1.0`.

| Fehlerbild | Gruppe | Befehl, der die Ursache zeigt | Ursache |
| --- | --- | --- | --- |
| 1 | Start | `docker compose ps -a`, `docker compose logs frontend` | Tippfehler `fronted.py` in `CMD` |
| 2 | Build | Build-Ausgabe, `cat frontend/.dockerignore` | `*.txt` schließt `requirements.txt` aus |
| 3 | Netzwerk | `docker compose exec frontend curl …`, `docker network inspect` | Frontend und Backend in getrennten Netzwerken |
| 4 | Ressourcen | `docker compose ps -a`, `docker inspect … OOMKilled` | Speichergrenze 8 MB zu klein |

## Erweiterung: Programmname falsch

Mit `CMD ["pyton", "frontend.py"]` scheitert nicht Python, sondern schon Docker beim Starten des Programms:

```text
Error response from daemon: failed to create task for container: … exec: "pyton": executable file not found in $PATH
```

`docker compose ps -a` zeigt für das Frontend einen Exit-Code `127` (Befehl nicht gefunden) statt `2` (Python findet die Datei nicht). Danach `pyton` wieder zu `python` ändern und mit `docker compose up -d --build` neu starten.
