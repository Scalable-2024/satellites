import json
import os


class NetworkConfig:
    def __init__(self):
        self.network_map = {
            'A': 5001,
            'B': 5002,
            'C': 5003,
            'D': 5004,
            'E': 5005
        }

    def save_config(self):
        with open('config/network.json', 'w') as f:
            json.dump(self.network_map, f)

    @staticmethod
    def load_config():
        with open('config/network.json', 'r') as f:
            return json.load(f)

    @staticmethod
    def get_satellite_config(satellite_id: str):
        network_map = NetworkConfig.load_config()
        return {
            'id': satellite_id,
            'port': network_map[satellite_id],
            'network_map': network_map
        }
