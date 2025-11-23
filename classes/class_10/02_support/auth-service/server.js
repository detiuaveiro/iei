const express = require('express');
const cors = require('cors');
const http = require('http');
const WebSocket = require('ws');
const crypto = require('crypto');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(cors());
app.use(express.json());

// Helper function to create SHA-256 hash
function createHash(text) {
    return crypto.createHash('sha256').update(text).digest('hex');
}

// Initialize the valid user with a computed hash
const VALID_USER = { 
    username: "admin", 
    // We compute the hash of "123" right now.
    passwordHash: createHash("123") 
};

console.log('Server initialized.');

app.post('/login', (req, res) => {
    const { username, password } = req.body;

    // 1. Convert strings to Buffers for safe comparison
    const inputBuffer = Buffer.from(password || '');
    const validBuffer = Buffer.from(VALID_USER.passwordHash);

    // 2. Use constant-time comparison to prevent timing attacks
    const isMatch = (inputBuffer.length === validBuffer.length) && 
                    crypto.timingSafeEqual(inputBuffer, validBuffer);

    if (username === VALID_USER.username && isMatch) {
        res.json({ success: true, token: "jwt-123" });
    } else {
        res.status(401).json({ success: false, message: "Invalid credentials" });
    }
})

// Chat Logic
wss.on('connection', (ws) => {
    ws.send('Support: Hello! How can I help you?');
    ws.on('message', (msg) => setTimeout(() => ws.send(`Support: Recv "${msg}"`), 1000));
});

server.listen(3000, () => console.log('Auth running on 3000'));
