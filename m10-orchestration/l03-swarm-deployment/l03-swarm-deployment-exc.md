# Lab 10.3 – Übung: Deployment in die Orchestrierungsplattform

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — neue Datei `playground/hello/stack.yml`; die Hello-App läuft danach als Swarm-Stack. Am Ende werden Stack und Swarm wieder entfernt.

## Vorbereitung

- Swarm aus Lab 10.1 aktiv (`docker info` zeigt `Swarm: active`); falls nicht: `docker swarm init`.
- Images `frontend:v1`, `frontend:v2`, `backend:v1` vorhanden (`docker images`); falls nicht: im Ordner `project/` `bash build-images.sh`.
- Stack-Datei holen, im Ordner `project/`: `cp examples/m10-orchestration/l03-swarm-deployment/hello/stack.yml playground/hello/`. Arbeitsordner: `project/playground/hello`.
- Port 999 frei.

## Aufgaben

1. Stoppe im Ordner `playground/hello` alle Compose-Stände der Hello-App (`docker compose down`, falls Traefik aus Lab 9.1 noch läuft auch `docker compose -f compose-traefik.yml down`). Starte den Stack mit `docker stack deploy -c stack.yml hello` und prüfe ihn mit `docker stack ls` und `docker stack services hello`.
2. Prüfe den Healthcheck-Status mit `docker ps` (Spalte `STATUS` der Backend-Container) und öffne `http://localhost:999`.
3. Skaliere das Frontend mit `docker service scale hello_frontend=5`. Lade `http://localhost:999` mehrmals neu (oder nutze `for i in 1 2 3 4 5 6; do curl -s http://localhost:999 | grep Frontend; done`) und beobachte die Frontend-IP.
4. Führe ein Rolling Update auf Version 2 aus: `docker service update --image frontend:v2 hello_frontend`. Lade die Seite während des Updates mehrmals neu und prüfe danach mit `docker service ps hello_frontend`, welche Tasks welches Image haben.
5. Gehe mit `docker service rollback hello_frontend` auf Version 1 zurück und prüfe die Seite. Räume danach mit `docker stack rm hello` und `docker swarm leave --force` auf.

## Checkpoint

- `docker stack services hello` zeigt `hello_frontend` mit `3/3` und `hello_backend` mit `2/2`, nach dem Skalieren `hello_frontend` mit `5/5`.
- `docker ps` zeigt die zwei Backend-Container mit `(healthy)`.
- Die Seite unter `http://localhost:999` zeigt „Hello World 1.0.0"; die Frontend-IP wechselt zwischen den Aufrufen.
- Während des Updates erscheinen „1.0.0" und „2.0.0" gemischt, danach nur „2.0.0"; `docker service ps hello_frontend` zeigt fünf laufende Tasks mit `frontend:v2`.
- Nach dem Rollback zeigt die Seite wieder „1.0.0".
- Nach dem Aufräumen zeigt `docker info` `Swarm: inactive`.

## Abschlusskriterien

- Die Hello-App lief als Stack mit fünf Frontend- und zwei Backend-Tasks.
- Update auf v2 und Rollback auf v1 waren im Browser ohne Ausfall sichtbar.

## Erweiterung

Vor dem Aufräumen in Aufgabe 5: Lies mit `docker service inspect --pretty hello_frontend` die Abschnitte `UpdateConfig` und `RollbackConfig` und vergleiche sie mit `stack.yml`. Führe das Update danach mit `docker service update --update-parallelism 2 --update-delay 2s --image frontend:v2 hello_frontend` schneller aus.

Mehrere Nodes: Die Schritte im Abschnitt „Swarm mit mehreren Nodes" der Theorie lassen sich in [Play with Docker](https://labs.play-with-docker.com/) mit drei Instanzen nachvollziehen (kostenloses Docker-Konto nötig).

## Fallback

- Port 999 belegt: in `stack.yml` `- 9999:80` eintragen, `docker stack deploy -c stack.yml hello` erneut ausführen und `http://localhost:9999` aufrufen.
- Seite zeigt „Backend nicht erreichbar": 10–20 Sekunden warten, bis die Backend-Tasks `healthy` sind.
- Nach dem Aufräumen die Hello-App wieder per Compose starten: im Ordner `playground/hello` `docker compose up -d`.
