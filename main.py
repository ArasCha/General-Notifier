from dscrd import start
from server import run
import concurrent.futures
import os




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run), executor.submit(start)]