
from app.user import User
from app.database import db
from app.utils import log

class UsersRepository:

    def get_all(self):
        return User.query.all()

    def add_user(self, user: User):
        db.session.add(user)
        db.session.commit()
        print("dadad")
        log('New username: ' + user.username + " - type: " + user.type)

    def get_user_by_api_key(self, api_key: str):
        return User.query.filter_by(api_key=api_key).first()

    def get_users_by_type(self, user_type: str):
        return User.query.filter_by(type=user_type).all()
    
    def get_user_by_id(self, user_id: str):
        return User.query.filter_by(id=user_id).first()
    
