import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from simple_rest_client.api import API

app = Flask(__name__)

# START database Section
# Configure the database to use SQLite in-memory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
   id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
   api_key = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
   type = db.Column(db.String(80), nullable=False)
   username = db.Column(db.String(80), nullable=False, unique=True)

   def as_dict(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# push context manually to app
with app.app_context():
   db.create_all()
# END database Section

# create users api instance
log_api = API(
   api_root_url='http://localhost:8000/',  # base api url
   params={},  # default params
   headers={},  # default headers
   timeout=2,  # default timeout in seconds
   append_slash=False,  # append slash to final url
   json_encode_body=True,  # encode body as json
)
log_api.add_resource(resource_name='log')

# START Log Section
def log_message(message, tag_type):
   body = {'service': "users api - service",
           'message': message,
           'tag_type': tag_type}
   log_api.log.create(body=body, params={}, headers={})
# END Log Section


@app.route('/users', methods=['POST'])
def add_user():
   data = request.get_json()
   new_user = User(type=data['type'], username=data['username'])
   db.session.add(new_user)
   db.session.commit()
   log_message('New username: ' + data['username'] + " - type: " + data['type'], "INFO")
   return jsonify({'message': 'User added', 'user': new_user.as_dict()}), 201


@app.route('/users', methods=['GET'])
def get_users():
   api_key = request.args.get('api_key')
   user_type = request.args.get('type')

   if api_key:
       users = User.query.filter_by(api_key=api_key)
   elif user_type:
       users = User.query.filter_by(type=user_type)
   else:
       users = User.query.all()
   return jsonify([user.as_dict() for user in users])


@app.route('/users/<string:user_id>', methods=['GET'])
def service(user_id):
   if not user_id:
       return jsonify({'error': 'Invalid or missing user id'}), 400

   # Perform the query filtering by the user's name in path
   user = User.query.filter_by(id=user_id).first()

   # Query db
   if user:
       return jsonify({'user_type': user.as_dict()['type'], 'username': user.as_dict()['username']}), 200
   else:
       return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
   app.run(debug=True)
