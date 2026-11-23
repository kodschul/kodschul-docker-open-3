# Lab 1.2: Vergleich zur Virtualisierung

**Leitfragen:**

<details>
<summary>Warum dauert der Start einer virtuellen Maschine länger als der eines normalen Programms?</summary>

Eine virtuelle Maschine bootet ein komplettes eigenes Betriebssystem, bevor das Programm überhaupt startet. Ein normales Programm (und ein Container) nutzt das bereits laufende Betriebssystem.

</details>

<details>
<summary>Was teilen sich zwei Programme auf demselben Rechner immer?</summary>

Hardware und Kern des Betriebssystems (Kernel): CPU, Arbeitsspeicher und die Verwaltung von Prozessen und Dateien. Container teilen sich genau diesen Kernel, VMs bringen je einen eigenen mit.

</details>

- Virtualisierung bildet einen ganzen Rechner mit eigenem Betriebssystem nach; Containerisierung schottet nur Prozesse auf einem gemeinsamen Kernel ab.
- Images bestehen aus schreibgeschützten Schichten; mehrere Container teilen sich dieselben Schichten.

## Begriffe

| Begriff | Bedeutung |
| --- | --- |
| Hypervisor | Software, die mehrere virtuelle Maschinen auf einem physischen Rechner ausführt, z. B. Hyper-V, VMware, VirtualBox |
| Gastbetriebssystem | das eigene Betriebssystem in einer VM, z. B. Windows Server in einer VM auf einem Linux-Server |
| Overhead | Zusatzverbrauch an Speicher und CPU, der nicht der Anwendung selbst dient (bei VMs: das ganze Gastbetriebssystem) |
| Isolationsgrad | wie stark zwei Anwendungen voneinander getrennt sind |
| Namespaces | Funktion des Linux-Kernels: Ein Prozess sieht nur seine eigenen Prozesse, Dateien und Netzwerkadressen; wie Trennwände in einem Großraumbüro |
| Cgroups | Funktion des Linux-Kernels, die CPU und Speicher eines Prozesses begrenzt (vertieft in Lab 6.2) |
| Schicht (Layer) | schreibgeschützter Teil eines Images mit den Dateiänderungen eines Bauschritts |
| Basis-Image | unterste Schicht eines Images, meist eine schlanke Linux-Distribution wie `alpine` oder `ubuntu` |
| Container-Schicht | beschreibbare Schicht, die jeder Container über dem Image bekommt |
| Dockerfile | Textdatei mit der Bauanleitung eines Images; hier nur als Beispiel, eigene Dockerfiles ab Lab 3.1 |
| Tag | Version eines Images hinter dem Doppelpunkt, z. B. `alpine:3.24` |

## Virtuelle Maschine und Container im Bild

<img src="https://www.docker.com/app/uploads/2021/11/docker-containerized-and-vm-transparent-bg-1110x454.png" alt="Links: Container App A bis F auf Docker, darunter ein Host-Betriebssystem und die Infrastruktur. Rechts: drei virtuelle Maschinen mit je App und eigenem Gastbetriebssystem auf einem Hypervisor über der Infrastruktur" width="680">

_Quelle: Docker Inc., „What is a Container?" (https://www.docker.com/resources/what-container/), abgerufen am 23.11.2026._

Links teilen sich sechs Container ein Betriebssystem. Rechts braucht jede der drei Anwendungen ein eigenes Gastbetriebssystem in einer eigenen VM.

## Technik von Virtualisierung und Containerisierung

| | Virtualisierung | Containerisierung |
| --- | --- | --- |
| Prinzip | simuliert eine vollständige Hardwareumgebung samt Betriebssystem | isoliert Anwendungen und ihre Abhängigkeiten auf einem gemeinsamen Kernel |
| enthält | komplettes Gastbetriebssystem + Anwendung | Anwendung + Bibliotheken, kein eigener Kernel |
| Größe | Gigabytes | meist wenige bis einige hundert Megabytes |
| läuft auf | Hypervisor | Container-Laufzeit (z. B. Docker) auf einem Betriebssystem |

<img src="https://thumb.wikimedia.org/wikipedia/commons/thumb/0/09/Docker-linux-interfaces.svg/500px-Docker-linux-interfaces.svg.png" alt="Diagramm: Docker oben, darunter die Schnittstellen libcontainer, libvirt, LXC und systemd-nspawn, ganz unten der Linux-Kernel mit cgroups, namespaces, SELinux, AppArmor, Netfilter, Netlink und capabilities" width="360">

_Quelle: Wikimedia Commons, „Docker-linux-interfaces.svg" (https://commons.wikimedia.org/wiki/File:Docker-linux-interfaces.svg), Maklaan, gemeinfrei, abgerufen am 23.11.2026._

Docker baut keine eigene Maschine nach, sondern nutzt Funktionen des Linux-Kernels: Namespaces trennen, was ein Container sieht; Cgroups begrenzen, was er verbraucht.

## Ressourcennutzung, Startzeit und Isolationsgrad

| Kriterium | Container | Virtuelle Maschine |
| --- | --- | --- |
| Ressourcennutzung | nutzen denselben Kernel und isolieren Anwendungen mit wenig Overhead | separate Betriebssysteme, daher hoher Speicher- und CPU-Verbrauch |
| Startzeit | unter einer Sekunde bis wenige Sekunden, kein Bootvorgang | Minuten bis zum Hochfahren, abhängig vom Betriebssystem |
| Isolationsgrad | gemeinsamer Kernel, Prozess- und Dateisystem-Isolation auf Anwendungsebene | vollständige Isolation, jede VM hat ihr eigenes Betriebssystem |
| typisch für | viele gleichartige Dienste, schnelle Auslieferung | verschiedene Betriebssysteme auf einem Server, harte Trennung zwischen Kunden |

Container und VMs schließen sich nicht aus: In der Cloud laufen Container meist in VMs, und Docker Desktop startet unter macOS und Windows selbst eine kleine Linux-VM (Lab 1.3). Deshalb zeigt `uname -r` im Container die Kernel-Version dieser Linux-VM, nicht die von macOS oder Windows.

```bash
docker run --rm alpine:3.24 uname -r     # Kernel-Version, die der Container sieht
```

- `--rm` entfernt den Container nach dem Ende automatisch.
- `alpine:3.24` ist ein sehr kleines Linux (Alpine Linux, Version 3.24); `uname -r` gibt die Kernel-Version aus.
- Unter Windows endet die Version auf `microsoft-standard-WSL2`, unter macOS auf `linuxkit`.

## Container-Layering

Container-Images bestehen aus mehreren schreibgeschützten Schichten (Layers), die aufeinander aufbauen. Images mit derselben Basis teilen sich diese Schichten auf der Festplatte. Änderungen erzeugen nur neue Schichten; das spart Speicherplatz und Downloadzeit.

<img src="https://docs.docker.com/engine/storage/drivers/images/sharing-layers.webp" alt="Vier Container mit je einer dünnen beschreibbaren Schicht (Thin R/W layer) zeigen alle auf dasselbe Image ubuntu:15.04 mit vier schreibgeschützten Schichten und Schloss-Symbol" width="520">

_Quelle: Docker Inc., „Storage drivers" (https://docs.docker.com/engine/storage/drivers/), abgerufen am 23.11.2026._

- Unten liegen die schreibgeschützten Schichten des Images (Schloss); das Image bleibt unverändert.
- Jeder Container bekommt oben eine eigene dünne, beschreibbare Container-Schicht. Was ein Programm im Container ändert, landet nur dort.
- Vier Container aus demselben Image belegen das Image nur einmal auf der Festplatte.

### Beispiel eines Dockerfiles mit Layering

Ein Dockerfile beschreibt Schritt für Schritt, wie ein Image entsteht. Jede Anweisung erzeugt eine Schicht:

```dockerfile
# Basis-Image (Schicht 1): festes Tag statt "latest"
FROM ubuntu:24.04
# neue Schicht: Pakete installieren
RUN apt-get update && apt-get install -y python3
# weitere Schicht: Anwendungscode hinzufügen
COPY app.py /app/app.py
```

| Anweisung | Schicht im Image |
| --- | --- |
| `FROM ubuntu:24.04` | Dateien von Ubuntu 24.04 als Basis |
| `RUN apt-get …` | die Dateien, die Python 3 installiert |
| `COPY app.py …` | nur die Datei `app.py` |

Ändert sich `app.py`, wird nur die letzte Schicht neu gebaut und verteilt; Ubuntu und Python bleiben. Die Anweisungen im Einzelnen folgen in Lab 3.1 und 3.2.

Feste Tags wie `ubuntu:24.04` statt `ubuntu:latest` legen fest, welche Version im Image steckt. `latest` zeigt beim nächsten Bauen womöglich auf eine neue Version, und das Image ändert sich unbemerkt.

## Typische Fehler

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| erster Start dauert mehrere Sekunden | Image wird erst heruntergeladen | Befehl wiederholen; ab dem zweiten Lauf liegt das Image lokal |
| `uname -r` zeigt im Container eine andere Version als auf dem Rechner | Container nutzen den Kernel der Linux-VM von Docker Desktop | erwartet, siehe oben |
| `time: command not found` | Shell ohne `time` (z. B. Windows-Eingabeaufforderung) | Kurs-Shell `bash` nutzen ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)) |

## Fazit

- VMs simulieren ganze Rechner mit eigenem Betriebssystem; Container sind abgeschottete Prozesse auf einem gemeinsamen Kernel.
- Container starten schneller und brauchen weniger Ressourcen; VMs trennen stärker.
- Images bestehen aus schreibgeschützten Schichten, die sich Container teilen; jeder Container schreibt in seine eigene Schicht.

In der Übung zeigen zwei verschiedene Linux-Distributionen denselben Kernel, und die Startzeit eines Containers wird gemessen.
