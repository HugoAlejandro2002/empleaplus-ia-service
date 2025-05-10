from fastapi import APIRouter

from controllers import resume_router

router = APIRouter()

router.include_router(resume_router, prefix="/resume", tags=["CV Generator"])