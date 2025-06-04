from typing import List, Optional

from pydantic import BaseModel


class Contact(BaseModel):
    email: str
    linkedin: str
    phone: str


class Education(BaseModel):
    institution: str
    degree: str
    startYear: int  # noqa: N815
    endYear: Optional[int]  # noqa: N815
    description: Optional[str]


class Experience(BaseModel):
    company: str
    position: str
    startDate: str  # noqa: N815
    endDate: Optional[str]  # noqa: N815
    responsibilities: List[str]


class Skill(BaseModel):
    name: str
    level: Optional[str]


class Language(BaseModel):
    name: str
    proficiency: str


class Certification(BaseModel):
    name: str
    institution: str
    year: Optional[int]


class ResumeData(BaseModel):
    fullName: str  # noqa: N815
    contact: Contact  # noqa: N815
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]
    languages: List[Language]
    certifications: List[Certification]
    summary: str  # noqa: N815


class ResumeReference(BaseModel):
    id: str
    filename: str
    created_at: str