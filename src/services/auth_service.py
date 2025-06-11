from fastapi import HTTPException

from src.models import UserDB, UserLoginRequest, UserRegisterRequest
from src.repositories import UsersRepository
from src.utils import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self):
        self.user_repo = UsersRepository()

    def register(self, data: UserRegisterRequest):
        existing_user = self.user_repo.get_user_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pwd = hash_password(data.password)
        new_user = UserDB(email=data.email, password=hashed_pwd, cvs=[])

        self.user_repo.insert_user(new_user)
        return {"message": "User registered successfully"}
    
    def login(self, data: UserLoginRequest):
        user = self.user_repo.get_user_by_email(data.email)
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(data={"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
