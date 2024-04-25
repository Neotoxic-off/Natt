import os
import json
import requests

from scrapper import Scrapper

class DiscordClient:
    def __init__(self, whitelist):
        self.scrapper = Scrapper()
        self.whitelist: list = whitelist

    def run(self):
        self.scrapper.get()

        headers = {
            "Content-Type": "application/json"
        }
        
        for item in self.scrapper.anime:
            payload = {
                "embeds": [
                    {
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
                    }
                ]
            }
        response = requests.post(os.environ.get("DISCORD_WEBHOOKS"), data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            print("Webhook sent successfully!")
        else:
            print(f"Failed to send webhook. Status code: {response.status_code}")
