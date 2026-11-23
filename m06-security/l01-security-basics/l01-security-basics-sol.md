# Lab 6.1 – Lösung: Grundlagen der Docker-Sicherheit

IDs, Prozessnummern, Zeiten und Ordnerlisten unterscheiden sich je Rechner.

## Aufgabe 1: Benutzer im Hello-Frontend

```bash
docker compose exec frontend whoami
docker compose exec frontend id -u
```

```text
root
0
```

Das Frontend-Dockerfile aus Lab 3.2 hat keine Anweisung `USER`, also läuft der Prozess als root (Benutzer-ID 0).

## Aufgabe 2: Prozesse im Container

```bash
docker compose top frontend
```

```text
SERVICE   #   UID   PID    PPID   C   STIME  TTY  TIME      CMD
frontend  1   root  22179  22153  9   22:23  ?    00:00:00  python frontend.py
```

Der Hauptprozess `python frontend.py` läuft als `root`. Die Spalte `PID` zeigt die Nummer auf dem Host (bzw. in der VM); im Container selbst hat er die Nummer 1 (vertieft in Lab 6.2).

## Aufgabe 3: Wurzelverzeichnis des Hosts einbinden

```bash
docker run --rm -v /:/host alpine:3.24 ls /host
```

Ausgabe unter Docker Desktop für macOS (gekürzt):

```text
Users
Volumes
bin
boot
containers
dev
etc
home
host_mnt
lib
…
root
run
sbin
services
srv
sys
tmp
usr
var
```

```bash
docker run --rm alpine:3.24 ls /
```

```text
bin
dev
etc
home
lib
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

- Ohne Mount zeigt der Container sein eigenes Dateisystem aus dem Image.
- Mit `-v /:/host` liegt unter `/host` das Dateisystem des Hosts: unter Linux das des Rechners, unter Docker Desktop das der Linux-VM. Die Ordnerliste weicht deshalb vom Alpine-Image ab.
- Unter Docker Desktop für macOS enthält die VM auch `/Users` und `/host_mnt`: die freigegebenen Ordner des Mac. Über diesen Umweg erreicht der Container auch dort die eigenen Dateien.

## Aufgabe 4: Als root auf dem Host schreiben

```bash
docker run --rm -v /:/host alpine:3.24 sh -c 'echo "geschrieben von einem Container" > /host/tmp/container-war-hier.txt'
docker run --rm -v /:/host alpine:3.24 ls -l /host/tmp/container-war-hier.txt
docker run --rm -v /:/host alpine:3.24 rm /host/tmp/container-war-hier.txt
```

```text
-rw-r--r--    1 root     root            32 Nov 23 22:23 /host/tmp/container-war-hier.txt
```

Die Datei bleibt nach dem Ende des Containers auf dem Host und gehört `root`. Genauso könnte ein Container Dateien unter `/host/etc` ändern. Deshalb gilt: Wer `docker run` ausführen darf, hat root-Rechte auf dem Host.

## Aufgabe 5: Benutzerordner schreibgeschützt einbinden

```bash
docker run --rm -v "$HOME":/home-host:ro alpine:3.24 sh -c 'ls /home-host | head -5; touch /home-host/test.txt'
```

```text
AndroidStudioProjects
Applications
Desktop
Documents
Downloads
touch: /home-host/test.txt: Read-only file system
```

Die ersten fünf Einträge sind die Ordner des eigenen Benutzerordners und unterscheiden sich je Rechner; `touch` endet mit Exit-Code 1.

- Auch unter Docker Desktop erreicht ein Container über die Dateifreigabe den eigenen Benutzerordner; ohne `:ro` könnte er dort Dateien ändern oder löschen.
- `:ro` erlaubt nur Lesen. Lesen allein kann schon Schlüssel oder Passwörter (z. B. `~/.ssh`) preisgeben; deshalb nur die Ordner einbinden, die der Container wirklich braucht.
