from unittest.mock import MagicMock, patch

import pytest

from src.models import InputCVRequest, ResumeData
from src.services import ResumeService


@pytest.fixture
def mock_resume_data():
    return ResumeData(
        fullName="Test User",
        summary="Experienced software engineer",
        contact={
            "email": "test@example.com",
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/test"
        },
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[]
    )


@pytest.fixture
def resume_service_mocked(mock_resume_data):
    with patch("src.services.resume_service.ResumeRepository") as mock_resume_repo_class, \
         patch("src.services.resume_service.UsersRepository") as mock_users_repo_class, \
         patch("src.services.resume_service.SkillsRepository") as mock_skills_repo_class, \
         patch("src.services.resume_service.ResumeGenerator") as mock_generator_class, \
         patch("src.services.resume_service.clean_json_output") as mock_clean_json, \
         patch("src.services.resume_service.parse_resume_json") as mock_parse_resume, \
         patch("src.services.resume_service.build_resume_reference") as mock_build_ref, \
         patch("src.services.resume_service.build_skill_entry") as mock_build_skill:

        mock_resume_repo = MagicMock()
        mock_users_repo = MagicMock()
        mock_skills_repo = MagicMock()
        mock_generator = MagicMock()

        mock_resume_repo_class.return_value = mock_resume_repo
        mock_users_repo_class.return_value = mock_users_repo
        mock_skills_repo_class.return_value = mock_skills_repo
        mock_generator_class.return_value.crew.return_value.kickoff.return_value.tasks_output = [
            MagicMock(), MagicMock(raw='{"fullName": "Test User"}')
        ]

        mock_clean_json.return_value = {"fullName": "Test User"}
        mock_parse_resume.return_value = mock_resume_data
        mock_build_ref.return_value = {"id": "resume123", "filename": "Test User"}
        mock_build_skill.return_value = {"skills": ["Python"]}

        yield ResumeService(), mock_resume_repo, mock_users_repo, mock_skills_repo


def test_generate_resume_success(resume_service_mocked):
    service, mock_resume_repo, mock_users_repo, mock_skills_repo = resume_service_mocked

    mock_input = InputCVRequest(
        personalData={
            "fullName": "Test User",
            "email": "test@example.com",
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/test"
        },
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[],
        professionalSummary={"summary": "Experienced professional"}
    )

    result = service.generate_resume(mock_input, "user@example.com")

    assert isinstance(result, ResumeData)
    assert result.fullName == "Test User"
    mock_resume_repo.insert_resume.assert_called_once()
    mock_users_repo.append_resume_entry.assert_called_once()
    mock_skills_repo.insert_skill_entry.assert_called_once()


@patch("src.services.resume_service.generate_cv_latex")
@patch("src.services.resume_service.compile_latex_to_pdf")
def test_generate_pdf_resume_success(mock_compile_pdf, mock_generate_latex, mock_resume_data):
    service = ResumeService()

    mock_generate_latex.return_value = r"\LaTeX code"
    mock_compile_pdf.return_value = "fake_path.pdf"

    result = service.generate_pdf_resume(mock_resume_data)

    assert result == "fake_path.pdf"
    mock_generate_latex.assert_called_once_with(mock_resume_data)
    mock_compile_pdf.assert_called_once_with(r"\LaTeX code")


def test_remove_resume_reference():
    service = ResumeService()
    service.users_repo = MagicMock()
    service.users_repo.remove_resume_reference.return_value = True

    result = service.remove_resume_reference("test@example.com", "resume123")
    assert result is True
    service.users_repo.remove_resume_reference.assert_called_once_with("test@example.com", "resume123")


def test_rename_resume_filename():
    service = ResumeService()
    service.users_repo = MagicMock()
    service.users_repo.rename_resume_filename.return_value = True

    result = service.rename_resume_filename("test@example.com", "resume123", "New Name")
    assert result is True
    service.users_repo.rename_resume_filename.assert_called_once_with("test@example.com", "resume123", "New Name")


def test_get_resume_by_id(mock_resume_data):
    service = ResumeService()
    service.resume_repo = MagicMock()
    service.resume_repo.get_resume_by_id.return_value = mock_resume_data

    result = service.get_resume_by_id("resume123")
    assert result == mock_resume_data
    service.resume_repo.get_resume_by_id.assert_called_once_with("resume123")
