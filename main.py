from bot import client, env
from server import run as run_server
import concurrent.futures
import time
import aiohttp, socket


def main():

    while True:

        try:

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(run_server)
                client.run(env["DISCORD_BOT_TOKEN"])
            
        except (aiohttp.ClientError, socket.gaierror, OSError) as exc:
            print(f"Network unavailable: {exc}. Retrying in 30 seconds...")
            time.sleep(INTERNET_CONNECTION_RETRY)


if __name__ == "__main__":

    INTERNET_CONNECTION_RETRY = 600 # seconds
    main()