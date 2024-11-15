from flask import Flask
from typing import Dict, List
import time


class Satellite:
    def __init__(self, satellite_id: str, port: int, network_map: Dict[str, int]):
        self.app = Flask(__name__)
        self.satellite_id = satellite_id
        self.port = port
        self.network_map = network_map
        self.routing_table: Dict[str, List[str]] = {}
        self.messages_received = []
        self.messages_sent = []
        self.ready = False  # Flag to indicate if satellite is ready

    def initialize(self, routing_table: Dict[str, List[str]]):
        """Initialize the satellite with routing table"""
        self.routing_table = routing_table
        self.ready = True

    def add_received_message(self, message: str, sender: str, path: List[str]):
        self.messages_received.append({
            'message': message,
            'sender': sender,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'path': path
        })

    def add_sent_message(self, message: str, destination: str, path: List[str]):
        self.messages_sent.append({
            'message': message,
            'destination': destination,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'path': path
        })
