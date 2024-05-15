import os
import torrentp

from torrentp import TorrentDownloader
from urllib.parse import urlparse

from models.torrent import Torrent

from src.invoker import Invoker

class Downloader:
    def __init__(self, destination: str, invoker: Invoker):
        self.destination: str = destination
        self.invoker: Invoker = invoker
        self.queue: list[Torrent] = []

    def add(self, torrent: Torrent):
        self.queue.append(torrent)

    async def download(self):
        downloader: TorrentDownloader = None
        path: str = None

        print(f"{len(self.queue)} torrents in queue")
        for torrent in self.queue:
            path = os.path.basename(urlparse(torrent.link).path)
            self.__download_torrent_file__(torrent.link, path)
            downloader = TorrentDownloader(path, self.destination)

            await downloader.start_download(download_speed=0, upload_speed=0)
            downloader.stop_download()

        self.queue.clear()

    def __download_torrent_file__(self, torrent_file: str, path: str):
        r = self.invoker.invoke(
            method="GET",
            url=torrent_file,
            params=[],
            headers={},
            data={},
            auth={}
        )

        with open(path, "wb") as f:
            f.write(r.content)
