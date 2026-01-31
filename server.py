from flask import Flask, request, jsonify
import asyncio
from bot import notifier, client, env
import traceback
from functools import wraps



app = Flask(__name__)

def require_at(fn):
    """
    Requirement for authentification token
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        """
        Must be executed at each endpoint before handling the request
        """
        auth = request.headers.get("Authorization", "") # return "" if no "Authorization" provided

        if auth != env["AUTHORIZATION_TOKEN"]:
            return jsonify(error="Bad authorization token"), 401

        return fn(*args, **kwargs)

@app.route("/", methods=["POST"])
@require_at
def handle_post_request():
    """
    Accepts requests in such format:
    POST
    url = http://{env["LISTENER_HOST"]}:{env["LISTENER_PORT"]}
    headers = { "Accept-Charset": "utf-8" , "Authorization": <authorization> }
    payload = {"message": <message>}
    requests.post(url, headers, json=payload)
    """
    try:
        data = request.get_json()  # or force=False and handle None

        if not data:
            return jsonify(error="Invalid or missing JSON"), 400

        if "message" not in data:
            return jsonify(error="Missing 'message'"), 400
        
        try:
            asyncio.run_coroutine_threadsafe(notifier(data["message"]), client.loop)
            return "OK"

        except:
            return jsonify(error=f"""Server error. Error executing the notifier:
                {traceback.format_exc()}"""), 500

    except:
        return jsonify(error=f"""Server error. Error executing the notifier:
                {traceback.format_exc()}"""), 500


@app.route("/ping", methods=["GET"])
@require_at
def ping():
    """
    Endpoint to test connection with this General Notifier
    """
    return jsonify(
        status="ok",
        message="API reachable"
    ), 200


def run():

    HOST = env["LISTENER_HOST"]
    PORT = int(env["LISTENER_PORT"])

    app.run(port=PORT, host=HOST)
