import os
import torrentp
import asyncio

from threading import Thread
from torrentp import TorrentDownloader
from urllib.parse import urlparse

from models.torrent import Torrent

from src.invoker import Invoker

class Downloader:
    def __init__(self, destination: str, torrent_folder: str, invoker: Invoker):
        self.destination: str = destination
        self.torrent_folder: str = torrent_folder
        self.invoker: Invoker = invoker
        self.queue: list[Torrent] = []

    def add(self, torrent: Torrent):
        self.queue.append(torrent)

    async def download(self):
        print(f"{len(self.queue)} torrents in queue")
        tasks = []

        for torrent in self.queue:
            tasks.append(self.__download_torrent__(torrent))

        await asyncio.gather(*tasks)
        self.queue.clear()

    async def __download_torrent__(self, torrent):
        path = f"{self.torrent_folder}/{os.path.basename(urlparse(torrent.link).path)}"
        self.__download_torrent_file__(torrent.link, path)
        downloader = TorrentDownloader(path, self.destination)

        await downloader.start_download(download_speed=0, upload_speed=0)
        downloader.stop_download()

    def __download_torrent_file__(self, torrent_file: str, path: str):
        r = self.invoker.invoke(
            method="GET",
            url=torrent_file,
            params=[],
            headers={},
            data={},
            auth={}
        )

        with open(f"{path}", "wb") as f:
            f.write(r.content)
