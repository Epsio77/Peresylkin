from telethon.sync import TelegramClient
import os

api_id = int(input("API ID: "))
api_hash = input("API HASH: ").strip()

client = TelegramClient("telegram", api_id, api_hash)

client.start()

print()
print("Авторизация успешно завершена.")
print("Файл telegram.session создан.")
