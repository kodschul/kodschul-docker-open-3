# Cheatsheet: Repositories und Registries

Befehle aus Modul 8 (Labs 8.1–8.2) und aus Lab 3.3. Kurs-Shell `bash`; unter Windows Git Bash mit `MSYS_NO_PATHCONV=1`. `<docker-id>` = eigene Docker-ID.

## Image-Namen

| Name | Bedeutung |
| --- | --- |
| `nginx:1.30-alpine` | Docker Hub, offizielles Image (`docker.io/library/nginx:1.30-alpine`) |
| `<docker-id>/hello-frontend:2.0.0` | Docker Hub, Repository eines Kontos |
| `127.0.0.1:5001/frontend:2.0.0` | eigene Registry auf diesem Rechner, Port 5001 |
| `<name>@sha256:<digest>` | genau ein Image, unabhängig vom Tag |

## Eigene Registry mit Compose

```yaml
services:
  registry:
    image: registry:3
    ports:
      - "5001:5000"
    volumes:
      - registry-data:/var/lib/registry
    restart: unless-stopped
volumes:
  registry-data:
```

| Befehl | Wirkung |
| --- | --- |
| `docker rm -f registry` | Registry-Container aus Lab 3.3 entfernen (Port 5001 frei) |
| `docker compose up -d` (Ordner `registry`) | Registry starten |
| `docker compose down` | stoppen; Volume und Images bleiben |
| `docker compose down -v` | stoppen und Volume mit allen Images löschen |
| `curl -s http://localhost:5001/v2/_catalog` | alle Repositories der Registry |
| `curl -s http://localhost:5001/v2/frontend/tags/list` | alle Tags eines Repositorys |
| `curl -sI -H "Accept: application/vnd.oci.image.index.v1+json" -H "Accept: application/vnd.docker.distribution.manifest.v2+json" http://localhost:5001/v2/frontend/manifests/latest` | Digest eines Tags im Header `Docker-Content-Digest` |

## Taggen, pushen, ziehen

| Befehl | Wirkung |
| --- | --- |
| `docker tag frontend:v2 127.0.0.1:5001/frontend:2.0.0` | weiteren Namen für ein Image anlegen (keine Kopie) |
| `docker push 127.0.0.1:5001/frontend:2.0.0` | einen Tag hochladen |
| `docker push --all-tags 127.0.0.1:5001/frontend` | alle lokalen Tags eines Repositorys hochladen |
| `docker pull 127.0.0.1:5001/frontend:1.0.0` | Image aus der Registry ziehen |
| `docker rmi 127.0.0.1:5001/frontend:1.0.0` | lokalen Namen entfernen |
| `docker images --digests` | lokale Images mit Digest |

## Docker Hub

| Befehl / Pfad | Wirkung |
| --- | --- |
| hub.docker.com > **My Hub > Repositories > Create repository** | Repository anlegen, Sichtbarkeit Public oder Private |
| app.docker.com > Avatar > **Account settings > Personal access tokens > Generate new token** | Zugangstoken erzeugen (Rechte z. B. Read & Write) |
| `docker login --username <docker-id>` | anmelden; bei `Password:` den Token einfügen |
| `docker logout` | abmelden |
| `docker tag frontend:v2 <docker-id>/hello-frontend:2.0.0` | für Docker Hub taggen |
| `docker push <docker-id>/hello-frontend:2.0.0` | auf Docker Hub hochladen |

| Grenze (Gratis-Plan, Stand 11/2026) | Wert |
| --- | --- |
| private Repositories | 1 |
| Pulls ohne Anmeldung | 100 je 6 h je IP-Adresse |
| Pulls mit Konto | 200 je 6 h |

## Versionen

| Tag | Einsatz |
| --- | --- |
| `2.1.3` | genau diese Version (MAJOR.MINOR.PATCH) |
| `2.1` / `2` | jeweils neueste Fehlerkorrektur bzw. kompatible Version |
| `latest` | zuletzt so getaggt; wandert mit, nicht für Server |

## Signaturen

| Befehl | Wirkung |
| --- | --- |
| `cosign generate-key-pair` | Schlüsselpaar `cosign.key` / `cosign.pub` erzeugen (Programm cosign, Sigstore) |
| `cosign sign --key cosign.key <image>@sha256:<digest>` | Image signieren |
| `cosign verify --key cosign.pub <image>@sha256:<digest>` | Signatur prüfen |
| `export DOCKER_CONTENT_TRUST=1` | veraltet: Docker Content Trust, Dienst wird am 08.12.2026 abgeschaltet |

## Multi-Plattform und Compose aus der Registry

| Befehl | Wirkung |
| --- | --- |
| `docker version --format '{{.Server.Os}}/{{.Server.Arch}}'` | eigene Plattform |
| `docker buildx build --platform linux/amd64,linux/arm64 -t <docker-id>/hello-web:2.0.0 --push frontend` | für zwei Plattformen bauen und pushen |
| `docker buildx imagetools inspect <docker-id>/hello-web:2.0.0` | Plattformen eines Images in der Registry |
| `docker run --platform linux/amd64 <image>` | bestimmte Variante starten (fremde per Emulation) |
| `docker compose -f compose-registry.yml pull` | Images einer Compose-Datei aus der Registry holen |
| `docker compose -f compose-registry.yml up -d` | mit anderer Compose-Datei starten |
| `docker compose -f compose-registry.yml images` | Herkunft der Images je Container |

```yaml
# Compose auf Servern: image mit Registry und Version, kein build
services:
  frontend:
    image: 127.0.0.1:5001/frontend:2.0.0
  backend:
    image: 127.0.0.1:5001/backend:1.0.0
```

## CI/CD-Ablauf

| Schritt | typischer Befehl |
| --- | --- |
| bauen | `docker build -t $IMAGE .` |
| testen | `docker run -d -p 8080:80 $IMAGE` und `curl -f http://localhost:8080` |
| scannen | `docker scout cves --exit-code --only-severity critical,high $IMAGE` |
| pushen | `docker login …` und `docker push $IMAGE` |
| ausrollen | `docker compose pull` und `docker compose up -d` auf dem Server |
