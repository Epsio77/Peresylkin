import os
import requests


class VKClient:

    API = "https://api.vk.com/method/"
    VERSION = "5.199"

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = str(group_id).replace("-", "")

    def call(self, method, params):

        params["access_token"] = self.token
        params["v"] = self.VERSION

        r = requests.post(
            self.API + method,
            data=params
        ).json()

        if "error" in r:
            raise Exception(r["error"])

        return r["response"]

    def upload_photo(self, filename):

        server = self.call(
            "photos.getWallUploadServer",
            {
                "group_id": self.group_id
            }
        )

        with open(filename, "rb") as f:

            upload = requests.post(
                server["upload_url"],
                files={"photo": f}
            ).json()

        saved = self.call(
            "photos.saveWallPhoto",
            {
                "group_id": self.group_id,
                "photo": upload["photo"],
                "server": upload["server"],
                "hash": upload["hash"]
            }
        )

        p = saved[0]

        return f"photo{p['owner_id']}_{p['id']}"

    def publish(self, message):

        attachments = []

        for photo in message["photos"]:
            attachments.append(
                self.upload_photo(photo)
            )

        self.call(
            "wall.post",
            {
                "owner_id": f"-{self.group_id}",
                "from_group": 1,
                "message": message["text"],
                "attachments": ",".join(attachments)
            }
        )

        print("Опубликовано:", message["id"])
