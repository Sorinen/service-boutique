"""
Backend sécurisé pour l'application Boutique
- Authentification avec mots de passe hashés
- Sessions sécurisées
- API REST pour les ventes
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from passlib.context import CryptContext
from datetime import datetime
import secrets
import json
import os

# ============================================
# CONFIGURATION
# ============================================

app = FastAPI(title="Boutique SaaS", version="1.0.0")

# Hashage des mots de passe (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète générée aléatoirement (en production, utiliser une variable d'environnement)
SECRET_KEY = secrets.token_hex(32)

# Sessions actives (en mémoire pour la démo, utiliser Redis en production)
active_sessions = {}

# Fichier pour stocker les utilisateurs
USERS_FILE = "users.json"

# Fichiers statiques et templates
app.mount("/static", StaticFiles(directory="../fondend/static"), name="static")
templates = Jinja2Templates(directory="../templates/fondend")


# ============================================
# GESTION DES UTILISATEURS
# ============================================

def load_users():
    """Charger les utilisateurs depuis le fichier JSON"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    # Utilisateurs par défaut avec mots de passe hashés
    default_users = {
        "admin": pwd_context.hash("admin123"),
        "boutique": pwd_context.hash("boutique123")
    }
    save_users(default_users)
    return default_users

def save_users(users):
    """Sauvegarder les utilisateurs dans le fichier JSON"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe contre son hash"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Hasher un mot de passe"""
    return pwd_context.hash(password)


# ============================================
# GESTION DES SESSIONS
# ============================================

def create_session(username: str) -> str:
    """Créer une nouvelle session sécurisée"""
    token = secrets.token_urlsafe(32)
    active_sessions[token] = {
        "username": username,
        "created": datetime.now().isoformat()
    }
    return token

def get_session(token: str):
    """Récupérer une session"""
    return active_sessions.get(token)

def delete_session(token: str):
    """Supprimer une session"""
    if token in active_sessions:
        del active_sessions[token]

def is_logged_in(request: Request) -> bool:
    """Vérifier si l'utilisateur est connecté"""
    token = request.cookies.get("session_token")
    if not token:
        return False
    return token in active_sessions

def get_username(request: Request) -> str:
    """Récupérer le nom d'utilisateur depuis la session"""
    token = request.cookies.get("session_token")
    if token and token in active_sessions:
        return active_sessions[token]["username"]
    return ""


# ============================================
# PAGES PUBLIQUES
# ============================================

@app.get("/login", response_class=HTMLResponse)
def page_login(request: Request):
    """Page de connexion"""
    if is_logged_in(request):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@app.post("/login")
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Traitement de la connexion"""
    users = load_users()
    
    if username not in users:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Utilisateur inconnu"}
        )
    
    if not verify_password(password, users[username]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Mot de passe incorrect"}
        )
    
    # Connexion réussie
    token = create_session(username)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,  # Mettre True en production avec HTTPS
        samesite="lax",
        max_age=86400  # 24 heures
    )
    return response


@app.get("/logout")
def do_logout(request: Request):
    """Déconnexion"""
    token = request.cookies.get("session_token")
    if token:
        delete_session(token)
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_token")
    return response


# ============================================
# PAGES PROTÉGÉES
# ============================================

@app.get("/", response_class=HTMLResponse)
def page_dashboard(request: Request):
    """Dashboard principal"""
    if not is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": get_username(request)}
    )


@app.get("/ventes", response_class=HTMLResponse)
def page_ventes(request: Request):
    """Page liste des ventes"""
    if not is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(
        "ventes.html",
        {"request": request, "username": get_username(request)}
    )


# ============================================
# API REST (pour future utilisation)
# ============================================

@app.get("/api/status")
def api_status():
    """Vérifier le statut de l'API"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/user")
def api_user(request: Request):
    """Récupérer les infos de l'utilisateur connecté"""
    if not is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    return {
        "username": get_username(request),
        "logged_in": True
    }


# ============================================
# GESTION DES ERREURS
# ============================================

@app.exception_handler(404)
def not_found(request: Request, exc):
    """Page 404"""
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Page non trouvée"},
        status_code=404
    )
