# Docker Swarm – Cheatsheet (Modul 10)

## Swarm einrichten

| Befehl | Wirkung |
| --- | --- |
| `docker swarm init` | Rechner wird Manager eines neuen Swarms |
| `docker swarm init --advertise-addr <Manager-IP>` | dasselbe, mit fester Adresse (Rechner mit mehreren IPs) |
| `docker swarm join-token worker` | Beitrittsbefehl für Worker anzeigen |
| `docker swarm join --token <token> <Manager-IP>:2377` | Rechner tritt dem Swarm bei (auf dem Worker) |
| `docker node ls` | Nodes mit Status, Verfügbarkeit und Manager-Rolle (`Leader`) |
| `docker info --format '{{.Swarm.LocalNodeState}}'` | `active` oder `inactive` |
| `docker swarm leave --force` | Swarm verlassen; beim letzten Manager wird der Swarm aufgelöst |

## Services

| Befehl | Wirkung |
| --- | --- |
| `docker service create --name web -p 8001:80 nginx:1.30-alpine` | Service mit einem Task, Port 8001 auf jedem Node |
| `docker service create --name web --replicas 3 -p 8001:80 nginx:1.29-alpine` | Service gleich mit drei Tasks |
| `docker service ls` | Services mit `REPLICAS` laufend/gewünscht |
| `docker service ps web` | Tasks mit Node, gewünschtem und aktuellem Zustand, Fehler |
| `docker service ps web --no-trunc` | dasselbe mit vollständiger Fehlermeldung |
| `docker service inspect --pretty web` | Konfiguration lesbar: Image, Replikas, Update- und Rollback-Regeln |
| `docker service scale web=10` | Anzahl der Replikas ändern |
| `docker service update --image nginx:1.31-alpine web` | Rolling Update auf ein anderes Image |
| `docker service update --update-parallelism 2 --update-delay 2s --image … web` | Update mit eigenem Tempo |
| `docker service rollback web` | zur vorherigen Konfiguration zurück |
| `docker service rm web` | Service mit allen Tasks entfernen |
| `docker ps --filter name=web.` | Task-Container auf diesem Node (`web.<Nr>.<Task-ID>`) |

## Stacks

| Befehl | Wirkung |
| --- | --- |
| `docker stack deploy -c stack.yml hello` | Stack `hello` aus einer Compose-Datei starten oder aktualisieren |
| `docker stack ls` | Stacks mit Zahl der Services |
| `docker stack services hello` | Services des Stacks (`hello_frontend`, `hello_backend`) mit Replikas |
| `docker stack ps hello` | alle Tasks des Stacks |
| `docker stack rm hello` | Stack mit Services und Netzwerk entfernen |

## `deploy:` in der Stack-Datei

| Schlüssel | Wirkung |
| --- | --- |
| `replicas: 3` | Anzahl der Tasks (Replicated Mode) |
| `mode: global` | ein Task je Node (Global Mode) |
| `update_config.parallelism: 1` | Tasks, die gleichzeitig ersetzt werden |
| `update_config.delay: 5s` | Pause zwischen zwei Schritten des Updates |
| `update_config.failure_action` | Verhalten bei scheiternden neuen Tasks: `pause` (Standard), `rollback`, `continue` |
| `rollback_config.parallelism: 1` | Tasks, die beim Rollback gleichzeitig ersetzt werden |
| `healthcheck:` | Task gilt erst als laufend, wenn `healthy`; ungesunde Tasks werden ersetzt |

## Kubernetes-Gegenstücke (Lab 10.2)

| Docker Swarm | Kubernetes |
| --- | --- |
| `docker service create` | `kubectl create deployment` |
| `docker service scale` | `kubectl scale deployment` |
| `docker service update --image` | `kubectl set image` |
| `docker service rollback` | `kubectl rollout undo` |
| Task | Pod |
