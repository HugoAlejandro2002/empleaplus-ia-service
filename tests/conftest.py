from unittest.mock import MagicMock

import pytest

from src.models import (
    CapybaraResume,
    InputCVRequest,
    ResumeData,
    ResumeReference,
    UserDB,
)

# === USERS ===

@pytest.fixture
def mock_users_repo():
    repo = MagicMock()
    repo.get_user_by_email.return_value = UserDB(
        email="test@example.com",
        password="hashedpwd",
        cvs=[
            ResumeReference(
                id="cv1",
                filename="cv1.pdf",
                created_at="2024-01-01T00:00:00Z"
            )
        ]
    )
    return repo

@pytest.fixture
def sample_user():
    return UserDB(
        email="test@example.com",
        password="hashedpwd",
        cvs=[]
    )


# === RESUMES ===

@pytest.fixture
def mock_resume_repo():
    repo = MagicMock()
    repo.get_resume_by_id.return_value = ResumeData(
        id="resume-id",
        fullName="Test User",
        contact=None,
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[],
        summary=""
    )
    repo.insert_resume.return_value = "resume-id"
    return repo


# === SKILLS ===

@pytest.fixture
def mock_skills_repo():
    repo = MagicMock()
    repo.insert_skill_entry.return_value = None
    return repo


# === GENERATORS ===

@pytest.fixture
def mock_resume_generator():
    mock = MagicMock()
    mock.crew.return_value.kickoff.return_value.tasks_output = [
        None,
        MagicMock(raw='{"fullName":"Test User"}')
    ]
    return mock


# === INPUT DATA ===

@pytest.fixture
def fake_input_cv_request():
    fake = MagicMock(spec=InputCVRequest)
    fake.personalData.model_dump.return_value = {}
    fake.education = []
    fake.experience = []
    fake.skills = []
    fake.languages = []
    fake.certifications = []
    fake.professionalSummary.model_dump.return_value = {}
    return fake


# === CAPYBARA RESUME ===

@pytest.fixture
def capybara_resume_data():
    return CapybaraResume(
        fullName="Test User",
        contact=None,
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[],
        summary="",
        achievements=[],
        complementaryEducation=[],
        projectExperience=None
    )