from typing import List, Optional

from pydantic import BaseModel, EmailStr


class PersonalData(BaseModel):
    fullName: str  # noqa: N815
    email: EmailStr
    phone: str
    linkedin: str # noqa: N815

class EducationItem(BaseModel):
    institution: str
    degree: str
    startYear: str # noqa: N815
    endYear: str # noqa: N815
    notes: Optional[str]

class ExperienceItem(BaseModel):
    projectName: str # noqa: N815
    role: str
    achievements: str
    teamwork: str
    coordination: str
    presentation: str

class Skill(BaseModel):
    skill: str
    level: str

class Language(BaseModel):
    language: str
    level: str

class Certification(BaseModel):
    course: str
    provider: str
    year: str
    certificate: Optional[str]

class ProfessionalSummary(BaseModel):
    summary: str

class InputCVRequest(BaseModel):
    personalData: PersonalData # noqa: N815
    education: List[EducationItem]
    experience: List[ExperienceItem]
    skills: List[Skill]
    languages: List[Language]
    certifications: List[Certification]
    professionalSummary: ProfessionalSummary # noqa: N815
