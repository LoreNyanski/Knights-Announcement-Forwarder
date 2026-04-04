const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

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

client.isReady = false;

// QR login
client.on('qr', (qr) => {
    console.log('Scan this QR code with your WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// Ready event
client.on('ready', () => {
    console.log('WhatsApp client is ready!');
    client.isReady = true;
});

// Handle disconnects (VERY important)
client.on('disconnected', (reason) => {
    console.error('WhatsApp disconnected:', reason);
    client.isReady = false;
});

async function shutdown(signal) {
    console.log(`Received ${signal}, shutting down gracefully...`);

    try {
        if (client) {
            await client.destroy(); // <-- critical
            console.log('WhatsApp client destroyed');
        }
    } catch (err) {
        console.error('Error during shutdown:', err);
    }

    process.exit(0);
}

// Register handlers ONCE
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
process.on('SIGQUIT', shutdown);

client.initialize();

module.exports = client;