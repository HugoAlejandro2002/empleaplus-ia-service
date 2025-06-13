from fastapi import APIRouter

from src.controllers import auth_router, capybara_router, resume_router

router = APIRouter()

router.include_router(capybara_router, prefix="/capybara", tags=["Capybara Resume Generator"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(resume_router, prefix="/resume", tags=["Resume Generator"])

