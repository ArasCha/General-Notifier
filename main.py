from flask import Flask, request
import os
import json
import traceback


app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_post_request():

    try:
        content = request.get_data().decode("utf-8")
        data = json.loads(content)
        if data["authorization"] != os.getenv("AUTHORIZATION_TOKEN"):
            return 'Bad authorization token'
        
        try:
            return "oui"

        except Exception:
            return f"""Server error. The Discord bot might not be launched:
                {traceback.format_exc()}
            """

    except Exception:
        return f'''Send JSON data in the format {"message":"...", "authorization":"..."}:
            {traceback.format_exc()}
        '''


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))