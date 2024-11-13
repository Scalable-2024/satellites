import json
import threading
import argparse
from flask import Flask, jsonify, request
import asyncio
from flask_cors import CORS
import websockets

from controllers import get_posn

app = Flask(__name__)
latest_message = None  # Ensure this is defined globally

CORS(app)  # Enable CORS for all URIs and origins

async def websocket_listener(uri):
    global latest_message
    async with websockets.connect(uri) as websocket:
        while True:
            latest_message = await websocket.recv()  # Continuously receive messages
            # print(f"Latest message updated: {latest_message}")


def start_websocket_listener(uri):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_listener(uri))


@app.route('/get_pos', methods=['GET'])
def _():
    arg1 = request.args.get('satellite_name', default=None, type=str)
    return get_posn.test_websocket(latest_message, satellite_key=arg1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Flask server with WebSocket listener.')
    parser.add_argument('--websocket-uri', type=str,
                        required=True, help='WebSocket URI to connect to')
    parser.add_argument('--http-port', type=int, required=True,
                        help='Port for the Flask HTTP server')
    args = parser.parse_args()

    # Start the WebSocket listener in a separate thread
    threading.Thread(target=start_websocket_listener, args=(
        args.websocket_uri,), daemon=True).start()

    # Start the Flask server
    app.run(port=args.http_port, debug=True, use_reloader=False)
