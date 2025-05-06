from pathlib import Path

from generators.resume_pdf import compile_latex_to_pdf, generate_cv_latex
from models import InputCVRequest, ResumeData
from resume_generator import ResumeGenerator
from utils import clean_json_output, parse_resume_json


class ResumeService:
    def generate_resume(self, input_data: InputCVRequest) -> ResumeData:
        inputs = {
            "personal_data": input_data.personalData.model_dump(),
            "education": [edu.model_dump() for edu in input_data.education],
            "experience": [exp.model_dump() for exp in input_data.experience],
            "skills": [skill.model_dump() for skill in input_data.skills],
            "languages": [lang.model_dump() for lang in input_data.languages],
            "certifications": [cert.model_dump() for cert in input_data.certifications],
            "professional_summary": input_data.professionalSummary.model_dump()
        }

        result = ResumeGenerator().crew().kickoff(inputs=inputs)
        resume_dict = clean_json_output(result.raw)
        return parse_resume_json(resume_dict)
    
    def generate_pdf_resume(self, resume_data: ResumeData) -> Path:
        latex_code = generate_cv_latex(resume_data)
        return compile_latex_to_pdf(latex_code)

