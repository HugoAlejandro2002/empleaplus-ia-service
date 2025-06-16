from datetime import datetime
from pathlib import Path

from dateutil.parser import parse

from src.generators.resume_capybara import generate_capybara_pdf_resume
from src.models import CapybaraResume


class CapybaraResumeService:
    def generate_pdf(self, resume_data: CapybaraResume) -> Path:
        prepared = self._prepare_resume(resume_data)
        return generate_capybara_pdf_resume(prepared)

    def _prepare_resume(self, resume: CapybaraResume) -> CapybaraResume:
        def get_dt(val):
            if isinstance(val, datetime):
                return val
            try:
                return parse(val)
            except Exception:
                return datetime.min

        def fmt(val):
            dt = get_dt(val)
            return dt.strftime("%m/%Y")

        # 1) Ordenar y formatear EXPERIENCE
        exps = sorted(
            resume.experience,
            key=lambda e: get_dt(e.endDate),
            reverse=True
        )
        formatted_exps = [
            e.copy(update={
                "startDate": fmt(e.startDate),
                "endDate":   fmt(e.endDate),
            })
            for e in exps
        ]

        # 2) Formatear EDUCATION (sin reordenar)
        formatted_eds = [
            ed.copy(update={
                "startDate": fmt(ed.startDate),
                "endDate":   fmt(ed.endDate),
            })
            for ed in resume.education
        ]

        # 3) Ordenar y formatear PROJECT EXPERIENCE (si existe)
        proj = resume.projectExperience
        if proj and proj.experiences:
            sorted_proj = sorted(
                proj.experiences,
                key=lambda e: get_dt(e.endDate),
                reverse=True
            )
            formatted_proj = [
                e.copy(update={
                    "startDate": fmt(e.startDate),
                    "endDate":   fmt(e.endDate),
                })
                for e in sorted_proj
            ]
            proj = proj.copy(update={"experiences": formatted_proj})

        # 4) Formatear ACHIEVEMENTS.date
        achs = None
        if resume.achievements:
            achs = [
                ach.copy(update={"date": fmt(ach.date)})
                for ach in resume.achievements
            ]

        # 5) Formatear COMPLEMENTARY EDUCATION.date
        comps = None
        if resume.complementaryEducation:
            comps = [
                c.copy(update={"date": fmt(c.date)})
                for c in resume.complementaryEducation
            ]

        # 6) Reconstruir el CapybaraResume con todo formateado
        return resume.copy(update={
            "experience":           formatted_exps,
            "education":            formatted_eds,
            "projectExperience":    proj,
            "achievements":         achs,
            "complementaryEducation": comps,
        })
