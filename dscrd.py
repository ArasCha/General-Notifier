import discord
from datetime import datetime
from dotenv import dotenv_values
from discord.ext import commands
import asyncio



client = commands.Bot(command_prefix = '/')

running = True

config = dotenv_values(".env")
notification_channel = int(config["DISCORD_CHANNEL"])


#-----------------------------------------------------------------------------------------


# décorateur pour les coroutines (équivalent des promesses en JS):
@client.event # Pour dire que la fonction on_ready est une fonction d'événements.
async def on_ready() -> None: # lorsque l'on a lancé le bot par client.run()
    
    print("Bot ready")
    await notifier("coucoue")

    # async def issou():
    #     while True:
    #         if running:
    #             await prg()
    #         await asyncio.sleep(60)
    
    # prog = asyncio.create_task(issou())


#---------------------------------------COMMANDS-----------------------------------------


@client.command()
async def status(context:commands.Context) -> None:

    if running:
        await context.send("Le programme est en cours de fonctionnement")
    else:
        await context.send("Le programme est arrêté")

@client.command()
async def stop(context:commands.Context) -> None:

    if running:
        set_running(False)
        await context.send("Le programme s'arrête")
        print("Restarting...")
    else:
        await context.send("Le programme est déjà arrêté")

@client.command()
async def start(context:commands.Context) -> None:

    if not running:
        set_running(True)
        await context.send("Le programme se redémarre")
        print("Stopped")
    else:
        await context.send("Le programme est déjà démarré")


@client.command()
async def clear(context:commands.Context, nb) -> None: # delete the last nb messages

    channel: discord.TextChannel = client.get_channel(notification_channel)
    messages: list[discord.Message] = await get_previous_msgs(channel)

    nb = int(nb)

    if nb > len(messages):
        nb = len(messages)

    for i in range(nb):
        await messages[i].delete()


#-------------------------------------NOTIFIER-----------------------------------------


async def notifier(msg:str) -> None:
    print("message:", msg)
    channel: discord.TextChannel = client.get_channel(notification_channel)
    await channel.send(msg)
    # await clean_old_msgs(channel)
    # if not await already_sent(msg, channel):
    #     await send_msg(msg)


async def send_msg(msg:str) -> None:

    channel: discord.TextChannel = client.get_channel(notification_channel)
    await channel.send(msg)


async def get_previous_msgs(channel: discord.TextChannel) -> list[discord.Message]:
    
    messages: list[discord.Message] = []
    async for message in channel.history(limit=200):
        messages.append(message)
    return messages


async def clean_old_msgs(channel: discord.TextChannel):
    
    messages = await asyncio.create_task(get_previous_msgs(channel))

    for msg in messages:
        now = datetime.now()
        one_day = datetime(2000, 1, 2, 0, 0, 0) - datetime(2000, 1, 1, 0, 0, 0)

        if now - msg.created_at > one_day:
            await msg.delete()


async def already_sent(msg:str, channel:discord.TextChannel) -> bool:

    messages: list[discord.Message] = await get_previous_msgs(channel)

    for message in messages:
        if message.content == msg:
            return True

    return False


def not_async_notifier(msg:str):
    asyncio.run(notifier(msg))


def set_running(val:bool) -> None:
    import dscrd as ds
    ds.running = val


# ---------------------------------------------------------------------------


def start():
    client.run(config["DISCORD_BOT_TOKEN"])