from flask_sqlalchemy import SQLAlchemy


# Initialize the database

db = SQLAlchemy()


# Import User model
from app.user import User

def init_database(app):
   db.init_app(app)

   with app.app_context():
      db.create_all()
