from decimal import Decimal
from typing import Any

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

    def to_str_if_decimal(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return str(value)
        return value

    def convert_resume_item(self, item: dict) -> dict:
        # Convierte los campos anidados con Decimal a str
        if "education" in item:
            for edu in item["education"]:
                edu["startYear"] = self.to_str_if_decimal(edu.get("startYear"))
                edu["endYear"] = self.to_str_if_decimal(edu.get("endYear"))

        if "certifications" in item:
            for cert in item["certifications"]:
                cert["year"] = self.to_str_if_decimal(cert.get("year"))

        return item

    def get_resume_by_id(self, resume_id: str) -> ResumeData | None:
        response = self.table.get_item(Key={"id": resume_id})
        item = response.get("Item")
        if item:
            item = self.convert_resume_item(item)
            return ResumeData(**item)
        return None
