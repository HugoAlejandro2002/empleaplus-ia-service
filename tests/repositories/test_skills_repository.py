from unittest.mock import MagicMock, patch

import pytest

from src.models import SkillEntry
from src.repositories.skills_repository import SkillsRepository


@pytest.fixture
def skills_repository():
    with patch("src.repositories.skills_repository.get_skills_table") as mock_get_table:
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        repo = SkillsRepository()
        return repo, mock_table


def test_insert_skill_entry(skills_repository):
    repo, table = skills_repository

    entry = SkillEntry(
        id="skill-001",
        name="Test",
        lastname="User",
        email="test@example.com",
        phone="123456789",
        linkedin="https://linkedin.com/in/test",
        skills=["Python", "FastAPI"],
        extracted_from="ai"
    )

    repo.insert_skill_entry(entry)

    table.put_item.assert_called_once_with(Item=entry.model_dump())