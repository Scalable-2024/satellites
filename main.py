import asyncio
import click
from hypercorn.config import Config
from hypercorn.asyncio import serve
from models.satellite import Satellite
from routes.message_routes import create_routes
from helpers.route_generator import RouteManager
import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(satellite_id: str) -> logging.Logger:
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(f'satellite_{satellite_id}')
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        f'logs/satellite_{satellite_id}.log',
        maxBytes=1024*1024,
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def create_app(satellite_id: str, port: int, network_map: dict):
    logger = setup_logging(satellite_id)

    # Get consistent routes for all satellites
    routes = RouteManager.get_or_create_routes(list(network_map.keys()))

    satellite = Satellite(satellite_id, port, network_map)
    satellite.routing_table = routes[satellite_id]  # Set routes directly

    app = satellite.app
    routes_blueprint = create_routes(satellite)
    app.register_blueprint(routes_blueprint)
    app.logger = logger

    return app


@click.command()
@click.option('--id', required=True, help='Satellite ID (e.g., A, B, C)')
@click.option('--port', required=True, type=int, help='Port number')
@click.option('--network', required=True, help='Network map in format "A:5001,B:5002,C:5003"')
def main(id: str, port: int, network: str):
    try:
        network_map = dict(pair.split(':') for pair in network.split(','))
        network_map = {k: int(v) for k, v in network_map.items()}
    except ValueError:
        click.echo(
            "Error: Network map should be in format 'A:5001,B:5002,C:5003'")
        return

    if id not in network_map:
        click.echo(f"Error: Satellite ID {id} not found in network map")
        return

    if network_map[id] != port:
        click.echo(f"Error: Port {
                   port} doesn't match network map for satellite {id}")
        return

    app = create_app(id, port, network_map)

    print(f"Starting satellite {id} on port {port}")

    config = Config()
    config.bind = [f"0.0.0.0:{port}"]
    config.workers = 1
    config.accesslog = f"logs/access_{id}.log"
    config.errorlog = f"logs/error_{id}.log"

    asyncio.run(serve(app, config))


if __name__ == "__main__":
    main()
