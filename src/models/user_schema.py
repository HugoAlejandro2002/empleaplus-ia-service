from typing import List

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserDB(BaseModel):
    email: EmailStr
    password: str
    cvs: List[str] = Field(default_factory=list)
