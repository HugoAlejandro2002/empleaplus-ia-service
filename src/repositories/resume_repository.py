from src.core import get_resumes_table
from src.models import ResumeData
from src.utils import generate_uuid


class ResumeRepository:
    def __init__(self):
        self.table = get_resumes_table()

    def insert_resume(self, resume: ResumeData) -> str:
        resume_id = generate_uuid()
        item = resume.model_dump()
        item["id"] = resume_id
        self.table.put_item(Item=item)
        return resume_id

    def get_resume_by_id(self, resume_id: str) -> ResumeData | None:
        response = self.table.get_item(Key={"id": resume_id})
        item = response.get("Item")
        if item:
            return ResumeData(**item)
        return None
