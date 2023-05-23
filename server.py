import json
from dotenv import dotenv_values
from flask import Flask, request
import asyncio


app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_post_request():
    content = request.get_data().decode("utf-8")
    from dscrd import notifier, client

    try:
        data = json.loads(content)
        if data["authorization"] != dotenv_values(".env")["AUTHORIZATION_TOKEN"]:
            return 'Bad authorization token'
        try:
            asyncio.run_coroutine_threadsafe(notifier(data["message"]), client.loop)

        except Exception as e:
            print(e)
            return "Server error. The Discord bot might not be launched"

    except:
        return 'Send JSON data in the format {"message":"...", "authorization":"..."}'

    return "OK"


def run():

    env = dotenv_values(".env")
    HOST = env["LISTENER_HOST"]
    PORT = int(env["LISTENER_PORT"])

    app.run(port=PORT, host=HOST)
