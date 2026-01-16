'''
Docstring for bots.Knights-Announcement-Forwarder.whatsapp_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to whatsapp
'''
import re
from announcement import Announcement
from playwright.sync_api import sync_playwright
from config import whatsapp_channel
import time, random

# Human-like typing delays
def human_sleep(min_sec=0.4, max_sec=1.2):
    time.sleep(random.uniform(min_sec, max_sec))

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
def send_to_whatsapp(announcement: Announcement):
    message = translate_dsc_wha(announcement.message)
    images = announcement.images

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=False,  # headless=False is safer for WhatsApp detection
            slow_mo=random.uniform(45,55)  # optional: slow down actions to mimic human behavior
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        
        # Wait for page to load
        page.wait_for_selector('div[role="grid"]', timeout=60000)  # main chat list
        human_sleep()
        
        # Click the community announcements channel by name
        channel = page.locator(f'span[title="{whatsapp_channel}"]')
        channel.wait_for(state="visible")
        channel.click()
        human_sleep()
        
        # Upload images if any TODO
        if images:
            pass
            # page.click('span[data-icon="clip"]')  # attachment button
            # file_input = page.locator('input[type="file"]')
            # file_input.set_input_files(images)
            
            # # Wait for preview to appear
            # page.wait_for_selector('div[contenteditable="true"]')
            
            # # Type caption for the images
            # caption_box = page.locator('div[contenteditable="true"]').last
            # caption_box.fill(message)
            # human_sleep()
            
            # # Send images + caption
            # caption_box.press("Enter")
        else:
            # Just send text if no images
            message_box = page.locator('footer div[contenteditable="true"]')
            message_box.fill(message)
            human_sleep()
            message_box.press("Enter")
        
        # Optional: wait a bit before closing
        human_sleep(1, 2)

def setup_wha_profile():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com")
        input("Scan QR, then press Enter...")

        page.wait_for_selector('text="{}"'.format(whatsapp_channel))
        page.click('text="{}"'.format(whatsapp_channel))

        message_box = page.locator('div[contenteditable="true"][data-tab="10"]')
        message_box.fill("does this work?")
        page.keyboard.press("Enter")

        input("Check if the message was sent correctly, then press Enter...")

#if __name__ == '__main__':
#    send_to_whatsapp(Announcement())