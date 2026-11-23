# Lab 1.3 – Lösung: Container-Ökosystem kennenlernen

## Aufgabe 1: Client und Server

```bash
docker version
```

```text
Client:
 Version:           29.9.3
 API version:       1.56
 OS/Arch:           darwin/arm64
 Context:           desktop-linux
 …
Server: Docker Desktop 4.99.0 (245822)
 Engine:
  Version:          29.9.3
  API version:      1.56 (minimum version 1.40)
  OS/Arch:          linux/arm64
 containerd:
  Version:          v2.4.2
 runc:
  Version:          1.5.2
 …
```

| Teil | Version | OS/Arch | Bedeutung |
| --- | --- | --- | --- |
| Client | 29.9.3 | `darwin/arm64` (Windows: `windows/amd64`) | das Kommando `docker` auf dem Rechner |
| Server | 29.9.3 | `linux/arm64` (bzw. `linux/amd64`) | Docker Engine in der Linux-VM von Docker Desktop |

Versionsnummern weichen je nach Installationsstand ab. Client und Server sprechen über die API (`API version`); der Server akzeptiert auch ältere Clients bis zur `minimum version`.

## Aufgabe 2: docker info

```bash
docker info
```

```text
Server:
 Containers: 5
  Running: 0
  …
 Images: 3
 …
 Kernel Version: 7.0.14-linuxkit
 Operating System: Docker Desktop
 OSType: linux
 Architecture: aarch64
 CPUs: 8
 Total Memory: 10.68GiB
 …
```

- `Kernel Version` ist dieselbe wie `uname -r` im Container aus Lab 1.2: Alle Container nutzen den Kernel dieser VM.
- `CPUs` und `Total Memory` sind die Ressourcen der Linux-VM, nicht des ganzen Rechners; Docker Desktop legt sie unter **Settings > Resources** fest.
- `Containers` zählt auch beendete Container, `Images` die lokal gespeicherten Images (hier `hello-world`, `alpine:3.24`, `ubuntu:24.04`).

Einzelne Werte lassen sich gezielt abfragen:

```bash
docker info --format '{{.OperatingSystem}} | {{.KernelVersion}} | {{.NCPU}} CPUs'
```

```text
Docker Desktop | 7.0.14-linuxkit | 8 CPUs
```

## Aufgabe 3: Ansicht Containers

Die Ansicht **Containers** listet die `hello-world`-Container mit Zufallsnamen (z. B. `brave_swirles`) und dem Status **Exited**: Das Programm hat seinen Text ausgegeben und sich beendet. Die Container aus Lab 1.2 fehlen, weil `--rm` sie nach dem Ende entfernt hat.

## Aufgabe 4: Ansichten Images und Volumes

- **Images** zeigt `hello-world`, `alpine` (Tag `3.24`) und `ubuntu` (Tag `24.04`) mit ihrer Größe; die Anzahl stimmt mit `Images` aus `docker info` überein.
- **Volumes** ist noch leer; Volumes entstehen erst in Lab 4.3.

Docker Desktop und das Terminal zeigen dieselben Daten, weil beide als Client mit demselben Docker Daemon sprechen.
