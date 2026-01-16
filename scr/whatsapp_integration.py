'''
Docstring for bots.Knights-Announcement-Forwarder.whatsapp_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to whatsapp
'''
import re
import asyncio
import random
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from announcement import Announcement
from config import whatsapp_channel


# Human-like typing delays
async def human_sleep(min_sec=0.4, max_sec=0.9):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

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
    message = translate_dsc_wha(announcement.message)
    images = announcement.images

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=False,  # headless=False is safer for WhatsApp detection
            slow_mo=random.uniform(45,55)  # optional: slow down actions to mimic human behavior
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.goto("https://web.whatsapp.com")
        
        # Wait for page to load
        await page.wait_for_selector('div[role="grid"]', timeout=60000)  # main chat list
        await human_sleep()
        
        # Click the community announcements channel by name
        chat = page.locator(f'span[title="{whatsapp_channel}"]')
        await chat.wait_for(state="visible")
        await chat.click()
        await human_sleep()
        
        # Upload images if any TODO
        if images:
            pass
        #     # Open attachment menu
        #     await page.click('span[data-icon="clip"]')
        #     await human_sleep()

        #     file_input = page.locator('input[type="file"]')
        #     await file_input.set_input_files(images)
        #     await human_sleep()
            
        #     # Caption box appears after image preview
        #     caption_box = page.locator('div[contenteditable="true"]').last
        #     await caption_box.fill(message)
        #     await human_sleep()
            
        #     await caption_box.press("Enter")
        else:
            # Just send text if no images
            message_box = page.locator('footer div[contenteditable="true"]')
            await message_box.fill(message)
            await human_sleep()
            await message_box.press("Enter")
        
        # Optional: wait a bit before closing
        await human_sleep(1, 2)

# def setup_wha_profile():
#     with sync_playwright() as p:
#         browser = p.chromium.launch_persistent_context(
#             user_data_dir="wha_profile",
#             headless=False
#         )
#         page = browser.new_page()
#         page.goto("https://web.whatsapp.com")
#         input("Scan QR, then press Enter...")

#         page.wait_for_selector('text="{}"'.format(whatsapp_channel))
#         page.click('text="{}"'.format(whatsapp_channel))

#         message_box = page.locator('div[contenteditable="true"][data-tab="10"]')
#         message_box.fill("does this work?")
#         page.keyboard.press("Enter")

#         input("Check if the message was sent correctly, then press Enter...")

#if __name__ == '__main__':
#    send_to_whatsapp(Announcement())