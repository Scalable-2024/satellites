import random
from flask import jsonify
from typing import Dict, List, Optional, Tuple, Any
from models.satellite import Satellite
from helpers.network_utils import send_request
import logging

logger = logging.getLogger(__name__)


class MessageController:
    def __init__(self, satellite: Satellite):
        self.satellite = satellite

    def find_available_path(self, destination: str, current_path: List[str]) -> Optional[List[str]]:
        if destination not in self.satellite.routing_table:
            return None

        # Get all possible paths
        possible_paths = self.satellite.routing_table[destination]

        # Shuffle paths to maintain randomness
        random.shuffle(possible_paths)

        for path in possible_paths:
            next_hop = path[0]  # First satellite in the path
            try:
                # Test if next hop is reachable
                response = send_request(
                    f'http://localhost:{
                        self.satellite.network_map[next_hop]}/status',
                    'GET',
                    retries=1  # Quick check
                )
                if response.get('status') != 'error':
                    return path
            except Exception:
                continue

        return None

    def handle_send(self, data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        try:
            message = data.get('message')
            destination = data.get('destination')
            current_path = data.get('path', [])

            logger.info(f"Handling send request from {
                        self.satellite.satellite_id} to {destination}")

            if self.satellite.satellite_id in current_path:
                return jsonify({
                    'status': 'error',
                    'message': 'Loop detected'
                }), 400

            current_path.append(self.satellite.satellite_id)

            # If we're the destination
            if destination == self.satellite.satellite_id:
                self.satellite.add_received_message(
                    message, current_path[0], current_path)
                return jsonify({
                    'status': 'success',
                    'message': 'Message delivered',
                    'path': current_path
                }), 200

            # Find an available path
            next_path = self.find_available_path(destination, current_path)

            if not next_path:
                return jsonify({
                    'status': 'error',
                    'message': 'No available route to destination - some satellites might be offline'
                }), 404

            next_hop = next_path[0]
            try:
                response = send_request(
                    f'http://localhost:{
                        self.satellite.network_map[next_hop]}/send',
                    'POST',
                    {
                        'message': message,
                        'destination': destination,
                        'path': current_path
                    }
                )

                if response.get('status') == 'success':
                    self.satellite.add_sent_message(
                        message, destination, current_path)

                return jsonify(response), 200

            except Exception as e:
                logger.error(f"Failed to send message: {str(e)}")
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to send message: {str(e)}'
                }), 500

        except Exception as e:
            logger.error(f"Error in handle_send: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to process send request: {str(e)}'
            }), 500
