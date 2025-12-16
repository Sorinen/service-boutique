"""
Configuration centralisée de l'application
"""
import secrets
from passlib.context import CryptContext

# Configuration de l'application
APP_TITLE = "Boutique SaaS"
APP_VERSION = "1.0.0"

# Clé secrète (en production, utiliser une variable d'environnement)
SECRET_KEY = secrets.token_hex(32)

# Fichiers et chemins
USERS_FILE = "users.json"
STATIC_DIR = "../fondend/static"
TEMPLATES_DIR = "../templates/fondend"

# Configuration de sécurité
COOKIE_MAX_AGE = 86400  # 24 heures
COOKIE_HTTPONLY = True
COOKIE_SECURE = False  # Mettre True en production avec HTTPS
COOKIE_SAMESITE = "lax"

# Hashage des mots de passe (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

