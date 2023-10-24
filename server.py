import json
from flask import Flask, request
import asyncio
import os
import traceback
import gunicorn.app.base


app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_post_request():

    try:
        content = request.get_data().decode("utf-8")
        data = json.loads(content)
        if data["authorization"] != os.getenv("AUTHORIZATION_TOKEN"):
            return 'Bad authorization token'
        
        try:
            from dscrd import notifier, client
            asyncio.run_coroutine_threadsafe(notifier(data["message"]), client.loop)

        except Exception:
            return f"""Server error. The Discord bot might not be launched:
                {traceback.format_exc()}
            """

    except Exception:
        return f'''Send JSON data in the format {"message":"...", "authorization":"..."}:
            {traceback.format_exc()}
        '''


class App(gunicorn.app.base.BaseApplication):
    def __init__(self, application, options=None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self.application


def run():

    options = {
        'bind': f'0.0.0.0:{os.getenv("PORT", default=5000)}',
        'workers': 1,
    }

    App(app, options).run()
