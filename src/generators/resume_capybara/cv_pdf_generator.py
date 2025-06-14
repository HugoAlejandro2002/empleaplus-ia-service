from pathlib import Path

from src.models import CapybaraResume

from .compile_pdf import compile_latex_to_pdf
from .formatter import (
    format_achievements,
    format_complementary_education,
    format_contact,
    format_education,
    format_experience,
    format_header,
    format_languages,
    format_project_experience,
    format_skills_and_softwares,
)

TEMPLATE_PATH = Path(__file__).parent / "template.tex"


def generate_capybara_pdf_resume(resume: CapybaraResume) -> Path:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    def safe(val: str) -> str:
        return val.replace("%", "\\%") if val else ""

    latex_filled = template
    latex_filled = latex_filled.replace("{{ header }}", format_header(safe(resume.fullName)))
    latex_filled = latex_filled.replace("{{ contact }}", format_contact(resume.contact))
    latex_filled = latex_filled.replace("{{ skills_and_softwares }}", format_skills_and_softwares(resume.skills, resume.softwares))
    latex_filled = latex_filled.replace("{{ experience }}", format_experience(resume.experience))
    
    if resume.projectExperience:
        latex_filled = latex_filled.replace("{{ project_experience }}", format_project_experience(resume.projectExperience))
    else:
        latex_filled = latex_filled.replace("{{ project_experience }}", "")

    latex_filled = latex_filled.replace("{{ education }}", format_education(resume.education))
    
    latex_filled = latex_filled.replace(
        "{{ achievements }}",
        format_achievements(resume.achievements) if resume.achievements else ""
    )
    
    latex_filled = latex_filled.replace(
        "{{ complementary_education }}",
        format_complementary_education(resume.complementaryEducation) if resume.complementaryEducation else ""
    )

    latex_filled = latex_filled.replace("{{ languages }}", format_languages(resume.languages))

    latex_filled.replace('%', r'\%')

    return compile_latex_to_pdf(latex_filled, filename="capybara_resume")
