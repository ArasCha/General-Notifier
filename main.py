import asyncio
from dscrd import start
from server import run



async def async_launch_server():
    return await asyncio.to_thread(run)

async def async_launch_bot():
    return await asyncio.to_thread(start)

async def main():
    await asyncio.gather(async_launch_server(), async_launch_bot())


if __name__ == "__main__":
    asyncio.run(main())