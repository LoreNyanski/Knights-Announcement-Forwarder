from __future__ import annotations

from pathlib import Path
import uuid
import discord
from dataclasses import dataclass

from config import IMAGE_DIR

@dataclass
class Announcement():
    message: str
    images: list[Path]

    @staticmethod
    async def fromDiscord(msg: discord.Message) -> Announcement:
        message = msg.content or ""
        images = await Announcement.download_images(msg)
        return Announcement(message, images)

    @staticmethod
    async def download_images(message: discord.Message) -> list[Path]:
        paths = []
        for attachment in message.attachments:
            if not attachment.content_type or not attachment.content_type.startswith("image/"):
                continue

            suffix = Path(attachment.filename).suffix
            filename = f"{uuid.uuid4()}{suffix}"
            path = IMAGE_DIR / filename

            await attachment.save(path)
            paths.append(path)

        return paths

    def delete_images(self):
        for image in self.images:
            try:
                if image.exists():
                    image.unlink()
            except Exception:
                # log if you want, but never crash cleanup
                pass
        self.images.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.delete_images()