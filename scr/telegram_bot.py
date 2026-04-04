import re
import telegram as tel
import mimetypes
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
    attachments = announcement.attachments
    msg = translate_dsc_tel(announcement.message)

    async with bot:
        medias = []
        exceed_caption_length = False
        for i, file in enumerate(attachments):
            mime_type, _ = mimetypes.guess_type(file)
            caption = None
            if i == len(attachments) - 1:
                if len(msg) <= tel.constants.MessageLimit.CAPTION_LENGTH: caption = msg
                else: exceed_caption_length = True # If caption is too long send image seperately and THEN the message

            if mime_type and mime_type.startswith("image/"):
                medias.append(tel.InputMediaPhoto(media=open(file, 'rb'), caption=caption, parse_mode=markdown))
            else:
                medias.append(tel.InputMediaDocument(media=open(file, 'rb'), caption=caption, parse_mode=markdown))

        if medias:
            await bot.send_media_group(chat_id=telegram_channel, media=medias)
            if exceed_caption_length: await bot.send_message(chat_id=telegram_channel, text=msg, parse_mode=markdown)
        elif msg:
            await bot.send_message(chat_id=telegram_channel, text=msg, parse_mode=markdown)
