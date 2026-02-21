import asyncio
import re
import telegram as tel
from announcement import Announcement

from config import TELEGRAM_TOKEN, telegram_channel

markdown = tel.constants.ParseMode.MARKDOWN

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

async def tel_send(announcement: Announcement):
    bot = tel.Bot(token=TELEGRAM_TOKEN)
    imgs = announcement.images
    msg = translate_dsc_tel(announcement.message)
    async with bot:
        if imgs: # announcement has images
            if len(msg) <= tel.constants.MessageLimit.CAPTION_LENGTH:
                medias = [tel.InputMediaPhoto(
                              media=open(img, 'rb'), 
                              caption=(msg if img == imgs[-1] else None),
                              parse_mode=markdown)
                          for img 
                          in imgs]
                await bot.send_media_group(chat_id=telegram_channel, media=medias)
            else:
                medias = [tel.InputMediaPhoto(media=open(img, 'rb'))        
                          for img 
                          in imgs]
                await bot.send_media_group(chat_id=telegram_channel, media=medias)
                await bot.send_message(chat_id=telegram_channel, text=msg, parse_mode=markdown)
        else: # announcement has no images
            await bot.send_message(chat_id=telegram_channel, text=msg, parse_mode=markdown)
