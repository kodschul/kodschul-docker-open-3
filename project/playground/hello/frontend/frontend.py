"""Hello-Frontend: HTML-Seite mit Version, Farbe, IP des Containers und Antwort des Backends.

Einstellungen über Umgebungsvariablen (Standardwert in Klammern):
  APP_DISPLAY_VERSION  angezeigte Version; im Dockerfile aus dem Build-Argument APP_VERSION gesetzt  (0.0.0)
  APP_COLOR            Hintergrundfarbe der Seite                                                 (yellow)
  BACKEND_URL          Adresse des Backends                                                       (http://backend:80)
  DATA_DIR             Ordner für access.log                                                      (/data)
"""

import os
import socket
from datetime import datetime

import requests
from flask import Flask

APP_VERSION = os.getenv("APP_DISPLAY_VERSION", "0.0.0")
APP_COLOR = os.getenv("APP_COLOR", "yellow")
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:80")
DATA_DIR = os.getenv("DATA_DIR", "/data")

hostname = socket.gethostname()                    # im Container: die Container-ID (kurz)
ips = socket.gethostbyname_ex(hostname)[2]         # alle IP-Adressen des Containers

app = Flask(__name__)


def write_access_log():
    """Hängt eine Zeile an DATA_DIR/access.log an und gibt die Anzahl der Zeilen zurück."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        path = os.path.join(DATA_DIR, "access.log")
        with open(path, "a") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {hostname} {APP_VERSION}\n")
        with open(path) as f:
            return sum(1 for _ in f)
    except OSError:
        return "nicht beschreibbar"                # z. B. Ordner gehört einem anderen Benutzer


def ask_backend():
    """Fragt das Backend; bei einem Fehler erscheint ein Hinweis statt eines Absturzes."""
    try:
        data = requests.get(BACKEND_URL, timeout=2).json()
        return f"{data['hostname']} ({', '.join(data['ip'])}) um {data['now']}"
    except Exception as e:
        return f"Backend nicht erreichbar ({BACKEND_URL}): {type(e).__name__}"


@app.route("/")
def index():
    visits = write_access_log()
    return f"""<!doctype html>
<html lang="de">
<head><meta charset="utf-8"><title>Hello-App {APP_VERSION}</title></head>
<body style="background:{APP_COLOR}; font-family:sans-serif; padding:2rem;">
  <h1>Hello World {APP_VERSION}</h1>
  <p><b>Frontend:</b> {hostname} ({', '.join(ips)})</p>
  <p><b>Backend:</b> {ask_backend()}</p>
  <p><b>Aufrufe in access.log:</b> {visits}</p>
</body>
</html>"""


if __name__ == "__main__":
    print(f"Hello-Frontend {APP_VERSION} auf Port 80", flush=True)
    app.run(host="0.0.0.0", port=80)
