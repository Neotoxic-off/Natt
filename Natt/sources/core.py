from client import DiscordClient

class Core:
    def __init__(self):
        self.whitelist = []
        self.discord_client = DiscordClient(self.whitelist)
        
        self.__run__()
        
    def __run__(self):
        self.discord_client.run()


