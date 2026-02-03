'''
Docstring for bots.Knights-Announcement-Forwarder.whatsapp_integration
This is probably not the proper place to put this file but whatever
Includes any helper stuff for getting messages posted to whatsapp
'''
import base64
from pathlib import Path
import re
import asyncio
import random
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from announcement import Announcement
from config import whatsapp_channel, HEADLESS

# Image translation
def image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()

# Human-like typing delays
async def human_sleep(min_sec=0.4, max_sec=0.9):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def type_lines(page, text: str):
    for i, line in enumerate(text.split("\n")):
        await page.keyboard.type(text=line, delay=random.randint(40, 60))
        if i < text.count("\n"):
            await page.keyboard.down("Shift")
            await page.keyboard.press("Enter")
            await page.keyboard.up("Shift")

async def paste_image_via_clipboard(page, image_path: Path):
    image_b64 = image_to_base64(image_path)

    await page.evaluate(
        """
        async (imageBase64) => {
            const binary = atob(imageBase64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {
                bytes[i] = binary.charCodeAt(i);
            }

            const blob = new Blob([bytes], { type: 'image/png' });

            const clipboardItem = new ClipboardItem({
                'image/png': blob
            });

            await navigator.clipboard.write([clipboardItem]);
        }
        """,
        image_b64
    )

    await page.keyboard.press("Control+V")

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

async def send_to_whatsapp(announcement: Announcement):
    message = translate_dsc_wha(announcement.message)
    images = announcement.images

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=HEADLESS,  # headless=False is safer for WhatsApp detection
            slow_mo=random.uniform(45,55),  # optional: slow down actions to mimic human behavior
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

        message_box = page.locator('footer div[contenteditable="true"]')
        for image in images:
            img_path = Path(image)
            await paste_image_via_clipboard(page, img_path)
            await human_sleep()
        await type_lines(page, message)
        await human_sleep()
        await page.keyboard.press("Enter")
        human_sleep(10, 11) # fuck it, just wait a bunch

async def whatsapp_testing():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="wha_profile",
            headless=False,  # headless=False is safer for WhatsApp detection
            slow_mo=random.uniform(45,55)  # optional: slow down actions to mimic human behavior
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        await page.goto("https://web.whatsapp.com")

        input("Press enter when done testing")

if __name__ == '__main__':
    asyncio.run(whatsapp_testing())