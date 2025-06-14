from pathlib import Path

from src.generators.resume_capybara import generate_capybara_pdf_resume
from src.models import CapybaraResume


class CapybaraResumeService:
    def generate_pdf(self, resume_data: CapybaraResume) -> Path:
        return generate_capybara_pdf_resume(resume_data)
