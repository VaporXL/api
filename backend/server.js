const express = require('express');
const cors = require('cors');
const app = express();

// Use CORS to allow cross-origin requests (Minecraft mod will access this API)
app.use(cors());

// Simple route to check if the server is working
app.get('/', (req, res) => {
  res.send('Pop! API is running');
});

// Sample API endpoint to get server status
app.get('/status', (req, res) => {
  res.json({ status: 'online', message: 'Pop! server is working' });
});

// Start the server on port 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
