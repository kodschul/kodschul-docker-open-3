# Lab 6.3 – Lösung: Docker Security Scanning und andere Tools

Die Zahl der Lücken ändert sich täglich: Neue CVEs kommen hinzu, neue Paketversionen beheben alte. Die Zahlen unten stammen aus einem Trivy-Scan vom 23.11.2026 (Fallback); Docker Scout nutzt eigene Datenbanken und zählt deshalb nicht genau gleich.

Ohne Anmeldung bricht jeder `docker scout`-Befehl ab (Exit-Code 1):

```text
Log in with your Docker ID or email address to use docker scout.

If you don't have a Docker ID, head over to https://hub.docker.com to
create one. You can log in with your password or a Personal Access Token (PAT)
by running docker login.
…
You can also log in using Docker Desktop.
```

Dann `docker login` ausführen oder den Trivy-Fallback am Ende nutzen.

## Aufgabe 1: Kurzfassung mit `quickview`

```bash
docker scout quickview frontend:v1
docker pull python:3.9-alpine
docker scout quickview python:3.9-alpine
```

Aufbau der Ausgabe nach `docker login` (schematisch, Zahlen aus dem Trivy-Scan vom 23.11.2026):

```text
  Target     │  frontend:v1          │    0C     0H     7M     4L
  Base image │  python:3.13-alpine   │    0C     0H     7M     4L

  Target     │  python:3.9-alpine    │    2C    28H    32M    51L
```

| Image | Betriebssystem-Pakete | Python-Pakete |
| --- | --- | --- |
| `frontend:v1` (Alpine 3.24) | 11 (0 C, 0 H, 7 M, 4 L) | 8 (0 C, 5 H, 2 M, 1 L) |
| `python:3.9-alpine` (Alpine 3.22) | 113 (2 C, 28 H, 32 M, 51 L) | 12 (0 C, 3 H, 7 M, 2 L) |

- Die Lücken von `frontend:v1` stammen fast alle aus dem Basisimage `python:3.13-alpine`, nicht aus dem eigenen Code.
- `python:3.9-alpine` ist veraltet: Python 3.9 bekommt seit Oktober 2025 keine Sicherheitsupdates mehr, das Image basiert auf einem älteren Alpine mit vielen behobenen, aber hier nicht eingespielten Lücken.

## Aufgabe 2: Kritische und hohe Lücken mit `cves`

```bash
docker scout cves --only-severity critical,high frontend:v1
docker scout cves --only-severity critical,high python:3.9-alpine
```

Beispiele aus den Ergebnissen (Ausschnitt):

| Image | Paket | Installiert | CVE | Schweregrad | Fixed Version |
| --- | --- | --- | --- | --- | --- |
| `frontend:v1` | `urllib3` (pip) | 2.7.0 | CVE-2026-97687 | HIGH | 2.8.0 |
| `frontend:v1` | `setuptools` (pip) | 70.3.0 | CVE-2025-47273 | HIGH | 78.1.1 |
| `python:3.9-alpine` | `libcrypto3`, `libssl3` (OpenSSL) | 3.5.4-r0 | CVE-2026-31789 | CRITICAL | 3.5.6-r0 |

- Die betroffenen Python-Pakete in `frontend:v1` sind Kopien, die `pip` selbst mitbringt, nicht die Pakete aus `requirements.txt`.
- `Fixed Version` sagt, welche Version die Lücke schließt: hier reicht ein neueres Basisimage bzw. ein Update von `pip`.

## Aufgabe 3: Empfehlungen mit `recommendations`

```bash
docker scout recommendations python:3.9-alpine
```

Die Ausgabe schlägt zwei Wege vor:

- **Refresh base image:** dasselbe Tag neu laden (`docker pull python:3.9-alpine`), falls inzwischen eine neuere Bauversion existiert.
- **Change base image:** auf ein aktuelles Tag wechseln, z. B. `python:3.13-alpine` oder `python:3.14-alpine`, jeweils mit der Zahl der Lücken, die dadurch wegfallen.

Für die Hello-App heißt das: Basisimage `python:3.13-alpine` behalten und regelmäßig neu bauen (`docker compose build --pull`; `--pull` lädt dabei das Basisimage neu), damit Sicherheitsupdates von Alpine und Python ankommen.

## Aufgabe 4: Frontend ohne root bauen

Ergänzung in `project/playground/hello/frontend/Dockerfile` direkt vor `CMD` (vollständig in `project/examples/m06-security/l03-security-scanning/hello/frontend/Dockerfile`):

```dockerfile
# Benutzer app ohne Passwort anlegen (-D, Alpine), Ordner /data für access.log ihm übergeben
RUN adduser -D app && mkdir -p /data && chown app /data
# Ab hier laufen weitere Anweisungen und der Container als app statt root
USER app

CMD ["python", "frontend.py"]
```

```bash
docker compose up -d --build frontend
```

```text
…
#21 [frontend 8/8] RUN adduser -D app && mkdir -p /data && chown app /data
#21 DONE 0.3s
…
#22 naming to docker.io/library/frontend:v2 done
…
 Image frontend:v2 Built
 Container hello-backend-1 Running
 Container hello-frontend-1 Recreate
 Container hello-frontend-1 Recreated
 Container hello-backend-1 Waiting
 Container hello-backend-1 Healthy
 Container hello-frontend-1 Starting
 Container hello-frontend-1 Started
```

Der Build ersetzt das lokale Image `frontend:v2`; ab jetzt läuft jedes Frontend aus `frontend:v2` als `app`.

`USER` steht am Ende, damit `apk add` und `pip install` weiter als root laufen; nur der fertige Container verliert die Rechte.

## Aufgabe 5: Benutzer und Seite prüfen

```bash
docker compose exec frontend whoami
```

```text
app
```

Die Hello-Seite zeigt „Hello World 2.0.0" und die Backend-Antwort, aber „Aufrufe in access.log: nicht beschreibbar": `access.log` im Volume `hello-data` wurde in Lab 4.3 von root angelegt.

```bash
docker compose exec frontend ls -l /data
docker compose exec --user root frontend chown -R app /data
docker compose exec frontend ls -l /data
```

```text
total 4
-rw-r--r--    1 root     root           117 Nov 23 22:24 access.log
total 4
-rw-r--r--    1 app      root           117 Nov 23 22:24 access.log
```

Nach dem Neuladen zählt die Seite wieder weiter. `--user root` gilt nur für diesen einen Befehl; der Dienst selbst läuft weiter als `app`.

## Erweiterung: Images vergleichen

```bash
docker scout compare frontend:v2 --to frontend:v1
```

Beide Images enthalten dieselben Pakete; der Vergleich zeigt deshalb keine neuen oder behobenen Lücken. `USER` beseitigt keine Lücken, begrenzt aber den Schaden, wenn eine ausgenutzt wird.

## Fallback: Trivy statt Docker Scout

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivy-cache:/root/.cache/ \
  aquasec/trivy:0.76.2 image --severity CRITICAL,HIGH python:3.9-alpine
```

```text
Report Summary

┌──────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                       Target                         │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ python:3.9-alpine (alpine 3.22.2)                    │   alpine   │       30        │    -    │
├──────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ …                                                    │            │                 │         │

python:3.9-alpine (alpine 3.22.2)
=================================
Total: 30 (HIGH: 28, CRITICAL: 2)

┌────────────┬─────────────────┬──────────┬────────┬───────────────────┬───────────────┬──────────────────────────────────────────────────────────────┐
│  Library   │  Vulnerability  │ Severity │ Status │ Installed Version │ Fixed Version │                            Title                             │
├────────────┼─────────────────┼──────────┼────────┼───────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ libcrypto3 │ CVE-2026-31789  │ CRITICAL │ fixed  │ 3.5.4-r0          │ 3.5.6-r0      │ openssl: OpenSSL: Heap buffer overflow on 32-bit systems     │
│            │                 │          │        │                   │               │ from large X.509 certificate...                              │
…
```

Der erste Lauf lädt die Schwachstellen-Datenbank (ca. 140 MB) ins Volume `trivy-cache`; weitere Läufe sind schneller.
