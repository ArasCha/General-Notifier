from flask import Flask, request, jsonify
import asyncio
from bot import notifier, client, env
import traceback



app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_post_request():
    """
    Accepts requests in such format:
    POST
    url = http://{env["LISTENER_HOST"]}:{env["LISTENER_PORT"]}
    headers = { "Accept-Charset": "utf-8" }
    payload = {"authorization": <authorization>, "message": <message>}
    requests.post(url, headers, json=payload)
    """
    try:
        data = request.get_json()  # or force=False and handle None

        if not data:
            return jsonify(error="Invalid or missing JSON"), 400

        if "authorization" not in data or "message" not in data:
            return jsonify(error="Missing 'authorization' or 'message'"), 400

        if data["authorization"] != env["AUTHORIZATION_TOKEN"]:
            return jsonify(error="Bad authorization token"), 401
        
        try:
            asyncio.run_coroutine_threadsafe(notifier(data["message"]), client.loop)
            return "OK"

        except:
            return jsonify(error=f"""Server error. Error executing the notifier:
                {traceback.format_exc()}"""), 500

    except:
        return jsonify(error=f"""Server error. Error executing the notifier:
                {traceback.format_exc()}"""), 500



def run():

    HOST = env["LISTENER_HOST"]
    PORT = int(env["LISTENER_PORT"])

    app.run(port=PORT, host=HOST)
