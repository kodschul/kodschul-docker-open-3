# Lab 4.3 – Übung: Datenvolumes und Persistenz

**Dauer:** ca. 25 Minuten
**Ändert die Hello-App-Projektbasis?** Ja — `playground/hello/compose.yml` bekommt den Stand, mit dem die Hello-App ab jetzt läuft (ein Frontend auf Port 8080, Volume `hello-data`). Neu entsteht `playground/recipe-book/`.

## Vorbereitung

- Stand aus Lab 4.2 in `project/playground/hello/`; keine Hello-Container laufen (`docker compose down` im Ordner `playground/hello`). Fehlt der Stand, im Ordner `project/`:
  `cp -r examples/m03-images-registries/l02-own-images/. playground/ && cp -r examples/m04-compose/l02-multi-container/. playground/`
- Starter für das Rezeptbuch kopieren (im Ordner `project/`):
  `cp -r starters/m04-l03-recipe-book/. playground/`
  Arbeitsdateien: `playground/recipe-book/app/Dockerfile` und `playground/recipe-book/compose.yml` (beide mit `TODO`). `app/index.js` und `app/package.json` sind fertig: eine kleine API mit Express 5 und Mongoose 9, die Rezepte in MongoDB speichert (Port 3000, Endpunkte `GET /recipes` und `POST /recipes`).
- Port 3000 frei; Befehle der Aufgaben 1–4 laufen im Ordner `project/playground/recipe-book`, Aufgabe 5 in `project/playground/hello`.

## Aufgaben

1. Ergänze `app/Dockerfile` nach den `TODO`: Basisimage `node:24-alpine`, Arbeitsordner `/app`, erst `package.json` kopieren und `npm install --omit=dev` ausführen, dann den restlichen Code kopieren, Port 3000 dokumentieren, Start mit `node index.js`.
2. Ergänze `compose.yml` nach den `TODO`: Dienst `recipe-app` aus `./app` gebaut, Port 3000, startet nach `recipe-database`; Dienst `recipe-database` mit `mongo:8` und dem Named Volume `recipe-data` unter `/data/db`. Starte mit `docker compose up -d --build` und lies `docker compose logs recipe-app`.
3. Lege ein Rezept an und rufe alle Rezepte ab:

   ```bash
   curl -X POST http://localhost:3000/recipes -H "Content-Type: application/json" \
     -d '{"title":"Spaghetti Carbonara","ingredients":["Spaghetti","Eier","Speck","Parmesan"],"instructions":"Spaghetti kochen, Speck anbraten, mit Eiern und Käse mischen."}'
   curl http://localhost:3000/recipes
   ```

   Zeige danach das Volume mit `docker volume ls` und `docker volume inspect recipe-book_recipe-data` an.
4. Entferne die Container mit `docker compose down`, starte mit `docker compose up -d` neu und rufe die Rezepte erneut ab. Entferne danach alles mit `docker compose down -v`, starte noch einmal und rufe die Rezepte ab. Räume zum Schluss mit `docker compose down -v` auf.
5. Wechsle nach `playground/hello` und bringe `compose.yml` auf den Stand ab Lab 4.3: `deploy.replicas` entfernen, Port `8080:80`, Volume `hello-data` unter `/data` beim Frontend und `hello-data` unter `volumes:` auf oberster Ebene. Starte mit `docker compose up -d`, lade `http://localhost:8080` dreimal, führe `docker compose down` und `docker compose up -d` aus und lade die Seite erneut.

## Checkpoint

- Aufgabe 2: `docker compose ps` zeigt `recipe-book-recipe-app-1` und `recipe-book-recipe-database-1`; die Logs enthalten `Recipe Book App listening on port 3000` und `Mit MongoDB verbunden`.
- Aufgabe 3: `POST` antwortet mit dem Rezept samt `_id`; `GET` liefert eine Liste mit diesem Rezept; `docker volume ls` listet `recipe-book_recipe-data`.
- Aufgabe 4: Nach `down`/`up` ist das Rezept noch da; nach `down -v`/`up` liefert `GET` eine leere Liste `[]`.
- Aufgabe 5: „Aufrufe in access.log" zählt nach `down`/`up` weiter (z. B. 4 statt 1); `docker volume ls` listet `hello_hello-data`.

## Abschlusskriterien

- Das Rezeptbuch startet mit einem Befehl, und Rezepte überstehen `down`/`up`.
- `playground/hello/compose.yml` startet ein Frontend auf Port 8080 mit Volume `hello-data`; die Hello-App läuft am Ende weiter (Grundlage für Lab 4.4).

## Erweiterung

Öffne in Docker Desktop die Ansicht **Volumes**, wähle `hello_hello-data` und öffne im Reiter **Stored data** die Datei `access.log`.

## Fallback

- `npm install` scheitert (kein Zugang zu npmjs.org, z. B. Proxy): fertigen Stand verwenden (`cp -r examples/m04-compose/l03-volumes/. playground/` im Ordner `project/`) und den Build mit Netzzugang wiederholen; ohne Internetzugang ist das Rezeptbuch nicht baubar.
- Windows ohne `curl` in Git Bash: `curl.exe` verwenden; die Anführungszeichen bleiben wie oben.
- Hello-Stand kaputt: `cp -r examples/m04-compose/l03-volumes/hello/. playground/hello/` im Ordner `project/`.
