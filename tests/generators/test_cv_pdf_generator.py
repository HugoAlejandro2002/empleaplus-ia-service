from unittest.mock import patch

from src.generators.resume_pdf import generate_cv_latex
from src.models import Contact, ResumeData


@patch("src.generators.resume_pdf.cv_pdf_generator.open", create=True)
@patch("src.generators.resume_pdf.cv_pdf_generator.format_certifications", return_value="Certs")
@patch("src.generators.resume_pdf.cv_pdf_generator.format_education", return_value="Edu")
@patch("src.generators.resume_pdf.cv_pdf_generator.format_experience", return_value="Exp")
@patch("src.generators.resume_pdf.cv_pdf_generator.format_header", return_value="Header")
@patch("src.generators.resume_pdf.cv_pdf_generator.format_skills_and_languages", return_value="SkillsLangs")
@patch("src.generators.resume_pdf.cv_pdf_generator.format_summary", return_value="Summary")
def test_generate_cv_latex(
    mock_summary,
    mock_skills_langs,
    mock_header,
    mock_experience,
    mock_education,
    mock_certifications,
    mock_open,
):
    fake_template = (
        "{{ header }}\n{{ summary }}\n{{ experience }}\n{{ education }}\n{{ skills_and_languages }}\n{{ certifications }}\nExtra % symbol"
    )
    mock_open.return_value.__enter__.return_value.read.return_value = fake_template

    dummy_resume = ResumeData(
        fullName="John Doe",
        contact=Contact(email="john@example.com", linkedin="linkedin.com/in/johndoe", phone="123456789"),
        summary="Software Engineer",
        education=[],
        experience=[],
        skills=[],
        languages=[],
        certifications=[],
    )

    result = generate_cv_latex(dummy_resume)

    assert "Header" in result
    assert "Summary" in result
    assert "Exp" in result
    assert "Edu" in result
    assert "SkillsLangs" in result
    assert "Certs" in result
    assert r"\%" in result  # Ahora sí verifica el escape

