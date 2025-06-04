from pathlib import Path

from generators.resume_pdf import compile_latex_to_pdf, generate_cv_latex
from models import InputCVRequest, ResumeData
from repositories import ResumeRepository, SkillsRepository, UsersRepository
from resume_generator import ResumeGenerator
from utils import (
    build_resume_reference,
    build_skill_entry,
    clean_json_output,
    parse_resume_json,
)


class ResumeService:

    def __init__(self):
        self.skill_repo = SkillsRepository()
        self.resume_repo = ResumeRepository()
        self.users_repo = UsersRepository()

    def generate_resume(self, input_data: InputCVRequest, email: str) -> ResumeData:
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
        resume_dict = clean_json_output(result.tasks_output[1].raw)
        parsed_resume = parse_resume_json(resume_dict)

        resume_id = self.resume_repo.insert_resume(parsed_resume)
        resume_ref = build_resume_reference(resume_id, parsed_resume.fullName)

        self.users_repo.append_resume_entry(email, resume_ref)

        skill_entry = build_skill_entry(parsed_resume, result)
        self.skill_repo.insert_skill_entry(skill_entry)
        
        return parsed_resume
    
    def generate_pdf_resume(self, resume_data: ResumeData) -> Path:
        latex_code = generate_cv_latex(resume_data)
        return compile_latex_to_pdf(latex_code)
    
    def remove_resume_reference(self, email: str, resume_id: str) -> bool:
        return self.users_repo.remove_resume_reference(email, resume_id)

    def rename_resume_filename(self, email: str, resume_id: str, new_filename: str) -> bool:
        return self.users_repo.rename_resume_filename(email, resume_id, new_filename)
    
    def get_resume_by_id(self, resume_id: str) -> ResumeData | None:
        return self.resume_repo.get_resume_by_id(resume_id)

