# Basisimage: Python 3.13 auf Alpine Linux (klein, offiziell gepflegt)
FROM python:3.13-alpine

# curl für Tests aus dem Container heraus (wie im Backend)
RUN apk add --no-cache curl

# Arbeitsordner im Image; alle folgenden Pfade beziehen sich darauf
WORKDIR /app

# Erst die Abhängigkeiten: diese Schicht bleibt im Cache, solange requirements.txt gleich bleibt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build-Argument: nur beim Bauen vorhanden, z. B. docker build --build-arg APP_VERSION=2.0.0
ARG APP_VERSION=0.0.0
# Umgebungsvariable: bleibt im Image und ist zur Laufzeit lesbar (frontend.py zeigt sie an)
ENV APP_DISPLAY_VERSION=$APP_VERSION

# Schreibt die Version beim Bauen in eine Datei im Image
RUN echo "Last version updated: $APP_VERSION" > version.info

# Danach den Code (ändert sich oft)
COPY . .

# Dokumentiert den Port, auf dem die App lauscht
EXPOSE 80

# Startbefehl des Containers
CMD ["python", "frontend.py"]
