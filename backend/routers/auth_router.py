"""
Router pour l'authentification
Routes : /login, /logout
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services import user_service, session_service
from config import TEMPLATES_DIR, COOKIE_MAX_AGE, COOKIE_HTTPONLY, COOKIE_SECURE, COOKIE_SAMESITE

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/login", response_class=HTMLResponse)
def page_login(request: Request):
    """Page de connexion"""
    if session_service.is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Traitement de la connexion"""
    
    # Vérifier si l'utilisateur existe
    if not user_service.user_exists(username):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Utilisateur inconnu"}
        )
    
    # Authentifier l'utilisateur
    if not user_service.authenticate(username, password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Mot de passe incorrect"}
        )
    
    # Connexion réussie - créer une session
    token = session_service.create_session(username)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=COOKIE_HTTPONLY,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=COOKIE_MAX_AGE
    )
    return response


@router.get("/logout")
def do_logout(request: Request):
    """Déconnexion"""
    token = session_service.get_session_token(request)
    if token:
        session_service.delete_session(token)
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_token")
    return response

