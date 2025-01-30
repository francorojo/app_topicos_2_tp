from datetime import datetime
import requests
from os import environ

BASE_LOG_URL = environ.get('LOGGER_SERVICE_BASE_URL', 'http://localhost:5000')

print(f"Using LOGGER_SERVICE_BASE_URL: {BASE_LOG_URL}")


def log(message: str, tags: list[tuple[str,str]] = None) -> None:
    body = {
        'service': 'prediction_service',
        'message': message,
        'tag_timestamp': datetime.utcnow().isoformat(),
        'tag_type': 'prediction'
    }

    # add tags to the body if provided
    if tags:
        for tag in tags:
            body[f'tag_{tag[0]}'] = tag[1]

    response = requests.post(f"{BASE_LOG_URL}/log", json=body, timeout=5)
    if(response.status_code!= 200):
        raise f"Failed to log: {response.text}"
