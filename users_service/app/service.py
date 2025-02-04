from app.repository import UsersRepository
from app.user import User

class UsersService:

    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    def add_user(self, user: User):
        self.users_repository.add_user(user)
        return user

    def get_all(self, api_key: str, user_type: str):
        return self.users_repository.get_all()
    
    def get_users_by_api_key(self, api_key: str) -> list[User]:
        if not api_key:
           raise ValueError("API key is required")
        return self.users_repository.get_user_by_api_key(api_key)
      
    def get_users_by_type(self, user_type: str):
        if not user_type:
            raise ValueError("User type is required")
        return self.users_repository.get_users_by_type(user_type)
    
    def get_user_by_id(self, user_id: str) -> User:
        if not user_id:
            raise ValueError("User ID is required")
        return self.users_repository.get_user_by_id(user_id)


def init_service() -> UsersService:
    users_repository = UsersRepository()
    return UsersService(users_repository)
