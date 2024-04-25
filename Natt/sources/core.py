from client import DiscordClient

class Core:
    def __init__(self):
        self.whitelist = [
            "orverlord",
            "Solo Leveling",
            "The Misfit of Demon King Academy",
            "Blue Exorcist",
            "Chainsaw Man",
            "Darling in the franxx",
            "Darwin's Game",
            "Food wars",
            "Grisaia no Kajitsu",
            "Rakudai Kishi no Cavalry",
            "I Got a Cheat Skill in Another World and Became Unrivaled in The Real World Too",
            "Sekai Saikou no Ansatsusha, Isekai Kizoku ni Tensei Suru",
            "Shinmai Maou no Testament",
            "Sky High Survival"
        ]
        self.discord_client = DiscordClient(self.whitelist)
        
        self.discord_client.run()
