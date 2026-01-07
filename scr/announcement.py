import discord
import random
from alarm_lib import Alarm

class AnnouncementManager():
    pass

class Announcement(Alarm):

    # Base init
    # TODO Replace list type with something thats not a discord attachment
    def __init__(self, message: str, images: list[discord.Attachment] = None):
        self.message = message
        self.images = images

    @staticmethod
    def fromDiscord(message: discord.Message):
        msg = message.content
        img = message.attachments
        return Announcement(msg, img)

    def generate_greeting(self, exclude: list[str] = []) -> str:
        origin = ["Dearest", "Knights"]
        replace_index = 0
        new_word = self.jumble_word(list(origin[replace_index]))
        origin[replace_index] = new_word
        return " ".join(origin) + "!"

    def jumble_word(self, letters: list[str] = []) -> str:
        pass