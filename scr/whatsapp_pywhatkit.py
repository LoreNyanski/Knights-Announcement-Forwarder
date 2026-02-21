import re
import os
from config import whatsapp_groupid
from announcement import Announcement
from pywhatkit import sendwhatmsg_to_group_instantly, sendwhats_image

from pyautogui import locateOnScreen, click, moveTo, press, hotkey, typewrite
from pywhatkit.core.core import _web, check_number
import time

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

def select_announcements_channel(receiver: str, tries: int = 10) -> None:
    """Clicks on the announcemenent channel of a community"""
    _web(receiver=receiver, message="")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = None
    for i in range(tries):
        time.sleep(5)
        location = locateOnScreen(f"{dir_path}/assets/speaker_icon.png")
        try:
            moveTo(location)
            click()
            return
        except:
            print(f"Try {i} failed :(")

def send_message_to_announcements(message: str, receiver: str, wait_time: int) -> None:
    """Parses and Sends the Message\n
    This is the function send_message from pywhatkit edited by LoreNyanski for the purposes of sending messages to the announcement chat of a community"""

    if not check_number(number=receiver):
        select_announcements_channel(receiver=receiver)
        time.sleep(min(wait_time,1))
        for char in message:
            if char == "\n":
                hotkey("shift", "enter")
            else:
                typewrite(char)
    press("enter")

# def sendwhatmsg_to_group_instantly(
#     group_id: str,
#     message: str,
#     wait_time: int = 15,
#     tab_close: bool = False,
#     close_time: int = 3,
# ) -> None:
#     """Send WhatsApp Message to a Group Instantly"""

#     current_time = time.localtime()

#     time.sleep(wait_time)
#     core.send_message(message=message, receiver=group_id, wait_time=wait_time)
#     if tab_close:
#         core.close_tab(wait_time=close_time)

# def wha_send(announcement: Announcement):
#     msg = announcement.message
#     imgs = announcement.images
#     if announcement.images:
#         sendwhats_image()
#     else:
#         sendwhatmsg_to_group_instantly(
#             group_id=whatsapp_groupid,
#             message=translate_dsc_wha(msg),
#             wait_time=10,
#             tab_close=True
#         )

if __name__ == '__main__':
    select_announcements_channel(whatsapp_groupid)