from dscrd import starte
from server import run

import concurrent.futures




if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(starte), executor.submit(run)]
