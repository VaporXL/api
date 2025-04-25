// api/status.js

module.exports = (req, res) => {
  res.status(200).json({ status: 'online', message: 'Pop! server is running' });
};
