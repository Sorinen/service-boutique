"""
Routers de l'application
"""
from .auth_router import router as auth_router
from .pages_router import router as pages_router
from .api_router import router as api_router

__all__ = [
    "auth_router",
    "pages_router",
    "api_router",
]

