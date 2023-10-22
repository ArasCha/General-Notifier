from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


@app.route("/", methods=["POST"])
def handle_post_request():

    try:
        print("a request is received")
        return "si"
        content = request.get_data().decode("utf-8")
        data = json.loads(content)
        if data["authorization"] != dotenv_values(".env")["AUTHORIZATION_TOKEN"]:
            return 'Bad authorization token'
        
        try:
            return "oui"

        except Exception as e:
            print(e)
            return "Server error. The Discord bot might not be launched"

    except Exception as e:
        return 'Send JSON data in the format {"message":"...", "authorization":"..."}:' + f"\n{e}"

    return "OK"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))