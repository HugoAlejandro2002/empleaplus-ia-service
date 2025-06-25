from unittest.mock import MagicMock, patch

import pytest

from src.models import Contact, ResumeData, SkillEntry
from src.utils.skills_extractor import build_skill_entry


@pytest.fixture
def parsed_resume():
    return ResumeData(
        fullName="Jane Doe",
        contact=Contact(
            email="jane@example.com",
            phone="123456789",
            linkedin="https://linkedin.com/in/janedoe"
        ),
        summary="Software Engineer",
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[]
    )


def test_build_skill_entry(parsed_resume):
    mock_result = MagicMock()
    mock_result.tasks_output = [None, None, MagicMock(raw='{"skills": ["Python", "FastAPI"]}')]

    with patch("src.utils.skills_extractor.generate_uuid", return_value="test-uuid"), \
         patch("src.utils.skills_extractor.clean_json_output", return_value={"skills": ["Python", "FastAPI"]}):
        
        entry = build_skill_entry(parsed_resume, mock_result)

        assert isinstance(entry, SkillEntry)
        assert entry.id == "test-uuid"
        assert entry.name == "Jane"
        assert entry.lastname == "Doe"
        assert entry.email == "jane@example.com"
        assert entry.phone == "123456789"
        assert entry.linkedin == "https://linkedin.com/in/janedoe"
        assert entry.skills == ["Python", "FastAPI"]
