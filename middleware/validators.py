from functools import wraps
from flask import request, jsonify
from typing import Callable


def validate_message_request(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        required_fields = ['message', 'destination']
        if not all(field in data for field in required_fields):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        if not isinstance(data.get('path', []), list):
            return jsonify({
                'status': 'error',
                'message': 'Path must be a list'
            }), 400

        return f(*args, **kwargs)
    return decorated_function


def validate_route_update(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        if 'routes' not in data or not isinstance(data['routes'], dict):
            return jsonify({
                'status': 'error',
                'message': 'Invalid routes format'
            }), 400

        return f(*args, **kwargs)
    return decorated_function
