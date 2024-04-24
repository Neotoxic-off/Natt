import time
import requests

import xml.etree.ElementTree as ET

class Scrapper:
    def __init__(self):
        self.host = "https://nyaa.land/?page=rss"
        self.wait = 86400
        self.content = None
        self.is_running = True
        self.anime = []

    def get(self):
        self.__fetch__()
        self.anime.clear()

    def __fetch__(self):
        r = requests.get(self.host)

        if (r.status_code == 200):
            self.content = self.text
        else:
            self.content = None
    
    def __extract__(self):
        root = None

        if (self.content != None):
            root = ET.fromstring(self.content)

            for item in root.findall('.//item'):
                category = item.find('nyaa:category').text
                if ("anime" in category.lower()):
                    self.anime.append({
                        "title": item.find('title').text,
                        "link": item.find('link').text
                    })
