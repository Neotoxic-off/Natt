class Torrent:
    def __init__(self,
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
    ) -> None:
        
        self.title: str = title
        self.link: str = link
        self.guid: str = guid
        self.publication: str = publication
        self.seeders: str = seeders
        self.leechers: str = leechers
        self.downloads: str = downloads
        self.hash: str = hash
        self.category: str = category
        self.size: str = size
        self.origin: str = origin
