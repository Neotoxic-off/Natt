from src.downloader import Downloader
from src.invoker import Invoker
from src.notifier import Notifier
from src.nyaa_parser import NyaaParser

from models.torrent import Torrent

class Core:
    def __init__(self, webhook: str, whitelist: list[str]):
        self.invoker: Invoker = Invoker()
        self.downloader: Downloader = Downloader("Anime", self.invoker)
        self.notifier: Notifier = Notifier(
            webhook,
            self.invoker
        )
        self.parser: NyaaParser = NyaaParser()

        self.torrents: list[Torrent] = []
        self.whitelist: list[str] = whitelist

    async def __cycle__(self):
        content: str = self.__rss__()

        if (content != None):
            self.torrents = self.parser.parse(content)
            for torrent in self.torrents:
                if (torrent.category.lower().startswith("anime") == True):
                    if (self.__is_whitelisted__(torrent.title) == True):
                        self.notifier.send(torrent)
                        self.downloader.add(torrent)
            await self.downloader.download()

    def __is_whitelisted__(self, title: str):
        for anime in self.whitelist:
            if (anime.lower() in title.lower()):
                return (True)
        return (False)

    def __rss__(self):
        r = self.invoker.invoke(
            method="GET",
            url="https://nyaa.land",
            params=[
                ("page", "rss")
            ],
            headers={},
            data={},
            auth={}
        )

        if (r.status_code == 200):
            return (r.text)
        return (None)

