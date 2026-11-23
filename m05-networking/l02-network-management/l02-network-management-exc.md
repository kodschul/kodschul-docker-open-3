# Lab 5.2 – Übung: Erstellen und Verwalten von Docker-Netzwerken

**Dauer:** ca. 25 Minuten (Live-Coding zum Mitmachen)
**Ändert die Hello-App-Projektbasis?** Nein — die Übung arbeitet mit busybox- und nginx-Containern; am Ende werden alle Container und Netzwerke entfernt.

## Vorbereitung

- Terminal mit der Kurs-Shell `bash` ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)); ein beliebiger Ordner genügt.
- Die Hello-App darf weiterlaufen; sie stört nicht.
- Keine Reste aus einem früheren Versuch: `docker rm -f container1 container2 web-host fix` und `docker network rm demo-network lab-net` (Fehlermeldungen „No such …" sind in Ordnung).
- Die Container `container1` und `container2` führen nur `sleep 3600` aus: Sie laufen eine Stunde lang und dienen als Gegenstellen für `ping`. Befehle darin startet `docker exec`.

## Aufgaben

1. Erstelle das Bridge-Netzwerk `demo-network` mit `docker network create demo-network` und prüfe mit `docker network inspect demo-network`, dass noch kein Container darin ist.
2. Starte `container1` im Netzwerk `demo-network` und `container2` ohne Netzwerkangabe:
   `docker run -d --name container1 --network demo-network busybox:1.37 sleep 3600`
   `docker run -d --name container2 busybox:1.37 sleep 3600`
   Pinge danach `container2` von `container1` aus an: `docker exec container1 ping -c 3 container2`.
3. Füge `container2` mit `docker network connect demo-network container2` zum Netzwerk hinzu, wiederhole den Ping aus Aufgabe 2 und zeige mit `docker network inspect demo-network` beide Container an.
4. Starte nginx im Host-Netzwerk mit `docker run -d --name web-host --network host nginx:1.30-alpine` und prüfe die Verbindung mit `curl http://localhost:80`. Unter Docker Desktop prüfe zusätzlich mit `docker run --rm --network host busybox:1.37 wget -qO- http://localhost:80`. Entferne `web-host` danach. Starte anschließend einen Container ohne Netzwerk und teste die Verbindung: `docker run --rm --network none busybox:1.37 ping -c 2 8.8.8.8`.
5. Entferne `container2` mit `docker network disconnect demo-network container2` aus dem Netzwerk und wiederhole den Ping. Lege danach das Netzwerk `lab-net` mit `--subnet 172.30.0.0/24` an, starte darin den Container `fix` mit `--ip 172.30.0.10` (Image und `sleep` wie in Aufgabe 2) und prüfe die Adresse mit `docker network inspect lab-net`. Räume zum Schluss alle Container und beide Netzwerke auf.

## Checkpoint

- Aufgabe 1 gibt eine lange Netzwerk-ID aus; `inspect` zeigt `"Containers": {}`.
- Aufgabe 2: `ping: bad address 'container2'`.
- Aufgabe 3: drei Antworten `64 bytes from 172.x.x.x`, `0% packet loss`; `inspect` listet `container1` und `container2`.
- Aufgabe 4: unter Linux liefert `curl` „Welcome to nginx!"; unter Docker Desktop scheitert `curl` (ohne Host-Networking in den Settings), der zweite Host-Netzwerk-Container liefert die nginx-Seite. Der Container ohne Netzwerk meldet `Network is unreachable`.
- Aufgabe 5: nach `disconnect` wieder `bad address 'container2'`; `inspect lab-net` zeigt `"Subnet": "172.30.0.0/24"` und `fix` mit `172.30.0.10/24`.

## Abschlusskriterien

- Alle Schritte der Live-Demo sind im eigenen Terminal nachvollzogen und die Ergebnisse entsprechen dem Checkpoint.
- `docker ps -a` zeigt weder `container1`, `container2`, `web-host` noch `fix`; `docker network ls` zeigt weder `demo-network` noch `lab-net`.

## Fallback

- `curl` fehlt unter Windows in einem anderen Terminal als Git Bash: Git Bash nutzen oder im Browser `http://localhost` öffnen.
- Port 80 unter Linux belegt (nginx startet nicht, `docker logs web-host` zeigt `Address in use`): Aufgabe 4 nur mit dem `--network none`-Teil durchführen und das Host-Netzwerk in der Lösung nachlesen.
- `toomanyrequests` beim Laden von `busybox` oder `nginx`: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
