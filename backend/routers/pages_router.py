"""
Router pour les pages web
Routes : /, /ventes
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services import session_service
from config import TEMPLATES_DIR

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def page_dashboard(request: Request):
    """Dashboard principal"""
    if not session_service.is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": session_service.get_username(request)}
    )


@router.get("/ventes", response_class=HTMLResponse)
def page_ventes(request: Request):
    """Page liste des ventes"""
    if not session_service.is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        "ventes.html",
        {"request": request, "username": session_service.get_username(request)}
    )

