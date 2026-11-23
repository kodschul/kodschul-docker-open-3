# Lab 2.2 – Übung: Verwaltung und Inspektion von Containern

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Nein — die App bleibt unverändert; nur `test.txt` im Ordner `project/playground/hello` bekommt eine zusätzliche Zeile.

## Vorbereitung

- Docker Desktop läuft (`Engine running`), Terminal in der Kurs-Shell `bash` ist offen ([Setup](../../00-setup-and-installation.md#kurs-shell-bash)). Windows: interaktive Befehle (`-it`) im Terminal von VS Code ausführen oder `winpty` voranstellen.
- Der Container `webserver` aus Lab 2.1 läuft (`docker ps`). Falls nicht: `docker run -d --name webserver -p 8080:80 nginx:1.30-alpine`.
- Arbeitsordner: `project/playground/hello` der Kursdateien ([Setup](../../00-setup-and-installation.md#kursdateien-holen)); Arbeitsdatei: `test.txt`.

## Aufgaben

1. Starte mit `docker run -it --name kaputt busybox:1.37` einen Container mit Shell. Probiere darin `ls`, `cat /etc/hostname` und `uptime` aus. Führe danach `rm -rf /bin` aus, probiere die drei Befehle erneut und verlasse den Container mit `exit`.
2. Starte den Container `kaputt` mit `docker start -ai kaputt` erneut. Starte danach mit `docker run -it --rm busybox:1.37` einen neuen Container und teste darin `ls`. Verlasse ihn mit `exit`.
3. Wechsle in den Ordner `project/playground/hello` und zeige `test.txt` an. Binde den Ordner mit `-v .:/hello` in einen neuen Busybox-Container ein, hänge darin mit `echo "modified by Docker Container!" >> /hello/test.txt` eine Zeile an, verlasse den Container und zeige `test.txt` auf dem Rechner erneut an.
4. Zeige mit `docker exec` den Inhalt von `/usr/share/nginx/html` im Container `webserver`. Kopiere `index.html` von dort mit `docker cp` auf den Rechner, ändere im Editor die Überschrift „Welcome to nginx!" in „Hallo aus dem Kurs!", kopiere die Datei zurück und lade `http://localhost:8080` neu. Lies danach mit `docker logs --tail 3 webserver` die letzten Anfragen.
5. Räume auf: Entferne die Container `webserver` und `kaputt` mit `docker rm -f` und lösche die kopierte `index.html` im Ordner `hello`.

## Checkpoint

- Aufgabe 1: Nach `rm -rf /bin` meldet jeder Befehl `sh: ls: not found` bzw. `sh: uptime: not found`.
- Aufgabe 2: `docker start -ai kaputt` scheitert mit `exec: "sh": executable file not found in $PATH`; im neuen Container funktioniert `ls` wieder.
- Aufgabe 3: `test.txt` auf dem Rechner enthält nach dem Container zusätzlich die Zeile `modified by Docker Container!`.
- Aufgabe 4: Der Browser zeigt „Hallo aus dem Kurs!"; `docker logs` zeigt den neuen Aufruf mit `"GET / HTTP/1.1" 200`.
- Aufgabe 5: `docker ps -a` listet weder `webserver` noch `kaputt`.

## Abschlusskriterien

- Erklärt: Warum der Container `kaputt` nicht mehr startet, ein neuer Container aus demselben Image aber schon.
- Erklärt: Warum die Änderung an `test.txt` nach dem Ende des Containers erhalten bleibt, die Änderung an `index.html` im Container aber nicht.

## Fallback

- `the input device is not a TTY` (Git Bash): `winpty docker run -it …` oder das Terminal in VS Code nutzen.
- `/hello` ist im Container leer: Befehl nicht im Ordner `project/playground/hello` gestartet; mit `pwd` prüfen.
- Kein Editor zur Hand für Aufgabe 4: die Zeile in `index.html` mit einem beliebigen Texteditor (VS Code, TextEdit, Notepad) ändern; wichtig ist nur, dass die Datei danach wieder `index.html` heißt.
