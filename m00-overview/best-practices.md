# Best Practices

## Images

| Regel | Warum |
| --- | --- |
| feste Tags (`python:3.13-alpine`), nie nur `latest` | gleicher Build heute und in drei Monaten |
| schlankes Basisimage | weniger Größe, weniger Schwachstellen |
| `requirements.txt` vor dem Code kopieren | Build-Cache bleibt bei Code-Änderungen erhalten |
| `.dockerignore` pflegen | kleiner Build-Kontext, keine Geheimnisse im Image |
| Multistage-Build für Build-Werkzeuge | Compiler und Dev-Pakete bleiben draußen |
| eigener Benutzer mit `USER` | Angreifer im Container ist nicht root |

## Container und Daten

| Regel | Warum |
| --- | --- |
| Daten in Volumes, nie in der Container-Schicht | `docker rm` löscht die Schicht |
| Konfiguration über Umgebungsvariablen | ein Image für Test und Produktion |
| Logs nach stdout/stderr | `docker logs` und Sammler finden sie |
| Limits für Speicher und CPU setzen | ein Container legt nicht den Host lahm |
| Healthcheck für jeden Dienst | „läuft" heißt noch nicht „antwortet" |

## Netzwerk und Sicherheit

| Regel | Warum |
| --- | --- |
| nur nötige Ports veröffentlichen | Backend und Datenbank bleiben intern |
| eigene Netzwerke statt Standard-Bridge | Namen statt IPs, Trennung je Anwendung |
| Docker-Socket nur lesend und nur wo nötig | Zugriff darauf entspricht root |
| Images vor dem Einsatz scannen | bekannte Lücken früh finden |
| Zugangstoken statt Passwort für Registries | einzeln widerrufbar |

## Betrieb

| Regel | Warum |
| --- | --- |
| Versionen nach `MAJOR.MINOR.PATCH` taggen | Änderungen nachvollziehbar |
| Rolling Update mit Rollback-Konfiguration | Fehler ohne Ausfall zurücknehmen |
| Compose für einen Host, Swarm/Kubernetes für mehrere | Werkzeug passend zur Größe |
