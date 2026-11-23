# Lab 8.1 – Lösung: Eigene Docker-Repositories erstellen und verwalten

Fertige Datei: `project/examples/m08-repositories/l01-own-repositories/registry/compose.yml`. Wiederherstellen im Ordner `project/`:

```bash
mkdir -p playground/registry
cp examples/m08-repositories/l01-own-repositories/registry/compose.yml playground/registry/
```

## Aufgabe 1: Registry mit Compose und Volume

```bash
docker rm -f registry
```

```text
registry
```

Meldet der Befehl `No such container: registry`, lief kein alter Container; das ist kein Fehler.

`playground/registry/compose.yml`:

```yaml
services:
  registry:
    image: registry:3
    ports:
      - "5001:5000"
    volumes:
      - registry-data:/var/lib/registry   # TODO 1
    restart: unless-stopped               # TODO 2

volumes:
  registry-data:                          # TODO 3
```

```bash
cd project/playground/registry
docker compose up -d
docker compose ps
```

```text
NAME                  IMAGE        COMMAND                  SERVICE    CREATED         STATUS         PORTS
registry-registry-1   registry:3   "/entrypoint.sh /etc…"   registry   3 seconds ago   Up 2 seconds   0.0.0.0:5001->5000/tcp, [::]:5001->5000/tcp
```

Ohne TODO 3 bricht Compose mit `service "registry" refers to undefined volume registry-data` ab.

## Aufgabe 2: Taggen und pushen

```bash
docker tag frontend:v1 127.0.0.1:5001/frontend:1.0.0
docker tag frontend:v2 127.0.0.1:5001/frontend:2.0.0
docker tag frontend:v2 127.0.0.1:5001/frontend:latest
docker tag backend:v1  127.0.0.1:5001/backend:1.0.0
docker tag backend:v1  127.0.0.1:5001/backend:latest

docker push --all-tags 127.0.0.1:5001/frontend
docker push --all-tags 127.0.0.1:5001/backend
```

```text
The push refers to repository [127.0.0.1:5001/frontend]
…
1.0.0: digest: sha256:cbf0f67e… size: 856
2.0.0: digest: sha256:6b7c18db… size: 856
latest: digest: sha256:6b7c18db… size: 856
```

`2.0.0` und `latest` haben denselben Digest: Es ist dasselbe Image unter zwei Namen. Schichten, die schon in der Registry liegen (z. B. `python:3.13-alpine`), meldet der Push als `Layer already exists` und lädt sie nicht erneut hoch. Einzeln geht es ebenso: `docker push 127.0.0.1:5001/frontend:1.0.0` usw.

```bash
curl -s http://localhost:5001/v2/_catalog; echo
curl -s http://localhost:5001/v2/frontend/tags/list; echo
curl -s http://localhost:5001/v2/backend/tags/list; echo
```

```text
{"repositories":["backend","frontend"]}
{"name":"frontend","tags":["1.0.0","2.0.0","latest"]}
{"name":"backend","tags":["1.0.0","latest"]}
```

Hat Lab 3.3 bereits in eine Registry ohne Volume gepusht, ist davon nichts mehr übrig: Der Container `registry` wurde gelöscht, mit ihm seine Daten.

## Aufgabe 3: Neustart, Images bleiben

```bash
docker compose down
docker compose up -d
curl -s http://localhost:5001/v2/_catalog; echo     # direkt nach dem Start evtl. leer: einige Sekunden warten
```

```text
 Container registry-registry-1 Removed
 Network registry_default Removed
 …
 Container registry-registry-1 Started
{"repositories":["backend","frontend"]}
```

`docker compose down` löscht Container und Netzwerk, das Volume `registry_registry-data` bleibt. Erst `docker compose down -v` würde es mitlöschen.

```bash
docker rmi 127.0.0.1:5001/frontend:1.0.0
docker pull 127.0.0.1:5001/frontend:1.0.0
```

```text
Untagged: 127.0.0.1:5001/frontend:1.0.0
1.0.0: Pulling from frontend
Digest: sha256:cbf0f67e…
Status: Downloaded newer image for 127.0.0.1:5001/frontend:1.0.0
127.0.0.1:5001/frontend:1.0.0
```

`docker rmi` entfernt nur den Namen; die Schichten bleiben, solange `frontend:v1` darauf zeigt. Daher lädt der Pull kaum Daten, holt den Namen aber aus der Registry zurück.

## Aufgabe 4: Privates Repository und Zugangstoken

Repository anlegen auf [hub.docker.com](https://hub.docker.com):

1. **My Hub > Repositories > Create repository**
2. Namespace: eigene Docker-ID; Repository Name: `hello-frontend`; Visibility: **Private**
3. **Create**

Token erzeugen auf [app.docker.com](https://app.docker.com): Avatar oben rechts > **Account settings > Personal access tokens > Generate new token**, Beschreibung `docker-kurs`, Ablauf z. B. 30 Tage, Rechte **Read & Write**, **Generate**, Token kopieren.

```bash
docker login --username <docker-id>
```

```text
Password:
Login Succeeded
```

Bei `Password:` den Token einfügen; die Eingabe bleibt unsichtbar. Der Token ersetzt die bisherige Anmeldung aus dem Setup.

## Aufgabe 5: Push in das private Repository

```bash
docker tag frontend:v2 <docker-id>/hello-frontend:2.0.0
docker push <docker-id>/hello-frontend:2.0.0
```

```text
The push refers to repository [docker.io/<docker-id>/hello-frontend]
…
2.0.0: digest: sha256:6b7c18db… size: 856
```

Der Digest ist derselbe wie in der eigenen Registry: Das Image ist identisch, nur der Speicherort unterscheidet sich. Docker Hub zeigt unter **My Hub > Repositories** das Repository `hello-frontend` mit dem Hinweis **Private** und im Reiter **Tags** den Tag `2.0.0`. Ohne Anmeldung lässt sich das Image nicht ziehen; andere Konten erhalten `pull access denied`.

## Erweiterung: Digest von latest und 2.0.0

```bash
for t in 2.0.0 latest; do
  curl -sI -H "Accept: application/vnd.oci.image.index.v1+json" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
    http://localhost:5001/v2/frontend/manifests/$t | grep -i docker-content-digest
done
```

```text
Docker-Content-Digest: sha256:6b7c18db…
Docker-Content-Digest: sha256:6b7c18db…
```

Nach `docker tag frontend:v1 127.0.0.1:5001/frontend:latest` und `docker push 127.0.0.1:5001/frontend:latest` zeigt `latest` den Digest von `1.0.0` (`sha256:cbf0f67e…`): Derselbe Tag meint jetzt ein anderes Image. Wiederherstellen:

```bash
docker tag frontend:v2 127.0.0.1:5001/frontend:latest
docker push 127.0.0.1:5001/frontend:latest
```

Die gekürzten Digests (`cbf0f67e…`, `6b7c18db…`) stammen aus einem Testlauf; im eigenen Terminal stehen andere Werte, weil jedes selbst gebaute Image einen eigenen Digest hat.
