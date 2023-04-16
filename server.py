import json
from dotenv import dotenv_values
from http.server import BaseHTTPRequestHandler, HTTPServer
from dscrd import notifier, client
import asyncio


# async def run_notifier(data):
#     await notifier(data)

class MyRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body)

            status_code = 200
            status = "success"
            # proc = asyncio.create_task(run_notifier(data))
            client.loop.create_task(notifier(data))

        except json.decoder.JSONDecodeError:
            status_code = 400
            status = "fail"
        # except:
        #     status_code = 500
        #     status = "server error"

        # do something with the data (e.g., store it in a database)
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {'status': status}
        if status_code == 400:
            response["message"] = "Please give JSON"
        self.wfile.write(json.dumps(response).encode('utf-8'))



def run():

    env = dotenv_values(".env")
    HOST = env["LISTENER_HOST"]
    PORT = int(env["LISTENER_PORT"])

    server = HTTPServer((HOST, PORT), MyRequestHandler)
    print(f"Server listening on http://{HOST}:{PORT}")
    server.serve_forever()
    server.close()
    print("Server stopped")

    # client request example: curl -X POST -H "Content-Type: application/json" -H "Accept-Charset: utf-8" -d '{"key": "😘"}' http://localhost:8889