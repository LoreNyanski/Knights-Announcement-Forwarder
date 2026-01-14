import discord
from config import DISCORD_TOKEN, discord_channel, discord_guild, discord_role
from announcement import Announcement
from telegram_integration import send_to_telegram
from whatsapp_integration import send_to_whatsapp

'''
IDEAS
- Popup after posting thingy asking if you want to send it to the other channels
- Way to link whatsapp and telegram within the bot
    - classes for WhatsappConnection and TelegramConnection
- Popup letting you schedule/repeat the announcements
    - Look at existing announcements yet to be sent and editing them.

EXECUTION:
/Announce - command that gives you a popup then lets you add rules and dates in a message context
Fields:
- Body - text/image

- Generate Greeting - Y/N
- Generate Dininglist - Y/N
- Mode - Remind in DMs / Instant send

- Base time - Date selector - All the rules will be calculated from this instance
- Add Time - button
- Add Rule - button
- Rule Type [Daily Weekly Monthly] 
    Daily - every [x] days
    Weekly - every [x] weeks & Each [mon, tue...] 
    Monthy - every [x] months & Each [1-31] | On the [first, second, last...] [Mon, tue...]

/Check Announcements - list of current announcements and edit them

/Config - popup for condfiguring where the telegram bot should send shit towards
'''


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
    client.run(DISCORD_TOKEN)