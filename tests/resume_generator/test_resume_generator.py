from unittest.mock import MagicMock, patch

import pytest

from src.resume_generator import ResumeGenerator


@pytest.fixture
def mock_resume_generator():
    with patch("src.resume_generator.crew.TextFileKnowledgeSource"), \
         patch("src.resume_generator.crew.Agent") as mock_agent, \
         patch("src.resume_generator.crew.Task") as mock_task, \
         patch("src.resume_generator.crew.Crew") as mock_crew:

        # Simula resultado de kickoff
        mock_instance = MagicMock()
        mock_instance.kickoff.return_value.tasks_output = [
            MagicMock(raw="Redacted CV text"),  # generate_cv
            MagicMock(raw='{"fullName": "Test User"}'),  # structure_cv
            MagicMock(raw='{"skills": ["Python", "FastAPI"]}')  # extract_skills
        ]
        mock_crew.return_value = mock_instance

        yield ResumeGenerator(), mock_instance


def test_resume_generator_crew_kickoff(mock_resume_generator):
    resume_gen, mock_crew_instance = mock_resume_generator

    mock_input = {
        "personal_data": {"fullName": "Test User"},
        "education": [],
        "experience": [],
        "skills": [],
        "languages": [],
        "certifications": [],
        "professional_summary": {"summary": "Ingeniero de software"}
    }

    result = resume_gen.crew().kickoff(inputs=mock_input)

    assert result.tasks_output[1].raw == '{"fullName": "Test User"}'
    mock_crew_instance.kickoff.assert_called_once_with(inputs=mock_input)


def test_crew_structure(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    crew_instance = resume_gen.crew()

    assert hasattr(crew_instance, "agents")
    assert hasattr(crew_instance, "tasks")
    assert crew_instance.agents is not None
    assert crew_instance.tasks is not None

# Agentes
def test_cv_writer_is_agent_instance(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    agent = resume_gen.cv_writer()
    assert agent is not None

def test_json_formatter_is_agent_instance(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    agent = resume_gen.json_formatter()
    assert agent is not None

def test_skills_extractor_is_agent_instance(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    agent = resume_gen.skills_extractor()
    assert agent is not None

# Tareas
def test_generate_cv_task(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    task = resume_gen.generate_cv()
    assert task is not None

def test_structure_cv_task(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    task = resume_gen.structure_cv()
    assert task is not None

def test_extract_skills_task(mock_resume_generator):
    resume_gen, _ = mock_resume_generator
    task = resume_gen.extract_skills()
    assert task is not None
