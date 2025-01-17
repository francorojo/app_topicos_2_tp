import uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Configure the database to use SQLite in-memory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database
db = SQLAlchemy(app)




# Define a simple model
class User(db.Model):
   id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # TODO cambiar key por ir para identificacion
   api_key = db.Column(db.String(36), default=lambda: str(uuid.uuid4())) # TODO sumarlo como query param
   type = db.Column(db.String(80), nullable=False)
   username = db.Column(db.String(80), nullable=False, unique) # TODO buscar como setear unique


   def as_dict(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}




# push context manually to app
with app.app_context():
   db.create_all()




# Add a user
@app.route('/users', methods=['POST'])
def add_user():
   data = request.get_json()
   new_user = User(type=data['type'])
   db.session.add(new_user)
   db.session.commit()
   return jsonify({'message': 'User added', 'user': new_user.as_dict()}), 201




# Get all users
@app.route('/users', methods=['GET'])
def get_users():
   user_type = request.args.get('type')  # Get the 'type' parameter


   if not user_type:
       users = User.query.all()
   else:
       users = User.query.filter_by(type=user_type)
   return jsonify([user.as_dict() for user in users])




@app.route('/users/<string:user_key>', methods=['GET'])
def service(user_key):
   if not user_key:
       return jsonify({'error': 'Invalid or missing user key'}), 400


   # Example operations
   print(f"User key: {user_key}")


   # Perform the query filtering by the user's name in path
   user = User.query.filter_by(key=user_key).first()


   # Query db
   if user:
       return jsonify({'user_type': user.as_dict()['type']}), 200
   else:
       return jsonify({'error': 'User not found'}), 404




if __name__ == '__main__':
   app.run(debug=True)
