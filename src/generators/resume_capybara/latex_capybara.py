from pathlib import Path

from src.generators.resume_pdf import compile_latex_to_pdf
from src.models.capybara_resume import CapybaraResume

TEMPLATE_PATH = Path(__file__).parent / "template.tex"  # Usa el mismo template base


def generate_capybara_latex(resume: CapybaraResume) -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    def escape(text: str) -> str:
        return text.replace('%', r'\%') if text else ""

    # Reemplazos básicos (puedes ir sumando más con funciones tipo `format_header`)
    latex_filled = template
    latex_filled = latex_filled.replace("{{ header }}", escape(resume.fullName))
    latex_filled = latex_filled.replace("{{ summary }}", "")  # No se incluye en el modelo
    latex_filled = latex_filled.replace("{{ experience }}", "")
    latex_filled = latex_filled.replace("{{ education }}", "")
    latex_filled = latex_filled.replace("{{ skills_and_languages }}", "")
    latex_filled = latex_filled.replace("{{ certifications }}", "")

    return latex_filled


def generate_capybara_pdf_resume(resume: CapybaraResume) -> Path:
    latex_code = generate_capybara_latex(resume)
    return compile_latex_to_pdf(latex_code, filename="capybara_resume")
