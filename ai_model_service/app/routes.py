from app.service import format_prediction_input, predict

from app import app
from flask import request, jsonify, Response

@app.route('/predict', methods=['POST'])
def model_predict():
    try:
        formatted_input = format_prediction_input(request.json)
        prediction:float = predict(formatted_input)
        return jsonify({'prediction': prediction}), 200
    except Exception as e:
        return Response(f"An error occurred: {str(e)}\n", status=500)
