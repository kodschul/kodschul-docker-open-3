# Basisimage: Python 3.13 auf Alpine Linux (klein, offiziell gepflegt)
FROM python:3.13-alpine

RUN apk add --no-cache curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Build-Argument: nur beim Bauen vorhanden, z. B. docker build --build-arg APP_VERSION=2.0.0
ARG APP_VERSION=0.0.0
# Umgebungsvariable: bleibt im Image und ist zur Laufzeit lesbar (frontend.py zeigt sie an)
ENV APP_DISPLAY_VERSION=$APP_VERSION

# Schreibt die Version beim Bauen in eine Datei im Image
RUN echo "Last version updated: $APP_VERSION" > version.info

COPY . .

EXPOSE 80

CMD ["python", "fronted.py"]
