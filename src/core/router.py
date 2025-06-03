from fastapi import APIRouter

from controllers import auth_router, resume_router

router = APIRouter()

router.include_router(resume_router, prefix="/resume", tags=["CV Generator"])
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
