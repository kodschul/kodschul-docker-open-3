# Hello-Frontend (Lab 3.2, Aufgabe 3)
# Basisimage: Python 3.13 auf Alpine Linux (klein, offiziell gepflegt)
FROM python:3.13-alpine

RUN apk add --no-cache curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# TODO 1: Build-Argument APP_VERSION mit Standardwert 0.0.0 anlegen (ARG)

# TODO 2: Umgebungsvariable APP_DISPLAY_VERSION auf $APP_VERSION setzen (ENV);
#         frontend.py zeigt diesen Wert an

# TODO 3: beim Bauen die Zeile "Last version updated: <Version>" in die Datei version.info schreiben (RUN echo ...)

# TODO 4: restlichen Code kopieren (COPY . .)

# TODO 5: Port 80 dokumentieren (EXPOSE) und Startbefehl python frontend.py festlegen (CMD in Listenform)
