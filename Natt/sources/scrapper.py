import feedparser

class Scrapper:
    def __init__(self):
        self.host = "https://nyaa.land/?page=rss"
        self.wait = 86400
        self.content = None
        self.anime = []
        self.feed = feedparser.parse(self.host)

    def get(self):
        self.__fetch__()

    def __fetch__(self):
        for entry in self.feed.entries:
            title = entry.title
            link = entry.link
            pub_date = entry.published
            seeders = entry.get('nyaa_seeders', '0')  # Default to 0 if not present
            leechers = entry.get('nyaa_leechers', '0')  # Default to 0 if not present
            category = entry.get('nyaa_category')
            downloads = entry.get('nyaa_downloads', 0)
            size = entry.get('nyaa_size')
            info_hash = entry.get('nyaa_infohash')

            description = entry.description

            self.anime.append(
                {
                    "title": title,
                    "link": link,
                    "pub_date": pub_date,
                    "seeders": seeders,
                    "leechers": leechers,
                    "category": category,
                    "downloads": downloads,
                    "size": size,
                    "info_hash": info_hash,
                    "description": description
                }
            )
