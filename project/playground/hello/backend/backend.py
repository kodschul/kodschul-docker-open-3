"""Hello-Backend: antwortet mit JSON (Container-Name, IP-Adressen, Uhrzeit)."""

import socket
from datetime import datetime

from flask import Flask

hostname = socket.gethostname()                    # im Container: die Container-ID (kurz)
ips = socket.gethostbyname_ex(hostname)[2]         # alle IP-Adressen des Containers

app = Flask(__name__)


@app.route("/")
def index():
    return {"hostname": hostname, "ip": ips, "now": datetime.now().strftime("%H:%M:%S")}


if __name__ == "__main__":
    print("Hello-Backend auf Port 80", flush=True)
    app.run(host="0.0.0.0", port=80)
