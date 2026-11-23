// Todo-App aus github.com/docker/multi-container-app, angepasst für Lab 9.3:
// Live-Reload nur, wenn die Entwicklungspakete installiert sind (Entwicklungs-Image).
// Im Produktions-Image fehlen livereload und connect-livereload; die App startet dann ohne Live-Reload.
const mongoose = require('mongoose');
const bodyParse = require('body-parser');
const app = require('express')();
const moment = require('moment');

// Live Reload configuration (nur Entwicklung)
try {
    const livereload = require('livereload');
    const connectLiveReload = require('connect-livereload');
    const liveReloadServer = livereload.createServer();
    liveReloadServer.server.once("connection", () => {
        setTimeout(() => {
            liveReloadServer.refresh("/");
        }, 100);
    });
    app.use(connectLiveReload());
    console.log('Live-Reload aktiv');
} catch (error) {
    console.log('Live-Reload aus (Entwicklungspakete nicht installiert)');
}

// Fontend route
const FrontRouter = require('./routes/front');

// Set ejs template engine
app.set('view engine', 'ejs');

app.use(bodyParse.urlencoded({ extended: false }));
app.locals.moment = moment;

// Database connection (useNewUrlParser entfernt: veraltete Option ohne Wirkung)
const db = require('./config/keys').mongoProdURI;
mongoose
    .connect(db)
    .then(() => console.log(`Mongodb Connected`))
    .catch(error => console.log(error));


app.use(FrontRouter);


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
