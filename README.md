<div align="center">

<img src="assets/kodschul-logo.png" alt="Kodschul" width="220" />

# Docker Einführung

3-Tage-Workshop · Docker Engine 29, Compose, Swarm · Deutsch

**Anwendungen als Container bauen, verbinden, absichern und orchestrieren**

</div>

---

[Worum es geht](#worum-es-geht) · [Start](#start) · [Tag 1](#tag-1) · [Tag 2](#tag-2) · [Tag 3](#tag-3) · [Hilfe](#hilfe)

## Worum es geht

- Container lösen das „Works on my machine"-Problem: ein Image läuft überall gleich.
- Der Workshop baut alles an einem durchgehenden Projekt auf: der Hello-App aus Frontend und Backend.
- Jeder Schritt läuft auf dem eigenen Rechner: vom ersten `docker run` bis zum Swarm-Stack mit Rolling Update.
- Stand November 2026: Compose v2 ohne `version:`, Docker Scout, Traefik v3, `registry:3`.

| | |
| --- | --- |
| **Für** | Softwareentwicklung, DevOps und IT-Betrieb ohne Docker-Erfahrung |
| **Vorkenntnisse** | Terminal-Grundlagen; Programmierkenntnisse nicht nötig |
| **Werkzeuge** | Docker Desktop, Docker-Konto, VS Code, Browser |
| **Projekt** | Hello-App: zwei Python/Flask-Dienste, vom Dockerfile zum Swarm-Stack |
| **Material** | Handout pro Lab, Cheatsheet pro Modul, fertiger Projektstand für jedes Lab |

## Start

1. Rechner einrichten: [Setup und Installation](00-setup-and-installation.md)
2. Ziel und Tagesablauf lesen: [Kursüberblick](m00-overview/overview.md)
3. Projektordner öffnen: [Hello-App](project/README.md), im Terminal `cd project/playground/hello`
4. Mit dem ersten Lab starten: [Lab 1.1: Warum Container?](m01-container-intro/l01-why-containers/l01-why-containers-thx.md)

## Tag 1

| Modul | Kernthemen | Ergebnis |
| --- | --- | --- |
| 1 [Einführung in Containertechnologie](m01-container-intro/l01-why-containers/l01-why-containers-thx.md) | Warum Container, VM-Vergleich, Ökosystem | erster Container, Docker Desktop eingerichtet |
| 2 [Arbeit mit Containern](m02-container-basics/l01-cli/l01-cli-thx.md) | CLI, Inspektion, Bind Mount, Alternativen | nginx im Browser, Datei aus dem Container geändert |
| 3 [Images und lokale Registries](m03-images-registries/l01-image-layers/l01-image-layers-thx.md) | Layer, Dockerfile, Build-Args, Registry, Tags | `frontend:v1`/`v2`, `backend:v1` in der lokalen Registry |

## Tag 2

| Modul | Kernthemen | Ergebnis |
| --- | --- | --- |
| 4 [Docker Compose](m04-compose/l01-compose-intro/l01-compose-intro-thx.md) | Compose-Datei, Healthcheck, Watch, Replikas, Volumes, Microservices | Hello-App mit einem Befehl, Daten bleiben |
| 5 [Docker Networking](m05-networking/l01-network-basics/l01-network-basics-thx.md) | Bridge, Host, eigene Netzwerke, Namensauflösung | Container finden sich per Name |
| 6 [Docker Sicherheit](m06-security/l01-security-basics/l01-security-basics-thx.md) | Angriffsflächen, Namespaces, Limits, Scans, Nicht-root | begrenzte, gescannte Hello-App ohne root |

## Tag 3

| Modul | Kernthemen | Ergebnis |
| --- | --- | --- |
| 7 [Debugging und Monitoring](m07-debugging/l01-debugging/l01-debugging-thx.md) | Fehlerbilder, Logs, Prometheus, Grafana, ELK | vier Fehler behoben, Container-Metriken im Dashboard |
| 8 [Docker-Repositories](m08-repositories/l01-own-repositories/l01-own-repositories-thx.md) | eigene Registry, Docker Hub, Tokens, Multi-Plattform | Hello-Images in Registry und auf Docker Hub |
| 9 [Frontend- und Backend-Stack](m09-frontend-backend-stack/l01-traefik-intro/l01-traefik-intro-thx.md) | Traefik, Routing per Hostname, Redis, Multistage | Hello-App unter `app.localhost`, kleinere Images |
| 10 [Orchestrierung mit Swarm](m10-orchestration/l01-swarm-basics/l01-swarm-basics-thx.md) | Swarm, Services, Stack, Rolling Update, Kubernetes-Vergleich | Hello-App als Stack, Update `v1 → v2` und zurück |

- Jedes Lab hat drei Seiten: Theorie (`…-thx.md`), Übung (`…-exc.md`) und Lösung (`…-sol.md`).
- Cheatsheets liegen im jeweiligen Modulordner.
- Alle Labs mit Zeiten: [Module und Labs](m00-overview/topics.md).

## Hilfe

- **Projektstand wiederherstellen:** jeder Lab-Stand liegt fertig unter `project/examples/<modul>/<lab>/`, z. B. für den Stand nach Lab 4.3:

  ```bash
  cd project
  cp -r examples/m04-compose/l03-volumes/. playground/
  ```

- **Images fehlen** (neuer Rechner, Speicher aufgeräumt): `bash build-images.sh` im Ordner `project/` baut `frontend:v1`, `frontend:v2` und `backend:v1` neu.
- **Lösungen vergleichen:** jede Übung hat eine Lösung mit Befehlen und erwarteter Ausgabe; die Projektdateien je Lab stehen in der [Projektübersicht](project/README.md).
- **Nachschlagen:** [Glossar](m00-overview/glossary.md) · [FAQ](m00-overview/faq.md) · [Best Practices](m00-overview/best-practices.md)

---

<div align="center">

<sub>© Nextise GmbH · <a href="https://www.kodschul.com">kodschul.com</a> · Kompetenz aufbauen – von der sicheren KI-Anwendung bis zur modernen IT-Basis</sub>

</div>
