const { Client, LocalAuth } = require('whatsapp-web.js');
const express = require('express');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

// Use LocalAuth to persist session
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ]
    }
});

// Generate QR code for first login
client.on('qr', (qr) => {
    console.log('Scan this QR code with your WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// Confirm ready
client.on('ready', () => {
    console.log('WhatsApp client is ready!');
});

client.initialize();

// --- HTTP endpoint to send messages ---
const CHAT_ID = '120363424609598589@g.us'; // replace with your group ID

app.post('/send', async (req, res) => {
    const { message, chat_id } = req.body;
    try {
        await client.sendMessage(chat_id, message);
        res.json({ success: true });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to send message' });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});