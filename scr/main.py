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
from telegram_integration import *

'''
IDEAS
- Popup after posting thingy asking if you want to send it to the other channels
- Way to link whatsapp and telegram within the bot
    - classes for WhatsappConnection and TelegramConnection
- Popup letting you schedule/repeat the announcements
    - Look at existing announcements yet to be sent and editing them.

EXECUTION:
/Announce - command that gives you a popup 
Fields:
    - Generate Greeting - Y/N
- Body - text
    - Generate Dininglist - Y/N
- Forward to Tel - Y/N
- Forward to Wha - Y/N
- Mode - Remind in DMs / Post with Webhook
X Add Time - button
- Select time - Now/Date selector
X Add Rule - button
- At - 24 hr time selector for the rule
X Rule Type [Daily Weekly Monthly Yearly]
    Daily - every [x] days
    Weekly - every [x] weeks & Each [mon, tue...] 
    Monthy - every [x] months & Each [1-31] | On the [first, second, last...] [Mon, tue...]
    Yearly - every
/Check Announcements - list of current announcements and edit them

/Config - popup for condfiguring where the telegram bot should send shit towards
'''

load_dotenv()
TEST_MODE = True
# me = os.getenv('me')

# variables for discord
TOKEN = os.getenv('DISCORD_TOKEN')
discord_guild = int(os.getenv('test_dsc_guild') if TEST_MODE else os.getenv('main_dsc_guild'))
discord_channel = int(os.getenv('test_dsc_channel') if TEST_MODE else os.getenv('main_dsc_channel'))
discord_role = int(os.getenv('test_dsc_role') if TEST_MODE else os.getenv('main_dsc_role'))

# TODO: proper intents my guy
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has logged in\n\nConnected to the following guilds:')
    for guild in client.guilds:
        print(f'    {guild.name} (id: {guild.id})')

@client.event
async def on_message(message: discord.Message):

    if message.author.bot:
        return

    if message.channel.id == discord_channel and discord_role in [x.id for x in message.author.roles]:
        announcement = Announcement.fromDiscord(message)
        await send_to_telegram(announcement)
        # TODO not implemented yet
        # await send_to_whatsapp(announcement)
        


if __name__ == "__main__":
    client.run(TOKEN)