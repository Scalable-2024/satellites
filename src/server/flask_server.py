import json
import threading
from flask import Flask, jsonify
import asyncio
import websockets

app = Flask(__name__)


async def websocket_listener(uri):
    global latest_message
    async with websockets.connect(uri) as websocket:
        while True:
            latest_message = await websocket.recv()  # Continuously receive messages
            # print(f"Latest message updated: {latest_message}")


def start_websocket_listener():
    uri = "ws://localhost:8765"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_listener(uri))


# Start the WebSocket listener in a separate thread
threading.Thread(target=start_websocket_listener, daemon=True).start()


@app.route('/get_pos', methods=['GET'])
def test_websocket():
    if latest_message:
        try:
            return jsonify(json.loads(latest_message))
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON received", "details": str(e)}), 500
    else:
        return jsonify({"error": "No data received yet"}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
