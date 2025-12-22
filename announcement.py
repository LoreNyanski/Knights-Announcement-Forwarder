import discord
import re

class Announcement:

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
    
    # TODO
    def fromWhatsapp(self, message):
        return Announcement(None, None)

    # in case whatsapp was the primary channel
    def translate_wha_dsc(self) -> str:
        pass

    # in case whatsapp was the primary channel
    def translate_wha_tel(self) -> str:
        # too lazy to implement properly lol
        ret = self.translate_wha_dsc()
        orig = self.message
        self.message = ret
        ret = self.translate_dsc_tel()
        self.message = orig
        return ret
    
    def translate_dsc_wha(self) -> str:
        text = self.message

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

    def translate_dsc_tel(self) -> str:
        text = self.message
        
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

        return text

# Testing
if __name__ == "__main__":
    msg = "# Hello **World** this is *italic* and ~~crossed~~ and __under__ and ||hidden||"
    anc = Announcement(msg)
    # doesn't actually work unless the method is static
    # print(Announcement.translate_telegram(msg))
    print(anc.translate_dsc_tel())