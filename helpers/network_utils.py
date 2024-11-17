import requests
from typing import Dict, Any
import logging
from time import sleep, time
import random
from config.constants import MIN_LATENCY, MAX_LATENCY, MESSAGE_LOSS_PROBABILITY

logger = logging.getLogger(__name__)


def send_request(url: str, method: str, data: Dict[str, Any] = None, retries: int = 3) -> Dict[str, Any]:
    """
    Sends an HTTP request with added simulation for latency, jitter, and interference.

    Args:
        url (str): The target URL for the request.
        method (str): The HTTP method ('GET' or 'POST').
        data (Dict[str, Any]): The JSON payload for POST requests.
        retries (int): The number of retry attempts for the request.

    Returns:
        Dict[str, Any]: The JSON response or an error dictionary.
    """
    last_exception = None

    for attempt in range(retries):
        try:
            # Simulate latency and jitter
            latency = random.uniform(MIN_LATENCY, MAX_LATENCY)
            sleep(latency)

            # Simulate interference: Random chance to drop the request
            if random.random() < MESSAGE_LOSS_PROBABILITY:
                logger.warning(f"[Interference] Request to {url} dropped due to interference.")
                continue  # Skip this attempt

            logger.info(f"Attempt {attempt + 1} to {method} {url} (Simulated Latency: {latency:.2f}s)")
            
            # Perform the HTTP request
            if method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=5)
            else:
                response = requests.get(url, timeout=5)

            response.raise_for_status()  # Raise exception for HTTP error codes
            return response.json()

        except requests.RequestException as e:
            last_exception = e
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries - 1:
                sleep(1)  # Wait before retrying

    # If we get here, all retries failed
    error_message = f"Request failed after {retries} attempts: {str(last_exception)}"
    logger.error(error_message)
    return {
        'status': 'error',
        'message': error_message
    }


def initialize_satellite(port: int, routes: Dict[str, Any]) -> bool:
    """
    Initializes a satellite by updating its routing table via an HTTP request.

    Args:
        port (int): The port of the satellite to initialize.
        routes (Dict[str, Any]): The routing table for the satellite.

    Returns:
        bool: True if initialization was successful, False otherwise.
    """
    try:
        response = send_request(
            f'http://localhost:{port}/update_routes',
            'POST',
            {'routes': routes}
        )
        return response.get('status') == 'success'
    except Exception as e:
        logger.error(f"Failed to initialize satellite: {str(e)}")
        return False
