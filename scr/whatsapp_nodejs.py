import requests
from announcement import Announcement

from config import whatsapp_groupid

def wha_send(announcement: Announcement):
    requests.post("http://localhost:3000/send", json={"message": announcement.message, "chat_id": whatsapp_groupid})