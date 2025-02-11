from app.exception import LoggingError, PredictionError, UsersError
from app.utils import log, prediction
from flask import request, jsonify
from app.__init__ import get_user_type_rate_limit
from app import app
from app import limiter


@app.route('/service', methods=['POST'])
@limiter.limit(lambda: get_user_type_rate_limit())
def service():
   authorization = request.headers.get('Authorization')
   data = request.get_json()

   if not data:
       log('Key user: ' + authorization + " - Invalid or missing JSON data", "ERROR")
       raise ValueError("Invalid or missing JSON data")
   else:
       predictionModel = prediction(data.get('real_state_index'))

   log('New request key user: ' + authorization + " - Result: " + predictionModel, "INFO")
   return jsonify(predictionModel), 200

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({'error': str(error)}), 500

@app.errorhandler(UsersError)
def handle_users_error(error):
    return jsonify({'error': str(error)}), 500

@app.errorhandler(LoggingError)
def handle_logging_error(error):
    return jsonify({'error': str(error)}), 500

@app.errorhandler(PredictionError)
def handle_prediction_error(error):
    return jsonify({'error': str(error)}), 500

@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({'error': str(error)}), 400
