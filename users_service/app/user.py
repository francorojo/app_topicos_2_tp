import uuid
from app.database import db


# Define a User model
class User(db.Model):
   id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
   api_key = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
   type = db.Column(db.String(80), nullable=False)
   username = db.Column(db.String(80), nullable=False, unique=True)

   def as_dict(self):
       return {col.name: getattr(self, col.name) for col in self.__table__.columns}
