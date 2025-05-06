import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from models import InputCVRequest, ResumeData
from services import ResumeService

router = APIRouter()
resume_service = ResumeService()

@router.post("/generate", response_model=ResumeData)
def generate_cv(data: InputCVRequest):
    resume_json = resume_service.generate_resume(data)
    return resume_json

@router.post("/download-pdf")
def preview_cv_latex(data: ResumeData):
    pdf_path = resume_service.generate_pdf_resume(data)

    def cleanup():
        os.remove(pdf_path)

    return FileResponse(
        path=pdf_path,
        filename="resume.pdf",
        media_type="application/pdf",
        background=BackgroundTask(cleanup)
    )