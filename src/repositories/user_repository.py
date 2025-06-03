from core import get_users_table
from models import UserDB


class UsersRepository:
    def __init__(self):
        self.table = get_users_table()

    def insert_user(self, user: UserDB):
        return self.table.put_item(Item=user.model_dump())

    def get_user_by_email(self, email: str) -> UserDB | None:
        response = self.table.get_item(Key={"email": email})
        item = response.get("Item")
        if item:
            return UserDB(**item)
        return None
