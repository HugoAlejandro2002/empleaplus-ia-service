from core import get_users_table
from models import ResumeReference, UserDB


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
     
    def append_resume_entry(self, email: str, resume_ref: ResumeReference):
        self.table.update_item(
            Key={"email": email},
            UpdateExpression="SET cvs = list_append(if_not_exists(cvs, :empty_list), :entry)",
            ExpressionAttributeValues={
                ":entry": [resume_ref.model_dump()],
                ":empty_list": []
            }
        )

    def remove_resume_reference(self, email: str, resume_id: str) -> bool:
        user = self.get_user_by_email(email)
        if not user:
            return False

        updated_cvs = [entry.model_dump() for entry in user.cvs if entry.id != resume_id]
        if len(updated_cvs) == len(user.cvs):
            return False

        self.table.update_item(
            Key={"email": email},
            UpdateExpression="SET cvs = :cvs",
            ExpressionAttributeValues={":cvs": updated_cvs}
        )
        return True
    
    def rename_resume_filename(self, email: str, resume_id: str, new_filename: str) -> bool:
        user = self.get_user_by_email(email)
        if not user:
            return False

        updated = False
        updated_cvs = []
        for entry in user.cvs:
            if entry.id == resume_id:
                entry.filename = new_filename
                updated = True
            updated_cvs.append(entry.model_dump())

        if not updated:
            return False

        self.table.update_item(
            Key={"email": email},
            UpdateExpression="SET cvs = :cvs",
            ExpressionAttributeValues={":cvs": updated_cvs}
        )
        return True

