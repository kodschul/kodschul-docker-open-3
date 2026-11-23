# Cheatsheet: Debugging, Logging und Monitoring

Befehle aus Modul 7 (Labs 7.1–7.2). Kurs-Shell `bash`; unter Windows Git Bash mit `MSYS_NO_PATHCONV=1`.

## Vorgehen nach Fehlergruppe

| Gruppe | Symptom | erste Befehle |
| --- | --- | --- |
| Build | kein Image, `failed to solve` | Build-Ausgabe lesen, `cat .dockerignore`, `docker build --no-cache` |
| Start | Container sofort `Exited` | `docker ps -a`, `docker logs`, `docker run -it --rm --entrypoint sh <image>` |
| Netzwerk | läuft, erreicht anderen Dienst nicht | `docker exec … curl`, `docker network inspect` |
| Ressourcen | langsam oder `Exited (137)` | `docker stats`, `docker inspect … OOMKilled` |

## Status und Exit-Code

| Befehl | Wirkung |
| --- | --- |
| `docker ps -a` | alle Container inkl. beendeter, mit Exit-Code in `STATUS` |
| `docker compose ps -a` | dasselbe für die Dienste eines Compose-Projekts |
| `docker inspect -f '{{.State.Status}} {{.State.ExitCode}}' <container>` | Zustand und Exit-Code |
| `docker inspect -f '{{.State.OOMKilled}}' <container>` | `true`, wenn der OOM-Killer den Prozess beendet hat |
| `docker inspect -f '{{.HostConfig.Memory}}' <container>` | Speichergrenze in Bytes (`0` = keine) |

| Exit-Code | Bedeutung |
| --- | --- |
| `0` | regulär beendet |
| `1` | allgemeiner Programmfehler |
| `2` | falscher Aufruf, z. B. Python findet die Startdatei nicht |
| `126` / `127` | Befehl nicht ausführbar / nicht gefunden |
| `137` | `SIGKILL`: OOM oder `docker kill` |
| `143` | `SIGTERM`: `docker stop` |

## Logs

| Befehl | Wirkung |
| --- | --- |
| `docker logs <container>` | alle bisherigen Ausgaben, auch nach dem Absturz |
| `docker logs -f <container>` | live mitlesen (`--follow`), `Strg+C` beendet nur das Mitlesen |
| `docker logs --tail 20 <container>` | nur die letzten 20 Zeilen |
| `docker logs --since 10m <container>` | nur die letzten 10 Minuten |
| `docker logs -t <container>` | mit Zeitstempel |
| `docker compose logs <dienst>` | Logs eines Compose-Dienstes |
| `docker compose logs -f --tail 20` | alle Dienste live, je 20 Zeilen Rückblick |

## In Container hineinsehen

| Befehl | Wirkung |
| --- | --- |
| `docker exec -it <container> sh` | Shell in einem laufenden Alpine-Container |
| `docker exec -it <container> /bin/bash` | Shell in Images mit bash |
| `docker compose exec <dienst> sh` | Shell in einem Compose-Dienst |
| `docker compose exec <dienst> env` | Umgebungsvariablen, z. B. `BACKEND_URL` |
| `docker run -it --rm --entrypoint sh <image>` | Image untersuchen, dessen Programm sofort abstürzt |
| `docker run --rm --entrypoint ls <image>` | Dateien im Arbeitsordner des Images auflisten |

## Netzwerk

| Befehl | Wirkung |
| --- | --- |
| `docker network ls` | alle Netzwerke; Compose-Netzwerke heißen `<projekt>_<name>` |
| `docker network inspect <netz> --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'` | Container und IPs eines Netzwerks |
| `docker inspect -f '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' <container>` | Netzwerke eines Containers |
| `docker compose exec frontend curl -sS http://backend:80` | Dienst aus Sicht eines anderen Containers abrufen |
| `docker compose exec frontend ping -c 1 backend` | Namensauflösung und Erreichbarkeit prüfen |
| `docker network connect --alias backend <netz> <container>` | laufenden Container zusätzlich verbinden, unter Namen `backend` |
| `docker run --rm -it --network <netz> nicolaka/netshoot` | Werkzeug-Container mit `curl`, `dig`, `ping` im selben Netzwerk |

| Meldung | Bedeutung |
| --- | --- |
| `Could not resolve host` / `bad address` | Name unbekannt: anderes Netzwerk oder Tippfehler |
| `Connection refused` | Name bekannt, auf dem Port lauscht nichts |
| Timeout | Ziel nicht erreichbar |

## Build

| Befehl | Wirkung |
| --- | --- |
| `docker build --no-cache -t <name> .` | alle Schritte ohne Cache neu ausführen |
| `docker compose build --no-cache <dienst>` | dasselbe für einen Compose-Dienst |
| `docker compose up -d --build` | neu bauen und Container mit neuem Image ersetzen |
| `!requirements.txt` in `.dockerignore` | Ausnahme von einer vorherigen Regel wie `*.txt` |

## Ressourcen

| Befehl | Wirkung |
| --- | --- |
| `docker stats` | CPU, Speicher mit Grenze, Netzwerk, Datenträger aller Container live |
| `docker stats --no-stream <container>` | einmalige Ausgabe |
| `docker run --memory="256m" --cpus="1" <image>` | Grenzen beim Start setzen |
| `deploy.resources.limits.memory: 64M` | Speichergrenze in Compose |

## Monitoring-Stack (Lab 7.2)

| Befehl / Adresse | Wirkung |
| --- | --- |
| `docker compose up -d` (Ordner `monitoring`) | Prometheus, cAdvisor, Node Exporter, Grafana starten |
| `docker compose restart prometheus` | geänderte `prometheus.yml` laden |
| `http://localhost:9090` > **Status > Target health** | Ziele von Prometheus mit `UP` / `DOWN` |
| `http://localhost:9090` > **Query** | PromQL-Abfrage als Tabelle oder Graph |
| `curl -s http://localhost:9090/api/v1/targets` | Ziele im Terminal prüfen |
| `http://localhost:8081` | cAdvisor-Oberfläche (im Container Port 8080) |
| `http://localhost:9100/metrics` | Rohwerte des Node Exporters |
| `http://localhost:3000` | Grafana, Dashboard **Docker-Kurs > Hello-Container** |

```yaml
# prometheus.yml: Ziel = Dienstname und Port im Container
scrape_configs:
  - job_name: cadvisor
    static_configs:
      - targets: ['cadvisor:8080']
```

| PromQL | Wirkung |
| --- | --- |
| `container_memory_usage_bytes{name="hello-frontend-1"}` | Speicher eines Containers |
| `sum by (name) (rate(container_cpu_usage_seconds_total{name=~"hello-.*"}[1m]))` | CPU je Container, `1` = ein Kern |
| `node_memory_MemAvailable_bytes` | freier Arbeitsspeicher des Hosts |
| `1 - avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))` | CPU-Auslastung des Hosts |

## Logs zentral (ELK)

| Befehl / Adresse | Wirkung |
| --- | --- |
| `docker run --log-driver gelf --log-opt gelf-address=udp://localhost:12201 <image>` | Ausgaben eines Containers an Logstash senden |
| `curl -s http://localhost:9200` | Elasticsearch antwortet mit Version |
| `http://localhost:5601` | Kibana; Data View `logstash-*`, Bereich **Discover** |
