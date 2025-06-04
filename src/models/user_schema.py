from typing import List

from pydantic import BaseModel, EmailStr, Field

from .resume_schema import ResumeReference


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserDB(BaseModel):
    email: EmailStr
    password: str
    cvs: List[ResumeReference] = Field(default_factory=list)
