from typing import Any

from models import (
    Certification,
    Contact,
    Education,
    Experience,
    Language,
    ResumeData,
    Skill,
)


def parse_resume_json(data: dict[str, Any]) -> ResumeData:
    return ResumeData(
        fullName=data["fullName"],
        contact=Contact(**data["contact"]),
        summary=data["summary"],
        education=[
            Education(
                institution=edu["institution"],
                degree=edu["degree"],
                startYear=edu.get("startDate", ""),
                endYear=edu.get("endDate", ""),
                description=edu.get("description", "")
            )
            for edu in data.get("education", [])
        ],
        experience=[
            Experience(
                company=exp.get("company"),
                position=exp.get("role"),
                startDate=exp.get("startDate") or "",
                endDate=exp.get("endDate") or "",
                responsibilities=exp.get("achievements", []),
            )
            for exp in data.get("experience", [])
        ],
        skills=[
            Skill(**skill) for skill in data.get("skills", [])
        ],
        languages=[
            Language(**lang) for lang in data.get("languages", [])
        ],
        certifications=[
            Certification(**cert) for cert in data.get("certifications", [])
        ]
    )
