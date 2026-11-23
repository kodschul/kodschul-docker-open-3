#!/usr/bin/env bash
# Lokale Registry (Lab 3.3): starten, Images taggen und pushen, Inhalt lesen, Image ziehen und starten.
# Voraussetzung: Images frontend:v1 (Lab 3.2) und recipe-page:1.0.0 (Lab 3.3, Aufgabe 1) sind gebaut.
# Aufruf aus dem Ordner project/playground/registry:  bash registry.sh
set -euo pipefail

REG=127.0.0.1:5001   # Adresse der Registry; Port 5001, weil macOS Port 5000 selbst belegt (AirPlay)

# 1. Registry starten: Image registry:3, im Container Port 5000, auf dem Rechner Port 5001
docker rm -f registry 2>/dev/null || true
docker run -d -p 5001:5000 --name registry registry:3
sleep 2   # kurz warten, bis die Registry antwortet

# 2. Images mit der Registry-Adresse taggen (neuer Name, gleiches Image) und pushen
docker tag frontend:v1 $REG/frontend:v1
docker push $REG/frontend:v1

docker tag recipe-page:1.0.0 $REG/recipe-page:1.0.0
docker push $REG/recipe-page:1.0.0

# 3. Inhalt der Registry abfragen; dieselben Adressen funktionieren im Browser:
#    http://localhost:5001/v2/_catalog
#    http://localhost:5001/v2/<image-name>/tags/list
curl -s http://localhost:5001/v2/_catalog; echo
curl -s http://localhost:5001/v2/frontend/tags/list; echo
curl -s http://localhost:5001/v2/recipe-page/tags/list; echo

# 4. Lokale Kopien der Rezeptseite löschen (Container und beide Namen), danach aus der Registry ziehen
docker rm -f recipe-page 2>/dev/null || true
docker rmi recipe-page:1.0.0 $REG/recipe-page:1.0.0
docker pull $REG/recipe-page:1.0.0

# 5. Gezogene Images starten: Rezeptseite auf Port 8081, Hello-Frontend auf Port 8080
docker run -d --name recipe-page -p 8081:80 $REG/recipe-page:1.0.0

docker pull $REG/frontend:v1
docker rm -f hello-frontend 2>/dev/null || true
docker run -d --name hello-frontend -p 8080:80 $REG/frontend:v1

docker ps --filter name=registry --filter name=recipe-page --filter name=hello-frontend
