from bot import client
from server import run
import concurrent.futures
from dotenv import dotenv_values




if __name__ == "__main__":

    env = dotenv_values(".env")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run), client.run(env["DISCORD_BOT_TOKEN"])]
