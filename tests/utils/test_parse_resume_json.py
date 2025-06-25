import pytest
from pydantic import ValidationError

from src.models import ResumeData
from src.utils import parse_resume_json


def test_parse_resume_json_full_data():
    raw_data = {
        "fullName": "Jane Doe",
        "contact": {
            "email": "jane@example.com",
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/janedoe"
        },
        "summary": "Experienced software engineer.",
        "education": [
            {
                "institution": "Tech University",
                "degree": "B.Sc. Computer Science",
                "startDate": "2015",
                "endDate": "2019",
                "description": "Graduated with honors"
            }
        ],
        "experience": [
            {
                "company": "Dev Company",
                "role": "Backend Developer",
                "startDate": "2020",
                "endDate": "2023",
                "achievements": ["Improved API response time by 50%"]
            }
        ],
        "skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "FastAPI", "level": "Intermediate"}
        ],
        "languages": [
            {"name": "English", "proficiency": "Native"},
            {"name": "Spanish", "proficiency": "Intermediate"}
        ],
        "certifications": [
            {"name": "AWS Certified Developer", "institution": "Amazon", "year": 2022}
        ]
    }

    parsed = parse_resume_json(raw_data)

    assert isinstance(parsed, ResumeData)
    assert parsed.fullName == "Jane Doe"
    assert parsed.contact.email == "jane@example.com"
    assert parsed.education[0].degree == "B.Sc. Computer Science"
    assert parsed.experience[0].responsibilities[0].startswith("Improved")
    assert parsed.skills[1].name == "FastAPI"
    assert parsed.languages[0].proficiency == "Native"
    assert parsed.certifications[0].institution == "Amazon"

def test_parse_resume_json_invalid_contact_field():
    """Test de error: linkedin con valor inválido (None)"""
    raw_data = {
        "fullName": "Jane Doe",
        "contact": {
            "email": "jane@example.com",
            "phone": "123456789",
            "linkedin": None  # <-- inválido, espera str
        },
        "summary": "Software Developer",
        "education": [],
        "experience": [],
        "skills": [],
        "languages": [],
        "certifications": []
    }

    with pytest.raises(ValidationError) as exc_info:
        parse_resume_json(raw_data)

    assert "linkedin" in str(exc_info.value)
    assert "Input should be a valid string" in str(exc_info.value)


def test_parse_resume_json_missing_required_field():
    """Test de error: falta campo requerido 'email' en contact"""
    raw_data = {
        "fullName": "Jane Doe",
        "contact": {
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/jane"
            # Falta 'email'
        },
        "summary": "Software Developer",
        "education": [],
        "experience": [],
        "skills": [],
        "languages": [],
        "certifications": []
    }

    with pytest.raises(ValidationError) as exc_info:
        parse_resume_json(raw_data)

    assert "email" in str(exc_info.value)
    assert "Field required" in str(exc_info.value)