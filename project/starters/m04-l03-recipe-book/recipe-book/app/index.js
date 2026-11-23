// Rezeptbuch: kleine REST-API mit Express 5 und Mongoose 9 (MongoDB)
const express = require("express");
const mongoose = require("mongoose");

const app = express();
app.use(express.json()); // JSON im Anfragekörper lesen

// Hostname = Dienstname aus der Compose-Datei; die Datenbank "recipes" entsteht beim ersten Speichern
mongoose
  .connect("mongodb://recipe-database:27017/recipes")
  .then(() => console.log("Mit MongoDB verbunden"))
  .catch((err) => console.error("MongoDB nicht erreichbar:", err.message));

// Aufbau eines Rezepts
const recipeSchema = new mongoose.Schema({
  title: String,
  ingredients: [String],
  instructions: String,
});
const Recipe = mongoose.model("Recipe", recipeSchema);

app.get("/", (req, res) => {
  res.send("Rezeptbuch-API: GET /recipes listet alle Rezepte, POST /recipes legt eines an.");
});

// Rezept anlegen
app.post("/recipes", async (req, res) => {
  const recipe = new Recipe(req.body);
  await recipe.save();
  res.status(201).send(recipe);
});

// Alle Rezepte abrufen
app.get("/recipes", async (req, res) => {
  const recipes = await Recipe.find();
  res.send(recipes);
});

app.listen(3000, () => console.log("Recipe Book App listening on port 3000"));
