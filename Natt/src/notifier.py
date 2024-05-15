import json

from datetime import datetime

from src.invoker import Invoker

from models.torrent import Torrent


class Notifier:
    def __init__(self, webhook: str, invoker: Invoker):
        self.webhook: str = webhook
        self.invoker: Invoker = invoker

    def __retrieve_splash__(self, torrent: Torrent):
        query = """
            query ($title: String) {
                Media (search: $title, type: ANIME) {
                    title
                    {
                        romaji
                        english
                        native
                    }
                    coverImage
                    {
                        large
                    }
                }
            }
        """
        variables = {
            "title": torrent.title
        }

        r = self.invoker.invoke(
            method="POST",
            url="https://graphql.anilist.co",
            params=[],
            headers={},
            data={
                "query": query,
                "variables": variables
            },
            auth={}
        )

        return r.json().get("data", {}).get("Media")

    def __build__(self, torrent: Torrent):
        splash = self.__retrieve_splash__(torrent).get("coverImage")

        embed = {
            "title": torrent.title,
            "fields": [
                {"name": "Seeders", "value": torrent.seeders, "inline": True},
                {"name": "Leechers", "value": torrent.leechers, "inline": True},
                {"name": "Downloads", "value": torrent.downloads, "inline": True},
                {"name": "Category", "value": torrent.category, "inline": True},
                {"name": "Size", "value": torrent.size, "inline": True}
            ],
            "color": 16711680,
            "image": {
                "url": splash.get("large") if splash != None else "https://nyaa.land/static/img/icons/nyaa/1_1.png"
            },
            "timestamp": datetime.now().isoformat()
        }

        return (embed)

    def send(self, torrent: Torrent):
        payload = self.__build__(torrent)
        payload_json = json.dumps({
            "embeds": [
                payload
            ]
        })

        r = self.invoker.invoke(
            method="POST",
            url=self.webhook,
            params=[],
            data=payload_json,
            headers={
                "Content-Type": "application/json"
            },
            auth={}
        )


