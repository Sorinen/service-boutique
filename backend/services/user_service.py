"""
Service de gestion des utilisateurs (Domain-Driven Design)
Responsabilités :
- Chargement et sauvegarde des utilisateurs
- Authentification et vérification des mots de passe
- Gestion du cache des utilisateurs
"""
import json
import os
from typing import Dict, Optional
from config import pwd_context, USERS_FILE


class UserService:
    """Service de gestion des utilisateurs"""
    
    def __init__(self):
        self._users_cache: Optional[Dict[str, str]] = None
    
    def load_users(self) -> Dict[str, str]:
        """
        Charger les utilisateurs depuis le fichier JSON (avec cache)
        
        Returns:
            Dict[str, str]: Dictionnaire {username: hashed_password}
        """
        # Utiliser le cache si disponible
        if self._users_cache is not None:
            return self._users_cache
        
        # Charger depuis le fichier si existant
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                self._users_cache = json.load(f)
                return self._users_cache
        
        # Créer les utilisateurs par défaut
        default_users = {
            "admin": pwd_context.hash("admin123"),
            "boutique": pwd_context.hash("boutique123")
        }
        self.save_users(default_users)
        self._users_cache = default_users
        return default_users
    
    def save_users(self, users: Dict[str, str]) -> None:
        """
        Sauvegarder les utilisateurs dans le fichier JSON
        
        Args:
            users: Dictionnaire {username: hashed_password}
        """
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
        self._users_cache = users  # Mettre à jour le cache
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Vérifier un mot de passe contre son hash
        
        Args:
            plain_password: Mot de passe en clair
            hashed_password: Hash du mot de passe
            
        Returns:
            bool: True si le mot de passe correspond
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        """
        Hasher un mot de passe
        
        Args:
            password: Mot de passe en clair
            
        Returns:
            str: Hash du mot de passe
        """
        return pwd_context.hash(password)
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authentifier un utilisateur
        
        Args:
            username: Nom d'utilisateur
            password: Mot de passe en clair
            
        Returns:
            bool: True si l'authentification réussit
        """
        users = self.load_users()
        
        if username not in users:
            return False
        
        return self.verify_password(password, users[username])
    
    def user_exists(self, username: str) -> bool:
        """
        Vérifier si un utilisateur existe
        
        Args:
            username: Nom d'utilisateur
            
        Returns:
            bool: True si l'utilisateur existe
        """
        users = self.load_users()
        return username in users
    
    def initialize(self) -> None:
        """Initialiser le service (charger les utilisateurs au démarrage)"""
        self.load_users()


# Instance singleton du service
user_service = UserService()

