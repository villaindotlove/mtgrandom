import json
import os
import random
import time
from urllib.parse import urlparse

import requests


class MidjourneyApi():
    def __init__(self, prompt, application_id, guild_id, channel_id, version, id, authorization):
        self.application_id = application_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.version = version
        self.id = id
        self.authorization = authorization
        self.prompt = prompt
        self.message_id = ""
        self.custom_id = ""
        self.image_path_str = ""
        self.send_message()
        self.get_message()
        self.choose_images()
        self.download_image()

    def send_message(self):
        url = "https://discord.com/api/v9/interactions"
        data = {
            "type": 2,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "session_id": "cannot be empty",
            "data": {
                "version": self.version,
                "id": self.id,
                "name": "imagine",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": self.prompt
                    }
                ],
                "application_command": {
                    "id": self.id,
                    "application_id": self.application_id,
                    "version": self.version,
                    "default_member_permissions": None,
                    "type": 1,
                    "nsfw": False,
                    "name": "imagine",
                    "description": "Create images with Midjourney",
                    "dm_permission": True,
                    "contexts": None,
                    "options": [
                        {
                            "type": 3,
                            "name": "prompt",
                            "description": "The prompt to imagine",
                            "required": True
                        }
                    ]
                },
                "attachments": []
            },
        }
        headers = {
            'Authorization': self.authorization,
            'Content-Type': 'application/json',
        }
        # print("Sending message", headers, data)
        response = requests.post(url, headers=headers, json=data)

    def get_message(self):
        headers = {
            'Authorization': self.authorization,
            "Content-Type": "application/json",
        }
        for i in range(3):
            time.sleep(random.uniform(25, 35))
            try:
                response = requests.get(f'https://discord.com/api/v9/channels/{self.channel_id}/messages', headers=headers)
                messages = response.json()
                most_recent_message_id = messages[0]['id']
                # print("Messages", messages)
                self.message_id = most_recent_message_id
                components = messages[0]['components'][0]['components']
                buttons = [comp for comp in components if comp.get('label') in ['U1', 'U2', 'U3', 'U4']]
                custom_ids = [button['custom_id'] for button in buttons]
                random_custom_id = random.choice(custom_ids)
                self.custom_id = random_custom_id
                break
            except:
                ValueError("Timeout")

    def choose_images(self):
        url = "https://discord.com/api/v9/interactions"
        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
        }
        data = {
            "type": 3,
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "message_flags": 0,
            "message_id": self.message_id,
            "application_id": self.application_id,
            "session_id": "cannot be empty",
            "data": {
                "component_type": 2,
                "custom_id": self.custom_id,
            }
        }
        # print("Choosing images", headers, data)
        response = requests.post(url, headers=headers, data=json.dumps(data))

    def download_image(self):
        headers = {
            'Authorization': self.authorization,
            "Content-Type": "application/json",
        }
        for i in range(3):
            time.sleep(random.uniform(25, 35))
            try:
                response = requests.get(f'https://discord.com/api/v9/channels/{self.channel_id}/messages', headers=headers)
                messages = response.json()
                most_recent_message_id = messages[0]['id']
                # print("Downloading image", messages)
                self.message_id = most_recent_message_id
                image_url = messages[0]['attachments'][0]['url']
                image_response = requests.get(image_url)
                a = urlparse(image_url)
                image_name = os.path.basename(a.path)
                self.image_path_str = f"images/{image_name}"
                if not os.path.exists('images'):
                    os.makedirs('images')
                with open(f"images/{image_name}", "wb") as file:
                    file.write(image_response.content)
                break
            except Exception as e:
                # print("Got error downloading image:", e)
                raise ValueError("Timeout")

    def image_path(self):
        return self.image_path_str

if __name__ == "__main__":
    MJ_APPLICATION_ID = os.environ["MJ_APPLICATION_ID"]
    MJ_GUILD_ID = os.environ["MJ_GUILD_ID"]
    MJ_CHANNEL_ID = os.environ["MJ_CHANNEL_ID"]
    MJ_VERSION = os.environ["MJ_VERSION"]
    MJ_ID = os.environ["MJ_ID"]
    MJ_AUTHORIZATION = os.environ["MJ_AUTHORIZATION"]

    midjourney = MidjourneyApi(prompt="Awesome wizard battle but both wizards are birds", application_id=MJ_APPLICATION_ID, guild_id=MJ_GUILD_ID, channel_id=MJ_CHANNEL_ID, version=MJ_VERSION, id=MJ_ID, authorization=MJ_AUTHORIZATION)

    # print("Final image:", midjourney.image_path())
