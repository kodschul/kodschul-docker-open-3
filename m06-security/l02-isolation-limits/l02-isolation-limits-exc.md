# Lab 6.2 – Übung: Containerisolierung und Ressourcenbeschränkungen

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — `compose.yml` bekommt Ressourcengrenzen für `frontend` und `backend`; Lab 6.3 baut darauf auf.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)), Ordner `project/playground/hello`.
- Arbeitsdatei: `project/playground/hello/compose.yml` (Stand Lab 4.3). Fehlt er, im Ordner `project/` `cp -r examples/m04-compose/l03-volumes/. playground/`.
- Keine Reste aus einem früheren Versuch: `docker rm -f backend-limits oom-test` (Meldung „No such container" ist in Ordnung).

## Aufgaben

1. Starte das Hello-Backend als Einzelcontainer mit Grenzen: `docker run -d --name backend-limits --memory 64m --cpus 0.5 backend:v1`. Prüfe den Verbrauch mit `docker stats --no-stream backend-limits` und die gesetzten Werte mit `docker inspect backend-limits --format '{{.HostConfig.Memory}} {{.HostConfig.NanoCpus}}'`.
2. Erhöhe die Speichergrenze im laufenden Betrieb auf 128 MB mit `docker update` (siehe Theorie) und prüfe sie erneut mit `docker stats --no-stream backend-limits`. Entferne `backend-limits` danach.
3. Starte den Container `oom-test` aus der Theorie (`python:3.13-alpine`, Grenze 32 MB, Speicherlast 100 MB) und prüfe Status und Grund mit `docker ps -a --filter name=oom-test` und `docker inspect oom-test --format '{{.State.OOMKilled}} {{.State.ExitCode}}'`. Entferne `oom-test` danach.
4. Ergänze in `compose.yml` für beide Dienste `deploy.resources.limits` mit `cpus: "0.5"` und `memory: 128M` und starte die Hello-App mit `docker compose up -d` neu.
5. Prüfe die Grenzen mit `docker stats --no-stream` und öffne `http://localhost:8080`.

## Checkpoint

- Aufgabe 1: `MEM USAGE / LIMIT` endet auf `/ 64MiB`; `inspect` zeigt `67108864 500000000`.
- Aufgabe 2: `/ 128MiB`.
- Aufgabe 3: `Exited (137)`; `inspect` zeigt `true 137`.
- Aufgabe 4: `docker compose up -d` meldet beide Container als `Recreated` bzw. `Started`.
- Aufgabe 5: `hello-frontend-1` und `hello-backend-1` zeigen `/ 128MiB`; die Hello-Seite zeigt „Hello World 2.0.0" mit Backend-Antwort, der Zähler in `access.log` läuft weiter.

## Abschlusskriterien

- Grenzen per `docker run`, `docker update` und Compose gesetzt und in `docker stats` sichtbar.
- Ein Container mit zu kleinem Limit wurde mit `OOMKilled` beendet.
- `compose.yml` enthält die Grenzen; die Hello-App läuft damit. `backend-limits` und `oom-test` sind entfernt.

## Erweiterung

Starte `docker stats` ohne `--no-stream` und erzeuge im Frontend CPU-Last: `docker compose exec frontend sh -c 'while :; do :; done'`. Beobachte `CPU %` von `hello-frontend-1` und beende die Schleife mit Strg+C.

## Fallback

- `compose.yml` startet nicht (`yaml: line …`): Einrückung mit dem Stand in `project/examples/m06-security/l02-isolation-limits/hello/compose.yml` vergleichen oder ihn kopieren (im Ordner `project/`: `cp -r examples/m06-security/l02-isolation-limits/. playground/`).
- `python:3.13-alpine` lässt sich nicht laden: `backend:v1` statt `python:3.13-alpine` verwenden; das Image enthält Python.
