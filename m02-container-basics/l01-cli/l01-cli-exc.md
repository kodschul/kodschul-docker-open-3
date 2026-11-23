# Lab 2.1 – Übung: Container über die CLI steuern

**Dauer:** ca. 20 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die Übung nutzt nginx-Container; `webserver` bleibt für Lab 2.2 stehen, die übrigen Container werden gelöscht.

## Vorbereitung

- Docker Desktop läuft (`Engine running`), Terminal in der Kurs-Shell `bash` ist offen ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)).
- Ports 8080, 8081 und 8082 sind frei; `docker ps` listet keinen Container mit diesen Ports.
- Starter und Arbeitsdatei: keine, alle Schritte sind Befehle.

## Aufgaben

1. Lade das Image `nginx:1.30-alpine` mit `docker pull` und prüfe es mit `docker images`.
2. Starte daraus im Hintergrund den Container `webserver` mit Port 8080 des Rechners auf Port 80 im Container, öffne `http://localhost:8080` im Browser und zeige den Container mit `docker ps` an.
3. Starte zwei weitere nginx-Container `container1` und `container2`, beide mit `-p 8081:80`. Behebe den Fehler beim zweiten Container: Lösche ihn und starte ihn mit Port 8082 neu. Zeige danach die laufenden Container an.
4. Beende `container1` mit `docker stop` und `container2` mit `docker kill`. Vergleiche die Ausgabe von `docker ps` und `docker ps -a`.
5. Lösche `container1` und `container2` mit `docker rm` und prüfe mit `docker ps -a`, dass nur `webserver` übrig ist.

## Checkpoint

- Der Browser zeigt unter `http://localhost:8080` „Welcome to nginx!".
- Aufgabe 3: Der erste Versuch für `container2` meldet `port is already allocated`; danach zeigt `docker ps` drei Container mit den Ports 8080, 8081 und 8082.
- Aufgabe 4: `docker ps` listet nur noch `webserver`; `docker ps -a` zeigt `container1` mit `Exited (0)` und `container2` mit `Exited (137)`.

## Abschlusskriterien

- `webserver` läuft auf Port 8080; `container1` und `container2` sind gelöscht.
- Erklärt: warum zwei Container nicht denselben Port des Rechners nutzen können, und warum sich die Exit-Codes von `stop` und `kill` unterscheiden.

## Fallback

- Port 8080 belegt (z. B. durch ein anderes Programm): einen freien Port wie 8090 wählen und im Browser entsprechend aufrufen.
- `toomanyrequests` beim Download: `docker login` ([Setup](../../00-setup-and-installation.md#docker-hub-limit-und-docker-login)).
