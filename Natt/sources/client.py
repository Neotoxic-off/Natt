import os
import json
import requests

from scrapper import Scrapper

class DiscordClient:
    def __init__(self, whitelist):
        self.scrapper = Scrapper()
        self.whitelist: list = whitelist

    def __is_whitelisted__(self, item_title):
        for item in self.whitelist:
            if (item.lower() in item_title.lower()):
                return (True)
        return (False)

    def run(self):
        self.scrapper.get()
        embeds = []
        headers = {
            "Content-Type": "application/json"
        }
        messages = []
        
        for item in self.scrapper.anime:
            if ("anime" in item["category"].lower() and self.__is_whitelisted__(item["title"])):
                if (len(embeds) == 10):
                    messages.append(embeds.copy())
                    embeds.clear()

                embeds.append({
                    "title": item["title"],
                    "url": item["link"],
                    "color": 0xce00ff,
                    "thumbnail": {"url": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Nyaa_Logo.png"},
                    "fields": [
                        {"name": "Publication Date", "value": item["pub_date"], "inline": False},
                        {"name": "Category", "value": item["category"], "inline": False},
                        {"name": "Seeders", "value": item["seeders"], "inline": True},
                        {"name": "Leechers", "value": item["leechers"], "inline": True},
                        {"name": "Downloads", "value": item["downloads"], "inline": True},
                        {"name": "Size", "value": item["size"], "inline": False}
                    ]
                })
        if (len(embeds) > 0):
            messages.append(embeds.copy())
            embeds.clear()

        for i in range(0, len(messages)):
            payload = {
                "embeds": messages[i]
            }

            response = requests.post(os.environ.get("DISCORD_WEBHOOKS"), data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                print("Webhook sent successfully!")
            else:
                print(f"Failed to send webhook. Status code: {response.status_code} {response.text}")
