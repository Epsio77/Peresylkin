import os
import json
from telegram_client import TelegramClient
from vk_client import VKClient

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_id": 0}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=4)


def main():
    state = load_state()

    tg = TelegramClient(
        api_id=os.environ["TG_API_ID"],
        api_hash=os.environ["TG_API_HASH"],
        session="telegram"
    )

    vk = VKClient(
        token=os.environ["VK_TOKEN"],
        group_id=os.environ["VK_GROUP_ID"]
    )

    messages = tg.get_new_messages(
        channel=os.environ["TG_CHANNEL"],
        last_id=state["last_id"]
    )

    if not messages:
        print("Новых сообщений нет.")
        return

    for message in messages:

        print(f"Публикуем {message['id']}")

        vk.publish(message)

        state["last_id"] = message["id"]

    save_state(state)


if __name__ == "__main__":
    main()
