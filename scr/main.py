import discord

from config import DISCORD_TOKEN, discord_channel, discord_guild, discord_role
from announcement import Announcement
from telegram_integration import send_to_telegram
from whatsapp_integration import send_to_whatsapp

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

    if message.guild.id == discord_guild and message.channel.id == discord_channel and discord_role in [x.id for x in message.author.roles]:
        with await Announcement.fromDiscord(message) as announcement:
            await send_to_telegram(announcement)
            await send_to_whatsapp(announcement)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)