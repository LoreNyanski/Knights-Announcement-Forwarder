from __future__ import annotations

from pathlib import Path
import uuid
import discord
from dataclasses import dataclass

from config import IMAGE_DIR

@dataclass
class Announcement():
    message: str
    attachments: list[Path]

    @staticmethod
    async def fromDiscord(msg: discord.Message) -> Announcement:
        message = msg.content or ""
        attachments = await Announcement.download_attachments(msg)
        return Announcement(message, attachments)

    @staticmethod
    async def download_attachments(message: discord.Message) -> list[Path]:
        paths = []
        for attachment in message.attachments:
            suffix = Path(attachment.filename).suffix or ""
            filename = attachment.filename or f"{uuid.uuid4()}{suffix}"
            path = IMAGE_DIR / filename

            await attachment.save(path)
            paths.append(path)

        return paths

    def delete_attachments(self):
        for image in self.attachments:
            try:
                if image.exists():
                    image.unlink()
            except Exception:
                pass
        self.attachments.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.delete_attachments()