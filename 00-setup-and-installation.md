# Setup und Installation

Alle Übungen laufen auf dem eigenen Rechner: Docker Desktop bringt Docker Engine, Docker CLI, Docker Compose und den Swarm-Modus mit, dazu kommen ein Editor und ein Browser.
Die Installation gehört vor den ersten Kurstag; sie dauert etwa 20–30 Minuten, Downloads eingeschlossen.

## Software für den Kurs

| Software | Zweck im Kurs | Prüfen mit | Gebraucht ab |
| --- | --- | --- | --- |
| Docker Desktop (aktuelle Version, Engine 29.x) | Container bauen und starten, Compose, Swarm, Docker Scout | `docker version` | Lab 1.1 |
| kostenloses Docker-Konto | höhere Download-Grenze, Docker Scout, Push auf Docker Hub | `docker login` | Lab 1.1 (empfohlen), Pflicht ab Lab 6.3 |
| VS Code mit Erweiterung **Docker** bzw. **Container Tools** | Dockerfiles und Compose-Dateien schreiben, Syntaxhilfe | Erweiterungen-Ansicht | Lab 3.2 |
| Browser | Webseiten der Container öffnen | – | Lab 2.1 |
| `curl` | HTTP-Anfragen im Terminal | `curl --version` | Lab 4.3 |
| nur Windows: WSL 2 | Linux-Unterbau für Docker Desktop | `wsl --version` | Lab 1.1 |
| nur Windows: Git for Windows (Git Bash) | Kurs-Shell `bash` | `bash --version` | Lab 1.1 |

Stand der Versionen: 11/2026, vor Kursbeginn prüfen. Git selbst wird im Kurs nicht gebraucht; die Kursdateien gibt es auch als ZIP.

## Voraussetzungen am Rechner

- **Arbeitsspeicher:** mindestens 8 GB, 16 GB empfohlen; der Monitoring-Stack in Lab 7.2 belegt zusätzlich etwa 1 GB.
- **Betriebssystem:** macOS in einer der drei neuesten Hauptversionen; Windows 10 22H2 oder Windows 11 23H2 und neuer, jeweils 64 Bit; Linux mit Docker Engine oder Docker Desktop.
- **Virtualisierung:** im BIOS/UEFI eingeschaltet (Windows); auf Firmenrechnern kann eine Richtlinie sie sperren.
- **Rechte:** WSL 2 einschalten braucht einmalig Administratorrechte; Docker Desktop selbst lässt sich unter Windows auch pro Benutzer installieren.
- **Netzwerk:** Zugriff auf `docker.io` (Docker Hub), `ghcr.io`, `github.com` und `registry.npmjs.org`; hinter einem Firmen-Proxy muss Docker Desktop den Proxy kennen (**Settings > Resources > Proxies**).
- **Lizenz:** Docker Desktop ist für Firmen ab 250 Beschäftigten oder 10 Mio. USD Jahresumsatz kostenpflichtig ([Docker Desktop License](https://docs.docker.com/subscription/desktop-license/), Stand: 11/2026). Alternativen stehen in Lab 2.3.

Quellen: [Docker Desktop für Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [Docker Desktop für Mac](https://docs.docker.com/desktop/setup/install/mac-install/), [Docker Engine für Linux](https://docs.docker.com/engine/install/), abgerufen am 23.11.2026.

## Kurs-Shell: bash

Alle Befehle in den Handouts sind für die Shell `bash` geschrieben.

| System | Shell | Öffnen |
| --- | --- | --- |
| macOS | Terminal (zsh versteht alle Kursbefehle) | **Programme > Dienstprogramme > Terminal** oder Terminal in VS Code |
| Linux | Terminal mit bash | Terminal oder Terminal in VS Code |
| Windows | **Git Bash** aus Git for Windows | Startmenü > **Git Bash**, oder in VS Code als Standard-Terminal |

Git Bash unter Windows einrichten:

1. Installiere Git for Windows von [git-scm.com](https://git-scm.com/downloads/win) oder per `winget install --id Git.Git -e` (PowerShell). Die vorgeschlagenen Standardoptionen passen.
2. Setze Git Bash in VS Code als Standard-Terminal: `Strg+Umschalt+P` > **Terminal: Select Default Profile** > **Git Bash**.
3. Schalte in Git Bash die automatische Pfad-Umwandlung ab. Git Bash schreibt sonst Linux-Pfade wie `/usr/share/nginx/html` in Windows-Pfade um, und Befehle wie `docker exec … ls /usr/share/nginx/html` schlagen fehl:

   ```bash
   echo 'export MSYS_NO_PATHCONV=1' >> ~/.bashrc
   source ~/.bashrc
   ```

4. Für interaktive Befehle (`docker run -it`, `docker exec -it`) das Terminal in VS Code nutzen oder `winpty` voranstellen.

## Docker Desktop installieren

| System | Weg |
| --- | --- |
| macOS | Installer von [docs.docker.com/desktop/setup/install/mac-install](https://docs.docker.com/desktop/setup/install/mac-install/) (Apple silicon oder Intel wählen) oder `brew install --cask docker-desktop` |
| Windows | Zuerst WSL 2: PowerShell **als Administrator** öffnen, `wsl --install` (neu) bzw. `wsl --update` (vorhanden), neu starten. Dann den Installer von [docs.docker.com/desktop/setup/install/windows-install](https://docs.docker.com/desktop/setup/install/windows-install/) ausführen, Backend **WSL 2** belassen. |
| Linux | Docker Engine mit Compose-Plugin nach [docs.docker.com/engine/install](https://docs.docker.com/engine/install/) oder Docker Desktop für Linux; Benutzer danach in die Gruppe `docker` aufnehmen (Lab 6.1 erklärt, was das bedeutet) |

<img src="https://www.docker.com/app/uploads/2025/05/DD-hiroko-2320x1456.png" alt="Docker Desktop, Ansicht Containers: links die Navigation mit Containers, Images, Volumes, Builds und Docker Scout, rechts eine Tabelle mit Containern, Images und Ports; unten links die Statusleiste mit Engine running" width="640">

_Quelle: Docker Inc., „Docker Desktop" (https://www.docker.com/products/docker-desktop/), abgerufen am 23.11.2026._

Das Dashboard zeigt links die Ansichten **Containers**, **Images** und **Volumes**; die Statusleiste unten meldet `Engine running`, sobald Docker bereit ist.

## VS Code mit Docker-Erweiterung

Installiere VS Code von [code.visualstudio.com](https://code.visualstudio.com/) und danach in der Erweiterungen-Ansicht (`Strg+Umschalt+X`, macOS `Cmd+Shift+X`) die Erweiterung **Container Tools** von Microsoft (früher „Docker"). Sie markiert Fehler in Dockerfiles und Compose-Dateien und zeigt Container, Images und Volumes in der Seitenleiste. Name der Erweiterung: Stand 11/2026, vor Kursbeginn prüfen.

## Kursdateien holen

Beide Wege führen zum selben Ordner.

| Weg | Schritte |
| --- | --- |
| ZIP | [ZIP herunterladen](https://github.com/kodschul/kodschul-docker-open-3/archive/refs/heads/main.zip), entpacken, z. B. nach `~/kurs/` |
| git (optional) | `git clone https://github.com/kodschul/kodschul-docker-open-3.git ~/kurs/kodschul-docker-open-3` |

Öffne den Ordner danach in VS Code (**File > Open Folder**) und im Terminal den Unterordner `project/`:

```bash
cd ~/kurs/kodschul-docker-open-3/project    # beim ZIP heißt der Ordner kodschul-docker-open-3-main
ls
```

```text
build-images.sh  examples  playground  starters  variants
```

| Ordner | Inhalt |
| --- | --- |
| `playground/` | eigener Arbeitsbereich; `playground/hello/` ist die Hello-App, weitere Übungs-Apps entstehen daneben |
| `starters/` | unvollständige Startdateien der Übungen zum Kopieren nach `playground/` |
| `examples/<modul>/<lab>/` | fertiger Stand jedes Labs zum Vergleichen und Wiederherstellen |
| `variants/` | absichtlich fehlerhafte Dateien für die Fehlersuche in Lab 7.1 |

## Installation prüfen

Führe die Befehle in der Kurs-Shell aus. Versionsnummern dürfen abweichen; wichtig ist, dass jeder Befehl antwortet.

```bash
docker version --format 'Client {{.Client.Version}} / Server {{.Server.Version}}'
docker compose version
docker run --rm hello-world
```

Erwartete Ausgabe (gekürzt):

```text
Client 29.9.3 / Server 29.9.3
Docker Compose version v2.x.x
Hello from Docker!
This message shows that your installation appears to be working correctly.
…
```

## Docker-Hub-Limit und docker login

Docker Hub begrenzt Downloads (Pulls) von Images je 6 Stunden:

| Nutzer | Pulls je 6 Stunden |
| --- | --- |
| ohne Anmeldung | 100 je IPv4-Adresse |
| mit kostenlosem Docker-Konto | 200 je Konto |

In einem Firmennetz teilen sich oft alle Rechner eine öffentliche IP-Adresse; dann ist das anonyme Limit schnell aufgebraucht und `docker pull` meldet `toomanyrequests`. Abhilfe: ein kostenloses Konto auf [hub.docker.com](https://hub.docker.com/) anlegen und anmelden.

```bash
docker login
```

Der Befehl zeigt einen Code und eine Adresse; im Browser bestätigen, danach meldet das Terminal `Login Succeeded`. Alternativ in Docker Desktop oben rechts **Sign in** wählen. Das Konto braucht der Kurs außerdem für Docker Scout (Lab 6.3) und Docker Hub (Lab 8.1, 8.2). Quelle: [Docker Hub Pull-Limits](https://docs.docker.com/docker-hub/usage/pulls/), Stand: 11/2026.

## Fallback ohne Docker Desktop

| Situation | Weg |
| --- | --- |
| Docker Desktop aus Lizenzgründen nicht erlaubt | Rancher Desktop (Engine **dockerd (moby)** wählen), Podman Desktop oder unter macOS OrbStack; die Kursbefehle funktionieren dort weitgehend gleich (Lab 2.3) |
| keine Installation auf dem Rechner möglich | Linux-VM mit Docker Engine (z. B. Ubuntu 24.04) |
| Docker Scout ohne Konto | Trivy als Container (Lab 6.3) |

## Typische Installationsprobleme

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `Cannot connect to the Docker daemon` / `failed to connect to the docker API` | Docker Desktop läuft nicht | Docker Desktop starten, warten bis `Engine running` |
| Windows: „WSL 2 installation is incomplete" oder „Virtualization support not detected" | WSL fehlt oder Virtualisierung aus | PowerShell als Administrator: `wsl --install` bzw. `wsl --update`; Virtualisierung im BIOS/UEFI einschalten |
| `docker: unknown command: docker compose` | altes Docker ohne Compose-Plugin | Docker Desktop aktualisieren bzw. unter Linux das Paket `docker-compose-plugin` installieren |
| `toomanyrequests: You have reached your pull rate limit` | Docker-Hub-Limit der gemeinsamen IP erreicht | `docker login` (siehe oben) |
| `permission denied while trying to connect to the Docker daemon socket` (Linux) | Benutzer nicht in der Gruppe `docker` | `sudo usermod -aG docker $USER`, danach ab- und wieder anmelden |
| Git Bash: `ls: cannot access 'C:/Program Files/Git/usr/share/…'` | Pfad-Umwandlung von Git Bash | `export MSYS_NO_PATHCONV=1` in `~/.bashrc` (siehe Kurs-Shell) |
| Git Bash: `the input device is not a TTY` bei `docker exec -it` | Git-Bash-Fenster (mintty) ohne echtes Terminal | Befehl mit `winpty` beginnen oder das Terminal in VS Code nutzen |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | anderer Container oder Dienst nutzt den Port | `docker ps` prüfen, alten Container mit `docker rm -f <name>` bzw. `docker compose down` entfernen |
