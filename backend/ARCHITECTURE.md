# 🏗️ Architecture de l'Application Boutique SaaS

## 📋 Vue d'ensemble

Cette application suit les principes du **Domain-Driven Design (DDD)** avec une séparation claire des responsabilités.

## 📁 Structure du projet

```
backend/
├── config.py                 # Configuration centralisée
├── main.py                   # Point d'entrée de l'application
├── requirements.txt          # Dépendances Python
├── users.json               # Base de données utilisateurs (JSON)
├── sales.json               # Base de données ventes (JSON)
│
├── services/                # Couche métier (Domain Layer)
│   ├── __init__.py
│   ├── user_service.py      # Gestion des utilisateurs
│   ├── session_service.py   # Gestion des sessions
│   └── sales_service.py     # Gestion des ventes
│
└── routers/                 # Couche présentation (API Layer)
    ├── __init__.py
    ├── auth_router.py       # Routes d'authentification
    ├── pages_router.py      # Routes des pages web
    └── api_router.py        # Routes API REST
```

## 🎯 Principes DDD appliqués

### 1. **Séparation des préoccupations**
- **Services** : Logique métier pure (domaine)
- **Routers** : Gestion des requêtes HTTP (présentation)
- **Config** : Configuration centralisée

### 2. **Services (Domain Layer)**

#### 🔐 UserService (`user_service.py`)
**Responsabilités :**
- Chargement et sauvegarde des utilisateurs
- Authentification et vérification des mots de passe
- Gestion du cache des utilisateurs

**Méthodes principales :**
- `load_users()` : Charger les utilisateurs (avec cache)
- `save_users(users)` : Sauvegarder les utilisateurs
- `authenticate(username, password)` : Authentifier un utilisateur
- `verify_password(plain, hashed)` : Vérifier un mot de passe
- `hash_password(password)` : Hasher un mot de passe
- `user_exists(username)` : Vérifier l'existence d'un utilisateur

#### 🎫 SessionService (`session_service.py`)
**Responsabilités :**
- Création et suppression de sessions
- Vérification de l'état de connexion
- Récupération des informations de session

**Méthodes principales :**
- `create_session(username)` : Créer une session
- `delete_session(token)` : Supprimer une session
- `is_logged_in(request)` : Vérifier si l'utilisateur est connecté
- `get_username(request)` : Récupérer le nom d'utilisateur
- `get_session_token(request)` : Récupérer le token de session
- `get_active_sessions_count()` : Nombre de sessions actives

#### 💰 SalesService (`sales_service.py`)
**Responsabilités :**
- Gestion des ventes
- Calculs et statistiques
- Persistance des données de ventes

**Méthodes principales :**
- `load_sales()` : Charger les ventes
- `save_sales(sales)` : Sauvegarder les ventes
- `add_sale(sale)` : Ajouter une vente
- `get_sale_by_id(id)` : Récupérer une vente par ID
- `get_sales_by_user(username)` : Ventes d'un utilisateur
- `get_total_revenue()` : Chiffre d'affaires total
- `delete_sale(id)` : Supprimer une vente

**Modèle de données :**
```python
@dataclass
class Sale:
    id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    customer_name: str
    sale_date: str
    created_by: str
```

### 3. **Routers (Presentation Layer)**

#### 🔑 AuthRouter (`auth_router.py`)
**Routes :**
- `GET /login` : Page de connexion
- `POST /login` : Traitement de la connexion
- `GET /logout` : Déconnexion

#### 📄 PagesRouter (`pages_router.py`)
**Routes :**
- `GET /` : Dashboard principal (protégé)
- `GET /ventes` : Page liste des ventes (protégé)

#### 🔌 ApiRouter (`api_router.py`)
**Routes :**
- `GET /api/status` : Statut de l'API
- `GET /api/user` : Info utilisateur connecté
- `GET /api/sales` : Toutes les ventes
- `GET /api/sales/user` : Ventes de l'utilisateur
- `GET /api/sales/{id}` : Détail d'une vente

### 4. **Configuration (`config.py`)**
Centralise toutes les configurations :
- Paramètres de l'application
- Configuration de sécurité
- Chemins des fichiers
- Configuration des cookies
- Configuration bcrypt

## 🔄 Flux de données

### Authentification
```
1. User → POST /login → auth_router
2. auth_router → user_service.authenticate()
3. user_service → Vérifie le mot de passe
4. auth_router → session_service.create_session()
5. session_service → Crée un token
6. auth_router → Retourne cookie avec token
```

### Accès à une page protégée
```
1. User → GET / → pages_router
2. pages_router → session_service.is_logged_in()
3. session_service → Vérifie le token dans les cookies
4. pages_router → Affiche la page ou redirige vers /login
```

### Récupération des ventes
```
1. User → GET /api/sales → api_router
2. api_router → session_service.is_logged_in()
3. api_router → sales_service.load_sales()
4. sales_service → Charge depuis sales.json (avec cache)
5. api_router → Retourne les données JSON
```

## ✅ Avantages de cette architecture

### 1. **Maintenabilité**
- Code organisé et facile à naviguer
- Chaque fichier a une responsabilité claire
- Modifications isolées (pas d'effet domino)

### 2. **Testabilité**
- Services testables indépendamment
- Pas de dépendances circulaires
- Mock facile des services

### 3. **Réutilisabilité**
- Services utilisables par plusieurs routers
- Logique métier centralisée
- Pas de duplication de code

### 4. **Scalabilité**
- Facile d'ajouter de nouveaux services
- Facile d'ajouter de nouvelles routes
- Pattern singleton pour les services

### 5. **Sécurité**
- Configuration centralisée
- Validation au niveau des services
- Séparation des préoccupations

## 🚀 Utilisation

### Démarrer l'application
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Ajouter un nouveau service
1. Créer `services/mon_service.py`
2. Définir la classe `MonService`
3. Créer l'instance singleton `mon_service = MonService()`
4. Exporter dans `services/__init__.py`
5. Importer dans les routers nécessaires

### Ajouter un nouveau router
1. Créer `routers/mon_router.py`
2. Définir `router = APIRouter()`
3. Ajouter les routes avec `@router.get/post/etc`
4. Exporter dans `routers/__init__.py`
5. Enregistrer dans `main.py` avec `app.include_router()`

## 📚 Bonnes pratiques appliquées

✅ **Singleton Pattern** : Un seul instance de chaque service  
✅ **Dependency Injection** : Services injectés dans les routers  
✅ **Cache Pattern** : Cache en mémoire pour les données fréquentes  
✅ **Repository Pattern** : Services comme couche d'abstraction des données  
✅ **Type Hints** : Types Python pour meilleure documentation  
✅ **Docstrings** : Documentation de toutes les fonctions  
✅ **Dataclasses** : Modèles de données structurés  

## 🔧 Améliorations futures possibles

1. **Base de données** : Remplacer JSON par PostgreSQL/MongoDB
2. **Redis** : Cache distribué pour les sessions
3. **JWT** : Tokens JWT au lieu de sessions en mémoire
4. **Validation** : Pydantic models pour validation des données
5. **Tests** : Tests unitaires et d'intégration
6. **Logging** : Système de logs structurés
7. **Middleware** : Middleware d'authentification global
8. **CORS** : Configuration CORS pour API
9. **Rate Limiting** : Limitation du nombre de requêtes
10. **Documentation** : Swagger/OpenAPI automatique

## 📖 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

