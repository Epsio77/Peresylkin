from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os


class TelegramClient:

    def __init__(self, api_id, api_hash, session):
        self.client = TelegramClient(
            session,
            int(api_id),
            api_hash
        )

        self.client.start()

    def get_new_messages(self, channel, last_id):

        messages = []

        for msg in self.client.iter_messages(channel, limit=20):

            if msg.id <= last_id:
                break

            item = {
                "id": msg.id,
                "text": msg.message or "",
                "photos": [],
                "videos": []
            }

            if msg.media:

                filename = None

                if isinstance(msg.media, MessageMediaPhoto):
                    filename = self.client.download_media(
                        msg,
                        file=f"downloads/{msg.id}"
                    )
                    item["photos"].append(filename)

                elif isinstance(msg.media, MessageMediaDocument):
                    filename = self.client.download_media(
                        msg,
                        file=f"downloads/{msg.id}"
                    )

                    if filename.lower().endswith((".mp4", ".mov", ".avi")):
                        item["videos"].append(filename)
                    else:
                        item["photos"].append(filename)

            messages.append(item)

        messages.reverse()

        return messages
