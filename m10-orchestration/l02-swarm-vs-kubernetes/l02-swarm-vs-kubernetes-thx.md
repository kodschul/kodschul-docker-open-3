# Lab 10.2: Vergleich von Docker Swarm und Kubernetes

**Leitfragen:**

<details>
<summary>Ab wie vielen Servern lohnt sich ein eigener Orchestrator?</summary>

Es gibt keine feste Zahl. Schon ab zwei Servern hilft einer, sobald Ausfälle automatisch abgefangen werden sollen; der Aufwand für Einrichtung und Betrieb muss zum Team passen.

</details>

<details>
<summary>Was ist wichtiger: schnell eingerichtet oder alles möglich?</summary>

Hängt vom Bedarf ab: Swarm ist in Minuten eingerichtet und reicht für viele kleinere Anwendungen; Kubernetes kann fast alles, verlangt aber deutlich mehr Wissen und Betrieb.

</details>

- Docker Swarm und Kubernetes lösen dieselbe Aufgabe: Container auf mehreren Rechnern verteilen, skalieren und ersetzen (Lab 10.1).
- Swarm ist Teil der Docker Engine und nutzt Docker-Befehle; Kubernetes ist ein eigenes System mit eigenem Werkzeug `kubectl` und eigenen Begriffen.

## Begriffe

| Begriff | Bedeutung |
| --- | --- |
| Kubernetes (K8s) | Open-Source-Orchestrator, 2014 von Google veröffentlicht, seit 2015 bei der Cloud Native Computing Foundation (CNCF) |
| `kubectl` | Kommandozeilenwerkzeug von Kubernetes, vergleichbar mit `docker` |
| Pod | kleinste Einheit in Kubernetes: ein oder mehrere Container, die zusammen laufen und sich eine IP teilen |
| Deployment | beschreibt in Kubernetes, welches Image mit wie vielen Pods laufen soll; entspricht etwa einem Swarm-Service |
| ReplicaSet | sorgt dafür, dass die gewünschte Anzahl Pods läuft; ein Deployment legt es an |
| Service (Kubernetes) | feste Adresse vor einer Gruppe von Pods; anderes Wort für die Rolle, die Swarm im Service mit erledigt |
| Ingress-Controller / Gateway | Reverse Proxy im Kubernetes-Cluster, wie Traefik aus Lab 9.1 |
| CNI-Plugin | Netzwerk-Erweiterung, die in Kubernetes die Verbindung zwischen Pods herstellt |

## Wichtige Features von Swarm und Kubernetes

| Docker Swarm | Kubernetes |
| --- | --- |
| in die Docker CLI integriert | automatische Skalierung von Containern (nach Last) |
| einfache Einrichtung und Konfiguration | Selbstheilung für Pods |
| automatische Lastverteilung über Nodes hinweg | integrierte Service Discovery und Lastverteilung |
| Rolling Updates und Wiederherstellung von Services | umfassende API für Automatisierung und Verwaltung |

## Architekturvergleich

<img src="https://kubernetes.io/images/docs/components-of-kubernetes.svg" alt="Komponenten eines Kubernetes-Clusters: Control Plane mit API-Server, etcd, Scheduler, Controller-Manager und Cloud-Controller-Manager; mehrere Nodes mit kubelet und kube-proxy, darin Pods" width="620">

_Quelle: The Kubernetes Authors, „Kubernetes Components" (https://kubernetes.io/docs/concepts/overview/components/), CC BY 4.0, abgerufen am 23.11.2026._

| Merkmal | Docker Swarm | Kubernetes |
| --- | --- | --- |
| Installation | einfach, direkt über die Docker CLI (`docker swarm init`) | komplexer, eigene Werkzeuge (kubeadm, verwaltete Cluster in der Cloud, lokal z. B. Docker Desktop, kind, minikube) |
| Skalierung | manuell (`docker service scale`) | manuell oder automatisch horizontal nach Last (Horizontal Pod Autoscaler) |
| Lastverteilung | integriert, einfach (Routing Mesh, Lab 10.3) | fortgeschritten, mit Ingress-Controller oder Gateway API |
| Verwaltung | zentral durch die Swarm-Manager | über den API-Server der Control Plane; Controller arbeiten unabhängig voneinander |
| Netzwerk | einfach mit Overlay-Netzwerk | flexibel und komplexer mit CNI-Plugins |
| Steuerung | Docker-Befehle und Compose-Dateien (`docker stack deploy`) | YAML-Manifeste und `kubectl apply` |

Die Swarm-Architektur mit Managern und Workern zeigt Lab 10.1; Kubernetes trennt entsprechend Control Plane (Steuerung) und Nodes (Ausführung).

## Vor- und Nachteile von Swarm und Kubernetes

| | Docker Swarm | Kubernetes |
| --- | --- | --- |
| Vorteile | einfache Einrichtung und Nutzung · nahtlos in Docker-Umgebungen · geringer Ressourcenverbrauch | skalierbar und hochverfügbar · vielfältige Erweiterungen · große Community, Unterstützung aller großen Cloud-Anbieter |
| Nachteile | begrenzte Skalierbarkeit · weniger Funktionen als Kubernetes · kleinere Community, weniger Erweiterungen | komplexe Einrichtung und Verwaltung · höherer Ressourcenverbrauch · steilere Lernkurve |

## Verbreitung und Support (Stand November 2026)

<img src="https://www.cncf.io/wp-content/uploads/2026/01/CNCF-Annual-Cloud-Native-Survey-The-Infrastructure-of-AIs-Future-infographic-scaled.jpg" alt="Infografik der CNCF-Umfrage 2025: 98 Prozent nutzen Cloud-native-Technologien, 82 Prozent der Container-Nutzer betreiben Kubernetes in Produktion (2023: 66 Prozent)" width="420">

_Quelle: CNCF, „Annual Cloud Native Survey 2025" (https://www.cncf.io/announcements/2026/01/20/kubernetes-established-as-the-de-facto-operating-system-for-ai-as-production-use-hits-82-in-2025-cncf-annual-cloud-native-survey/), veröffentlicht am 20.01.2026, abgerufen am 23.11.2026._

- **Kubernetes:** 82 % der Organisationen, die Container nutzen, betreiben Kubernetes in Produktion (CNCF-Umfrage 2025, 2023: 66 %). Drei Versionen pro Jahr; unterstützt sind 1.37 (26.08.2026), 1.36 und 1.35, jede etwa 14 Monate (Quelle: https://kubernetes.io/releases/, abgerufen am 23.11.2026).
- **Docker Swarm:** Swarm Mode ist in der aktuellen Docker Engine (29.x) enthalten. Mirantis sagt Support für Swarm in Mirantis Kubernetes Engine 3 bis 2030 zu (01.07.2025, https://www.mirantis.com/blog/mirantis-guarantees-long-term-support-for-swarm/). Neue Funktionen kommen selten; die Doku verweist für Kubernetes-Entwicklung auf das in Docker Desktop eingebaute Kubernetes (https://docs.docker.com/engine/swarm/, abgerufen am 23.11.2026).

## Wann Swarm, wann Kubernetes?

| Docker Swarm eignet sich für | Kubernetes eignet sich für |
| --- | --- |
| kleinere Anwendungen mit wenigen Containern | große, komplexe Anwendungen mit vielen Containern |
| Entwickler, die schnell einen Cluster aufbauen möchten | Unternehmen mit hohen Skalierungsanforderungen |
| Teams mit begrenzten Ressourcen und wenig Kubernetes-Wissen | Teams mit Erfahrung in DevOps und Container-Orchestrierung |

Ein Umstieg ist schrittweise möglich: Images und Registry (Module 3 und 8) bleiben gleich, nur die Beschreibung der Bereitstellung wechselt von Compose/Stack-Datei zu Kubernetes-Manifesten.

## Deployment-Konzepte in Kubernetes

| Kubernetes | Aufgabe | Gegenstück im Swarm |
| --- | --- | --- |
| Pod | kleinste Verwaltungseinheit, kann mehrere Container enthalten | Task (genau ein Container) |
| Deployment | legt fest, wie Pods verwaltet und skaliert werden | Service (Image, Replikas, Update-Regeln) |
| ReplicaSet | stellt sicher, dass die gewünschte Anzahl Pods läuft | im Service enthalten |
| Service | stellt den Zugang zu den Pods eines Deployments bereit (feste Adresse, Lastverteilung) | im Service enthalten (virtuelle IP, Routing Mesh) |

Ein einfaches Deployment und ein Rolling Update in Kubernetes:

```bash
kubectl create deployment web --image=nginx:1.30-alpine          # Deployment mit einem Pod
kubectl scale deployment web --replicas=5                        # auf fünf Pods skalieren
kubectl set image deployment/web nginx=nginx:1.31-alpine         # Rolling Update auf neue Version
kubectl rollout undo deployment/web                              # zurück zur vorherigen Version
```

Die alte Folie nutzt `nginx` und `nginx:latest`; feste Tags machen nachvollziehbar, welche Version läuft. Der Containername im Pod (`nginx=`) leitet sich aus dem Image ab.

## Deployments im Vergleich

| Merkmal | Docker Swarm | Kubernetes |
| --- | --- | --- |
| Deployment | `docker service create` | `kubectl create deployment` |
| Skalierung | `docker service scale` | `kubectl scale deployment` |
| Rolling Update | `docker service update --image …` | `kubectl set image` |
| Rollback | `docker service rollback` (oder `docker service update --rollback`) | `kubectl rollout undo` |
| Selbstheilung | automatisch durch die Manager (Lab 10.1) | automatisch durch Controller |

Korrektur zur alten Folie: Dort stand bei Swarm „Selbstheilung: manuell". Swarm ersetzt ausgefallene Tasks automatisch, wie in Lab 10.1 beobachtet.

Kubernetes hands-on ist nicht Teil dieses Kurses; der Kurs „Kubernetes" baut auf denselben Images und Begriffen auf.

## Fazit

- Swarm: schnell eingerichtet, Docker-Befehle und Compose-Dateien, genug für kleinere Umgebungen; Support durch Mirantis bis 2030 zugesagt.
- Kubernetes: Standard für große Umgebungen (82 % der Container-Nutzer in Produktion), mehr Möglichkeiten, mehr Aufwand.
- Die Konzepte entsprechen sich: Task ↔ Pod, Service ↔ Deployment plus Service, `scale`, Rolling Update und Rollback gibt es in beiden.
