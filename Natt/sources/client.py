import discord

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if (message.author == self.user):
            return

    async def send_anime(self, channel_name: str, animes: list):
        for anime in animes:
            embed = discord.Embed(title=anime["title"], url=anime["link"])
            channel = discord.utils.get(self.get_all_channels(), name=channel_name)
            await channel.send(embed)
