import requests
from datetime import datetime
from app.prediction_input import PredictionInput

def format_prediction_input(json: dict) -> PredictionInput:
    return PredictionInput()

def make_prediction() -> float:
    return 0.5

def log_prediction(prediction: float) -> None:
    """
    Logs a given prediction to log_service
    Args:
        prediction (float): The prediction to be logged.
    """

    service_url = 'http://localhost:5000/log'
    body = {
        'service': 'prediction_service',
        'message': f'Prediction: {prediction}',
        'tag_timestamp': datetime.utcnow().isoformat(),
        'tag_type': 'prediction'
    }

    response = requests.post(service_url, json=body)
    if(response.status_code!= 200):
        print(f"Failed to log prediction: {response.text}")
    else:
        print("Logged prediction successfully")
 
def predict(input: PredictionInput) -> float:
    """
    Given a prediction input, return a prediction of similarity.

    """

    prediction = make_prediction()
    log_prediction(prediction)
    
    return prediction
