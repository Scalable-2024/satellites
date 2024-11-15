from flask import Blueprint, request, jsonify
from middleware.validators import validate_message_request, validate_route_update
from controllers.message_controller import MessageController
from models.satellite import Satellite


def create_routes(satellite: Satellite) -> Blueprint:
    routes = Blueprint('routes', __name__)
    controller = MessageController(satellite)

    @routes.route('/receive', methods=['POST'])
    @validate_message_request
    def receive_message():
        return controller.handle_receive(request.get_json())

    @routes.route('/send', methods=['POST'])
    @validate_message_request
    def send_message():
        return controller.handle_send(request.get_json())

    @routes.route('/status', methods=['GET'])
    def get_status():
        return jsonify({
            'satellite_id': satellite.satellite_id,
            'routing_table': satellite.routing_table,
            'messages_received': satellite.messages_received,
            'messages_sent': satellite.messages_sent
        })

    @routes.route('/update_routes', methods=['POST'])
    @validate_route_update
    def update_routes():
        data = request.get_json()
        satellite.routing_table = data.get('routes', {})
        return jsonify({'status': 'success'})

    return routes
