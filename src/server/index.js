// src/server/index.js

const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;

db.on('error', (error) => console.error('MongoDB connection error:', error));
db.once('open', () => console.log('Connected to MongoDB'));

// Basic route
app.get('/', (req, res) => {
  res.send('Express server is running');
});

app.get('/api/quantum/grover', async (req, res) => {
  // spawn Python process to run grover.py
  res.json({ result: "Grover output here" });
});

app.get('/api/quantum/teleportation', async (req, res) => {
  // spawn Python process to run teleportation.py
  res.json({ result: "Teleportation output here" });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});