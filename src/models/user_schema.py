from typing import List

from pydantic import BaseModel, EmailStr, Field

from .resume_schema import ResumeReference


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResetPasswordRequest(BaseModel):
    oldPassword: str  # noqa: N815
    newPassword: str = Field(min_length=6)  # noqa: N815

class UserDB(BaseModel):
    email: EmailStr
    password: str
    cvs: List[ResumeReference] = Field(default_factory=list)
