import asyncio

from src.core import Core

if (__name__ == "__main__"):
    webhook_url: str = "https://test.com"
    anime_whitelist: list[str] = [
        "blue exorcist",
        "evangelion",
        "darling in the franxx"
    ]

    core: Core = Core(webhook_url, anime_whitelist)

    asyncio.run(core.__cycle__())
