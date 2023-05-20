import json
from dotenv import dotenv_values
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
async def handle_post_request():
    content = request.get_data().decode("utf-8")
    from dscrd import notifier, client

    try:
        data = json.loads(content)
        if data["authorization"] != dotenv_values(".env")["AUTHORIZATION_TOKEN"]:
            return 'Bad authorization token'
        try:
            await notifier(data["message"])
            # client.loop.create_task(notifier(data["message"]))
            # will be the same thing, just remove the async before function name

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

    # client request example:
    # curl -X POST -H "Content-Type: application/json" -H "Accept-Charset: utf-8" -d '{"message":"qsldkf", "authorization":"mdrrr"}' http://localhost:8889