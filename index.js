const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer(async (req, res) => {
  return res.end(`Hello!!v1`);
});

server.listen(PORT, () => {
  console.log('Server started on port', PORT);
});
