from fastapi import APIRouter, Depends

from src.dependencies.auth import get_current_user_email
from src.models import UserLoginRequest, UserRegisterRequest, UserResetPasswordRequest
from src.services import AuthService

router = APIRouter()

auth_service = AuthService()

@router.post("/register")
def register_user(data: UserRegisterRequest):
    return auth_service.register(data)

@router.post("/login")
def login_user(data: UserLoginRequest):
    return auth_service.login(data)

@router.put("/reset-password")
def reset_password(data: UserResetPasswordRequest, email: str = Depends(get_current_user_email)):
    return auth_service.reset_password(data, email)