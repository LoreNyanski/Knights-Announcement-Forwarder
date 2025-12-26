'''
Docstring for bots.Knights-Announcement-Forwarder.telegram_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to telegram
'''
import re
from announcement import Announcement
import httpx
import os
from dotenv import load_dotenv
from main import TEST_MODE

# TODO: variables for telegram
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
telegram_channel = int(os.getenv('test_tel_channel') if TEST_MODE else os.getenv('main_tel_channel'))



def translate_dsc_tel(text: str) -> str:
    # Italics: *text* or _text_ → _text_
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"_\1_", text)
    # Small text: -# Text → italic
    text = re.sub(r"^-#\s*(.+)", r"_\1_", text, flags=re.MULTILINE)
    # Bold: **text** → *text*
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    # Big text: # Text → bold
    text = re.sub(r"^#\s*(.+)", r"*\1*", text, flags=re.MULTILINE)
    # Strikethrough: ~~text~~ → ~text~
    text = re.sub(r"~~(.*?)~~", r"~\1~", text)
    return text

async def send_to_telegram(announcement: Announcement):
    msg = translate_dsc_tel(announcement.message)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_channel, 
        "text": msg
    }
    await httpx.AsyncClient().post(url, json=data)