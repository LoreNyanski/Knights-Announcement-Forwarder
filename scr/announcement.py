import discord
import random
import datetime
from alarm_lib import Alarm, SubscriberInterface, RecurrenceRule

class Announcement():

    # Base init
    # TODO Replace list type with something thats not a discord attachment
    def __init__(self, message: str, images: None = None):
        self.message = message
        self.images = images

    @staticmethod
    def fromDiscord(message: discord.Message):
        msg = message.content
        img = message.attachments
        return Announcement(msg, img)

class ScheduledAnnouncementConfig():
    def __init__(self, author: discord.User, message: str = "", greeting: bool = True, dininglist: bool = True, instant_send: bool = False, 
                 images = None, times: list[datetime.datetime] | None = None, rules: list[RecurrenceRule] | None = None):
        self.author = author
        self.message = message
        self.greeting = greeting
        self.dininglist = dininglist
        self.instant_send = instant_send
        self.images = images
        self.times = times or [datetime.datetime.now() + datetime.timedelta(days=1)]
        self.rules = rules or []

class ScheduledAnnouncement(SubscriberInterface):

    def __init__(self, conf: ScheduledAnnouncementConfig):
        self.conf = conf
        self.init_alarm(conf)

    def init_alarm(self, conf):
        self.alarm = Alarm(conf.times, conf.rules)
        self.alarm.subscribe(self)
        
    def get_config(self) -> ScheduledAnnouncementConfig:
        return self.conf
    
    def edit_config(self, new_conf:ScheduledAnnouncementConfig):
        self.conf = new_conf
        self.init_alarm(new_conf)

    def generate_greeting(self, exclude: list[str] = []) -> str:
        origin = ["Dearest", "Knights"]
        replace_index = 0
        new_word = self.jumble_word(list(origin[replace_index]))
        origin[replace_index] = new_word
        return " ".join(origin) + "!"

    def jumble_word(self, letters: list[str] = []) -> str:
        pass

    def receive_update(self, context):
        pass
