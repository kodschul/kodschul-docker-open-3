# Beispiel eines Dockerfiles mit Schichten (Lab 3.1)
# Basis-Image: Ubuntu 24.04, fester Tag statt latest
FROM ubuntu:24.04

# Neue Schicht: Paketliste laden und Python installieren
RUN apt-get update && apt-get install -y python3

# Weitere Schicht: Anwendungscode hinzufügen
COPY app.py /app/app.py
