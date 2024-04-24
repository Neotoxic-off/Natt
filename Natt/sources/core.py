import os
import time
import discord

from client import DiscordClient
from scrapper import Scrapper

class Core:
    def __init__(self):
        self.discord_client = None
        self.scrapper = Scrapper()
        self.wait = 43200
        self.run = True

        self.__load_discord_client__()
        self.__run__()

    def __run__(self):
        while (self.run == True):
            self.scrapper.get()
            print(self.scrapper.content)
            self.discord_client.send_anime(
                os.environ.get("DISCORD_CHANNEL"),
                self.scrapper.content
            )
            time.sleep(self.wait)

    def __load_discord_client__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        self.discord_client = DiscordClient(intents=intents)
        self.discord_client.run(
            os.environ.get("DISCORD_TOKEN")
        )
