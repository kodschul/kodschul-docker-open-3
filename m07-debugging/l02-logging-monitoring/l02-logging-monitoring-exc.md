# Lab 7.2 – Übung: Logging und Monitoring in Docker

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — der Monitoring-Stack ist eine eigene App in `playground/monitoring/`; die Hello-App wird nur beobachtet.

## Vorbereitung

- Docker Desktop läuft; Kurs-Shell bash ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)). Der Stack lädt vier Images (zusammen etwa 1 GB); bei `toomanyrequests` vorher `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
- Ports 3000, 8081, 9090 und 9100 sind frei: `docker ps` prüfen und alte Container auf diesen Ports stoppen (z. B. nginx-Container aus Tag 1 auf 8081).
- Die Hello-App hat den Stand aus Lab 4.3 (`playground/hello/compose.yml`). Fehlt er, im Ordner `project/`:

  ```bash
  cp -r examples/m04-compose/l03-volumes/. playground/
  ```

- Monitoring-Starter in den Arbeitsbereich kopieren (im Ordner `project/`):

  ```bash
  cp -r starters/m07-l02-monitoring playground/monitoring
  ```

- Arbeitsordner: `project/playground/monitoring` mit `compose.yml`, `prometheus.yml` (zwei TODOs) und `grafana/` (Datenquelle und Dashboard, nicht ändern).

## Aufgaben

1. Starte die Hello-App im Ordner `playground/hello` mit `docker compose up -d` und prüfe mit `docker compose ps`, dass `hello-frontend-1` und `hello-backend-1` laufen.
2. Ergänze in `playground/monitoring/prometheus.yml` die beiden TODOs: einen Job `cadvisor` und einen Job `node-exporter`. Die Ziele ergeben sich aus den Dienstnamen und den Ports **im Container** in `compose.yml`.
3. Starte im Ordner `playground/monitoring` den Stack mit `docker compose up -d`. Öffne `http://localhost:9090`, wähle **Status > Target health** und prüfe, dass alle drei Ziele `UP` sind. Öffne danach die cAdvisor-Oberfläche `http://localhost:8081` und suche unter **Docker Containers** den Hello-Frontend-Container.
4. Öffne Grafana unter `http://localhost:3000`, wähle **Dashboards > Docker-Kurs > Hello-Container**. Erzeuge Last auf die Hello-App und beobachte die Diagramme eine Minute lang:

   ```bash
   for i in $(seq 1 300); do curl -s http://localhost:8080 > /dev/null; done
   ```

   Vergleiche den Speicherwert des Frontends im Dashboard mit `docker stats --no-stream`.
5. Frage den Speicherverbrauch des Hello-Frontends direkt in Prometheus ab: `http://localhost:9090`, Menü **Query**, Abfrage `container_memory_usage_bytes{name="hello-frontend-1"}`, Ansicht **Graph**. Stoppe danach den Monitoring-Stack mit `docker compose down` (im Ordner `monitoring`).

## Checkpoint

- Nach Aufgabe 2: `prometheus.yml` enthält drei Jobs: `prometheus`, `cadvisor`, `node-exporter`.
- Nach Aufgabe 3: `docker compose ps` im Ordner `monitoring` zeigt vier Dienste mit `Up`; **Target health** zeigt drei Ziele mit Status `UP`.
- Nach Aufgabe 4: Das Dashboard zeigt je eine Linie für `hello-frontend-1` und `hello-backend-1`; während der Schleife steigt die CPU-Linie des Frontends.

## Abschlusskriterien

- CPU und Speicher der Hello-Container sind im Grafana-Dashboard sichtbar.
- Bekannt ist, welcher Dienst Werte je Container (cAdvisor) und welcher Werte des Hosts (Node Exporter) liefert, und warum in `prometheus.yml` der Port im Container steht.

## Erweiterung

- Erstelle in Grafana ein eigenes Panel: **Dashboards > New > New dashboard > Add visualization**, Datenquelle **Prometheus**, Abfrage `sum by (name) (rate(container_network_receive_bytes_total{name=~"hello-.*"}[1m]))`. Erzeuge erneut Last und beobachte die empfangenen Bytes je Container.
- Nur mit mindestens 6 GB Speicher für Docker (**Settings > Resources**): Starte den ELK-Stack aus `project/examples/m07-debugging/l02-logging-monitoring/elk/` in einer Kopie unter `playground/elk`, sende mit dem Logtreiber `gelf` Logzeilen an Logstash und suche sie in Kibana (`http://localhost:5601`, Data View `logstash-*`, **Discover**):

  ```bash
  docker run -d --name log-demo --log-driver gelf --log-opt gelf-address=udp://localhost:12201 \
    busybox:1.37 sh -c 'while true; do echo "Hallo ELK $(date)"; sleep 5; done'
  ```

  Danach aufräumen: `docker rm -f log-demo`, im Ordner `elk` `docker compose down -v`.

## Fallback

- Ein Image lässt sich nicht laden (Proxy, Pull-Grenze): `docker login`, danach `docker compose up -d` wiederholen.
- Port belegt (`port is already allocated`): den linken Port in `compose.yml` ändern, z. B. `"3001:3000"`, und die neue Adresse im Browser nutzen. In `prometheus.yml` ändert sich nichts.
- Das Dashboard bleibt leer, obwohl alle Ziele `UP` sind: In Prometheus unter **Query** `container_memory_usage_bytes` abfragen. Fehlt dort das Label `name` (nur `id="/docker/…"`), erreicht cAdvisor den Docker- oder containerd-Socket nicht: In `docker compose logs cadvisor` nach `Registration of the docker container factory failed` suchen und die beiden Socket-Zeilen in `compose.yml` prüfen. Als Ersatz zeigt `docker stats` die Werte je Container.
- Ausgangsstand verloren: `playground/monitoring` löschen und neu aus `starters/m07-l02-monitoring` kopieren; die fertige Lösung liegt in `examples/m07-debugging/l02-logging-monitoring/monitoring/`.
