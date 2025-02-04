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
    formatted_input = format_prediction_input(request.json)
    validate_input(formatted_input)
    prediction:float = predict(formatted_input)
    return jsonify(prediction), 200

def validate_input(input: PredictionInput) -> None:
    if not isinstance(input.property_index, int):
        raise ValueError("Property index must be an integer")
    if input.property_index < 0:
        raise ValueError("Property index must be positive")
    if input.property_index not in get_properties_from_model():
        raise ValueError("Property index does not exist in the dataset")

@app.route("/properties", methods=['GET'])
def get_properties():
    properties = get_properties_from_model()
    return jsonify(properties), 200

@app.errorhandler(ValueError)
def handle_value_error(error):
    return Response(f"Invalid input: {str(error)}\n", status=400)

@app.errorhandler(Exception)
def handle_exception(error):
    return Response(f"An error occurred: {str(error)}\n", status=500)
