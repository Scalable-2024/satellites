import subprocess
import time
import sys
import requests
import json
import os
from typing import Dict, List


class NetworkManager:
    def __init__(self):
        self.network_map = {
            'A': 5001,
            'B': 5002,
            'C': 5003,
            'D': 5004,
            'E': 5005
        }
        self.processes = {}

    def check_satellite(self, satellite_id: str) -> bool:
        """Check if a satellite is responding"""
        port = self.network_map[satellite_id]
        try:
            response = requests.get(
                f'http://localhost:{port}/status', timeout=1)
            return response.status_code == 200
        except:
            return False

    def wait_for_satellite(self, satellite_id: str, timeout: int = 10) -> bool:
        """Wait for a satellite to become responsive"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_satellite(satellite_id):
                return True
            time.sleep(0.5)
        return False

    def start_satellite(self, satellite_id: str) -> None:
        """Start a single satellite"""
        print(f"Starting satellite {satellite_id}...")
        cmd = f"./run_satellite.sh {satellite_id}"

        # Create log file
        log_path = f"logs/satellite_{satellite_id}.log"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, 'w') as log_file:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=log_file,
                stderr=log_file
            )
            self.processes[satellite_id] = process

        # Wait for satellite to become responsive
        if not self.wait_for_satellite(satellite_id):
            print(f"Warning: Satellite {satellite_id} may not have started properly")

    def start_network(self) -> None:
        """Start all satellites in the network"""
        print("Starting satellite network...")

        # Clear old routes file
        if os.path.exists('config/routes.json'):
            os.remove('config/routes.json')

        # Start satellites in sequence
        for satellite_id in self.network_map.keys():
            self.start_satellite(satellite_id)
            print(f"Satellite {satellite_id} started on port {self.network_map[satellite_id]}")
            time.sleep(2)  # Wait between starts

        print("\nChecking network status...")
        all_running = True
        for satellite_id in self.network_map.keys():
            status = self.check_satellite(satellite_id)
            print(f"Satellite {satellite_id}: {'RUNNING' if status else 'NOT RESPONDING'}")
            all_running = all_running and status

        if all_running:
            print("\nAll satellites are running!")
            print("\nExample commands:")
            print("1. Check status of satellite A:")
            print("   curl http://localhost:5001/status")
            print("\n2. Send message from A to D:")
            print(
                '   curl -X POST http://localhost:5001/send -H "Content-Type: application/json" -d \'{"message": "Test message", "destination": "D", "path": []}\'')
        else:
            print("\nWarning: Some satellites failed to start")

    def stop_network(self) -> None:
        """Stop all satellites"""
        print("Stopping satellite network...")
        for satellite_id, process in self.processes.items():
            print(f"Stopping satellite {satellite_id}...")
            process.terminate()
            process.wait()


if __name__ == "__main__":
    network = NetworkManager()
    try:
        network.start_network()
        print("\nPress Ctrl+C to stop the network")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping network...")
        network.stop_network()
        print("Network stopped")
