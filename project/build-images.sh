#!/usr/bin/env bash
# Baut die Hello-Images frontend:v1, frontend:v2 und backend:v1 aus den Beispielständen von Lab 3.2.
# Nutzen: wenn Images fehlen (neuer Rechner, nach docker system prune).
# Aufruf aus dem Ordner project/:  bash build-images.sh
set -euo pipefail
cd "$(dirname "$0")"

SRC=playground/hello                                  # Quellcode der App
D=examples/m03-images-registries/l02-own-images/hello # Dockerfiles aus Lab 3.2

docker build -t backend:v1  -f $D/backend/Dockerfile  $SRC/backend
docker build -t frontend:v1 -f $D/frontend/Dockerfile --build-arg APP_VERSION=1.0.0 $SRC/frontend
docker build -t frontend:v2 -f $D/frontend/Dockerfile --build-arg APP_VERSION=2.0.0 $SRC/frontend

docker images --filter "reference=frontend" --filter "reference=backend"
