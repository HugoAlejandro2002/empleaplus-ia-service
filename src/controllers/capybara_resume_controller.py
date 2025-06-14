import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from src.models import CapybaraResume
from src.services import CapybaraResumeService

router = APIRouter()
resume_service = CapybaraResumeService()


@router.post("/download-pdf")
def download_capybara_resume_pdf(data: CapybaraResume):
    pdf_path = resume_service.generate_pdf(data)

    def cleanup():
        os.remove(pdf_path)

    return FileResponse(
        path=pdf_path,
        filename="capybara_resume.pdf",
        media_type="application/pdf",
        background=BackgroundTask(cleanup),
    )
