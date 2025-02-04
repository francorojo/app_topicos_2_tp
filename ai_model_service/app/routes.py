from app.service import predict, get_properties_from_model

from app import app
from flask import request, jsonify, Response
from app.prediction_input import PredictionInput

def format_prediction_input(json: dict) -> PredictionInput:
    property_index = json.get("real_state_index")

    if property_index is None:
        raise ValueError("Property index is required")
        
    return PredictionInput(property_index)

@app.route('/predict', methods=['POST'])
def model_predict():
    try:
        formatted_input = format_prediction_input(request.json)
        prediction:float = predict(formatted_input)
        return jsonify(prediction), 200
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)

@app.route("/properties", methods=['GET'])
def get_properties():
    try:
        properties = get_properties_from_model()
        return jsonify(properties), 200
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)
