# Cheatsheet: Docker-Netzwerke

Befehle aus Modul 5 (Labs 5.1–5.3). Kurs-Shell `bash`; unter Windows Git Bash mit `MSYS_NO_PATHCONV=1`.

## Netzwerke anzeigen und prüfen

| Befehl | Wirkung |
| --- | --- |
| `docker network ls` | alle Netzwerke mit Treiber (`bridge`, `host`, `none`, eigene) |
| `docker network ls --filter driver=bridge` | nur Netzwerke mit einem bestimmten Treiber |
| `docker network inspect hello_default` | Treiber, Subnetz, Gateway, verbundene Container als JSON |
| `docker network inspect <netz> --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'` | nur Container und IPs eines Netzwerks |
| `docker inspect <container> --format '{{range $name, $net := .NetworkSettings.Networks}}{{$name}} {{$net.IPAddress}}{{"\n"}}{{end}}'` | Netzwerke und IPs eines Containers |
| `docker port <container>` | veröffentlichte Ports eines Containers |

## Netzwerke anlegen und löschen

| Befehl | Wirkung |
| --- | --- |
| `docker network create demo-network` | Bridge-Netzwerk anlegen (Standardtreiber) |
| `docker network create --driver bridge pizza-network` | Treiber ausdrücklich angeben |
| `docker network create --subnet 172.30.0.0/24 lab-net` | Netzwerk mit festem Adressbereich |
| `docker network create --subnet 172.30.0.0/24 --gateway 172.30.0.1 lab-net` | zusätzlich Gateway festlegen |
| `docker network create --internal intern-net` | Netzwerk ohne Weg nach außen |
| `docker network rm demo-network` | Netzwerk löschen (nur ohne verbundene Container) |

## Container verbinden

| Befehl | Wirkung |
| --- | --- |
| `docker run -d --name container1 --network demo-network busybox:1.37 sleep 3600` | Container beim Start einem Netzwerk zuordnen |
| `docker run -d --name fix --network lab-net --ip 172.30.0.10 busybox:1.37 sleep 3600` | feste IP (nur bei Netzwerk mit `--subnet`) |
| `docker run -d --name frontend --network hello-net -p 8080:80 frontend:v2` | Netzwerk und veröffentlichter Port |
| `docker network connect demo-network container2` | laufenden Container zusätzlich in ein Netzwerk hängen |
| `docker network disconnect demo-network container2` | Container aus einem Netzwerk entfernen |

## Netzwerkmodi beim Start

| Befehl | Wirkung |
| --- | --- |
| `docker run …` ohne `--network` | Standard-Bridge: eigene IP, keine Namensauflösung zwischen Containern |
| `docker run --network <eigenes-netz> …` | eigene IP, andere Container per Name erreichbar |
| `docker run --network host …` | Netzwerk des Hosts direkt, `-p` wirkungslos; Docker Desktop: Host = Linux-VM |
| `docker run --network none …` | nur Loopback, weder Container noch Internet erreichbar |

## Verbindung testen

| Befehl | Wirkung |
| --- | --- |
| `docker exec container1 ping -c 3 container2` | Ping per Name aus einem laufenden Container |
| `docker run --rm --network hello_default busybox:1.37 wget -qO- -T 3 http://backend` | HTTP-Abruf aus einem Wegwerf-Container im Netzwerk |
| `docker compose exec frontend curl -s http://backend` | HTTP-Abruf aus einem Compose-Dienst |
| `docker compose exec frontend getent hosts backend` | IP hinter einem Namen anzeigen |
| `docker compose exec frontend cat /etc/resolv.conf` | DNS-Server im Container (`127.0.0.11`) |

## Compose und Netzwerke

| Befehl / Angabe | Wirkung |
| --- | --- |
| `docker compose up -d` | legt `<projekt>_default` an und hängt alle Dienste hinein |
| `docker compose down` | entfernt Container und Projektnetzwerk |
| `ports: - 8080:80` | nur dieser Dienst ist von außen erreichbar |
| Dienstname, z. B. `backend` | Hostname des Dienstes im Projektnetzwerk |

## Treiber

| Treiber | Einsatz |
| --- | --- |
| `bridge` | Container auf einem Host, Standard |
| `host` | kein eigenes Netz, direkt am Host |
| `none` | kein Netzwerk |
| `overlay` | über mehrere Hosts (Swarm, Modul 10) |
| `macvlan` / `ipvlan` | Container mit eigener Adresse im physischen Netz |
