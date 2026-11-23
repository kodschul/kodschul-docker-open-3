# Lab 5.3 – Lösung: Kommunikation zwischen Containern

IDs, IP-Adressen und Zeiten unterscheiden sich je Rechner.

## Aufgabe 1: Netzwerk `pizza-network`

```bash
docker network create --driver bridge pizza-network
```

```text
2b7c4e1f9a08…
```

`--driver bridge` ist der Standard und dürfte auch fehlen; hier steht er, damit der Treiber sichtbar ist.

## Aufgabe 2: „Küche" und „Lieferung"

```bash
docker run -d --name kueche    --network pizza-network busybox:1.37 sleep 3600
docker run -d --name lieferung --network pizza-network busybox:1.37 sleep 3600
docker network inspect pizza-network --format '{{.Driver}}: {{range .Containers}}{{.Name}} {{end}}'
```

```text
bridge: kueche lieferung
```

Umlaute sind in Containernamen nicht erlaubt; `küche` scheitert mit `Invalid container name`.

## Aufgabe 3: Kommunikation testen

```bash
docker exec kueche ping -c 2 lieferung
docker exec lieferung ping -c 2 kueche
```

```text
PING lieferung (172.21.0.3): 56 data bytes
64 bytes from 172.21.0.3: seq=0 ttl=64 time=0.181 ms
64 bytes from 172.21.0.3: seq=1 ttl=64 time=0.192 ms

--- lieferung ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.181/0.186/0.192 ms
PING kueche (172.21.0.2): 56 data bytes
64 bytes from 172.21.0.2: seq=0 ttl=64 time=0.095 ms
64 bytes from 172.21.0.2: seq=1 ttl=64 time=0.204 ms

--- kueche ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.095/0.149/0.204 ms
```

Beide Namen lösen über den DNS-Server des Netzwerks auf die aktuelle IP auf.

## Aufgabe 4: Hello-App ohne Compose

```bash
docker compose down
docker network create hello-net
docker run -d --name backend  --network hello-net backend:v1
docker run -d --name frontend --network hello-net -p 8080:80 frontend:v2
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}'
```

```text
[+] Running 3/3
 ✔ Container hello-frontend-1  Removed
 ✔ Container hello-backend-1   Removed
 ✔ Network hello_default       Removed
d4f0c2a1e7b3…
6a1e5f3c9d20…
9c8b7a6f5e41…
frontend   frontend:v2   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
backend    backend:v1    80/tcp
…
```

`http://localhost:8080` zeigt „Hello World 2.0.0", unter **Frontend** die Container-ID mit einer IP aus `hello-net` und unter **Backend** die Antwort des Backends. Das Volume `hello-data` aus Lab 4.3 ist hier nicht eingebunden; `access.log` landet in der beschreibbaren Schicht des Containers und beginnt wieder bei 1.

`80/tcp` beim Backend bedeutet: Das Image dokumentiert Port 80 (`EXPOSE`), veröffentlicht ist er nicht.

## Aufgabe 5: Ports prüfen und aufräumen

```bash
docker port frontend
docker port backend
```

```text
80/tcp -> 0.0.0.0:8080
80/tcp -> [::]:8080
```

Für `backend` erscheint keine Zeile: kein veröffentlichter Port, das Backend ist nur im Netzwerk `hello-net` erreichbar.

```bash
docker rm -f kueche lieferung frontend backend
docker network rm pizza-network hello-net
docker compose up -d
docker compose ps
```

```text
kueche
lieferung
frontend
backend
pizza-network
hello-net
…
NAME               IMAGE         …   STATUS                    PORTS
hello-backend-1    backend:v1    …   Up 12 seconds (healthy)   80/tcp
hello-frontend-1   frontend:v2   …   Up 6 seconds              0.0.0.0:8080->80/tcp, [::]:8080->80/tcp
```

Compose legt `hello_default` neu an, bindet wieder das Volume `hello-data` ein und zählt `access.log` dort weiter.

## Erweiterung: `secret-lab` ohne Netzwerk

```bash
docker run --rm --name secret-lab --network none busybox:1.37 ping -c 2 kodschul.com
```

```text
ping: bad address 'kodschul.com'
```

```bash
docker run --rm busybox:1.37 ping -c 2 kodschul.com
```

```text
PING kodschul.com (188.166.192.28): 56 data bytes
64 bytes from 188.166.192.28: seq=0 ttl=63 time=89.239 ms
64 bytes from 188.166.192.28: seq=1 ttl=63 time=44.911 ms

--- kodschul.com ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
```

Ohne Netzwerk gibt es weder DNS noch eine Route nach außen: Schon die Namensauflösung scheitert. In der Standard-Bridge erreicht der Container das Internet über das Gateway des Hosts. Die IP von `kodschul.com` kann sich ändern.
