import os

from urllib.parse import urlparse
from threading import Thread

from src.library import Library
from src.downloader import Downloader
from src.invoker import Invoker
from src.notifier import Notifier
from src.nyaa_parser import NyaaParser

from models.torrent import Torrent

class Core:
    def __init__(self, webhook: str, tmdb_api_key: str, collection: str):
        self.collection: str = collection
        self.invoker: Invoker = Invoker()
        self.library: Library = Library(self.collection)
        self.downloader: Downloader = Downloader(self.collection, "Torrents", self.invoker)
        self.notifier: Notifier = Notifier(
            webhook,
            tmdb_api_key,
            self.invoker
        )
        self.parser: NyaaParser = NyaaParser()

        self.torrents: list[Torrent] = []
        self.whitelist: list[str] = self.library.collection

    def __load_whitelist__(self, path: str):
        anime: list[str] = []

        with open(path, 'r') as f:
            anime = f.read().split('\n')

        return (anime)

    async def cycle(self):
        content: str = self.__rss__()
        threads: list[Thread] = []

        if (content != None):
            self.torrents = self.parser.parse(content)
            for torrent in self.torrents:
                threads.append(Thread(target=self.__download_torrent__, args=(torrent, )))
                threads[len(threads) - 1].start()
            for thread in threads:
                thread.join()
            await self.downloader.download()

    def __download_torrent__(self, torrent: Torrent):
        origin: str = None

        if (torrent.category.lower().startswith("anime") == True and self.__is_downloaded__(torrent) == False):
            origin = self.__is_whitelisted__(torrent.title)
            if (origin != None):
                torrent.origin = origin
                self.notifier.send(torrent)
                self.downloader.add(torrent)

    def __is_downloaded__(self, torrent: Torrent):
        return (os.path.basename(urlparse(torrent.link).path) in os.listdir(self.downloader.torrent_folder))

    def __is_whitelisted__(self, title: str):
        for anime in self.whitelist:
            if (anime.lower() in title.lower()):
                return (anime.lower())
        return (None)

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

