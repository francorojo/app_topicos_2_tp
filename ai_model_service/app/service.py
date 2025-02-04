import requests
from datetime import datetime
from app.prediction_input import PredictionInput
from app.model import RealStatePredictor
from app.utils import log
import json


model = RealStatePredictor()

def predict_similars(property_index: int) -> float:
    return model.predict_best_similars(property_index)


def log_prediction(property_index:int, similar_predictions: list) -> None:
    log(f'{similar_predictions}', [('property_index', str(property_index) )])
 
def predict(predictionInput: PredictionInput) -> float:
    """
    Given a prediction input, return a prediction of similarity.

    """

    similar_real_states = predict_similars(predictionInput.property_index)

    try:
        log_prediction(predictionInput.property_index, similar_real_states)
    except Exception as e:
        print(f"Failed to log prediction: {str(e)}")
    
    return similar_real_states
