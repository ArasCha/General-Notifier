from dscrd import start
from server import run
import concurrent.futures
import os
import asyncio



async def func():
    await asyncio.gather(asyncio.to_thread(run), asyncio.to_thread(start))

if __name__ == "__main__":

    
    asyncio.run(func())
    