import json

from datetime import datetime

from src.invoker import Invoker

from models.torrent import Torrent


class Notifier:
    def __init__(self, webhook: str, tmdb_api_key: str, invoker: Invoker):
        self.webhook: str = webhook
        self.invoker: Invoker = invoker
        self.api_key: str = tmdb_api_key

    def __retrieve_splash__(self, torrent: Torrent):
        results: list[str] = None
        r = self.invoker.invoke(
            method="GET",
            url="https://api.themoviedb.org/3/search/tv",
            params={
                'api_key': self.api_key,
                'query': torrent.origin
            },
            headers={},
            data={},
            auth={}
        )
        results = r.json()["results"]

        if (len(results) > 0):
            return (f"https://image.tmdb.org/t/p/original/{results[0].get('poster_path')}")

        return ("https://i.redd.it/g9nptsecn0l61.jpg")

    def __build__(self, torrent: Torrent):
        splash = self.__retrieve_splash__(torrent)
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
                "url": splash
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


