# Glossar

| Begriff | Bedeutung | Lab |
| --- | --- | --- |
| Basisimage | Image, auf dem ein eigenes Image aufbaut (`FROM`) | 3.1 |
| Bind Mount | Ordner des Rechners im Container sichtbar machen | 2.2 |
| Bridge-Netzwerk | virtueller Switch für Container auf einem Host | 5.1 |
| Build-Argument (`ARG`) | Wert, der nur beim Bauen existiert | 3.2 |
| Build-Kontext | Ordner, den `docker build` an Docker übergibt | 3.2 |
| cAdvisor | sammelt CPU- und Speicherwerte je Container | 7.2 |
| Cgroups | Kernel-Funktion, die Ressourcen begrenzt | 6.2 |
| `CMD` | Standard-Startbefehl eines Images | 3.2 |
| Compose | Werkzeug für Mehr-Container-Anwendungen aus einer YAML-Datei | 4.1 |
| Compose Watch | baut oder synchronisiert bei Dateiänderung automatisch | 4.2 |
| Container | laufende, abgeschirmte Instanz eines Images | 1.1 |
| containerd | Laufzeit unter Docker, die Container verwaltet | 1.3 |
| CVE | öffentlich gelistete Sicherheitslücke | 6.3 |
| Daemon (`dockerd`) | Hintergrunddienst, der Container baut und startet | 1.3 |
| Digest | unveränderliche Prüfsumme eines Images (`sha256:…`) | 3.3 |
| Docker Desktop | Docker mit Linux-VM und Oberfläche für macOS und Windows | 1.3 |
| Docker Hub | öffentliche Registry von Docker | 1.3 |
| Docker Scout | Schwachstellen-Analyse für Images | 6.3 |
| Dockerfile | Bauanleitung für ein Image | 3.1 |
| `ENTRYPOINT` | fester Startbefehl; `CMD` liefert dann Argumente | 3.2 |
| `env_file` | Datei mit Umgebungsvariablen für einen Compose-Dienst | 4.1 |
| Exit-Code | Rückgabewert beim Ende; 137 = vom Kernel beendet | 2.1 |
| Grafana | Oberfläche für Dashboards aus Metriken | 7.2 |
| Healthcheck | regelmäßige Prüfung, ob ein Container antwortet | 4.2 |
| Host | Rechner, auf dem Container laufen | 1.1 |
| Image | unveränderliche Vorlage für Container | 1.1 |
| Kernel | Kern des Betriebssystems; Container teilen ihn | 1.2 |
| Layer | Schicht eines Images, entsteht je Dockerfile-Anweisung | 3.1 |
| Manager-Node | steuert im Swarm, wo Tasks laufen | 10.1 |
| Microservice | kleiner, eigenständig auslieferbarer Dienst | 4.4 |
| Multistage-Build | mehrere `FROM`-Stufen, nur das Ergebnis kommt ins Image | 9.3 |
| Named Volume | von Docker verwalteter Datenspeicher mit Namen | 4.3 |
| Namespaces | Kernel-Funktion, die Prozesse voneinander abschirmt | 6.2 |
| OCI | offener Standard für Images und Container-Laufzeit | 2.3 |
| OOMKilled | Container wegen Speicherüberschreitung beendet | 6.2 |
| Overlay-Netzwerk | Netzwerk über mehrere Docker-Hosts (Swarm) | 5.1 |
| Podman | Container-Werkzeug ohne Daemon, Befehle wie Docker | 2.3 |
| Port-Veröffentlichung (`-p`) | Rechner-Port auf Container-Port weiterleiten | 2.1 |
| Projektnetzwerk | Netzwerk, das Compose je Projekt anlegt | 5.1 |
| Prometheus | sammelt und speichert Metriken | 7.2 |
| Registry | Server, der Images speichert und ausliefert | 3.3 |
| Replika | eine von mehreren gleichen Kopien eines Dienstes | 4.2 |
| Repository | Sammlung von Image-Versionen unter einem Namen | 8.1 |
| Restart-Policy | Regel, wann Docker einen Container neu startet | 4.2 |
| Reverse Proxy | nimmt Anfragen an und leitet sie an Dienste weiter | 9.1 |
| Rolling Update | Tasks nacheinander auf die neue Version tauschen | 10.3 |
| Routing Mesh | jeder Swarm-Node nimmt Anfragen für einen Port an | 10.1 |
| Service (Swarm) | gewünschter Zustand: Image, Replikas, Ports | 10.1 |
| Stack | mehrere Swarm-Services aus einer Compose-Datei | 10.3 |
| Swarm | in Docker eingebaute Orchestrierung für mehrere Hosts | 10.1 |
| Tag | Versionsname eines Images, z. B. `v2` | 3.3 |
| Task | ein Container eines Swarm-Service | 10.1 |
| Traefik | Reverse Proxy, der Docker-Container selbst erkennt | 9.1 |
| Union Filesystem | legt Layer zu einem Dateisystem übereinander | 3.1 |
| virtuelle Maschine | nachgebildeter Rechner mit eigenem Betriebssystem | 1.2 |
| Volume | Speicher außerhalb der Container-Schicht | 4.3 |
| WSL 2 | Linux-Unterbau unter Windows für Docker Desktop | 1.3 |
