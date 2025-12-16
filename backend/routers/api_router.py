"""
Router pour l'API REST
Routes : /api/*
"""
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from services import session_service, sales_service
from config import APP_VERSION

router = APIRouter(prefix="/api")


@router.get("/status")
def api_status():
    """Vérifier le statut de l'API"""
    return {
        "status": "ok",
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "active_sessions": session_service.get_active_sessions_count()
    }


@router.get("/user")
def api_user(request: Request):
    """Récupérer les infos de l'utilisateur connecté"""
    if not session_service.is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    return {
        "username": session_service.get_username(request),
        "logged_in": True
    }


@router.get("/sales")
def api_sales(request: Request):
    """Récupérer toutes les ventes"""
    if not session_service.is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    sales = sales_service.load_sales()
    return {
        "sales": sales,
        "count": len(sales),
        "total_revenue": sales_service.get_total_revenue()
    }


@router.get("/sales/user")
def api_user_sales(request: Request):
    """Récupérer les ventes de l'utilisateur connecté"""
    if not session_service.is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    username = session_service.get_username(request)
    sales = sales_service.get_sales_by_user(username)
    return {
        "sales": sales,
        "count": len(sales)
    }


@router.get("/sales/{sale_id}")
def api_sale_detail(sale_id: str, request: Request):
    """Récupérer les détails d'une vente"""
    if not session_service.is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    sale = sales_service.get_sale_by_id(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Vente non trouvée")
    
    return sale

