from dscrd import client
from server import App, app, options
import concurrent.futures
import os




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [App(app, options).run(), client.run(os.getenv("DISCORD_BOT_TOKEN"))]