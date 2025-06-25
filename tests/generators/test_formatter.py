from src.generators.resume_pdf.formatter import (
    format_certifications,
    format_education,
    format_experience,
    format_header,
    format_skills_and_languages,
    format_summary,
)
from src.models import (
    Certification,
    Contact,
    Education,
    Experience,
    Language,
    Skill,
)


def test_format_header():
    contact = Contact(email="john@example.com", linkedin="linkedin.com/in/johndoe", phone="123456789")
    result = format_header("John Doe", contact)
    assert "John Doe" in result
    assert "john@example.com" in result
    assert "linkedin.com/in/johndoe" in result
    assert "123456789" in result

def test_format_summary():
    summary = "Experienced developer"
    result = format_summary(summary)
    assert "Experienced developer" in result

def test_format_education():
    education = [
        Education(
            institution="MIT",
            degree="BSc Computer Science",
            startYear=2015,
            endYear=2019,
            description="Top student"
        )
    ]
    result = format_education(education)
    assert "MIT" in result
    assert "BSc Computer Science" in result
    assert "2015" in result
    assert "2019" in result
    assert "Top student" in result

def test_format_experience():
    experience = [
        Experience(
            company="OpenAI",
            position="Engineer",
            startDate="2020-01",
            endDate="2023-01",
            responsibilities=["Built models", "Improved APIs"]
        )
    ]
    result = format_experience(experience)
    assert "OpenAI" in result
    assert "Engineer" in result
    assert "2020-01" in result
    assert "2023-01" in result
    assert "Built models" in result
    assert "Improved APIs" in result

def test_format_skills_and_languages():
    skills = [Skill(name="Python", level="Advanced")]
    languages = [Language(name="English", proficiency="Fluent")]
    result = format_skills_and_languages(skills, languages)
    assert "Python" in result
    assert "Advanced" in result
    assert "English" in result
    assert "Fluent" in result

def test_format_certifications():
    certifications = [
        Certification(name="AWS Certified", institution="Amazon", year=2022)
    ]
    result = format_certifications(certifications)
    assert "AWS Certified" in result
    assert "Amazon" in result
    assert "2022" in result
