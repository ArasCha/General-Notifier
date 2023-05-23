import discord
from datetime import datetime
from dotenv import dotenv_values
from discord.ext import commands
import asyncio



client = commands.Bot(command_prefix = '!')

running = True

config = dotenv_values(".env")
notification_channel = int(config["DISCORD_CHANNEL"])


#-----------------------------------------------------------------------------------------


@client.event
async def on_ready() -> None:

    print("Bot ready")


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

    messages: list[discord.Message] = await get_previous_msgs(context.channel)

    nb = int(nb)

    if nb > len(messages):
        nb = len(messages)

    for i in range(nb):
        try:
            await messages[i].delete()
        except discord.errors.HTTPException:
            print("discord.errors.HTTPException: currently waiting and retrying")
            await asyncio.sleep(5)
            await messages[i].delete()


#-------------------------------------NOTIFIER-----------------------------------------


async def notifier(msg:str) -> None:
    
    channel: discord.TextChannel = client.get_channel(notification_channel)

    await clean_old_msgs(channel)
    if not await already_sent(msg, channel):
        await channel.send(msg)


async def get_previous_msgs(channel: discord.TextChannel) -> list[discord.Message]:
    
    messages: list[discord.Message] = []
    async for message in channel.history(limit=200):
        messages.append(message)
    return messages


async def clean_old_msgs(channel: discord.TextChannel):
    
    messages = await get_previous_msgs(channel)

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


def set_running(val:bool) -> None:
    import dscrd as ds
    ds.running = val


# ---------------------------------------------------------------------------


def starte():
    client.run(config["DISCORD_BOT_TOKEN"])
