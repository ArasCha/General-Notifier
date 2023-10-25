from dscrd import client
from server import App, options, app
import concurrent.futures
import os
import asyncio




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [App(app, options).run(), asyncio.run(client.start(os.getenv("DISCORD_BOT_TOKEN")))]
        