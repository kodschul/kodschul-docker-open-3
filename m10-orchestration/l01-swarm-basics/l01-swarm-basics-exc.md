# Lab 10.1 – Übung: Grundlagen und Einrichtung von Docker Swarm

**Dauer:** ca. 15 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung nutzt nginx; der Swarm bleibt für Lab 10.3 aktiv.

## Vorbereitung

- Docker Desktop läuft; Terminal (Windows: Git Bash, siehe [Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Starter und Arbeitsdatei: keine, alle Schritte sind Befehle.
- Port 8001 frei.

## Aufgaben

1. Mache Docker Desktop mit `docker swarm init` zum Swarm-Manager und zeige die Nodes mit `docker node ls` an.
2. Erstelle den Service `web` mit `docker service create --name web -p 8001:80 nginx:1.30-alpine`, zeige ihn mit `docker service ls` und seine Tasks mit `docker service ps web` an und öffne `http://localhost:8001`.
3. Skaliere den Service mit `docker service scale web=10` und prüfe mit `docker service ls`, `docker service ps web` und `docker ps`, wie viele Container laufen.
4. Lösche einen Task-Container von Hand: Suche mit `docker ps --filter name=web.` eine Container-ID und entferne den Container mit `docker rm -f <ID>`. Beobachte danach `docker service ls` und `docker service ps web`.
5. Entferne den Service mit `docker service rm web` und prüfe mit `docker ps`, dass die nginx-Container weg sind. Der Swarm bleibt für Lab 10.3 bestehen.

## Checkpoint

- `docker node ls` zeigt einen Node `docker-desktop` mit `MANAGER STATUS` `Leader`.
- `docker service ls` zeigt `web` mit `REPLICAS 1/1`, nach dem Skalieren `10/10`.
- `docker service ps web` listet `web.1` bis `web.10` im Zustand `Running`.
- Nach dem Löschen eines Containers zeigt `docker service ls` nach wenigen Sekunden wieder `10/10`; `docker service ps web` zeigt für dieselbe Task-Nummer einen neuen Task und darunter den alten mit `Failed`.

## Abschlusskriterien

- Ein Ein-Node-Swarm läuft; der Service `web` lief mit zehn Tasks und hat einen gelöschten Container selbst ersetzt.
- Der Service `web` ist entfernt, der Swarm ist aktiv (`docker info` zeigt `Swarm: active`).

## Erweiterung

Zeige mit `docker swarm join-token worker` den Befehl an, mit dem ein weiterer Rechner als Worker beitreten würde. Mit einem zweiten Rechner (Kollege im selben Netz oder [Play with Docker](https://labs.play-with-docker.com/), kostenloses Docker-Konto nötig) lässt sich der Beitritt ausprobieren; in Play with Docker mit **+ ADD NEW INSTANCE** mehrere Instanzen anlegen, auf der ersten `docker swarm init --advertise-addr <IP der Instanz>`, auf den übrigen den ausgegebenen `join`-Befehl.

## Fallback

- `could not choose an IP address to advertise`: `docker swarm init --advertise-addr 127.0.0.1`.
- `This node is already part of a swarm`: Swarm ist schon aktiv; mit Aufgabe 2 weitermachen.
- Port 8001 belegt: `-p 8011:80` und `http://localhost:8011`.
