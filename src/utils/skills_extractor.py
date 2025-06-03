from typing import Any

from models import ResumeData, SkillEntry

from .json_cleaner import clean_json_output
from .uuid_generator import generate_uuid


def build_skill_entry(parsed_resume: ResumeData, result: Any) -> SkillEntry:
    """
    Construye un SkillEntry combinando los datos ya parseados del currículum
    (ResumeData) y las skills extraídas por el agente (result.tasks[2]).
    """
    skills_data = clean_json_output(result.tasks_output[2].raw)
    print
    skills_list = skills_data.get("skills", [])

    name_parts = parsed_resume.fullName.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    return SkillEntry(
        id=generate_uuid(),
        name=first_name,
        lastname=last_name,
        phone=parsed_resume.contact.phone,
        email=parsed_resume.contact.email,
        linkedin=parsed_resume.contact.linkedin,
        skills=skills_list
    )