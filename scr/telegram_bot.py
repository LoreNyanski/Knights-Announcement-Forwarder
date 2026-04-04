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
        for i, file in enumerate(attachments):
            mime_type, _ = mimetypes.guess_type(file)
            caption = msg if i == len(attachments) - 1 and len(msg) <= tel.constants.MessageLimit.CAPTION_LENGTH else None

            if mime_type and mime_type.startswith("image/"):
                medias.append(tel.InputMediaPhoto(media=open(file, 'rb'), caption=caption, parse_mode=markdown))
            else:
                medias.append(tel.InputMediaDocument(media=open(file, 'rb'), caption=caption, parse_mode=markdown))

        if medias:
            await bot.send_media_group(chat_id=telegram_channel, media=medias)
        elif msg:
            await bot.send_message(chat_id=telegram_channel, text=msg, parse_mode=markdown)
