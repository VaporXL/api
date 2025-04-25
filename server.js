const express = require("express");
const cors = require("cors");
const { v4: uuid } = require("uuid");

const app = express();
app.use(cors());
app.use(express.json());

const messages = [];

app.get("/chat", (req, res) => {
  res.json(messages);
});

app.post("/chat", (req, res) => {
  const { username, content } = req.body;
  const msg = { id: uuid(), username, content, time: Date.now() };
  messages.push(msg);
  res.status(201).json(msg);
});

app.listen(3000, () => console.log("API running on port 3000"));
