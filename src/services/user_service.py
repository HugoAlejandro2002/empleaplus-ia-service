from models import UserDB
from repositories import UsersRepository


class UserService:
    def __init__(self):
        self.users_repo = UsersRepository()

    def get_user_by_email(self, email: str) -> UserDB | None:
        return self.users_repo.get_user_by_email(email)
