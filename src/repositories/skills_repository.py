from src.core import get_skills_table
from src.models import SkillEntry


class SkillsRepository:
    def __init__(self):
        self.table = get_skills_table()

    def insert_skill_entry(self, entry: SkillEntry):
        return self.table.put_item(Item=entry.model_dump())
