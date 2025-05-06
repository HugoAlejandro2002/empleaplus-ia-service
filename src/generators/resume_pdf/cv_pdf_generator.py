from pathlib import Path

from models import ResumeData

from .formatter import (
    format_certifications,
    format_education,
    format_experience,
    format_header,
    format_skills_and_languages,
    format_summary,
)

TEMPLATE_PATH = Path(__file__).parent / "template.tex"

def generate_cv_latex(resume: ResumeData) -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    latex_filled = template
    latex_filled = latex_filled.replace("{{ header }}", format_header(resume.fullName, resume.contact))
    latex_filled = latex_filled.replace("{{ summary }}", format_summary(resume.summary))
    latex_filled = latex_filled.replace("{{ experience }}", format_experience(resume.experience))
    latex_filled = latex_filled.replace("{{ education }}", format_education(resume.education))
    latex_filled = latex_filled.replace("{{ skills_and_languages }}", format_skills_and_languages(resume.skills, resume.languages))
    latex_filled = latex_filled.replace("{{ certifications }}", format_certifications(resume.certifications))

    return latex_filled.replace('%','\%')
