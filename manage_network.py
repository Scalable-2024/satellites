import json
import os
import sys
import subprocess
import time
from typing import Dict


class NetworkManager:
    CONFIG_FILE = 'config/network.json'
    ROUTES_FILE = 'config/routes.json'
    BASE_PORT = 5001

    def __init__(self):
        self.load_config()

    def load_config(self):
        """Load existing network configuration"""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                self.network_map = json.load(f)
        except FileNotFoundError:
            self.network_map = {}

    def save_config(self):
        """Save network configuration"""
        os.makedirs('config', exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.network_map, f, indent=2)

    def add_node(self, node_id: str) -> bool:
        """Add a new node to the network"""
        if node_id in self.network_map:
            print(f"Node {node_id} already exists!")
            return False

        # Assign next available port
        used_ports = set(self.network_map.values())
        new_port = max(used_ports) + 1 if used_ports else self.BASE_PORT

        # Add new node
        self.network_map[node_id] = new_port
        self.save_config()

        # Clear existing routes
        if os.path.exists(self.ROUTES_FILE):
            os.remove(self.ROUTES_FILE)

        print(f"Added node {node_id} on port {new_port}")
        print("Routes have been cleared and will be regenerated on next start")
        return True

    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the network"""
        if node_id not in self.network_map:
            print(f"Node {node_id} does not exist!")
            return False

        del self.network_map[node_id]
        self.save_config()

        # Clear existing routes
        if os.path.exists(self.ROUTES_FILE):
            os.remove(self.ROUTES_FILE)

        print(f"Removed node {node_id}")
        print("Routes have been cleared and will be regenerated on next start")
        return True

    def list_nodes(self):
        """List all nodes in the network"""
        print("\nCurrent Network Configuration:")
        print("------------------------------")
        for node_id, port in sorted(self.network_map.items()):
            print(f"Node {node_id}: Port {port}")

    def restart_network(self):
        """Restart the entire network"""
        # Kill existing processes
        subprocess.run(['pkill', '-f', 'python main.py'])
        time.sleep(2)  # Wait for processes to die

        # Start network
        subprocess.Popen(['python', 'run_network.py'])
        print("\nNetwork is restarting...")
        print("Wait a few seconds for all nodes to initialize")


if __name__ == "__main__":
    manager = NetworkManager()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_network.py add <node_id>")
        print("  python manage_network.py remove <node_id>")
        print("  python manage_network.py list")
        print("  python manage_network.py restart")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add" and len(sys.argv) == 3:
        manager.add_node(sys.argv[2])
    elif command == "remove" and len(sys.argv) == 3:
        manager.remove_node(sys.argv[2])
    elif command == "list":
        manager.list_nodes()
    elif command == "restart":
        manager.restart_network()
    else:
        print("Invalid command!")
