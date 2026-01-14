from dotenv import load_dotenv
import os

load_dotenv()

TEST_MODE = bool(os.getenv("TEST_MODE"))

# variables for discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
# me = os.getenv('me')
discord_guild = int(os.getenv('test_dsc_guild') if TEST_MODE else os.getenv('main_dsc_guild'))
discord_channel = int(os.getenv('test_dsc_channel') if TEST_MODE else os.getenv('main_dsc_channel'))
discord_role = int(os.getenv('test_dsc_role') if TEST_MODE else os.getenv('main_dsc_role'))

# variables for telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
telegram_channel = int(os.getenv('test_tel_channel') if TEST_MODE else os.getenv('main_tel_channel'))

# variables for whatsapp
whatsapp_channel = os.getenv("test_wha_channel") if TEST_MODE else os.getenv("main_wha_channel")
