import os
import asyncio

from src.core import Core

if (__name__ == "__main__"):
    webhook_url: str = os.environ.get("DISCORD_WEBHOOKS")
    anime_whitelist: list[str] = [
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

    core: Core = Core(webhook_url, anime_whitelist)

    asyncio.run(core.__cycle__())
