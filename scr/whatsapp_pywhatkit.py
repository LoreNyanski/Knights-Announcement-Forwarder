import re
from config import whatsapp_groupid
from announcement import Announcement
from pywhatkit import sendwhatmsg_to_group_instantly, sendwhats_image

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
    msg = announcement.message
    imgs = announcement.images
    if announcement.images:
        sendwhats_image()
    else:
        sendwhatmsg_to_group_instantly(
            group_id=whatsapp_groupid,
            message=translate_dsc_wha(msg),
            wait_time=10,
            tab_close=True
        )

if __name__ == '__main__':
    sendwhatmsg_to_group_instantly(
        group_id=whatsapp_groupid,
        message=translate_dsc_wha("playeh"),
        wait_time=10,
        tab_close=True
    )
    