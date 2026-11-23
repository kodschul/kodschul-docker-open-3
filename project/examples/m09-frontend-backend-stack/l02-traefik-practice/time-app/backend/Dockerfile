FROM python:3.13-alpine
WORKDIR /code
# flask run liest die App aus FLASK_APP und lauscht auf FLASK_RUN_HOST (0.0.0.0 = alle Adressen im Container)
ENV FLASK_APP=backend.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Port des Flask-Servers; Traefik nimmt den ersten freigegebenen Port des Containers
EXPOSE 5000
COPY . .
# Entwicklungsserver mit Debug-Modus (wie im Live-Coding); für den Produktivbetrieb ungeeignet
CMD ["flask", "run", "--debug"]
