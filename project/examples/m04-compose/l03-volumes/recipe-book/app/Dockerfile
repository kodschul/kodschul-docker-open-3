# Rezeptbuch-Image: Node.js-App aus diesem Ordner
FROM node:24-alpine

WORKDIR /app

# Erst die Abhängigkeiten (Schicht bleibt im Cache, solange package.json gleich bleibt)
COPY package.json .
RUN npm install --omit=dev

# Danach den Code
COPY . .

EXPOSE 3000

# entspricht "npm start"; node direkt als Hauptprozess beendet sich bei docker stop sofort
CMD ["node", "index.js"]
