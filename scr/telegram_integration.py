'''
Docstring for bots.Knights-Announcement-Forwarder.telegram_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to telegram
'''
import json
import re
import httpx
from config import telegram_channel, TELEGRAM_TOKEN

from announcement import Announcement

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
    if announcement.images:
        await send_to_telegram_images(announcement)
    else:
        await send_to_telegram_text(announcement)

async def send_to_telegram_text(announcement: Announcement):
    msg = translate_dsc_tel(announcement.message)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": telegram_channel, 
        "text": msg,
        "parse_mode": "Markdown"
    }
    await httpx.AsyncClient().post(url, json=data)

async def send_to_telegram_images(announcement: Announcement):
    msg = translate_dsc_tel(announcement.message)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMediaGroup"

    media = []
    files = {}

    for i, image_path in enumerate(announcement.images):
        key = f"photo{i}"
        files[key] = open(image_path, "rb")

        item = {
            "type": "photo",
            "media": f"attach://{key}"
        }

        # put caption on last image
        if i == len(announcement.images) - 1:
            item["caption"] = msg
            item["parse_mode"] = "Markdown"

        media.append(item)

    async with httpx.AsyncClient() as client:
        await client.post(
            url,
            data={
                "chat_id": telegram_channel,
                "media": json.dumps(media)
            },
            files=files
        )

    # close files
    for f in files.values():
        f.close()
