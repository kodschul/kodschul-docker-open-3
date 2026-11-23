# Lab 10.1: Grundlagen und Einrichtung von Docker Swarm

**Leitfragen:**

<details>
<summary>Zehn Container auf drei Servern, ein Server fällt nachts aus: was muss passieren, und wer macht es?</summary>

Die ausgefallenen Container müssen auf den beiden anderen Servern neu starten, und Anfragen dürfen nur noch dorthin gehen. Das übernimmt ein Orchestrator wie Docker Swarm automatisch, ohne dass jemand eingreift.

</details>

<details>
<summary>Ein Container stürzt ab: wer startet ihn neu, wenn niemand zuschaut?</summary>

Auf einem einzelnen Rechner eine Neustart-Regel (`--restart`). Im Swarm vergleicht der Manager ständig die gewünschte Anzahl mit der laufenden und startet fehlende Container selbst neu (Selbstheilung).

</details>

- Bisher lief jeder Container auf genau einem Rechner, gestartet mit `docker run` oder `docker compose`. Fällt der Rechner aus, ist die Anwendung weg.
- Docker Swarm verbindet mehrere Docker-Rechner zu einem Cluster und verteilt Container darauf. Swarm ist Teil der Docker Engine; Docker Desktop bringt es mit.

## Begriffe

| Begriff | Bedeutung |
| --- | --- |
| Container-Orchestrierung | automatisierte Verwaltung vieler Container auf vielen Rechnern: starten, verteilen, skalieren, ersetzen |
| Cluster | Gruppe von Rechnern, die gemeinsam als ein System arbeiten |
| Node | ein Rechner (physisch oder virtuell) mit Docker im Swarm |
| Manager Node | Node, der den Zustand des Clusters führt und entscheidet, welche Container wo laufen |
| Worker Node | Node, der die zugewiesenen Container ausführt; Manager arbeiten standardmäßig auch als Worker |
| Service | Beschreibung einer Anwendung im Swarm: Image, Anzahl Kopien, Ports; wie eine Stellenbeschreibung mit „wir brauchen 10 Leute" |
| Task | ein einzelner Container, den der Swarm für einen Service startet; der Service `web` mit 10 Replikas hat 10 Tasks |
| Replika | eine Kopie eines Services; `replicas: 10` = zehn gleiche Tasks |
| Gewünschter Zustand (Desired State) | was laufen soll (z. B. 10 Tasks); der Manager gleicht den tatsächlichen Zustand laufend daran an |
| Join-Token | geheimer Schlüssel, mit dem ein weiterer Rechner dem Swarm beitreten darf |

## Container-Orchestrierung

Container-Orchestrierung ist die automatisierte Verwaltung von Container-Anwendungen:

- ermöglicht Skalierung, Lastverteilung und Fehlerbehebung,
- ist notwendig für Microservices-Architekturen (Lab 4.4) und verteilte Systeme,
- bekannte Orchestratoren: Docker Swarm (in Docker eingebaut), Kubernetes (Lab 10.2).

| Aufgabe | ohne Orchestrator (`docker run`, Compose) | mit Swarm |
| --- | --- | --- |
| Container starten | auf einem Rechner | auf beliebigen Nodes des Clusters |
| Absturz | `--restart` startet neu, nur auf demselben Rechner | Manager ersetzt den Task, notfalls auf einem anderen Node |
| Rechner fällt aus | Anwendung weg | Tasks starten auf den übrigen Nodes |
| Skalieren | `--scale`, nur ein Rechner | `docker service scale`, verteilt auf alle Nodes |
| Port veröffentlichen | auf dem einen Rechner | auf jedem Node (Lab 10.3) |

## Docker Swarm

Docker Swarm ist das in Docker integrierte Orchestrierungswerkzeug zur Verwaltung und Koordination von Containern auf mehreren Hosts. Es verteilt und skaliert Container-Anwendungen automatisch in einem Cluster.

| Warum Swarm? | Bedeutung |
| --- | --- |
| Einfache Einrichtung | in Docker integriert; ein Befehl `docker swarm init` genügt |
| Automatische Skalierung | Anwendungen lassen sich mit einem Befehl skalieren und auf mehrere Nodes verteilen |
| Hohe Verfügbarkeit | Swarm repliziert Container auf mehrere Nodes |

Stand November 2026:

- Der „Swarm Mode" ist seit Docker 1.12 (2016) Teil der Docker Engine und auch in Docker Engine 29 enthalten. Das ältere, eigenständige „Docker Classic Swarm" wird nicht mehr entwickelt (Quelle: https://docs.docker.com/engine/swarm/, abgerufen am 23.11.2026).
- Mirantis (Käufer von Docker Enterprise, 2019) sagt Support für Swarm in Mirantis Kubernetes Engine 3 bis 2030 zu (Quelle: Mirantis, „Mirantis guarantees long-term support for Swarm", 01.07.2025, https://www.mirantis.com/blog/mirantis-guarantees-long-term-support-for-swarm/, abgerufen am 23.11.2026).

## Hauptkomponenten von Docker Swarm

<img src="https://docs.docker.com/engine/swarm/images/swarm-diagram.webp" alt="Swarm-Architektur: oben drei Manager-Nodes in einer Raft-Konsensgruppe mit gemeinsamem verteiltem Zustandsspeicher, unten sieben Worker-Nodes, die mit den Managern verbunden sind" width="680">

_Quelle: Docker Inc., „How nodes work" (https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/), abgerufen am 23.11.2026._

| Komponente | Aufgabe |
| --- | --- |
| Manager Nodes | führen den Status des Clusters und entscheiden, welche Services wo gestartet werden; mehrere Manager stimmen sich ab (Raft) |
| Worker Nodes | führen die Container-Tasks aus, die die Manager verteilen |
| Services | Definition für eine oder mehrere identische Container-Instanzen im Swarm |
| Tasks | Einheit, die genau einen Container eines Services darstellt |

<img src="https://docs.docker.com/engine/swarm/images/services-diagram.webp" alt="Ein Service mit drei nginx-Replikas auf dem Swarm-Manager; er verteilt drei Tasks nginx.1 bis nginx.3 mit je einem Container auf drei verfügbare Nodes" width="460">

_Quelle: Docker Inc., „How services work" (https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/), abgerufen am 23.11.2026._

Service → Tasks → Container: Dieses Bild gilt für alle Swarm-Übungen. Der Manager plant die Tasks auf Nodes ein; jeder Task startet einen Container. Stirbt ein Container, endet sein Task, und der Manager plant einen neuen.

## Installation und Initialisierung

Voraussetzungen:

- Docker ist auf allen Nodes (Manager und Worker) installiert.
- Die Nodes erreichen sich im Netzwerk, mit offenen Ports TCP 2377 (Cluster-Verwaltung), TCP/UDP 7946 (Kommunikation der Nodes) und UDP 4789 (Overlay-Netzwerk, Lab 5.1).

### Schritt 1: Swarm-Cluster initialisieren

Auf dem Manager-Node:

```bash
docker swarm init --advertise-addr <Manager-IP>
```

`<Manager-IP>` ist die IP-Adresse des Servers, der Manager werden soll. Hat der Rechner nur eine Netzwerkadresse (wie Docker Desktop), reicht `docker swarm init`.

### Schritt 2: Worker-Nodes hinzufügen

`docker swarm init` gibt einen `join`-Befehl aus. Auf jedem weiteren Rechner:

```bash
docker swarm join --token <token> <Manager-IP>:2377
```

`<token>` ist der Join-Token aus der Ausgabe von `init`; `docker swarm join-token worker` zeigt ihn erneut an.

### Schritt 3: Cluster überprüfen

Auf dem Manager:

```bash
docker node ls
```

Die Liste zeigt alle Nodes im Cluster mit ihrer Rolle: `MANAGER STATUS` `Leader` (führender Manager), `Reachable` (weiterer Manager) oder leer (Worker).

## Ersten Service starten und skalieren

```bash
docker service create --name web -p 8001:80 nginx:1.30-alpine   # Service mit einem Task
docker service ls                                                # alle Services mit REPLICAS 1/1
docker service ps web                                            # Tasks des Services: Node, Zustand
docker service scale web=10                                      # gewünschter Zustand: 10 Tasks
```

| Befehl | Wirkung |
| --- | --- |
| `docker service create --name web -p 8001:80 <image>` | Service anlegen; `-p` veröffentlicht den Port |
| `docker service ls` | Services mit laufenden/gewünschten Replikas (`10/10`) |
| `docker service ps web` | Tasks mit Name `web.1` … `web.10`, Node, gewünschtem und aktuellem Zustand |
| `docker service scale web=10` | Anzahl der Replikas ändern |
| `docker service rm web` | Service und alle Tasks entfernen |

- Swarm-Container erscheinen auch in `docker ps`, mit Namen wie `web.3.k2l8…` (Service, Task-Nummer, Task-ID).
- Die alte Folie nutzt `nginx` ohne Tag und Port 80; im Kurs `nginx:1.30-alpine` auf Port 8001.

## Selbstheilung

Wird ein Task-Container gelöscht oder stürzt er ab, weicht der tatsächliche vom gewünschten Zustand ab. Der Manager startet innerhalb weniger Sekunden einen Ersatz-Task:

```text
NAME          IMAGE               NODE             DESIRED STATE   CURRENT STATE            ERROR
web.3         nginx:1.30-alpine   docker-desktop   Running         Running 4 seconds ago
 \_ web.3     nginx:1.30-alpine   docker-desktop   Shutdown        Failed 10 seconds ago    "task: non-zero exit (137)"
```

Die Zeile mit `\_` ist der alte Task; Swarm behält einige alte Tasks als Verlauf.

## Typische Fehler

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| `This node is already part of a swarm` | Swarm schon initialisiert | weiterarbeiten oder mit `docker swarm leave --force` verlassen |
| `could not choose an IP address to advertise since this system has multiple addresses` | Rechner mit mehreren Netzwerkadressen | `docker swarm init --advertise-addr <IP>` |
| `This node is not a swarm manager` | Service-Befehl ohne Swarm oder auf einem Worker | `docker swarm init` bzw. Befehl auf dem Manager ausführen |
| `port 8001 is already in use` / Task bleibt `Pending` | Port belegt | anderen Port wählen oder belegenden Container stoppen |
| `REPLICAS 0/1`, Task `Rejected` mit `No such image` | Image nicht ladbar (Tippfehler, kein Netz) | `docker service ps web --no-trunc` lesen, Image prüfen |

## Fazit

- Orchestrierung verteilt, skaliert und ersetzt Container automatisch; Swarm bringt das mit der Docker Engine mit.
- Manager planen, Worker führen aus; ein Service beschreibt den gewünschten Zustand, Tasks sind die einzelnen Container.
- `swarm init`, `node ls`, `service create`, `service ps`, `service scale` sind die Grundbefehle; gelöschte Tasks ersetzt der Manager selbst.

In der Übung wird Docker Desktop zum Ein-Node-Swarm mit einem nginx-Service, der auf zehn Tasks skaliert und sich nach einem gelöschten Container selbst heilt.
