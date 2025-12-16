# 🏪 Boutique SaaS

Application de gestion des ventes pour boutique - Simple, moderne et efficace.

## 📱 Aperçu

Application web mobile-first pour suivre les ventes de votre boutique en temps réel.

## ✨ Fonctionnalités

### Dashboard
- 💰 Revenu du jour en temps réel
- 📅 Revenu du mois
- 📆 Revenu de l'année
- 🏆 Revenu total
- 📈 Graphique des ventes (courbe par jour)
- ➕ Ajout rapide de ventes

### Liste des ventes
- 🔍 Filtres : Jour / Semaine / Mois / Année / Tout
- 📊 Total dynamique selon le filtre
- 📥 Export CSV

### Sécurité
- 🔐 Authentification requise
- 🔒 Mots de passe hashés (bcrypt)
- 🍪 Sessions sécurisées
- ⏱️ Expiration automatique (24h)

### Temps réel
- 🔄 Synchronisation automatique (5 secondes)
- 🔗 Sync entre onglets

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/VOTRE_USERNAME/boutique.git
cd boutique

# 2. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou .venv\Scripts\activate  # Windows

# 3. Installer les dépendances
cd backend
pip install -r requirements.txt

# 4. Lancer le serveur
uvicorn main:app --reload
```

### Accès
- **URL** : http://127.0.0.1:8000
- **Login** : `admin` / `admin123`
- **Login alternatif** : `boutique` / `boutique123`

#### 🔧 Modifier le code
1. 🏗️ [backend/ARCHITECTURE.md](./backend/ARCHITECTURE.md) - Structure du projet
2. 📖 [backend/QUICK_START.md](./backend/QUICK_START.md) - Exemples de modifications
3. 🧪 Tester avec `python backend/test_architecture.py`

### 📖 Tous les documents

| Document | Description | Durée |
|----------|-------------|-------|
| [backend/QUICK_START.md](./backend/QUICK_START.md) | Guide de démarrage rapide | 5 min |
| [backend/README.md](./backend/README.md) | Documentation complète | 15 min |
| [backend/ARCHITECTURE.md](./backend/ARCHITECTURE.md) | Architecture DDD détaillée | 30 min |
| [backend/DIAGRAM.md](./backend/DIAGRAM.md) | Diagrammes visuels | 20 min |
| [backend/CODE_REVIEW.md](./backend/CODE_REVIEW.md) | Review et recommandations | 45 min |
| [backend/INDEX.md](./backend/INDEX.md) | Navigation complète | 5 min |
| [REVIEW_SUMMARY.md](./REVIEW_SUMMARY.md) | Résumé de la review | 10 min |
| [CHANGELOG.md](./CHANGELOG.md) | Historique des modifications | 5 min |
| [FINAL_SUMMARY.md](./FINAL_SUMMARY.md) | Résumé final complet | 10 min |

---

## 🏗️ Architecture

### Structure du Projet

```
boutique/
├── backend/
│   ├── main.py              # Serveur FastAPI
│   ├── requirements.txt     # Dépendances Python
│   ├── users.json           # Utilisateurs (généré)
│   └── api/
│       └── sales.py         # (Future API)
│
├── fondend/
│   └── static/
│       ├── style.css        # Styles CSS
│       ├── script.js        # JS Dashboard
│       └── full-sales.js    # JS Liste ventes
│
├── templates/
│   └── fondend/
│       ├── login.html       # Page connexion
│       ├── index.html       # Dashboard
│       └── ventes.html      # Liste ventes
│
└── README.md
```

## 🛠️ Technologies

| Composant | Technologie |
|-----------|-------------|
| Backend | FastAPI (Python) |
| Frontend | HTML, CSS, JavaScript |
| Auth | Passlib + bcrypt |
| Templates | Jinja2 |
| Stockage | localStorage (client) |

## 📋 Feuille de route

### ✅ Version 1.0 (Actuelle)
- [x] Dashboard avec statistiques
- [x] Graphique des ventes
- [x] Ajout de ventes
- [x] Liste des ventes avec filtres
- [x] Export CSV
- [x] Authentification sécurisée
- [x] Design mobile-first
- [x] Synchronisation temps réel

### 🔜 Version 2.0 (Prévue)
- [ ] Base de données (SQLite/PostgreSQL)
- [ ] API REST complète
- [ ] Gestion des produits
- [ ] Multi-utilisateurs
- [ ] Tableau de bord admin
- [ ] Notifications

### 🔮 Version 3.0 (Future)
- [ ] PWA (Progressive Web App)
- [ ] Mode hors-ligne
- [ ] Rapports PDF
- [ ] Intégration paiement
- [ ] Multi-boutiques

## 👤 Auteur

Développé avec ❤️

## 📄 Licence

MIT License - Libre d'utilisation
# service-boutique
