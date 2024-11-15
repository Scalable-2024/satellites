import requests
from typing import Dict, Any
import logging
from time import sleep

logger = logging.getLogger(__name__)


def send_request(url: str, method: str, data: Dict[str, Any] = None, retries: int = 3) -> Dict[str, Any]:
    last_exception = None

    for attempt in range(retries):
        try:
            logger.info(f"Attempt {attempt + 1} to {method} {url}")
            if method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=5)
            else:
                response = requests.get(url, timeout=5)

            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()

        except requests.RequestException as e:
            last_exception = e
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries - 1:
                sleep(1)  # Wait before retrying

    # If we get here, all retries failed
    error_message = f"Request failed after {
        retries} attempts: {str(last_exception)}"
    logger.error(error_message)
    return {
        'status': 'error',
        'message': error_message
    }


def initialize_satellite(port: int, routes: Dict[str, Any]) -> bool:
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
