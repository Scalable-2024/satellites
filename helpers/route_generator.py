import random
import json
import os
from typing import Dict, List


class RouteManager:
    ROUTES_FILE = 'config/routes.json'

    @staticmethod
    def generate_routes(satellites: List[str], max_hops: int = 2) -> Dict[str, Dict[str, List[str]]]:
        """Generate consistent routes for all satellites"""
        routes = {}
        for source in satellites:
            routes[source] = {}
            for dest in satellites:
                if source != dest:
                    # Create direct path if possible
                    if random.random() < 0.7:  # 70% chance of direct path
                        routes[source][dest] = [[dest]]
                    else:
                        # Create path with one intermediate hop
                        intermediate = random.choice(
                            [s for s in satellites if s != source and s != dest])
                        routes[source][dest] = [[intermediate, dest]]
        return routes

    @staticmethod
    def save_routes(routes: Dict[str, Dict[str, List[str]]]) -> None:
        """Save routes to file"""
        os.makedirs('config', exist_ok=True)
        with open(RouteManager.ROUTES_FILE, 'w') as f:
            json.dump(routes, f)

    @staticmethod
    def load_routes() -> Dict[str, Dict[str, List[str]]]:
        """Load routes from file"""
        try:
            with open(RouteManager.ROUTES_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    @staticmethod
    def get_or_create_routes(satellites: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Get existing routes or create new ones"""
        routes = RouteManager.load_routes()
        if not routes:
            routes = RouteManager.generate_routes(satellites)
            RouteManager.save_routes(routes)
        return routes
