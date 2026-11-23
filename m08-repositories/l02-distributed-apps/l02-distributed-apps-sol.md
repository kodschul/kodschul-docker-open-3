# Lab 8.2 – Lösung: Verteilte und containerisierte Anwendungen mit Docker

Fertige Datei: `project/examples/m08-repositories/l02-distributed-apps/hello/compose-registry.yml`. Wiederherstellen im Ordner `project/`:

```bash
cp examples/m08-repositories/l02-distributed-apps/hello/compose-registry.yml playground/hello/
```

## Aufgabe 1: Multi-Plattform-Build und Push

Repository auf Docker Hub: **My Hub > Repositories > Create repository**, Name `hello-web`, Visibility **Public**, **Create**. Öffentlich, damit die Partnerperson es ohne Rechte am eigenen Konto ziehen kann; das eine private Repository des Gratis-Plans ist mit `hello-frontend` aus Lab 8.1 belegt.

```bash
cd project/playground/hello
docker buildx build --platform linux/amd64,linux/arm64 --build-arg APP_VERSION=2.0.0 \
  -t <docker-id>/hello-web:2.0.0 --push frontend
```

```text
#14 [linux/amd64 2/7] RUN apk add --no-cache curl
#17 [linux/amd64 5/7] RUN pip install --no-cache-dir -r requirements.txt
#17 DONE 9.2s
…
#20 exporting manifest list sha256:aefab7c2… done
#20 naming to docker.io/<docker-id>/hello-web:2.0.0 done
#20 pushing layers 1.1s done
#20 pushing manifest for docker.io/<docker-id>/hello-web:2.0.0@sha256:aefab7c2… done
```

Jeder Schritt läuft zweimal, einmal je Plattform; Schritte der eigenen Plattform kommen meist aus dem Cache von Lab 3.2. Die fremde Plattform (auf einem Mac mit Apple Silicon `linux/amd64`, auf Intel/AMD `linux/arm64`) läuft über Emulation; im Test auf Apple Silicon dauerte der ganze Build knapp 20 Sekunden. `frontend` am Ende ist der Build-Kontext; das Dockerfile darin stammt aus Lab 3.2.

## Aufgabe 2: Plattformen anzeigen

```bash
docker buildx imagetools inspect <docker-id>/hello-web:2.0.0
```

```text
Name:      docker.io/<docker-id>/hello-web:2.0.0
MediaType: application/vnd.oci.image.index.v1+json
Digest:    sha256:aefab7c2…

Manifests:
  Name:        docker.io/<docker-id>/hello-web:2.0.0@sha256:f1a951ac…
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/amd64

  Name:        docker.io/<docker-id>/hello-web:2.0.0@sha256:73dff405…
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    linux/arm64

  Name:        docker.io/<docker-id>/hello-web:2.0.0@sha256:6d06ce21…
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.digest: sha256:f1a951ac…
    vnd.docker.reference.type:   attestation-manifest

  Name:        docker.io/<docker-id>/hello-web:2.0.0@sha256:164e7361…
  MediaType:   application/vnd.oci.image.manifest.v1+json
  Platform:    unknown/unknown
  Annotations:
    vnd.docker.reference.type:   attestation-manifest
    vnd.docker.reference.digest: sha256:73dff405…
```

Der Name zeigt auf eine **Manifest-Liste** (`image.index`) mit je einem Image pro Plattform. Die Einträge `unknown/unknown` sind Attestierungen (Angaben zur Herkunft des Builds), kein lauffähiges Image.

```bash
docker version --format '{{.Server.Os}}/{{.Server.Arch}}'
```

```text
linux/arm64
```

Auf einem Mac mit Apple Silicon `linux/arm64`, auf Intel/AMD-Rechnern (auch Windows) `linux/amd64`. Docker Desktop läuft immer als Linux-VM, daher `linux` auch unter macOS und Windows.

## Aufgabe 3: Image der Partnerperson starten

```bash
docker run -d --name partner-web -p 8090:80 <partner-id>/hello-web:2.0.0
```

```text
Unable to find image '<partner-id>/hello-web:2.0.0' locally
2.0.0: Pulling from <partner-id>/hello-web
…
Status: Downloaded newer image for <partner-id>/hello-web:2.0.0
45088fe520fc161e5c22b11c81ee0dd290f59132c3397725670ae7ab6e8e180a
```

`http://localhost:8090` zeigt „Hello World 2.0.0", die eigene Container-ID (`45088fe520fc`, gleich den ersten zwölf Zeichen in `docker ps`) und „Backend nicht erreichbar (http://backend:80): ConnectionError". Das ist erwartet: Gestartet ist nur das Frontend, ohne Backend und ohne gemeinsames Netzwerk. Docker hat automatisch die Variante für die eigene Plattform gezogen, auch wenn die Partnerperson einen anderen Prozessor hat.

## Aufgabe 4: Hello-App aus der Registry

`compose-registry.yml`:

```yaml
services:
  frontend:
    image: 127.0.0.1:5001/frontend:2.0.0   # TODO 1
    depends_on:
      backend:
        condition: service_healthy
    ports:
      - 8080:80
    volumes:
      - hello-data:/data

  backend:
    image: 127.0.0.1:5001/backend:1.0.0    # TODO 2
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 10s
      timeout: 2s
      retries: 2
      start_period: 3s

volumes:
  hello-data:
```

```bash
docker compose -f compose-registry.yml pull
docker compose -f compose-registry.yml up -d
docker compose -f compose-registry.yml images
```

```text
 Image 127.0.0.1:5001/backend:1.0.0 Pulled
 Image 127.0.0.1:5001/frontend:2.0.0 Pulled
 …
 Container hello-backend-1 Recreated
 Container hello-frontend-1 Recreated
 Container hello-backend-1 Healthy
 Container hello-frontend-1 Started

CONTAINER          REPOSITORY                TAG       PLATFORM      IMAGE ID       SIZE      CREATED
hello-backend-1    127.0.0.1:5001/backend    1.0.0     linux/arm64   8286084874f1   103MB     9 minutes ago
hello-frontend-1   127.0.0.1:5001/frontend   2.0.0     linux/arm64   6b7c18dbc0fa   108MB     9 minutes ago
```

`Recreated`: Projektname ist der Ordner `hello`, die Dienstnamen sind gleich, daher ersetzt Compose die Container aus `compose.yml`. Das Volume `hello-data` bleibt, der Zähler „Aufrufe in access.log" läuft weiter. `http://localhost:8080` zeigt „Hello World 2.0.0" mit Backend-Antwort. Auf einem zweiten Rechner reicht diese Datei allein, sobald dort statt `127.0.0.1:5001` eine erreichbare Registry eingetragen ist.

## Aufgabe 5: Hauptstand wiederherstellen

```bash
docker compose up -d
docker rm -f partner-web
```

```text
 Container hello-backend-1 Recreated
 Container hello-frontend-1 Recreated
 …
partner-web
```

`docker compose ps` zeigt wieder `frontend:v2` und `backend:v1` aus `compose.yml`.

## Erweiterung: andere Plattform starten

```bash
docker run --rm --platform linux/amd64 <partner-id>/hello-web:2.0.0 uname -m
docker run --rm --platform linux/arm64 <partner-id>/hello-web:2.0.0 uname -m
```

```text
x86_64
aarch64
```

`x86_64` ist die Bezeichnung des Linux-Kernels für `amd64`, `aarch64` die für `arm64`. Die fremde Variante startet über Emulation, merklich langsamer. Ohne Multi-Plattform-Build fehlt eine Variante, und `docker run` ohne `--platform` meldet auf dem anderen Prozessor `no matching manifest` oder läuft nur emuliert mit einer Warnung zur Plattform.
