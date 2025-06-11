from fastapi import APIRouter

from src.models import UserLoginRequest, UserRegisterRequest
from src.services import AuthService

router = APIRouter()

auth_service = AuthService()

@router.post("/register")
def register_user(data: UserRegisterRequest):
    return auth_service.register(data)

@router.post("/login")
def login_user(data: UserLoginRequest):
    return auth_service.login(data)

