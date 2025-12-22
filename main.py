import discord
import os
import re
import random
import httpx

from discord.ext import commands
import discord.ext
import discord.ext.commands
from dotenv import load_dotenv

from announcement import *

'''
IDEAS
- Popup after posting thingy asking if you want to send it to the other channels
- Way to link whatsapp and telegram within the bot
    - classes for WhatsappConnection and TelegramConnection
- Popup letting you schedule/repeat the announcements
    - Look at existing announcements yet to be sent and editing them.
'''

load_dotenv()
TEST_MODE = True
# me = os.getenv('me')

# variables for discord
TOKEN = os.getenv('DISCORD_TOKEN')
discord_guild = os.getenv('test_guild') if TEST_MODE else os.getenv('main_guild')
discord_channel = os.getenv('test_channel') if TEST_MODE else os.getenv('main_channel')

# TODO: variables for telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHANNEL = os.getenv('test_tel_channel') if TEST_MODE else os.getenv('main_tel_channel')

# TODO: variables for whatsapp


# TODO: proper intents my guy
intents = discord.Intents.default()
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has logged in\n\nConnected to the following guilds:')
    for guild in client.guilds:
        print(f'    {guild.name} (id: {guild.id})')
    
    await send_to_telegram(Announcement("asd"))

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id == discord_channel:
        announcement = message
        await send_to_telegram(announcement)
        await send_to_whatsapp(announcement)
        
async def send_to_telegram(announcement: Announcement):
    msg = announcement.translate_dsc_tel()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHANNEL, 
        "text": msg
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data)

async def send_to_whatsapp(announcement: Announcement):
    msg = announcement.translate_dsc_wha()

if __name__ == "__main__":
    client.run(TOKEN)