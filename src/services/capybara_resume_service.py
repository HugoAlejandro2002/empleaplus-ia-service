from datetime import datetime, timezone
from pathlib import Path

from dateutil.parser import parse

from src.generators.resume_capybara import generate_capybara_pdf_resume
from src.models import (
    CapybaraResume,
)


class CapybaraResumeService:
    def generate_pdf(self, resume_data: CapybaraResume) -> Path:
        prepared = self._prepare_resume(resume_data)
        return generate_capybara_pdf_resume(prepared)

    def _prepare_resume(self, resume: CapybaraResume) -> CapybaraResume:

        def get_dt(val):
            # 1) None = en curso → ahora
            if val is None:
                return datetime.now()
            # 2) Si ya es datetime, úsalo
            if isinstance(val, datetime):
                dt = val
            else:
                # 3) parsear string a datetime
                try:
                    dt = parse(val)
                except Exception:
                    return datetime.min
            # 4) si viene con tzinfo, conviértelo a UTC y quita el tzinfo
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            return dt

        def fmt(val):
            if val is None:
                return "Actualidad"
            dt = get_dt(val)
            return dt.strftime("%m/%Y")

        # ahora get_dt() siempre entrega datetime naive → sorted() funciona
        exps = sorted(
            resume.experience or [],
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

        # — el resto igual que antes, usando get_dt/ fmt() —
        # 2) EDUCATION
        formatted_eds = [
            ed.copy(update={
                "startDate": fmt(ed.startDate),
                "endDate":   fmt(ed.endDate),
            })
            for ed in resume.education
        ]

        # 3) PROJECT EXPERIENCE
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

        # 4) ACHIEVEMENTS
        achs = None
        if resume.achievements:
            achs = [
                ach.copy(update={"date": fmt(ach.date)})
                for ach in resume.achievements
            ]

        # 5) COMPLEMENTARY EDUCATION
        comps = None
        if resume.complementaryEducation:
            comps = [
                c.copy(update={"date": fmt(c.date)})
                for c in resume.complementaryEducation
            ]

        return resume.copy(update={
            "experience":            formatted_exps,
            "education":             formatted_eds,
            "projectExperience":     proj,
            "achievements":          achs,
            "complementaryEducation": comps,
        })
