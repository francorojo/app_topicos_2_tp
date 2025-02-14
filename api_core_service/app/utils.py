from datetime import datetime
import requests
from os import environ
from app.exception import LoggingError, PredictionError, UsersError


BASE_LOG_URL = environ.get('LOGGER_SERVICE_BASE_URL', 'http://localhost:5000')
BASE_USERS_URL = environ.get('USERS_SERVICE_BASE_URL', 'http://localhost:5001')
BASE_AI_MODEL_URL = environ.get('AI_MODEL_SERVICE_BASE_URL', 'http://localhost:5002')


SERVICE_NAME = environ.get('SERVICE_NAME')

if not SERVICE_NAME:
    raise ValueError("SERVICE_NAME environment variable must be set")


def log(message: str, tags: list[tuple[str,str]] = None) -> None:
    
    body = {
        'service': SERVICE_NAME,
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
        raise LoggingError(f"Failed to log: {response.text}")


def user_by_api_key(authorization: str) -> list[dict]:
    response = requests.get(f"{BASE_USERS_URL}/users?api_key={authorization}", json={}, timeout=5)
    if(response.status_code!= 200):
        raise UsersError(f"Failed to get users: {response.text}")
    print(response, flush=True)
    return response.json()


def prediction(real_state_index: int) -> list[dict]:
    response = requests.post(f"{BASE_AI_MODEL_URL}/predict", json={"real_state_index":real_state_index}, timeout=60)
    if(response.status_code!= 200):
        raise PredictionError(f"Failed to get prediction: {response.text}")
    print("test: " + str(response.json()), flush=True)
    return response.json()
