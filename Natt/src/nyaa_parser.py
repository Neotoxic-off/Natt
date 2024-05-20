from xml.dom.minidom import parseString

from models.torrent import Torrent

class NyaaParser:
    def __init__(self):
        pass

    def parse(self, content: str) -> list[Torrent]:
        torrents: list[Torrent] = []
        torrent: Torrent = None
        document = parseString(content)
        items = document.getElementsByTagName("item")

        for item in items:
            title = item.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
            link = item.getElementsByTagName('link')[0].firstChild.nodeValue.strip()
            guid = item.getElementsByTagName('guid')[0].firstChild.nodeValue.strip()
            publication = item.getElementsByTagName('pubDate')[0].firstChild.nodeValue.strip()
            seeders = item.getElementsByTagName('nyaa:seeders')[0].firstChild.nodeValue.strip()
            leechers = item.getElementsByTagName('nyaa:leechers')[0].firstChild.nodeValue.strip()
            downloads = item.getElementsByTagName('nyaa:downloads')[0].firstChild.nodeValue.strip()
            hash = item.getElementsByTagName('nyaa:infoHash')[0].firstChild.nodeValue.strip()
            category = item.getElementsByTagName('nyaa:category')[0].firstChild.nodeValue.strip()
            size = item.getElementsByTagName('nyaa:size')[0].firstChild.nodeValue.strip()

            torrent: Torrent = self.__build_torrent__(title, link, guid, publication, seeders, leechers, downloads, hash, category, size, None)

            torrents.append(torrent)

        return (torrents)

    def __build_torrent__(self,
        title: str,
        link: str,
        guid: str,
        publication: str,
        seeders: str,
        leechers: str,
        downloads: str,
        hash: str,
        category: str,
        size: str,
        origin: str
    ) -> Torrent:

        return (
            Torrent(
                title,
                link,
                guid,
                publication,
                seeders,
                leechers,
                downloads,
                hash,
                category,
                size,
                origin
            )
        )