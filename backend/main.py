"""
Backend sécurisé pour l'application Boutique
Architecture DDD (Domain-Driven Design)
- Services séparés par domaine (users, sessions, sales)
- Routers organisés par fonctionnalité
- Configuration centralisée
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Configuration
from config import APP_TITLE, APP_VERSION, STATIC_DIR, TEMPLATES_DIR

# Services
from services import user_service, session_service, sales_service

# Routers
from routers import auth_router, pages_router, api_router


# ============================================
# INITIALISATION DE L'APPLICATION
# ============================================

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# Fichiers statiques et templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ============================================
# ENREGISTREMENT DES ROUTERS
# ============================================

app.include_router(auth_router, tags=["Authentication"])
app.include_router(pages_router, tags=["Pages"])
app.include_router(api_router, tags=["API"])


# ============================================
# ÉVÉNEMENTS DE DÉMARRAGE
# ============================================

@app.on_event("startup")
def startup_event():
    """Initialiser l'application au démarrage"""
    # Initialiser les services
    user_service.initialize()
    
    print(f"✅ {APP_TITLE} v{APP_VERSION} démarré avec succès")
    print(f"📁 Utilisateurs chargés : {len(user_service.load_users())}")


@app.on_event("shutdown")
def shutdown_event():
    """Nettoyer les ressources au shutdown"""
    print(f"🛑 {APP_TITLE} arrêté")


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


# ============================================
# POINT D'ENTRÉE
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
