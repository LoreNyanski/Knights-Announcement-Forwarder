import discord
import random
import datetime
from dataclasses import dataclass

from alarm_lib import Alarm, SubscriberInterface, RecurrenceRule

@dataclass
class Announcement():
    message: str
    images: list[str]

    @staticmethod
    def fromDiscord(msg: discord.Message) -> Announcement:
        message = msg.content or ""
        images = [attachment.url for attachment in msg.attachments]
        return Announcement(message, images)


class ScheduledAnnouncement(SubscriberInterface):

    def __init__(self, announcement: Announcement, alarm: Alarm, modifiers):
        self.announcement = announcement
        self.alarm = alarm
        self.alarm.subscribe(self)
        self.modifiers = modifiers or []

    def receive_update(self, context):
        pass

def jumbled_greeting(text: str, exclude: list[str]) -> str:
    exclude = exclude or []
    return "Dearest Knights!\n\n" + text

def add_dininglist(text: str) -> str:
    return text + ""