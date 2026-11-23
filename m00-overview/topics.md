# Module und Labs

## Tag 1 – Container und Images

| Modul | Lab | Min. | Kernthemen |
| --- | --- | --- | --- |
| 1 Einführung in Containertechnologie | [1.1 Warum Container?](../m01-container-intro/l01-why-containers/l01-why-containers-thx.md) | 20 | Works on my machine, Portabilität, Geschichte |
| | [1.2 Vergleich zur Virtualisierung](../m01-container-intro/l02-virtualization/l02-virtualization-thx.md) | 15 | VM vs. Container, Kernel, Startzeit |
| | [1.3 Container-Ökosystem kennenlernen](../m01-container-intro/l03-ecosystem/l03-ecosystem-thx.md) | 15 | Client, Daemon, Registry, Docker Desktop |
| 2 Arbeit mit Containern | [2.1 Container über die CLI steuern](../m02-container-basics/l01-cli/l01-cli-thx.md) | 35 | run, ps, stop, kill, rm, Ports |
| | [2.2 Verwaltung und Inspektion](../m02-container-basics/l02-inspection/l02-inspection-thx.md) | 40 | exec, logs, cp, inspect, Bind Mount |
| | [2.3 Einführung in Docker-Alternativen](../m02-container-basics/l03-alternatives/l03-alternatives-thx.md) | 15 | OCI, Podman, containerd, Desktop-Alternativen |
| 3 Images und lokale Registries | [3.1 Aufbau und Speichern von Images](../m03-images-registries/l01-image-layers/l01-image-layers-thx.md) | 30 | Layer, Union Filesystem, Basisimages |
| | [3.2 Eigene Images erstellen und verwalten](../m03-images-registries/l02-own-images/l02-own-images-thx.md) | 60 | Dockerfile, CMD/ENTRYPOINT, ARG, Hello-Images |
| | [3.3 Lokale Registry und Image-Verwaltung](../m03-images-registries/l03-local-registry/l03-local-registry-thx.md) | 60 | registry:3, Tags, push/pull, save/load |

## Tag 2 – Compose, Netzwerke und Sicherheit

| Modul | Lab | Min. | Kernthemen |
| --- | --- | --- | --- |
| 4 Docker Compose | [4.1 Einführung in Docker Compose](../m04-compose/l01-compose-intro/l01-compose-intro-thx.md) | 35 | compose.yml, build, environment, env_file, .env |
| | [4.2 Multi-Container-Anwendungen erstellen](../m04-compose/l02-multi-container/l02-multi-container-thx.md) | 40 | depends_on, Healthcheck, Watch, Replikas |
| | [4.3 Datenvolumes und Persistenz](../m04-compose/l03-volumes/l03-volumes-thx.md) | 40 | Named Volume, Bind Mount, Rezeptbuch mit MongoDB |
| | [4.4 Migration zu Microservices](../m04-compose/l04-microservices/l04-microservices-thx.md) | 20 | Strangler Fig, Zerlegung, Dienste einzeln aktualisieren |
| 5 Docker Networking | [5.1 Netzwerkverwaltung in Containern](../m05-networking/l01-network-basics/l01-network-basics-thx.md) | 30 | Bridge, Host, Overlay, Projektnetzwerk |
| | [5.2 Netzwerke erstellen und verwalten](../m05-networking/l02-network-management/l02-network-management-thx.md) | 45 | create, connect, disconnect, Subnetz |
| | [5.3 Kommunikation zwischen Containern](../m05-networking/l03-communication/l03-communication-thx.md) | 25 | Namensauflösung, Hello-App von Hand |
| 6 Docker Sicherheit | [6.1 Grundlagen der Docker-Sicherheit](../m06-security/l01-security-basics/l01-security-basics-thx.md) | 20 | Host, Image, Netzwerk, Container |
| | [6.2 Isolierung und Ressourcen](../m06-security/l02-isolation-limits/l02-isolation-limits-thx.md) | 35 | Namespaces, Cgroups, Limits, OOM |
| | [6.3 Security Scanning und andere Tools](../m06-security/l03-security-scanning/l03-security-scanning-thx.md) | 40 | Docker Scout, Trivy, Nicht-root, Signatur |

## Tag 3 – Debugging, Repositories, Stack und Orchestrierung

| Modul | Lab | Min. | Kernthemen |
| --- | --- | --- | --- |
| 7 Debugging und Fehlerbehebung | [7.1 Docker Debugging](../m07-debugging/l01-debugging/l01-debugging-thx.md) | 40 | Logs, Exit-Codes, Shell, Fehlerbilder |
| | [7.2 Logging und Monitoring](../m07-debugging/l02-logging-monitoring/l02-logging-monitoring-thx.md) | 35 | ELK, Prometheus, cAdvisor, Grafana |
| 8 Docker-Repositories | [8.1 Eigene Repositories](../m08-repositories/l01-own-repositories/l01-own-repositories-thx.md) | 50 | Registry mit Compose, Docker Hub, Tokens |
| | [8.2 Verteilte Anwendungen](../m08-repositories/l02-distributed-apps/l02-distributed-apps-thx.md) | 40 | CI/CD, Multi-Plattform, Images aus der Registry |
| 9 Frontend- und Backend-Stack | [9.1 Einführung in Traefik](../m09-frontend-backend-stack/l01-traefik-intro/l01-traefik-intro-thx.md) | 25 | Reverse Proxy, Labels, Dashboard |
| | [9.2 Traefik in der Praxis](../m09-frontend-backend-stack/l02-traefik-practice/l02-traefik-practice-thx.md) | 40 | Frontend, Backend, Redis hinter Traefik |
| | [9.3 Multistage Dockerfiles](../m09-frontend-backend-stack/l03-multistage/l03-multistage-thx.md) | 25 | Build-Stufen, kleinere Images |
| 10 Orchestrierung | [10.1 Grundlagen von Docker Swarm](../m10-orchestration/l01-swarm-basics/l01-swarm-basics-thx.md) | 30 | swarm init, Services, Skalieren |
| | [10.2 Docker Swarm und Kubernetes](../m10-orchestration/l02-swarm-vs-kubernetes/l02-swarm-vs-kubernetes-thx.md) | 15 | Vergleich, Einsatzempfehlung |
| | [10.3 Deployment in die Orchestrierungsplattform](../m10-orchestration/l03-swarm-deployment/l03-swarm-deployment-thx.md) | 30 | Stack, Rolling Update, Rollback |

## Cheatsheets

[Docker-CLI](../m02-container-basics/docker-cli-cheatsheet.md) · [Dockerfile](../m03-images-registries/dockerfile-cheatsheet.md) · [Compose](../m04-compose/compose-cheatsheet.md) · [Netzwerk](../m05-networking/network-cheatsheet.md) · [Sicherheit](../m06-security/security-cheatsheet.md) · [Debugging](../m07-debugging/debugging-cheatsheet.md) · [Registry](../m08-repositories/registry-cheatsheet.md) · [Traefik](../m09-frontend-backend-stack/traefik-cheatsheet.md) · [Swarm](../m10-orchestration/swarm-cheatsheet.md)
