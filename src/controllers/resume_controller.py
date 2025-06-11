import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from src.dependencies.auth import get_current_user_email
from src.models import InputCVRequest, RenameResumeRequest, ResumeData
from src.services import ResumeService, UserService

router = APIRouter(dependencies=[Depends(get_current_user_email)] )

resume_service = ResumeService()
user_service = UserService()

@router.post("/generate", response_model=ResumeData)
def generate_cv(data: InputCVRequest, email: str = Depends(get_current_user_email)):
    resume_json = resume_service.generate_resume(data, email)
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

@router.get("/")
def get_user_resume_refs(email: str = Depends(get_current_user_email)):
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user.cvs

@router.get("/{resume_id}", response_model=ResumeData)
def get_resume_by_id(resume_id: str):
    resume = resume_service.get_resume_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume no encontrado")
    return resume

@router.delete("/{resume_id}")
def delete_resume_entry(resume_id: str, email: str = Depends(get_current_user_email)):
    if not resume_service.remove_resume_reference(email, resume_id):
        raise HTTPException(status_code=404, detail="Resume no encontrado")
    return {"message": "Entrada de resume eliminada"}


@router.put("/{resume_id}/rename")
def rename_resume_entry(
    resume_id: str,
    request: RenameResumeRequest,
    email: str = Depends(get_current_user_email)
):
    if not resume_service.rename_resume_filename(email, resume_id, request.filename):
        raise HTTPException(status_code=404, detail="No se pudo actualizar el nombre")
    return {"message": "Nombre de archivo actualizado correctamente"}