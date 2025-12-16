"""
Service de gestion des sessions (Domain-Driven Design)
Responsabilités :
- Création et suppression de sessions
- Vérification de l'état de connexion
- Récupération des informations de session
"""
import secrets
from datetime import datetime
from typing import Dict, Optional
from fastapi import Request


class SessionService:
    """Service de gestion des sessions utilisateur"""
    
    def __init__(self):
        # Sessions actives (en mémoire pour la démo, utiliser Redis en production)
        self._active_sessions: Dict[str, Dict[str, str]] = {}
    
    def create_session(self, username: str) -> str:
        """
        Créer une nouvelle session sécurisée
        
        Args:
            username: Nom d'utilisateur
            
        Returns:
            str: Token de session
        """
        token = secrets.token_urlsafe(32)
        self._active_sessions[token] = {
            "username": username,
            "created": datetime.now().isoformat()
        }
        return token
    
    def get_session(self, token: str) -> Optional[Dict[str, str]]:
        """
        Récupérer une session
        
        Args:
            token: Token de session
            
        Returns:
            Optional[Dict]: Données de session ou None
        """
        return self._active_sessions.get(token)
    
    def delete_session(self, token: str) -> None:
        """
        Supprimer une session
        
        Args:
            token: Token de session
        """
        if token in self._active_sessions:
            del self._active_sessions[token]
    
    def is_logged_in(self, request: Request) -> bool:
        """
        Vérifier si l'utilisateur est connecté
        
        Args:
            request: Requête FastAPI
            
        Returns:
            bool: True si l'utilisateur est connecté
        """
        token = request.cookies.get("session_token")
        if not token:
            return False
        return token in self._active_sessions
    
    def get_username(self, request: Request) -> str:
        """
        Récupérer le nom d'utilisateur depuis la session
        
        Args:
            request: Requête FastAPI
            
        Returns:
            str: Nom d'utilisateur ou chaîne vide
        """
        token = request.cookies.get("session_token")
        if token and token in self._active_sessions:
            return self._active_sessions[token]["username"]
        return ""
    
    def get_session_token(self, request: Request) -> Optional[str]:
        """
        Récupérer le token de session depuis la requête
        
        Args:
            request: Requête FastAPI
            
        Returns:
            Optional[str]: Token de session ou None
        """
        return request.cookies.get("session_token")
    
    def get_active_sessions_count(self) -> int:
        """
        Obtenir le nombre de sessions actives
        
        Returns:
            int: Nombre de sessions actives
        """
        return len(self._active_sessions)


# Instance singleton du service
session_service = SessionService()

