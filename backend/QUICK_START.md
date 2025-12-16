# 🚀 Guide de Démarrage Rapide

## 📦 Installation (5 minutes)

### Étape 1 : Environnement virtuel
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Étape 2 : Dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Lancer l'application
```bash
uvicorn main:app --reload
```

✅ **C'est prêt !** Ouvrez http://localhost:8000

---

## 🎯 Utilisation

### Se connecter
1. Allez sur http://localhost:8000/login
2. Utilisez : **admin** / **admin123**
3. Vous êtes redirigé vers le dashboard

### Tester l'API
```bash
# Vérifier le statut
curl http://localhost:8000/api/status

# Réponse :
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2024-12-16T...",
  "active_sessions": 1
}
```

---

## 📁 Structure du Code

```
backend/
│
├── 🎯 main.py              ← Point d'entrée FastAPI
├── ⚙️  config.py            ← Configuration centralisée
│
├── 🔧 services/            ← Logique métier (Domain)
│   ├── user_service.py     ← Gestion utilisateurs
│   ├── session_service.py  ← Gestion sessions
│   └── sales_service.py    ← Gestion ventes
│
└── 🛣️  routers/             ← Routes HTTP (API)
    ├── auth_router.py      ← /login, /logout
    ├── pages_router.py     ← /, /ventes
    └── api_router.py       ← /api/*
```

---

## 🔍 Comment ça marche ?

### 1. Authentification
```
User → /login → auth_router → user_service → Vérif password
                                    ↓
                            session_service → Créer token
                                    ↓
                            Cookie avec token → Redirect /
```

### 2. Page protégée
```
User → / → pages_router → session_service.is_logged_in()
                                ↓
                          Token valide ? → Afficher page
                                ↓
                          Token invalide ? → Redirect /login
```

### 3. API
```
User → /api/sales → api_router → session_service.is_logged_in()
                                        ↓
                                  sales_service.load_sales()
                                        ↓
                                  Return JSON
```

---

## 🧪 Tester le Code

```bash
# Lancer les tests
python test_architecture.py

# Résultat attendu :
# ✅ PASS - Imports
# ✅ PASS - UserService
# ✅ PASS - SessionService
# ✅ PASS - SalesService
# ✅ PASS - Routers
# 🎯 Score: 5/5 tests réussis
```

---

## 🔧 Modifier le Code

### Ajouter une nouvelle route

**1. Dans le router approprié :**
```python
# routers/pages_router.py

@router.get("/nouvelle-page", response_class=HTMLResponse)
def page_nouvelle(request: Request):
    """Ma nouvelle page"""
    if not session_service.is_logged_in(request):
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse(
        "nouvelle.html",
        {"request": request, "username": session_service.get_username(request)}
    )
```

**2. Créer le template :**
```html
<!-- templates/fondend/nouvelle.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Nouvelle Page</title>
</head>
<body>
    <h1>Bienvenue {{ username }} !</h1>
</body>
</html>
```

**3. Tester :**
```bash
# Redémarrer le serveur (avec --reload, c'est automatique)
# Aller sur http://localhost:8000/nouvelle-page
```

### Ajouter une méthode à un service

```python
# services/user_service.py

def get_user_count(self) -> int:
    """
    Obtenir le nombre d'utilisateurs
    
    Returns:
        int: Nombre d'utilisateurs
    """
    users = self.load_users()
    return len(users)
```

### Ajouter une route API

```python
# routers/api_router.py

@router.get("/users/count")
def api_users_count(request: Request):
    """Obtenir le nombre d'utilisateurs"""
    if not session_service.is_logged_in(request):
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    count = user_service.get_user_count()
    return {"count": count}
```

---

## 🐛 Dépannage

### Problème : Port déjà utilisé
```bash
# Solution : Changer le port
uvicorn main:app --reload --port 8001
```

### Problème : Module non trouvé
```bash
# Solution : Activer le venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problème : Erreur bcrypt
```bash
# Solution : Réinstaller bcrypt
pip install bcrypt==4.0.1 --force-reinstall
```

### Problème : Fichier JSON corrompu
```bash
# Solution : Supprimer et relancer
rm users.json sales.json
python main.py
```

---

## 📚 Ressources

### Documentation
- 📖 [README.md](./README.md) - Guide complet
- 🏗️ [ARCHITECTURE.md](./ARCHITECTURE.md) - Architecture détaillée
- 📊 [DIAGRAM.md](./DIAGRAM.md) - Diagrammes visuels
- 📝 [CODE_REVIEW.md](./CODE_REVIEW.md) - Review et recommandations

### API
- 🌐 http://localhost:8000/docs - Documentation Swagger
- 🔍 http://localhost:8000/redoc - Documentation ReDoc

### FastAPI
- 🚀 https://fastapi.tiangolo.com/ - Documentation officielle
- 📚 https://fastapi.tiangolo.com/tutorial/ - Tutoriel complet

---

## 💡 Astuces

### 1. Voir les logs en temps réel
```bash
uvicorn main:app --reload --log-level debug
```

### 2. Recharger automatiquement
Le flag `--reload` recharge automatiquement quand vous modifiez le code !

### 3. Tester l'API avec curl
```bash
# Statut
curl http://localhost:8000/api/status

# Avec authentification (récupérer le cookie d'abord)
curl -b cookies.txt http://localhost:8000/api/user
```

### 4. Formater le code
```bash
pip install black
black .
```

### 5. Vérifier les types
```bash
pip install mypy
mypy main.py
```

---

## 🎯 Prochaines Étapes

1. ✅ Comprendre l'architecture DDD
2. ✅ Tester toutes les fonctionnalités
3. 📝 Ajouter des tests unitaires
4. 🔐 Ajouter la validation Pydantic
5. 💾 Migrer vers PostgreSQL
6. 🐳 Dockeriser l'application

---

## ❓ Questions Fréquentes

**Q: Où sont stockés les utilisateurs ?**  
R: Dans `users.json` (créé automatiquement au démarrage)

**Q: Comment ajouter un utilisateur ?**  
R: Modifiez `user_service.py` ou ajoutez-le manuellement dans `users.json` (avec mot de passe hashé)

**Q: Les sessions sont-elles persistantes ?**  
R: Non, elles sont en mémoire. Utilisez Redis en production.

**Q: Puis-je utiliser ce code en production ?**  
R: Oui, mais ajoutez d'abord : validation, tests, vraie BDD, HTTPS, logging.

**Q: Comment contribuer ?**  
R: Créez une branche, faites vos modifications, testez, puis créez une PR !

---

## 🎉 Félicitations !

Vous avez maintenant une application FastAPI moderne avec architecture DDD !

**Bon développement !** 🚀

