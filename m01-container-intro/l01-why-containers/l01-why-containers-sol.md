# Lab 1.1 – Lösung: Warum Container?

## Aufgabe 1: Docker Desktop starten

Docker Desktop startet im Hintergrund eine kleine Linux-VM mit der Docker Engine. Erst wenn die Statusleiste `Engine running` zeigt, nimmt Docker Befehle an.

## Aufgabe 2: Erster Container

```bash
docker run hello-world
```

```text
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
58dee6a49ef1: Pull complete
Digest: sha256:1e4c05b897a751332ce85c7e9449da2d93514ea2dea6dbb0e2753c9e949b2bfa
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
…
```

In Klammern steht die Prozessor-Architektur des Rechners: `arm64v8` auf Apple-Silicon-Macs, `amd64` auf den meisten Windows- und Linux-Rechnern. Docker Hub liefert automatisch die passende Variante.

## Aufgabe 3: Schritte zuordnen

| Schritt | Beteiligte | Was passiert |
| --- | --- | --- |
| 1 | Terminal (Docker Client) → Docker Daemon | Der Befehl `docker` schickt den Auftrag an den Dienst im Hintergrund |
| 2 | Docker Daemon → Docker Hub | Das Image `hello-world` fehlt lokal und wird heruntergeladen |
| 3 | Docker Daemon → Container | Aus dem Image entsteht ein Container, der sein Programm startet |
| 4 | Container → Docker Daemon → Terminal | Die Ausgabe des Programms landet im Terminal; danach endet der Container |

Client und Daemon sind zwei getrennte Programme; Lab 1.3 zeigt sie mit `docker version`.

## Aufgabe 4: Zweiter Lauf

```bash
docker run hello-world
```

```text

Hello from Docker!
This message shows that your installation appears to be working correctly.
…
```

Die Zeilen `Unable to find image …` und `Pull complete` fehlen: Das Image liegt nach dem ersten Lauf auf dem Rechner, Docker lädt es nicht erneut. Jeder Lauf erzeugt trotzdem einen neuen Container aus demselben Image.
