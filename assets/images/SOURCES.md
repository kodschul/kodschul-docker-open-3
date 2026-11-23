# Bildquellen

Externe Bilder sind per URL eingebunden (keine lokalen Kopien); eigene Screenshots liegen unter `assets/images/mNN/` und entstehen reproduzierbar mit `scripts/capture.mjs` und den Shot-Listen in `scripts/shots/` (nicht Teil der Teilnehmerunterlagen). Alle externen URLs geprüft am 23.11.2026 (HTTP 200, Bildformat).

## Setup

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| docker-desktop-containers | Docker Desktop, Ansicht Containers (Setup) | https://www.docker.com/products/docker-desktop/ | https://www.docker.com/app/uploads/2025/05/DD-hiroko-2320x1456.png | Docker Inc. | 23.11.2026 |

## Modul 1

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| docker-what-is-container | Containerized Applications: App A–F auf Docker, Host-OS, Infrastruktur (Lab 1.1) | https://www.docker.com/resources/what-container/ | https://www.docker.com/app/uploads/2021/11/container-what-is-container-1110x961.png | Docker Inc. | 23.11.2026 |
| hub-official-images | Docker Hub, Filter Docker Official Image: alpine, nginx, busybox mit Downloads (Lab 1.1) | https://docs.docker.com/build/ | https://docs.docker.com/build/images/hub-official-images.webp | Docker Inc. | 23.11.2026 |
| hello-world | eigener Screenshot: Ausgabe von docker run hello-world (Lab 1.1) | eigener Screenshot | m01/hello-world.png | Nextise GmbH | 23.11.2026 |
| docker-containerized-and-vm | Container auf Docker vs. VMs auf Hypervisor (Lab 1.2) | https://www.docker.com/resources/what-container/ | https://www.docker.com/app/uploads/2021/11/docker-containerized-and-vm-transparent-bg-1110x454.png | Docker Inc. | 23.11.2026 |
| docker-linux-interfaces | Docker nutzt Kernel-Funktionen: cgroups, namespaces, libcontainer, LXC (Lab 1.2) | https://commons.wikimedia.org/wiki/File:Docker-linux-interfaces.svg | https://thumb.wikimedia.org/wikipedia/commons/thumb/0/09/Docker-linux-interfaces.svg/500px-Docker-linux-interfaces.svg.png | Maklaan, gemeinfrei | 23.11.2026 |
| sharing-layers | vier Container teilen die Image-Schichten von ubuntu:15.04 (Lab 1.2) | https://docs.docker.com/engine/storage/drivers/ | https://docs.docker.com/engine/storage/drivers/images/sharing-layers.webp | Docker Inc. | 23.11.2026 |
| kernel-und-startzeit | eigener Screenshot: uname -r in Alpine und Ubuntu, time docker run (Lab 1.2) | eigener Screenshot | m01/kernel-und-startzeit.png | Nextise GmbH | 23.11.2026 |
| docker-architecture | Client, Docker Host mit Daemon/Images/Containern, Registry (Lab 1.3) | https://commons.wikimedia.org/wiki/File:Docker-architecture.png | https://thumb.wikimedia.org/wikipedia/commons/thumb/2/20/Docker-architecture.png/960px-Docker-architecture.png | Mohamed9Hassan (nach Docker-Doku), CC BY-SA 4.0 | 23.11.2026 |
| docker-version | eigener Screenshot: docker version mit Client und Server (Lab 1.3) | eigener Screenshot | m01/docker-version.png | Nextise GmbH | 23.11.2026 |
| docker-desktop-containers | Docker Desktop, Ansicht Containers mit Navigation und Statusleiste (Lab 1.3) | https://www.docker.com/products/docker-desktop/ | https://www.docker.com/app/uploads/2025/05/DD-hiroko-2320x1456.png | Docker Inc. | 23.11.2026 |
| wsl2-enabled | Windows-Features Virtual Machine Platform und WSL eingeschaltet (Lab 1.3) | https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/ | https://docs.docker.com/desktop/images/wsl2-enabled.png | Docker Inc. | 23.11.2026 |
| virtualization-enabled | Task-Manager, CPU: Virtualisierung aktiviert (Lab 1.3) | https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/ | https://docs.docker.com/desktop/images/virtualization-enabled.png | Docker Inc. | 23.11.2026 |

## Modul 2

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| nginx-willkommen | eigener Screenshot: nginx-Startseite unter localhost:8080 (Lab 2.1) | eigener Screenshot | m02/nginx-willkommen.png | Nextise GmbH | 23.11.2026 |
| docker-ps-a | eigener Screenshot: Port-Konflikt, stop/kill, docker ps -a mit Exit-Codes (Lab 2.1) | eigener Screenshot | m02/docker-ps-a.png | Nextise GmbH | 23.11.2026 |
| nginx-geaendert | eigener Screenshot: per docker cp geänderte nginx-Startseite (Lab 2.2) | eigener Screenshot | m02/nginx-geaendert.png | Nextise GmbH | 23.11.2026 |
| container-layers | beschreibbare Container-Schicht über schreibgeschützten Image-Schichten (Lab 2.2) | https://docs.docker.com/engine/storage/drivers/ | https://docs.docker.com/engine/storage/drivers/images/container-layers.webp | Docker Inc. | 23.11.2026 |
| bin-geloescht | eigener Screenshot: rm -rf /bin im Busybox-Container, Neustart scheitert (Lab 2.2) | eigener Screenshot | m02/bin-geloescht.png | Nextise GmbH | 23.11.2026 |
| bind-mount-test | eigener Screenshot: test.txt per Bind Mount im Container geändert (Lab 2.2) | eigener Screenshot | m02/bind-mount-test.png | Nextise GmbH | 23.11.2026 |
| podman-commands | echte Podman-Sitzung: version, image history, info Rootless true (Lab 2.3) | https://commons.wikimedia.org/wiki/File:Podman_commands_screenshot.webp | https://thumb.wikimedia.org/wikipedia/commons/thumb/2/29/Podman_commands_screenshot.webp/500px-Podman_commands_screenshot.webp | Software: Red Hat, Inc. und Podman-Community; Screenshot: VulcanSphere; Apache-2.0 | 23.11.2026 |
| rancher-desktop-container-engine | Rancher Desktop Preferences: Wahl containerd oder dockerd (moby) (Lab 2.3) | https://docs.rancherdesktop.io/ui/preferences/container-engine/general | https://suse-rancher-media.s3.amazonaws.com/desktop/v1.25/preferences/macOS_containerEngine_tabGeneral.png | SUSE | 23.11.2026 |
| podman-desktop-containers | Podman Desktop, Ansicht Containers (Lab 2.3) | https://commons.wikimedia.org/wiki/File:Podman_Desktop_Containers_screenshot.webp | https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bc/Podman_Desktop_Containers_screenshot.webp/960px-Podman_Desktop_Containers_screenshot.webp | Software: Red Hat, Inc. und Podman-Community; Screenshot: VulcanSphere; Apache-2.0 | 23.11.2026 |
| orbstack-hero | OrbStack unter macOS mit Compose-Projekt und Linux-Maschine (Lab 2.3) | https://orbstack.dev/ | https://orbstack.dev/img/hero.png | Orbital Labs, LLC | 23.11.2026 |

## Modul 3

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| container-layers | Container auf ubuntu:15.04: schreibgeschützte Image-Schichten und beschreibbare Container-Schicht (Lab 3.1) | https://docs.docker.com/engine/storage/drivers/ | https://docs.docker.com/engine/storage/drivers/images/container-layers.webp | Docker Inc. | 23.11.2026 |
| overlay-constructs | OverlayFS: lowerdir, upperdir, merged (Lab 3.1) | https://docs.docker.com/engine/storage/drivers/overlayfs-driver/ | https://docs.docker.com/engine/storage/drivers/images/overlay_constructs.webp | Docker Inc. | 23.11.2026 |
| sharing-layers | Vier Container teilen sich die Schichten eines Images (Lab 3.1) | https://docs.docker.com/engine/storage/drivers/ | https://docs.docker.com/engine/storage/drivers/images/sharing-layers.webp | Docker Inc. | 23.11.2026 |
| docker-images-sizes | Terminal: docker images mit ubuntu:24.04, alpine:3.24, python:3.13-alpine (Lab 3.1, Lösung 3.1) | eigener Screenshot (Werte aus docker images, linux/arm64) | output/assets/images/m03/docker-images-sizes.png | Nextise GmbH | 23.11.2026 |
| docker-history-python | Terminal: docker history python:3.13-alpine (Lab 3.1) | eigener Screenshot | output/assets/images/m03/docker-history-python.png | Nextise GmbH | 23.11.2026 |
| cache-stack-invalidated | Build-Cache: ab geänderter COPY-Anweisung wird neu gebaut (Lab 3.2) | https://docs.docker.com/build/cache/ | https://docs.docker.com/build/images/cache-stack-invalidated.png | Docker Inc. | 23.11.2026 |
| harbor-list-artifacts | Harbor-Weboberfläche: Repository mit Artefakten, Tags, Pull Command (Lab 3.3) | https://goharbor.io/docs/main/working-with-projects/working-with-images/repositories/ | https://goharbor.io/docs/main/img/list-artifacts.png | Harbor Authors (goharbor/website), Apache-2.0 | 23.11.2026 |
| hub-supported-tags | Docker Hub, Supported tags des Ubuntu-Images, mehrere Tags je Image (Lab 3.3) | https://docs.docker.com/docker-hub/image-library/trusted-content/ | https://docs.docker.com/docker-hub/images/supported_tags.webp | Docker Inc. | 23.11.2026 |
| recipe-page | Rezeptseite index.html mit Beispielrezept im Browser (Lösung 3.3) | eigener Screenshot | output/assets/images/m03/recipe-page.png | Nextise GmbH | 23.11.2026 |
| hello-frontend-v2 | Browser: Hello World 2.0.0 ohne Backend, Hinweis Backend nicht erreichbar (Lab 3.2, Lösung 3.2) | eigener Screenshot | output/assets/images/m03/hello-frontend-v2.png | Nextise GmbH | 23.11.2026 |
| registry-push-catalog | Terminal: docker tag/push frontend:v1 nach 127.0.0.1:5001, Katalog und Tag-Liste (Lab 3.3, Lösung 3.3) | eigener Screenshot (Testlauf auf Port 18250, im Bild Kursport 5001) | output/assets/images/m03/registry-push-catalog.png | Nextise GmbH | 23.11.2026 |

## Modul 4

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| compose-application | Compose-Anwendung: Frontend, Backend, Netzwerk, Volume, Config, Secret (Lab 4.1) | https://docs.docker.com/compose/intro/compose-application-model/ | https://docs.docker.com/compose/images/compose-application.webp | Docker Inc. | 23.11.2026 |
| compose-v1-v2-v5 | Compose v1 (Python, version-Feld, docker-compose) vs. v2 und v5 (Go, Compose Specification) (Lab 4.1) | https://docs.docker.com/compose/intro/history/ | https://docs.docker.com/compose/images/v1-versus-v2-versus-v5.png | Docker Inc. | 23.11.2026 |
| compose-watch-ga-figure2 | Compose Watch: rebuild bei package.json, sync für web/, ignore node_modules/ (Lab 4.2) | https://www.docker.com/blog/announcing-docker-compose-watch-ga-release/ | https://www.docker.com/app/uploads/2023/09/compose-watch-ga_figure2-1110x646.png | Docker Inc. | 23.11.2026 |
| container-layers | beschreibbare Container-Schicht über nur lesbaren Image-Schichten (Lab 4.3) | https://docs.docker.com/engine/storage/drivers/ | https://docs.docker.com/engine/storage/drivers/images/container-layers.webp | Docker Inc. | 23.11.2026 |
| microservices-sketch | Monolith vs. Microservices und ihre Skalierung (Lab 4.4) | https://martinfowler.com/articles/microservices.html | https://martinfowler.com/articles/microservices/images/sketch.png | James Lewis, Martin Fowler | 23.11.2026 |
| strangler-fig-pattern | Strangler-Fig-Muster in drei Phasen mit Fassade (Lab 4.4) | https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig | https://learn.microsoft.com/en-us/azure/architecture/patterns/_images/strangler-fig-pattern.svg | Microsoft (Microsoft Learn), CC BY 4.0 | 23.11.2026 |
| microservices-decentralised-data | eine Datenbank im Monolithen vs. eigene Datenbanken je Service (Lab 4.4) | https://martinfowler.com/articles/microservices.html | https://martinfowler.com/articles/microservices/images/decentralised-data.png | James Lewis, Martin Fowler | 23.11.2026 |
| hello-compose | eigener Screenshot: Hello-App mit compose-minimal.yml im Browser, Backend-Antwort sichtbar (Lab 4.1) | eigener Screenshot | m04/hello-compose.png | Nextise GmbH | 23.11.2026 |
| compose-ps-healthy | eigener Screenshot: up -d --build mit Healthy/Started und ps mit (healthy) (Lab 4.2) | eigener Screenshot | m04/compose-ps-healthy.png | Nextise GmbH | 23.11.2026 |
| compose-ps-replicas | eigener Screenshot: docker compose ps mit zehn Frontends und zufälligen Ports (Lab 4.2) | eigener Screenshot | m04/compose-ps-replicas.png | Nextise GmbH | 23.11.2026 |
| todo-app | eigener Screenshot: docker/multi-container-app mit mongo:8 im Browser (Lab 4.2) | eigener Screenshot | m04/todo-app.png | Nextise GmbH | 23.11.2026 |
| recipe-book-curl | eigener Screenshot: Rezeptbuch, curl POST/GET vor und nach down/up (Lab 4.3) | eigener Screenshot | m04/recipe-book-curl.png | Nextise GmbH | 23.11.2026 |

## Modul 5

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| nat-concept | NAT-Prinzip: Router übersetzt private in öffentliche Adresse (Lab 5.1) | https://commons.wikimedia.org/wiki/File:NAT_Concept-en.svg | https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c7/NAT_Concept-en.svg/330px-NAT_Concept-en.svg.png | Wikimedia Commons, CC BY-SA 4.0 | 23.11.2026 |
| macvlan-bridge-ipvlan-l2 | Macvlan: Container mit eigenen IPs im physischen Netz (Lab 5.1) | https://docs.docker.com/engine/network/drivers/macvlan/ | https://docs.docker.com/engine/network/drivers/images/macvlan-bridge-ipvlan-l2.webp | Docker Inc. | 23.11.2026 |
| network-inspect | docker network ls und inspect hello_default mit Containern und IPs (Lab 5.1) | eigener Screenshot, Hello-App | m05/network-inspect.png (scripts/shots/m05.json) | Nextise GmbH | 23.11.2026 |
| host-network-desktop | curl auf localhost:80 scheitert unter Docker Desktop, wget aus Host-Netzwerk-Container liefert nginx (Lab 5.2) | eigener Screenshot, Docker Desktop | m05/host-network-desktop.png (scripts/shots/m05.json) | Nextise GmbH | 23.11.2026 |
| ping-fail-success | Ping per Name scheitert, nach docker network connect erfolgreich (Lab 5.2, Lösung) | eigener Screenshot, Docker Desktop | m05/ping-fail-success.png (scripts/shots/m05.json) | Nextise GmbH | 23.11.2026 |
| hello-net-page | Hello-App ohne Compose im Netzwerk hello-net mit Backend-Antwort (Lab 5.3) | eigener Screenshot, Hello-App | m05/hello-net-page.png (scripts/shots/m05.json) | Nextise GmbH | 23.11.2026 |

## Modul 6

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| docker-architecture-wikimedia | Client, Daemon, Registry: wer den Daemon steuert, steuert alles (Lab 6.1) | https://commons.wikimedia.org/wiki/File:Docker-architecture.png | https://thumb.wikimedia.org/wikipedia/commons/thumb/2/20/Docker-architecture.png/960px-Docker-architecture.png | Wikimedia Commons, nach der Docker-Dokumentation, CC BY-SA 4.0 (auch in Lab 1.3) | 23.11.2026 |
| linux-cgroups | Linux-Kernel mit cgroups, Prozess- und Speicherverwaltung, Container darüber (Lab 6.2) | https://commons.wikimedia.org/wiki/File:Linux_kernel_unified_hierarchy_cgroups_and_systemd.svg | https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e7/Linux_kernel_unified_hierarchy_cgroups_and_systemd.svg/960px-Linux_kernel_unified_hierarchy_cgroups_and_systemd.svg.png | ScotXW, CC BY-SA 3.0 | 23.11.2026 |
| trivy-image-scan | Ablauf eines Image-Scans mit Trivy (Lab 6.3) | https://trivy.dev/docs/latest/guide/target/container_image/ | https://trivy.dev/docs/latest/imgs/image.png | Aqua Security, Apache-2.0 | 23.11.2026 |
| trivy-overview | Trivy: Ziele und Prüfarten (Lab 6.3) | https://trivy.dev/docs/latest/guide/ | https://trivy.dev/docs/latest/imgs/overview.png | Aqua Security, Apache-2.0 | 23.11.2026 |
| falco-events-flow | Falco: Systemaufrufe und Ereignisse rein, Warnungen raus (Lab 6.3) | https://falco.org/ | https://falco.org/img/falco-events-flow-simplified.png | The Falco Authors, CC BY 4.0 | 23.11.2026 |
| trivy-compare | Trivy-Summen frontend:v1 vs. python:3.9-alpine (Lab 6.3) | eigener Screenshot, Hello-App | m06/trivy-compare.png (scripts/shots/m06.json) | Nextise GmbH | 23.11.2026 |
| root-and-host-mount | whoami root im Hello-Frontend, Container mit -v /:/host schreibt als root (Lab 6.1) | eigener Screenshot, Hello-App | m06/root-and-host-mount.png (scripts/shots/m06.json) | Nextise GmbH | 23.11.2026 |
| oom-killed | Container oom-test über Speichergrenze: Exit-Code 137, OOMKilled true (Lab 6.2) | eigener Screenshot, Docker Desktop | m06/oom-killed.png (scripts/shots/m06.json) | Nextise GmbH | 23.11.2026 |

## Modul 7

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| fehler-cmd-logs.png | Fehlerbild 1: `docker compose ps -a` mit Exited (2), Logs `can't open file` (7.1) | eigener Screenshot (Terminal-Ausgabe aus Test 23.11.2026), Shot-Liste `scripts/shots/m07.json` | `output/assets/images/m07/fehler-cmd-logs.png` | Nextise GmbH | 23.11.2026 |
| fehler-speicher-oom.png | Fehlerbild 4: Exited (137), `docker inspect` mit oom=true (7.1) | eigener Screenshot (Terminal-Ausgabe aus Test 23.11.2026), Shot-Liste `scripts/shots/m07.json` | `output/assets/images/m07/fehler-speicher-oom.png` | Nextise GmbH | 23.11.2026 |
| (extern) Out of Memory in Linux | Kernel-Meldung des OOM-Killers (7.1) | https://commons.wikimedia.org/wiki/File:Out_of_Memory_in_Linux.jpg | https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6f/Out_of_Memory_in_Linux.jpg/960px-Out_of_Memory_in_Linux.jpg | Neo139, CC BY-SA 3.0 | 23.11.2026 |
| (extern) Elastic-Plattform | Bausteine Ingest, Store, Visualize (7.2) | https://www.elastic.co/docs/get-started | https://www.elastic.co/docs/get-started/images/elastic-platform.png | Elastic N.V., Herstellerdoku (Lizenz prüfen) | 23.11.2026 |
| (extern) Kibana Discover | Kibana-Oberfläche mit Zeitdiagramm und Logliste (7.2) | https://commons.wikimedia.org/wiki/File:Kibana_demo_screenshot.jpg | https://thumb.wikimedia.org/wikipedia/commons/thumb/8/84/Kibana_demo_screenshot.jpg/960px-Kibana_demo_screenshot.jpg | Klapi, CC BY-SA 4.0 | 23.11.2026 |
| (extern) Prometheus-Architektur | Server, Exporter, Alertmanager, Grafana (7.2) | https://prometheus.io/docs/introduction/overview/ | https://prometheus.io/assets/docs/architecture.svg | Prometheus Authors, Apache 2.0 (prometheus/docs) | 23.11.2026 |
| (extern) Grafana-Dashboard | Beispiel-Dashboard mit Kacheln und Zeitreihen (7.2) | https://grafana.com/docs/grafana/latest/dashboards/ | https://grafana.com/media/docs/grafana/dashboards-overview/complex-dashboard-example.png | Grafana Labs, Herstellerdoku (Lizenz prüfen) | 23.11.2026 |
| (extern) Loki-Überblick | Apps → Agent → Loki → Grafana/LogCLI (7.2) | https://grafana.com/docs/loki/latest/get-started/overview/ | https://grafana.com/docs/loki/latest/get-started/loki-overview-2.png | Grafana Labs, Herstellerdoku (Lizenz prüfen) | 23.11.2026 |
| grafana-hello-container.png | Grafana-Dashboard „Hello-Container" mit Lastspitzen (7.2) | eigener Screenshot (Monitoring-Stack im Test, Test-Port, Abfragen per label_replace auf hello-* umbenannt), Shot-Liste `scripts/shots/m07.json` | `output/assets/images/m07/grafana-hello-container.png` | Nextise GmbH | 23.11.2026 |
| prometheus-targets.png | Prometheus Status > Target health mit cadvisor und node-exporter UP (7.2) | eigener Screenshot (Monitoring-Stack im Test), Shot-Liste `scripts/shots/m07.json` | `output/assets/images/m07/prometheus-targets.png` | Nextise GmbH | 23.11.2026 |

## Modul 8

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| (extern) Semantic Versioning | v2.21.2 mit breaking changes / features / bugfixes (8.1) | https://commons.wikimedia.org/wiki/File:Semantic-versioning.svg | https://thumb.wikimedia.org/wikipedia/commons/thumb/0/09/Semantic-versioning.svg/330px-Semantic-versioning.svg.png | Surjit Bains, CC BY-SA 4.0 | 23.11.2026 |
| (extern) Continuous integration | CI-Lauf baut und pusht Images (8.2) | https://docs.docker.com/build/ci/ | https://docs.docker.com/build/ci/images/continuous-integration.svg | Docker Inc., Apache 2.0 (docker/docs) | 23.11.2026 |
| (extern) Continuous Delivery | CD-Prozess vom Commit bis Release (8.2) | https://commons.wikimedia.org/wiki/File:Continuous_Delivery_process_diagram.svg | https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c3/Continuous_Delivery_process_diagram.svg/500px-Continuous_Delivery_process_diagram.svg.png | Grégoire Détrez nach Jez Humble, CC BY-SA 4.0 | 23.11.2026 |
| (extern) Single vs. Multi-Plattform | Manifest-Liste mit amd64 und arm64 (8.2) | https://docs.docker.com/build/building/multi-platform/ | https://docs.docker.com/build/images/single-vs-multiplatform-image.svg | Docker Inc., Apache 2.0 (docker/docs) | 23.11.2026 |
| registry-katalog.png | Push mit --all-tags, Katalog und Tags nach Neustart (8.1) | eigener Screenshot (Terminal-Ausgabe aus Test 23.11.2026, Test-Port durch Kursport 5001 ersetzt), Shot-Liste `scripts/shots/m08.json` | `output/assets/images/m08/registry-katalog.png` | Nextise GmbH | 23.11.2026 |

## Modul 9

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| traefik-architecture | Traefik Proxy: Anfragen aus dem Internet, Routing Engine, Ziele in Kubernetes, Docker/Swarm und auf Servern (Lab 9.1) | https://doc.traefik.io/traefik/ | https://doc.traefik.io/traefik/assets/img/traefik-architecture.png | Traefik Labs | 23.11.2026 |
| traefik-dashboard | Traefik-Dashboard v3.8 mit Entrypoints traefik/web und HTTP-Routern der Hello-App (Lab 9.1) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/traefik-dashboard.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| traefik-routers | Traefik-Dashboard, HTTP Routers app@docker und api@docker (Lab 9.1) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/traefik-routers.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| traefik-docker-router | Traefik-Doku: Router whoami@docker mit Rule Host(`whoami.localhost`) (Lab 9.1) | https://doc.traefik.io/traefik/getting-started/docker/ | https://doc.traefik.io/traefik/assets/img/getting-started/docker-router.png | Traefik Labs | 23.11.2026 |
| hello-app-localhost | Hello-App v2 unter http://app.localhost hinter Traefik (Lab 9.1) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/hello-app-localhost.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| hello-api-localhost | Hello-Backend-JSON unter http://api.app.localhost (Lab 9.1) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/hello-api-localhost.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| traefik-webui-dashboard | Traefik-Dashboard-Übersicht aus der Doku (Lab 9.2) | https://doc.traefik.io/traefik/reference/install-configuration/api-dashboard/ | https://doc.traefik.io/traefik/assets/img/webui-dashboard.png | Traefik Labs | 23.11.2026 |
| time-app | Time-App unter http://localhost mit Current time und Last time (Lab 9.2) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/time-app.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| multistage-size | docker images todo-app (dev/prod) und nodemon-Prüfung (Lab 9.3) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/multistage-size.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| todo-app-prod | Todo-App aus dem Multistage-Image unter http://localhost:3000 (Lab 9.3) | eigener Screenshot (scripts/shots/m09.json) | assets/images/m09/todo-app-prod.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |

## Modul 10

| Datei | Inhalt (Lab) | Quelle | Bild-URL bzw. Pfad | Urheber/Lizenz | abgerufen am |
| --- | --- | --- | --- | --- | --- |
| swarm-diagram | Swarm: drei Manager (Raft) und sieben Worker (Lab 10.1) | https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/ | https://docs.docker.com/engine/swarm/images/swarm-diagram.webp | Docker Inc. | 23.11.2026 |
| services-diagram | Service mit drei nginx-Replikas, Tasks und Containern auf drei Nodes (Lab 10.1) | https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/ | https://docs.docker.com/engine/swarm/images/services-diagram.webp | Docker Inc. | 23.11.2026 |
| service-ps-web | docker service ps web mit zehn Tasks (Lab 10.1) | eigener Screenshot (scripts/shots/m10.json) | assets/images/m10/service-ps-web.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| components-of-kubernetes | Kubernetes-Komponenten: Control Plane und Nodes (Lab 10.2) | https://kubernetes.io/docs/concepts/overview/components/ | https://kubernetes.io/images/docs/components-of-kubernetes.svg | The Kubernetes Authors, CC BY 4.0 | 23.11.2026 |
| cncf-survey-2025 | Infografik CNCF Annual Cloud Native Survey 2025: 82 % Kubernetes in Produktion (Lab 10.2) | https://www.cncf.io/announcements/2026/01/20/kubernetes-established-as-the-de-facto-operating-system-for-ai-as-production-use-hits-82-in-2025-cncf-annual-cloud-native-survey/ | https://www.cncf.io/wp-content/uploads/2026/01/CNCF-Annual-Cloud-Native-Survey-The-Infrastructure-of-AIs-Future-infographic-scaled.jpg | CNCF / The Linux Foundation | 23.11.2026 |
| replicated-vs-global | Replicated und Global Mode im Swarm (Lab 10.3) | https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/ | https://docs.docker.com/engine/swarm/images/replicated-vs-global.webp | Docker Inc. | 23.11.2026 |
| ingress-routing-mesh | Routing Mesh: veröffentlichter Port auf allen Nodes (Lab 10.3) | https://docs.docker.com/engine/swarm/ingress/ | https://docs.docker.com/engine/swarm/images/ingress-routing-mesh.webp | Docker Inc. | 23.11.2026 |
| rolling-update-curl | curl-Schleife während des Rolling Updates, Antworten 1.0.0/2.0.0 gemischt (Lab 10.3) | eigener Screenshot (scripts/shots/m10.json) | assets/images/m10/rolling-update-curl.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| hello-v1-swarm | Hello-App v1 als Swarm-Stack auf Port 999 (Lab 10.3) | eigener Screenshot (scripts/shots/m10.json) | assets/images/m10/hello-v1-swarm.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
| hello-v2-swarm | Hello-App v2 nach dem Rolling Update auf Port 999 (Lab 10.3) | eigener Screenshot (scripts/shots/m10.json) | assets/images/m10/hello-v2-swarm.png | eigene Aufnahme, Nextise GmbH | 23.11.2026 |
