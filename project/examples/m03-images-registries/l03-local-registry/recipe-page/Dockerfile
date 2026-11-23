# Rezeptseite (Lab 3.3): statische HTML-Seite mit nginx ausliefern
# Basisimage: nginx 1.30 auf Alpine Linux, fester Tag
FROM nginx:1.30-alpine

# Eigene Startseite über die Standardseite von nginx kopieren
COPY index.html /usr/share/nginx/html/index.html

# nginx lauscht im Container auf Port 80; den Startbefehl bringt das Basisimage mit
EXPOSE 80
