import discord
from alarm.Interfaces import SubscriberInterface

class Announcement(SubscriberInterface):

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

    # def recieve_update(context):
    #    pass

    #TODO this has not been tested!!!
    def __str__(self):
        return self.message
    
if __name__ == "__main__":
    pass