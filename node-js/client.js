const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const os = require('os');
require('dotenv').config(); // load .env

let puppeteerConfig = {
    headless: true,
    args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-extensions',
        '--disable-background-networking',
        '--disable-background-timer-throttling',
        '--disable-client-side-phishing-detection',
        '--disable-default-apps',
        '--disable-hang-monitor',
        '--disable-sync',
        '--disable-translate',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--disable-logging',
        '--disable-popup-blocking',
        '--disable-ipc-flooding-protection',
        '--single-process',
        '--no-zygote'
    ]
};

if (process.env.CHROMIUM_PATH) {
    // If you set a path for a custom chromium then it runs on that
    puppeteerConfig.executablePath = process.env.CHROMIUM_PATH;
} else if (os.arch().startsWith('arm') || (os.platform() === 'linux' && os.arch() === 'arm64')) {
    // Fallback for ARM if no env variable set
    puppeteerConfig.executablePath = '/usr/bin/chromium-browser';
}

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: puppeteerConfig
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

// Handle disconnects
client.on('disconnected', (reason) => {
    console.error('WhatsApp disconnected:', reason);
    client.isReady = false;
});

async function shutdown(signal) {
    console.log(`Received ${signal}, shutting down gracefully...`);

    try {
        if (client) {
            await client.destroy();
            console.log('WhatsApp client destroyed');
        }
    } catch (err) {
        console.error('Error during shutdown:', err);
    }

    process.exit(0);
}

// Register handlers 
process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
process.on('SIGQUIT', shutdown);

client.initialize();

module.exports = client;