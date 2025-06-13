import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from src.generators.resume_capybara.latex_capybara import generate_capybara_pdf_resume
from src.models.capybara_resume import CapybaraResume

router = APIRouter()

@router.post("/download-pdf")
def download_capybara_resume_pdf(data: CapybaraResume):
    pdf_path = generate_capybara_pdf_resume(data)

    def cleanup():
        os.remove(pdf_path)

    return FileResponse(
        path=pdf_path,
        filename="capybara_resume.pdf",
        media_type="application/pdf",
        background=BackgroundTask(cleanup),
    )
