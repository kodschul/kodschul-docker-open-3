# Basisimage: Python 3.13 auf Alpine Linux (klein, offiziell gepflegt)
FROM python:3.13-alpine

# curl wird für den Healthcheck gebraucht (ab Lab 4.2)
RUN apk add --no-cache curl

# Arbeitsordner im Image; alle folgenden Pfade beziehen sich darauf
WORKDIR /app

# Erst die Abhängigkeiten: diese Schicht bleibt im Cache, solange requirements.txt gleich bleibt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Danach den Code (ändert sich oft)
COPY . .

# Dokumentiert den Port, auf dem die App lauscht
EXPOSE 80

# Startbefehl des Containers
CMD ["python", "backend.py"]
