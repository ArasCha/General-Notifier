import discord
from flask import Flask, request
import asyncio

app = Flask(__name__)
client = discord.Client()

bot_token = "MTA5NjkxNjA2NDIxNjAzMTM2NQ.G_7PTc.ivxDzG6lNSU9VeZzm_tcuLKdojZeLEiGkceM0g"
channel_id = "1096869715160350751"

@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@app.route("/", methods=["POST"])
def handle_post_request():
    content = request.get_data().decode("utf-8")
    client.loop.create_task(send_to_discord(content))
    return "OK"

async def send_to_discord(content):
    channel = client.get_channel(int(channel_id))
    await channel.send(content)

# ----------------------------------------------------



def launch_server():
    app.run(port=8009)
    
def launch_bot():
    client.run(bot_token)

async def async_launch_server():
    return await asyncio.to_thread(launch_server)

async def async_launch_bot():
    return await asyncio.to_thread(launch_bot)

async def main():
    await asyncio.gather(async_launch_server(), async_launch_bot())


if __name__ == "__main__":
    asyncio.run(main())
