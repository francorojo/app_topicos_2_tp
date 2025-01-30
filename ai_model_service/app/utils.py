from datetime import datetime
import requests

service_url = 'http://localhost:5000/log'


def log(message: str, tag: str = None) -> None:
    body = {
        'service': 'prediction_service',
        'message': message,
        'tag_timestamp': datetime.utcnow().isoformat(),
        'tag_type': 'prediction'
    }

    response = requests.post(service_url, json=body, timeout=5)
    if(response.status_code!= 200):
        raise f"Failed to log: {response.text}"
