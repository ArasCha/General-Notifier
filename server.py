import json
from flask import Flask, request
import asyncio
from bot import notifier, client, env
import traceback



app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_post_request():

    try:
        content = request.get_data().decode("utf-8")
        data = json.loads(content)
        if data["authorization"] != env["AUTHORIZATION_TOKEN"]:
            return 'Bad authorization token'
        
        try:
            asyncio.run_coroutine_threadsafe(notifier(data["message"]), client.loop)
            return "OK"

        except:
            return f"""Server error. Error executing the notifier:
                {traceback.format_exc()}"""
            
    except:
        return f"""Server error:
            {traceback.format_exc()}"""



def run():

    HOST = env["LISTENER_HOST"]
    PORT = int(env["LISTENER_PORT"])

    app.run(port=PORT, host=HOST)
