# FAQ

## Ist Docker Desktop kostenlos?

- Für Privatpersonen, Ausbildung und Firmen unter 250 Beschäftigten und 10 Mio. USD Umsatz ja.
- Größere Firmen brauchen eine Lizenz; Alternativen stehen in [Lab 2.3](../m02-container-basics/l03-alternatives/l03-alternatives-thx.md).

## Warum braucht Docker unter Windows und macOS eine Linux-VM?

- Linux-Container nutzen den Linux-Kernel.
- Docker Desktop startet dafür im Hintergrund eine kleine Linux-VM.

## Was ist der Unterschied zwischen Image und Container?

- Image: unveränderliche Vorlage.
- Container: laufende Instanz mit eigener beschreibbarer Schicht.

## Warum sind meine Änderungen nach `docker rm` weg?

- Sie lagen in der Container-Schicht.
- Dauerhafte Daten gehören in ein Volume ([Lab 4.3](../m04-compose/l03-volumes/l03-volumes-thx.md)).

## `port is already allocated` – was tun?

- Ein anderer Container oder Dienst nutzt den Port.
- `docker ps` prüfen, alten Container entfernen oder anderen Rechner-Port wählen.

## Warum findet das Frontend das Backend nicht?

- Beide müssen im selben benutzerdefinierten Netzwerk hängen.
- In der Standard-Bridge funktionieren Namen nicht ([Lab 5.3](../m05-networking/l03-communication/l03-communication-thx.md)).

## `docker-compose` oder `docker compose`?

- `docker compose` (mit Leerzeichen) ist aktuell.
- `docker-compose` (Version 1) wird nicht mehr gepflegt; `version:` in der Datei ist veraltet.

## Was bedeutet Exit-Code 137?

- Der Prozess wurde hart beendet: `docker kill` oder Speicherlimit überschritten.
- `docker inspect` zeigt `OOMKilled: true` beim Speicherfall ([Lab 7.1](../m07-debugging/l01-debugging/l01-debugging-thx.md)).

## `toomanyrequests` beim Pull?

- Download-Grenze von Docker Hub erreicht.
- `docker login` mit kostenlosem Konto verdoppelt die Grenze.

## Wie räume ich Speicherplatz auf?

- `docker system df` zeigt den Verbrauch.
- `docker image prune`, `docker builder prune` entfernen Unbenutztes; Volumes nur gezielt löschen.

## Brauche ich Swarm oder Kubernetes?

- Ein Server: Compose reicht.
- Wenige Server, einfache Bedienung: Swarm; großer Betrieb, viele Teams: Kubernetes ([Lab 10.2](../m10-orchestration/l02-swarm-vs-kubernetes/l02-swarm-vs-kubernetes-thx.md)).

## Wie stelle ich einen Lab-Stand wieder her?

- Im Ordner `project/`: `cp -r examples/<modul>/<lab>/. playground/`.
- Fehlende Images: `bash build-images.sh`.
