from unittest.mock import MagicMock, patch

import pytest

from src.models import ResumeData
from src.repositories import ResumeRepository


@pytest.fixture
def mock_resumes_table():
    with patch("src.repositories.resume_repository.get_resumes_table") as mock_get_table:
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        yield mock_table


@pytest.fixture
def sample_resume_data():
    return ResumeData(
        fullName="Jane Doe",
        summary="Software engineer",
        contact={
            "email": "jane@example.com",
            "phone": "1234567890",
            "linkedin": "https://linkedin.com/in/janedoe"
        },
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[]
    )


@patch("src.repositories.resume_repository.generate_uuid", return_value="uuid-123")
def test_insert_resume_stores_data(mock_uuid, mock_resumes_table, sample_resume_data):
    repo = ResumeRepository()
    resume_id = repo.insert_resume(sample_resume_data)

    assert resume_id == "uuid-123"
    mock_resumes_table.put_item.assert_called_once()
    stored_item = mock_resumes_table.put_item.call_args[1]["Item"]
    assert stored_item["id"] == "uuid-123"
    assert stored_item["fullName"] == "Jane Doe"


def test_get_resume_by_id_found(mock_resumes_table, sample_resume_data):
    mock_resumes_table.get_item.return_value = {
        "Item": sample_resume_data.model_dump()
    }

    repo = ResumeRepository()
    result = repo.get_resume_by_id("uuid-123")

    assert isinstance(result, ResumeData)
    assert result.fullName == "Jane Doe"
    mock_resumes_table.get_item.assert_called_once_with(Key={"id": "uuid-123"})


def test_get_resume_by_id_not_found(mock_resumes_table):
    mock_resumes_table.get_item.return_value = {}

    repo = ResumeRepository()
    result = repo.get_resume_by_id("uuid-123")

    assert result is None
    mock_resumes_table.get_item.assert_called_once_with(Key={"id": "uuid-123"})
