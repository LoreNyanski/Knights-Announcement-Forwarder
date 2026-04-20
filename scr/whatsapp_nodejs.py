import requests
import re
from announcement import Announcement

from config import whatsapp_groupid

def translate_dsc_wha(text: str) -> str:

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

    # Underline: __text__ → text  (WhatsApp has no underline)
    text = re.sub(r"__(.*?)__", r"\1", text)

    # Spoilers: ||text|| → text  (no WhatsApp equivalent)
    text = re.sub(r"\|\|(.*?)\|\|", r"(\1)", text)

    return text

def wha_send(announcement: Announcement):
    if announcement.attachments:
        payload = {
            "chat_id": whatsapp_groupid,
            "message": translate_dsc_wha(announcement.message),
            "attachment_paths": [str(path) for path in announcement.attachments]
        }
        requests.post("http://localhost:3000/send-attachments", json=payload)
    else:
        requests.post("http://localhost:3000/send", json={"chat_id": whatsapp_groupid, "message": announcement.message})