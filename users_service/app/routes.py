from flask import request, jsonify, Response
from app import app
from app.service import init_service
from app.user import User
from app.exception import NotFound, LoggingError

users_service = init_service()

@app.route('/users', methods=['POST'])
def add_user():
   data = request.get_json()
   new_user = User(type=data['type'], username=data['username'])
   new_user = users_service.add_user(new_user)
   return jsonify({'message': 'User added', 'user': new_user.as_dict()}), 201


@app.route('/users', methods=['GET'])
def get_users():
    api_key = request.args.get('api_key')
    user_type = request.args.get('type')

    if user_type:
       users = users_service.get_users_by_type(user_type)
    elif api_key:
        users = users_service.get_users_by_api_key(api_key)
    else:
        users = users_service.get_all(api_key, user_type)
    return jsonify([user.as_dict() for user in users])


@app.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if not user_id:
        raise ValueError("Invalid or missing user id")

    # Perform the query filtering by the user's name in path
    user = users_service.get_user_by_id(user_id)

    if not user:
        raise NotFound("User not found")
    return jsonify(user.as_dict()), 200

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({'error': str(error)}), 500

@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(NotFound)
def handle_not_found_error(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(LoggingError)
def handle_logging_error(error):
    return jsonify({'error': str(error)}), 500
