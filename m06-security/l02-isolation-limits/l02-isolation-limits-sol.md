# Lab 6.2 – Lösung: Containerisolierung und Ressourcenbeschränkungen

IDs, Messwerte und Zeiten unterscheiden sich je Rechner.

## Aufgabe 1: Backend mit Grenzen starten

```bash
docker run -d --name backend-limits --memory 64m --cpus 0.5 backend:v1
docker stats --no-stream backend-limits
docker inspect backend-limits --format '{{.HostConfig.Memory}} {{.HostConfig.NanoCpus}}'
```

```text
6d9e211f047e47d6075bab5505c8e35b2c6ac5746abf35b3063e33ba62c8a3ce
CONTAINER ID   NAME             CPU %     MEM USAGE / LIMIT   MEM %     NET I/O         BLOCK I/O    PIDS
6d9e211f047e   backend-limits   0.04%     21.23MiB / 64MiB    33.18%    1.26kB / 126B   0B / 172kB   1
67108864 500000000
```

- `docker inspect` speichert Speicher in Byte (64 × 1024 × 1024 = 67108864) und CPU in Milliardstel Kernen (`NanoCpus`, 0,5 Kerne = 500000000).
- Das Backend braucht im Leerlauf gut 20 MiB; 64 MiB reichen.

## Aufgabe 2: Grenze im Betrieb ändern

```bash
docker update --memory 128m --memory-swap 128m backend-limits
docker stats --no-stream backend-limits
docker rm -f backend-limits
```

```text
backend-limits
CONTAINER ID   NAME             CPU %     MEM USAGE / LIMIT   MEM %     NET I/O         BLOCK I/O    PIDS
6d9e211f047e   backend-limits   0.02%     21.23MiB / 128MiB   16.59%    1.26kB / 126B   0B / 172kB   1
backend-limits
```

`docker update` ändert die Cgroup des laufenden Containers; ein Neustart ist nicht nötig. `docker update --memory 128m backend-limits` allein funktioniert ebenfalls.

## Aufgabe 3: Speichergrenze überschreiten

```bash
docker run --name oom-test --memory 32m --memory-swap 32m python:3.13-alpine \
  python -c "x = bytearray(100 * 1024 * 1024)"
echo "Exit-Code: $?"
docker ps -a --filter name=oom-test
docker inspect oom-test --format '{{.State.OOMKilled}} {{.State.ExitCode}}'
docker rm oom-test
```

```text
Exit-Code: 137
CONTAINER ID   IMAGE                COMMAND                  CREATED                  STATUS                                PORTS     NAMES
d7a45978047c   python:3.13-alpine   "python -c 'x = byte…"   Less than a second ago   Exited (137) Less than a second ago             oom-test
true 137
oom-test
```

Python will 100 MB belegen, die Grenze erlaubt 32 MB. Der OOM-Killer beendet den Prozess sofort und ohne eigene Fehlermeldung; erst `OOMKilled: true` und Exit-Code 137 (128 + Signal 9 `KILL`) zeigen den Grund.

## Aufgabe 4: Grenzen in `compose.yml`

Änderung in `project/playground/hello/compose.yml` (vollständig in `project/examples/m06-security/l02-isolation-limits/hello/compose.yml`):

```yaml
services:
  frontend:
    # … image, build, depends_on, ports, volumes wie bisher …
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 128M
    develop:
      # … wie bisher …

  backend:
    # … image, build, healthcheck wie bisher …
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 128M
```

```bash
docker compose up -d
```

```text
 Container hello-backend-1 Recreate
 Container hello-backend-1 Recreated
 Container hello-frontend-1 Recreate
 Container hello-frontend-1 Recreated
 Container hello-backend-1 Starting
 Container hello-backend-1 Started
 Container hello-backend-1 Waiting
 Container hello-backend-1 Healthy
 Container hello-frontend-1 Starting
 Container hello-frontend-1 Started
```

Compose erkennt die geänderte Konfiguration und erstellt beide Container neu; das Volume `hello-data` bleibt erhalten.

## Aufgabe 5: Grenzen prüfen

```bash
docker stats --no-stream
```

```text
CONTAINER ID   NAME               CPU %     MEM USAGE / LIMIT   MEM %     NET I/O        BLOCK I/O    PIDS
5d5b0cb1c57d   hello-frontend-1   0.02%     25.72MiB / 128MiB   20.10%    872B / 126B    0B / 172kB   1
8742dff9824a   hello-backend-1    0.02%     21.24MiB / 128MiB   16.59%    1.3kB / 126B   0B / 172kB   1
```

`http://localhost:8080` zeigt „Hello World 2.0.0" mit Backend-Antwort; der Zähler „Aufrufe in access.log" zählt im Volume weiter.

## Erweiterung: CPU-Last im Frontend

```bash
docker stats                                                     # Terminal 1, läuft weiter
docker compose exec frontend sh -c 'while :; do :; done'         # Terminal 2, Strg+C beendet
```

```text
NAME               CPU %     MEM USAGE / LIMIT
hello-frontend-1   50.65%    26.07MiB / 128MiB
hello-backend-1    0.01%     21.25MiB / 128MiB
```

Die Endlosschleife will einen ganzen Kern (100 %), die Grenze `cpus: "0.5"` hält sie bei etwa 50 %. Der Container wird gebremst, aber nicht beendet.
