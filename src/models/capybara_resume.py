from typing import List, Optional

from pydantic import BaseModel


class CapybaraContact(BaseModel):
    email: str
    linkedin: str
    phone: str
    city: str
    country: str


class CapybaraEducation(BaseModel):
    institution: str
    degree: str
    relevantEducationData: Optional[str]  # noqa: N815
    startDate: str  # noqa: N815
    endDate: str  # noqa: N815
    city: str
    country: str


class CapybaraExperience(BaseModel):
    company: str
    position: str
    relevantCompanyData: Optional[str]  # noqa: N815
    startDate: str  # noqa: N815
    endDate: str  # noqa: N815
    city: str
    country: str
    successSentences: List[str]  # noqa: N815


class CapybaraProjectExperience(BaseModel):
    titleSection: str  # noqa: N815
    experiences: List[CapybaraExperience]


class CapybaraLanguage(BaseModel):
    name: str
    proficiency: str
    certification: Optional[str]


class CapybaraAchievement(BaseModel):
    name: str
    institution: str
    city: str
    country: str
    date: str


class CapybaraComplementaryEducation(BaseModel):
    courseType: str  # noqa: N815
    courseName: str  # noqa: N815
    institution: str
    city: str
    country: str
    date: str


class CapybaraResume(BaseModel):
    fullName: str  # noqa: N815
    contact: CapybaraContact
    education: List[CapybaraEducation]
    experience: List[CapybaraExperience]
    projectExperience: Optional[CapybaraProjectExperience] = None  # noqa: N815
    skills: List[str]
    softwares: List[str]
    languages: List[CapybaraLanguage]
    achievements: Optional[List[CapybaraAchievement]] = None
    complementaryEducation: Optional[List[CapybaraComplementaryEducation]] = None  # noqa: N815
