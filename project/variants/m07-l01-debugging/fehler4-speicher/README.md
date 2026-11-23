# Fehlerbild 4 (Lab 7.1)

Hello-App aus den fertigen Images `frontend:v2` und `backend:v1` (Lab 3.2).

```bash
docker compose up -d
```

- **Erwartet:** `http://localhost:8704` zeigt „Hello World 2.0.0" mit einer Backend-Antwort.
- **Beobachtet:** Die Seite lädt, das Backend fehlt.

Finde die Ursache, behebe sie in `compose.yml` und starte erneut. Aufräumen: `docker compose down`.
