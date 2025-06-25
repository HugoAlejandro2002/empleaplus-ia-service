from .config import get_settings
from .db_client import get_resumes_table, get_skills_table, get_users_table


def create_app():
    """
    Sólo cuando llamen a create_app() se importará init_app
    y se montará toda la aplicación FastAPI.
    Esto evita que importar src.core dispare
    la carga de routers y controladores en los tests.
    """
    from .init_app import create_app as _create_app
    return _create_app()

__all__ = [
    "create_app",
    "get_skills_table",
    "get_users_table",
    "get_resumes_table",
    "get_settings",
]
