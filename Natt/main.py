import os
import asyncio

from src.core import Core

if (__name__ == "__main__"):
    webhook_url: str = ""
    tmdb_api_key: str = ""
    library: str = "Anime"

    core: Core = Core(webhook_url, tmdb_api_key, library)

    asyncio.run(core.cycle())
