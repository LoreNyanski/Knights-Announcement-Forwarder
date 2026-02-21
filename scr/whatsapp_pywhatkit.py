import re
import time
import pyperclip
from config import whatsapp_groupid, WAIT_CHANNEL, WAIT_WHATSAPP, WAIT_CLOSE, WAIT_IMAGE, ANNOUNCEMENTS_COORDINATES
from announcement import Announcement

from pyautogui import click, press, hotkey, size
from pywhatkit.core.core import _web, check_number, close_tab, copy_image

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

def copy_text(messege: str):
    pyperclip.copy(messege)
    hotkey("ctrl", "v")
    time.sleep(1)

def select_announcements_channel(receiver: str) -> None:
    """Clicks on the announcemenent channel of a community
    Sorry but you just gotta like test it out on your own device what metrics work"""
    _web(receiver=receiver, message="")
    time.sleep(WAIT_WHATSAPP)
    click(ANNOUNCEMENTS_COORDINATES)
    time.sleep(WAIT_CHANNEL)

def send_message_to_announcements(
        message: str, 
        channel_id: str
) -> None:
    """Parses and Sends the Message\n
    This is a function from pywhatkit edited by LoreNyanski for the purposes of sending messages to the announcement chat of a community"""

    if not check_number(number=channel_id):
        select_announcements_channel(receiver=channel_id)
        copy_text(messege=message)
        press("enter")
    close_tab(wait_time=WAIT_CLOSE)

def send_images_to_announcements(
        img_paths: list[str], 
        caption: str, 
        channel_id: str
) -> None:
    """Sends the Image to a Contact or a Group based on the Receiver
    This is a function from pywhatkit modified by LoreNyanski for the purposes of sending images to the announcement chat of a community"""

    if not check_number(number=channel_id):
        select_announcements_channel(receiver=channel_id)
        for img_path in img_paths:
            copy_image(path=img_path)
            hotkey("ctrl", "v")
            time.sleep(WAIT_IMAGE)
        copy_text(messege=caption)
        press("enter")
    close_tab(wait_time=WAIT_CLOSE)


def wha_send(announcement: Announcement):
    msg = announcement.message
    imgs = announcement.images
    if imgs:
        send_images_to_announcements(
            img_paths=imgs,
            caption=translate_dsc_wha(msg),
            channel_id=whatsapp_groupid
        )
    else:
        send_message_to_announcements(
            message=translate_dsc_wha(msg),
            channel_id=whatsapp_groupid
        )

if __name__ == '__main__':
    send_message_to_announcements(message="*Tasty Legs* and *crispy* _thighs_", channel_id=whatsapp_groupid)