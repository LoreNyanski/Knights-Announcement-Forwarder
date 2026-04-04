const express = require('express');
const fs = require('fs');
const path = require('path')
const mime = require('mime-types');
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

            const data = fs.readFileSync(filePath);
            const mimeType = mime.lookup(filePath) || 'application/octet-stream';
            const fileName = path.basename(filePath);

            const media = new MessageMedia(
                mimeType,
                data.toString('base64'),
                fileName // <-- important for docs
            );

            const options = {};

            // caption only on last
            if (i === attachment_paths.length - 1 && message) {
                options.caption = message;
            }

            // force documents for non-image/non-video files
            if (!mimeType.startsWith('image/') && !mimeType.startsWith('video/')) {
                options.sendMediaAsDocument = true;
            }

            await client.sendMessage(chat_id, media, options);

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