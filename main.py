from flask import Flask, request
import os
from dotenv import dotenv_values
import json
import traceback


app = Flask(__name__)


@app.route('/')
def index():
    return '{"Choo Choo": "Welcome to your Flask app 🚅"}'


@app.route("/", methods=["POST"])
def handle_post_request():

    try:
        content = request.get_data().decode("utf-8")
        data = json.loads(content)
        print("data:", data)
        if data["authorization"] != dotenv_values(".env")["AUTHORIZATION_TOKEN"]:
            return 'Bad authorization token'
        
        try:
            return "oui"

        except Exception as e:
            print(e)
            return "Server error. The Discord bot might not be launched"

    except Exception as e:
        return 'Send JSON data in the format {"message":"...", "authorization":"..."}:' + f"\n{e}" + traceback.format_exc()

    return "OK"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))