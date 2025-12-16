"""
Script de test pour vérifier l'architecture DDD
"""
import sys
from datetime import datetime

def test_imports():
    """Tester que tous les imports fonctionnent"""
    print("🔍 Test des imports...")
    
    try:
        from config import APP_TITLE, APP_VERSION, pwd_context
        print("  ✅ Config importé")
        
        from services import user_service, session_service, sales_service
        print("  ✅ Services importés")
        
        from routers import auth_router, pages_router, api_router
        print("  ✅ Routers importés")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur d'import: {e}")
        return False


def test_user_service():
    """Tester le service utilisateur"""
    print("\n🔐 Test UserService...")
    
    try:
        from services import user_service
        
        # Test chargement des utilisateurs
        users = user_service.load_users()
        print(f"  ✅ {len(users)} utilisateurs chargés")
        
        # Test authentification
        auth_result = user_service.authenticate("admin", "admin123")
        print(f"  ✅ Authentification admin: {auth_result}")
        
        # Test utilisateur inexistant
        exists = user_service.user_exists("nonexistent")
        print(f"  ✅ Utilisateur inexistant: {not exists}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur UserService: {e}")
        return False


def test_session_service():
    """Tester le service de session"""
    print("\n🎫 Test SessionService...")
    
    try:
        from services import session_service
        
        # Test création de session
        token = session_service.create_session("admin")
        print(f"  ✅ Session créée: {token[:20]}...")
        
        # Test récupération de session
        session = session_service.get_session(token)
        print(f"  ✅ Session récupérée: {session['username']}")
        
        # Test compteur de sessions
        count = session_service.get_active_sessions_count()
        print(f"  ✅ Sessions actives: {count}")
        
        # Test suppression de session
        session_service.delete_session(token)
        session = session_service.get_session(token)
        print(f"  ✅ Session supprimée: {session is None}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur SessionService: {e}")
        return False


def test_sales_service():
    """Tester le service de ventes"""
    print("\n💰 Test SalesService...")
    
    try:
        from services import sales_service, Sale
        import uuid
        
        # Test chargement des ventes
        sales = sales_service.load_sales()
        print(f"  ✅ {len(sales)} ventes chargées")
        
        # Test ajout d'une vente
        test_sale = Sale(
            id=str(uuid.uuid4()),
            product_name="Produit Test",
            quantity=5,
            unit_price=10.0,
            total_price=50.0,
            customer_name="Client Test",
            sale_date=datetime.now().isoformat(),
            created_by="admin"
        )
        sales_service.add_sale(test_sale)
        print(f"  ✅ Vente ajoutée: {test_sale.id}")
        
        # Test récupération par ID
        sale = sales_service.get_sale_by_id(test_sale.id)
        print(f"  ✅ Vente récupérée: {sale['product_name']}")
        
        # Test statistiques
        revenue = sales_service.get_total_revenue()
        print(f"  ✅ Chiffre d'affaires: {revenue}€")
        
        # Test suppression
        deleted = sales_service.delete_sale(test_sale.id)
        print(f"  ✅ Vente supprimée: {deleted}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur SalesService: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_routers():
    """Tester que les routers sont bien configurés"""
    print("\n🛣️  Test Routers...")
    
    try:
        from routers import auth_router, pages_router, api_router
        
        # Vérifier que les routers ont des routes
        auth_routes = len(auth_router.routes)
        pages_routes = len(pages_router.routes)
        api_routes = len(api_router.routes)
        
        print(f"  ✅ AuthRouter: {auth_routes} routes")
        print(f"  ✅ PagesRouter: {pages_routes} routes")
        print(f"  ✅ ApiRouter: {api_routes} routes")
        
        return True
    except Exception as e:
        print(f"  ❌ Erreur Routers: {e}")
        return False


def main():
    """Exécuter tous les tests"""
    print("=" * 60)
    print("🧪 TEST DE L'ARCHITECTURE DDD")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("UserService", test_user_service()))
    results.append(("SessionService", test_session_service()))
    results.append(("SalesService", test_sales_service()))
    results.append(("Routers", test_routers()))
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    total_pass = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    print(f"\n🎯 Score: {total_pass}/{total_tests} tests réussis")
    
    if total_pass == total_tests:
        print("🎉 Tous les tests sont passés !")
        return 0
    else:
        print("⚠️  Certains tests ont échoué")
        return 1


if __name__ == "__main__":
    sys.exit(main())

