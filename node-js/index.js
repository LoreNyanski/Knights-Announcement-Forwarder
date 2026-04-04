const express = require('express');
const fs = require('fs');
const { MessageMedia } = require('whatsapp-web.js');
const client = require('./client.js');

const app = express();
app.use(express.json());


// ---- SEND TEXT ----
app.post('/send', async (req, res) => {
    const { chat_id, message } = req.body;

    if (!client.isReady) {
        return res.status(503).json({ error: 'WhatsApp client not ready yet' });
    }

    try {
        await client.sendMessage(chat_id, message);
        res.json({ success: true });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.message });
    }
});


// ---- SEND ATTACHMENTS ----
app.post('/send-attachments', async (req, res) => {
    const { chat_id, message, attachment_paths } = req.body;

    if (!client.isReady) {
        return res.status(503).json({ error: 'WhatsApp client not ready yet' });
    }

    if (!attachment_paths || !Array.isArray(attachment_paths) || attachment_paths.length === 0) {
        return res.status(400).json({ error: 'attachment_paths must be a non-empty array' });
    }

    try {
        for (let i = 0; i < attachment_paths.length; i++) {
            const filePath = attachment_paths[i];

            if (!fs.existsSync(filePath)) {
                throw new Error(`File does not exist: ${filePath}`);
            }

            // ✅ create fresh media EVERY time (important)
            const data = fs.readFileSync(filePath);
            const media = new MessageMedia(
                "application/octet-stream",
                data.toString('base64')
            );

            // only last gets caption
            if (i === attachment_paths.length - 1) {
                media.caption = message || '';
            }

            await client.sendMessage(chat_id, media);

            // small delay = prevents frame issues
            await new Promise(res => setTimeout(res, 200));
        }

        res.json({ success: true, sent: attachment_paths.length });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: err.toString() });
    }
});


app.listen(3000, () => {
    console.log('Server running on port 3000');
});