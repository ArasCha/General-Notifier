from bot import client, env
from server import run as run_server
import concurrent.futures




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_server), client.run(env["DISCORD_BOT_TOKEN"])]
