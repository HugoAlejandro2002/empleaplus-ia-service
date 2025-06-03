from typing import List

from pydantic import BaseModel


class SkillEntry(BaseModel):
    id: str
    name: str
    lastname: str
    phone: str
    email: str
    linkedin: str
    skills: List[str]
