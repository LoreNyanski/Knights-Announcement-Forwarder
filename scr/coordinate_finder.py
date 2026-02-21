from pyautogui import position
from config import DATA_DIR, COORD_FILE, whatsapp_groupid
from pywhatkit.core.core import _web, close_tab

_web(receiver=whatsapp_groupid, message="")
input("Press Enter when your mouse is on the correct position...")
with open(file=(DATA_DIR/COORD_FILE), mode="w+") as f:
    pos = position()
    f.writelines([str(pos.x), "\n", str(pos.y)])
close_tab()