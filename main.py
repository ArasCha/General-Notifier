from dscrd import client
from server import App, options, app
import concurrent.futures
import os
import asyncio
from threading import Thread



if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(client.start(os.getenv("DISCORD_BOT_TOKEN")))
    Thread(target=loop.run_forever).start()

    App(app, options).run()
        