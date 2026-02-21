from dotenv import load_dotenv
from pathlib import Path
import os

# ~~~~~~~~~~~~~~~~~~~~~~~ OTHER VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~ #
IMAGE_DIR = Path(".temp")

# ~~~~~~~~~~~~~~~~~~~~~~~~ RUN VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~ #
TEST_MODE = os.getenv("TEST_MODE", "True") == "True" # String bool isn't real it can't hurt you
print("Running in " + ("Test mode" if TEST_MODE else "Real mode"))

# ~~~~~~~~~~~~~~~~~~~~~~~~ ENV VARIABLES ~~~~~~~~~~~~~~~~~~~~~~~~ #
load_dotenv()

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
whatsapp_groupid = os.getenv("test_wha_groupid") if TEST_MODE else os.getenv("main_wha_groupid")

WAIT_WHATSAPP = int(os.getenv('wait_whatsapp'))
WAIT_CHANNEL = int(os.getenv('wait_channel'))
WAIT_IMAGE = int(os.getenv('wait_image'))
WAIT_CLOSE = int(os.getenv('wait_close'))