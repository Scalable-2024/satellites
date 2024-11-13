import json
from flask import jsonify


def test_websocket(latest_message, satellite_key=None):
    if latest_message:
        try:
            data = json.loads(latest_message)
            if satellite_key:
                if satellite_key in data:
                    return jsonify({satellite_key: data[satellite_key]})
                else:
                    return jsonify({"error": f"{satellite_key} not found in data"}), 404
            else:
                return jsonify(data)
        except json.JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON received", "details": str(e)}), 500
    else:
        return jsonify({"error": "No data received yet"}), 500
