const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const express = require('express');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

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


app.post('/send', async (req, res) => {
    const { chat_id, message } = req.body;
    try {
        await client.sendMessage(chat_id, message);
        res.json({ success: true });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to send message' });
    }
});

app.post('/send-attachments', async (req, res) => {
    const { chat_id, message, attachment_paths } = req.body;

    if (!attachment_paths || !Array.isArray(attachment_paths) || attachment_paths.length === 0) {
        return res.status(400).json({ error: 'attachment_paths must be a non-empty array' });
    }

    try {
        // Convert paths to MessageMedia objects
        const mediaArray = attachment_paths.map((filePath, idx) => {
            if (!fs.existsSync(filePath)) {
                throw new Error(`File does not exist: ${filePath}`);
            }

            const data = fs.readFileSync(filePath);
            const mimeType = "application/octet-stream"; // generic, can improve with mime lib
            const isLast = idx === attachment_paths.length - 1;

            return new MessageMedia(mimeType, data.toString('base64'), isLast ? undefined : '');
        });

        // Send all media
        // Only last item will have a caption
    for (let i = 0; i < mediaArray.length; i++) {
        const media = mediaArray[i];
        if (i === mediaArray.length - 1) media.caption = message || '';
        await client.sendMessage(targetChatId, media);
    }

        res.json({ success: true, sent: attachment_paths.length });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Failed to send attachments', details: err.toString() });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});