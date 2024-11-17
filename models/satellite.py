from flask import Flask
from typing import Dict, List
import time
import random
from config.constants import MIN_LATENCY, MAX_LATENCY, MESSAGE_LOSS_PROBABILITY


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
        # Simulate interference: Randomly drop messages
        if random.random() < MESSAGE_LOSS_PROBABILITY:
            print(f"[Interference] Message from {sender} lost due to interference.")
            return  # Exit the method if the message is lost

        # Simulate latency and jitter
        latency = random.uniform(MIN_LATENCY, MAX_LATENCY)
        time.sleep(latency)

        # Log the received message
        self.messages_received.append({
            'message': message,
            'sender': sender,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'path': path
        })
        print(f"[Received] Message from {sender}: '{message}' (Latency: {latency:.2f}s)")

    def add_sent_message(self, message: str, destination: str, path: List[str]):
        # Simulate interference: Randomly drop messages
        if random.random() < MESSAGE_LOSS_PROBABILITY:
            print(f"[Interference] Message to {destination} lost due to interference.")
            return  # Exit the method if the message is lost

        # Simulate latency and jitter
        latency = random.uniform(MIN_LATENCY, MAX_LATENCY)
        print(f"[Latency] Simulated latency for sending message: {latency:.2f}s")  # Log latency
        time.sleep(latency)

        # Log the sent message
        self.messages_sent.append({
            'message': message,
            'destination': destination,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'path': path
        })
        print(f"[Sent] Message to {destination}: '{message}' (Latency: {latency:.2f}s)")
        