from .auth_controller import router as auth_router
from .capybara_resume_controller import router as capybara_router
from .resume_controller import router as resume_router

__all__ = ["resume_router","auth_router", "capybara_router"]
