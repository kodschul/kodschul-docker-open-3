# Docker-CLI-Cheatsheet (Module 1 und 2)

Alle Befehle für die Kurs-Shell `bash` ([Setup](../00-setup-and-installation.md#kurs-shell-bash)). Platzhalter in spitzen Klammern ersetzen.

## Installation und Engine prüfen

| Befehl | Wirkung |
| --- | --- |
| `docker run hello-world` | Testcontainer starten; gibt `Hello from Docker!` aus (Lab 1.1) |
| `docker version` | Versionen von Client und Server (Docker Engine) |
| `docker info` | Details zur Engine: Kernel, CPUs, Speicher, Anzahl Container und Images |
| `docker info --format '{{.KernelVersion}}'` | nur ein Feld von `docker info` ausgeben |
| `docker --help` / `docker <befehl> --help` | alle Befehle bzw. Optionen eines Befehls |

## Images

| Befehl | Wirkung |
| --- | --- |
| `docker pull nginx:1.30-alpine` | Image aus der Registry laden, ohne Container zu starten |
| `docker images` | lokale Images mit Tag und Größe |
| `docker history <image>` | Bauschritte (Schichten) eines Images |

## Container starten

| Befehl | Wirkung |
| --- | --- |
| `docker run <image> <befehl>` | Container erstellen und Befehl darin ausführen, z. B. `docker run busybox:1.37 echo hallo` |
| `docker run --rm <image> …` | Container nach dem Ende automatisch löschen |
| `docker run -d --name webserver -p 8080:80 nginx:1.30-alpine` | im Hintergrund (`-d`), mit Namen, Port 8080 des Rechners auf Port 80 im Container |
| `docker run -it --name <name> busybox:1.37` | neuer Container mit interaktiver Shell; `exit` beendet ihn |
| `docker run -it --rm -v .:/hello busybox:1.37` | aktuellen Ordner als `/hello` im Container einbinden (Bind Mount) |
| `time docker run --rm alpine:3.24 echo hallo` | Startzeit eines Containers messen |

## Container anzeigen und steuern

| Befehl | Wirkung |
| --- | --- |
| `docker ps` | laufende Container |
| `docker ps -a` | alle Container, auch beendete (mit Exit-Code) |
| `docker stop <name>` | sauber beenden (`SIGTERM`, nach 10 s `SIGKILL`) |
| `docker kill <name>` | sofort beenden (`SIGKILL`, Exit-Code 137) |
| `docker start <name>` | beendeten Container wieder starten |
| `docker start -ai <name>` | wieder starten und mit seiner Shell verbinden |
| `docker restart <name>` | stoppen und starten, z. B. nach geänderter Konfiguration |
| `docker rm <name>` | beendeten Container löschen (Image bleibt) |
| `docker rm -f <name>` | auch laufenden Container stoppen und löschen |

## In Container hineinschauen

| Befehl | Wirkung |
| --- | --- |
| `docker exec <name> ls /usr/share/nginx/html` | Befehl im laufenden Container ausführen |
| `docker exec -it <name> sh` | interaktive Shell im laufenden Container |
| `docker logs <name>` | bisherige Ausgaben des Hauptprozesses |
| `docker logs --tail 3 <name>` | nur die letzten 3 Zeilen |
| `docker logs -f <name>` | live mitlesen (`Strg+C` beendet nur das Mitlesen) |

## Dateien

| Befehl | Wirkung |
| --- | --- |
| `docker cp <name>:/pfad/datei .` | Datei aus dem Container in den aktuellen Ordner kopieren |
| `docker cp datei <name>:/pfad/datei` | Datei vom Rechner in den Container kopieren |
| `-v <ordner-auf-dem-rechner>:<pfad-im-container>` | Option für `docker run`: Ordner des Rechners einbinden; Änderungen sind auf beiden Seiten sichtbar |

## Docker und Podman

| Docker | Podman (Lab 2.3) |
| --- | --- |
| `docker run -d -p 8080:80 nginx:1.30-alpine` | `podman run -d -p 8080:80 docker.io/library/nginx:1.30-alpine` |
| `docker ps`, `docker logs`, `docker rm -f` | `podman ps`, `podman logs`, `podman rm -f` |

## Windows mit Git Bash

| Befehl | Wirkung |
| --- | --- |
| `export MSYS_NO_PATHCONV=1` | Pfad-Umwandlung abschalten (einmalig in `~/.bashrc`) |
| `winpty docker run -it …` | interaktive Befehle im Git-Bash-Fenster; im VS-Code-Terminal nicht nötig |
