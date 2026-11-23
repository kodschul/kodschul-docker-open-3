# Wetter-App (Lab 3.2)
# Basisimage: Python 3.13 auf Alpine Linux (klein, offiziell gepflegt)
FROM python:3.13-alpine

# Arbeitsordner im Image; COPY und CMD beziehen sich darauf
WORKDIR /app

# Skript vom Rechner ins Image kopieren
COPY weather.py .

# Startbefehl (Listenform): läuft bei jedem docker run
CMD ["python", "weather.py"]
