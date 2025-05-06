from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import cv_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Generator API",
        version="1.0.0",
        description="Microservicio de generación de CV con FastAPI y CrewAI"
    )

    # CORS middleware (ajústalo según tus necesidades)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Registrar rutas
    app.include_router(cv_router, prefix="/resume", tags=["CV Generator"])

    return app
