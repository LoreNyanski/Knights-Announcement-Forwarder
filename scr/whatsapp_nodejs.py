import requests
from announcement import Announcement

from config import whatsapp_groupid

def wha_send(announcement: Announcement):
    if announcement.attachments:
        payload = {
            "chat_id": whatsapp_groupid,
            "message": announcement.message,
            "attachment_paths": [str(path) for path in announcement.attachments]
        }
        requests.post("http://localhost:3000/send-attachments", json=payload)
    else:
        requests.post("http://localhost:3000/send", json={"chat_id": whatsapp_groupid, "message": announcement.message})