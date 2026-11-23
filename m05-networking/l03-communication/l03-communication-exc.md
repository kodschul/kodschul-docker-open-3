# Lab 5.3 – Übung: Kommunikation zwischen Containern

**Dauer:** ca. 15 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — die Hello-App läuft vorübergehend ohne Compose im Netzwerk `hello-net` (gleiche Images, keine Dateiänderung); am Ende läuft sie wieder mit `docker compose up -d`.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)), Ordner `project/playground/hello`.
- Die Images `frontend:v2` und `backend:v1` sind vorhanden (`docker images`); sonst im Ordner `project/` `bash build-images.sh`.
- Keine Reste aus einem früheren Versuch: `docker rm -f kueche lieferung backend frontend` und `docker network rm pizza-network hello-net` (Meldungen „No such …" sind in Ordnung).

## Aufgaben

1. Erstelle das Netzwerk `pizza-network` mit dem Treiber `bridge`: `docker network create --driver bridge pizza-network`.
2. Starte zwei Container im `pizza-network`: `kueche` für die „Küche" und `lieferung` für die „Lieferung", beide aus `busybox:1.37` mit dem Befehl `sleep 3600` (wie in Lab 5.2).
3. Teste die Kommunikation in beide Richtungen per Namen: `docker exec kueche ping -c 2 lieferung` und `docker exec lieferung ping -c 2 kueche`.
4. Stoppe die Compose-Version der Hello-App mit `docker compose down`. Erstelle das Netzwerk `hello-net`, starte darin das Backend mit `--name backend` ohne Port aus `backend:v1` und das Frontend mit `--name frontend` und `-p 8080:80` aus `frontend:v2`. Öffne `http://localhost:8080`.
5. Prüfe die Ports beider Container mit `docker port frontend` und `docker port backend`. Räume danach alles auf (Container `kueche`, `lieferung`, `frontend`, `backend`, Netzwerke `pizza-network`, `hello-net`) und starte die Hello-App wieder mit `docker compose up -d`.

## Checkpoint

- `docker network inspect pizza-network` zeigt `"Driver": "bridge"` und die Container `kueche` und `lieferung`.
- Beide Pings: `2 packets transmitted, 2 packets received, 0% packet loss`.
- Die Hello-Seite auf Port 8080 zeigt „Hello World 2.0.0" und unter **Backend** eine Antwort mit Container-ID, IP und Uhrzeit (kein „Backend nicht erreichbar").
- `docker port frontend` zeigt `80/tcp -> 0.0.0.0:8080`; `docker port backend` gibt nichts aus.

## Abschlusskriterien

- Ping per Name zwischen „Küche" und „Lieferung" klappt.
- Die Hello-App lief ohne Compose: nur das Frontend mit veröffentlichtem Port, das Backend per Name im Netzwerk erreicht.
- Am Ende läuft die Hello-App wieder mit Compose (`docker compose ps` zeigt beide Dienste), `pizza-network` und `hello-net` sind gelöscht.

## Erweiterung

Starte einen Container mit dem Namen `secret-lab`, diesmal ohne Netzwerk (`--network none`), und versuche, von `secret-lab` aus `kodschul.com` anzupingen. Wiederhole den Ping mit einem Container ohne `--network`-Angabe.

## Fallback

- Port 8080 belegt, obwohl Compose gestoppt ist: mit `docker ps` den belegenden Container suchen und stoppen oder das Frontend mit `-p 8090:80` starten und `http://localhost:8090` öffnen.
- `ping` meldet keine Antwort aus dem Internet (Erweiterung): Firmennetze blockieren Ping oft; dann zählt nur die Meldung `bad address` des Containers ohne Netzwerk.
