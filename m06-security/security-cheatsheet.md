# Cheatsheet: Docker-Sicherheit

Befehle aus Modul 6 (Labs 6.1–6.3). Kurs-Shell `bash`; unter Windows Git Bash mit `MSYS_NO_PATHCONV=1`.

## Benutzer und Rechte prüfen

| Befehl | Wirkung |
| --- | --- |
| `docker compose exec frontend whoami` | Benutzer des Dienstes `frontend` (ohne `USER`: `root`) |
| `docker compose exec frontend id -u` | Benutzer-ID; `0` = root |
| `docker compose top frontend` | Prozesse des Dienstes mit Benutzer (Spalte `UID`) |
| `docker compose exec --user root frontend chown -R app /data` | einen einzelnen Befehl als root ausführen, z. B. Besitzer im Volume ändern |
| `docker run --rm -v /:/host alpine:3.24 ls /host` | zeigt, dass ein Container das ganze Host-Dateisystem einbinden kann (nur zur Demonstration) |
| `docker run --rm -v "$HOME":/home-host:ro alpine:3.24 ls /home-host` | Ordner schreibgeschützt einbinden (`:ro`) |
| `docker run -p 127.0.0.1:8080:80 …` | Port nur für den eigenen Rechner veröffentlichen |

## Eigener Benutzer im Dockerfile

| Anweisung | Wirkung |
| --- | --- |
| `RUN adduser -D app` | Benutzer `app` ohne Passwort anlegen (Alpine) |
| `RUN useradd -m app` | dasselbe für Debian/Ubuntu-Images |
| `RUN mkdir -p /data && chown app /data` | Ordner dem Benutzer übergeben, bevor `USER` greift |
| `USER app` | alle folgenden Anweisungen und der Container laufen als `app` |

## Ressourcen begrenzen

| Befehl / Flag | Wirkung |
| --- | --- |
| `docker run --memory 64m …` | harte Speichergrenze (`-m`); darüber: `OOMKilled`, Exit-Code 137 |
| `--memory-swap 64m` | Speicher plus Auslagerung; gleich `--memory` = keine Auslagerung |
| `--memory-reservation 32m` | weiche Untergrenze bei Speicherknappheit |
| `--cpus 0.5` | höchstens ein halber CPU-Kern; darüber wird gebremst |
| `--cpu-shares 512` | Gewichtung bei CPU-Konkurrenz (Standard 1024) |
| `--cpuset-cpus 0,1` | nur diese Kerne |
| `--blkio-weight 300` | Gewichtung beim Festplattenzugriff (10–1000), nur mit Kernel-Unterstützung |
| `--pids-limit 100` | höchstens 100 Prozesse |
| `docker update --memory 128m --memory-swap 128m <container>` | Grenzen eines laufenden Containers ändern |
| `docker inspect <container> --format '{{.HostConfig.Memory}} {{.HostConfig.NanoCpus}}'` | gesetzte Grenzen in Byte bzw. Milliardstel Kernen |
| `docker inspect <container> --format '{{.State.OOMKilled}} {{.State.ExitCode}}'` | wurde der Container wegen Speicher beendet? |

## Verbrauch messen

| Befehl | Wirkung |
| --- | --- |
| `docker stats` | CPU, Speicher, Netz, Festplatte aller laufenden Container, live (Strg+C beendet) |
| `docker stats --no-stream` | einmal messen und beenden |
| `docker stats --no-stream backend-limits` | nur ein Container |
| `docker info` | u. a. `Cgroup Version: 2` |

## Grenzen in Compose

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: "0.5"          # wie --cpus
          memory: 128M         # wie --memory
        reservations:
          memory: 64M          # wie --memory-reservation
```

## Images scannen

| Befehl | Wirkung |
| --- | --- |
| `docker scout quickview frontend:v1` | Lücken je Schweregrad (C, H, M, L) für Image und Basisimage |
| `docker scout cves frontend:v1` | alle Lücken mit Paket, CVE, Fixed Version |
| `docker scout cves --only-severity critical,high frontend:v1` | nur kritische und hohe Lücken |
| `docker scout recommendations python:3.9-alpine` | Vorschläge für ein besseres Basisimage |
| `docker scout compare frontend:v2 --to frontend:v1` | zwei Images vergleichen |
| `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivy-cache:/root/.cache/ aquasec/trivy:0.76.2 image frontend:v1` | Scan mit Trivy, ohne Docker-Konto |
| `… aquasec/trivy:0.76.2 image --severity CRITICAL,HIGH python:3.9-alpine` | Trivy: nur kritische und hohe Lücken |
| `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock anchore/grype:v0.122.1 frontend:v1` | Scan mit Grype |
| `docker compose build --pull` | neu bauen und dabei das Basisimage neu laden (Sicherheitsupdates) |

## Werkzeuge

| Bereich | Werkzeuge |
| --- | --- |
| Vulnerability Scanning | Docker Scout, Trivy, Grype |
| Image Signing | cosign (Sigstore), Notation (Notary Project); Docker Content Trust wird abgelöst |
| Runtime Protection | Falco, Docker Desktop Enhanced Container Isolation |
