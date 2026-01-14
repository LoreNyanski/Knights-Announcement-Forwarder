'''
Docstring for bots.Knights-Announcement-Forwarder.whatsapp_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to whatsapp
'''
import re
from announcement import Announcement
from playwright.sync_api import sync_playwright
from config import whatsapp_channel, TEST_MODE

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

#TODO not implemented yet
async def send_to_whatsapp(announcement: Announcement):
    msg = translate_dsc_wha(announcement.message)
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")

        page.wait_for_selector('text="{}"'.format(whatsapp_channel))
        page.click('text="{}"'.format(whatsapp_channel))

        page.fill('div[contenteditable="true"]', msg)
        page.keyboard.press("Enter")

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="wa_profile",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        input("Scan QR, then press Enter...")

