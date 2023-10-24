from dscrd import client
from server import run
import concurrent.futures
import os




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run), client.run(os.getenv("DISCORD_BOT_TOKEN"))]