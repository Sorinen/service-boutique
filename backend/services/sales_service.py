"""
Service de gestion des ventes (Domain-Driven Design)
Responsabilités :
- Gestion des ventes
- Calculs et statistiques
- Persistance des données de ventes
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Sale:
    """Modèle de données pour une vente"""
    id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    customer_name: str
    sale_date: str
    created_by: str


class SalesService:
    """Service de gestion des ventes"""
    
    def __init__(self, sales_file: str = "sales.json"):
        self.sales_file = sales_file
        self._sales_cache: Optional[List[Dict]] = None
    
    def load_sales(self) -> List[Dict]:
        """
        Charger les ventes depuis le fichier JSON
        
        Returns:
            List[Dict]: Liste des ventes
        """
        if self._sales_cache is not None:
            return self._sales_cache
        
        if os.path.exists(self.sales_file):
            with open(self.sales_file, "r") as f:
                self._sales_cache = json.load(f)
                return self._sales_cache
        
        # Retourner une liste vide si le fichier n'existe pas
        self._sales_cache = []
        return self._sales_cache
    
    def save_sales(self, sales: List[Dict]) -> None:
        """
        Sauvegarder les ventes dans le fichier JSON
        
        Args:
            sales: Liste des ventes
        """
        with open(self.sales_file, "w") as f:
            json.dump(sales, f, indent=2)
        self._sales_cache = sales
    
    def add_sale(self, sale: Sale) -> Sale:
        """
        Ajouter une nouvelle vente
        
        Args:
            sale: Objet Sale
            
        Returns:
            Sale: La vente ajoutée
        """
        sales = self.load_sales()
        sales.append(asdict(sale))
        self.save_sales(sales)
        return sale
    
    def get_sale_by_id(self, sale_id: str) -> Optional[Dict]:
        """
        Récupérer une vente par son ID
        
        Args:
            sale_id: ID de la vente
            
        Returns:
            Optional[Dict]: Vente ou None
        """
        sales = self.load_sales()
        for sale in sales:
            if sale.get("id") == sale_id:
                return sale
        return None
    
    def get_sales_by_user(self, username: str) -> List[Dict]:
        """
        Récupérer les ventes d'un utilisateur
        
        Args:
            username: Nom d'utilisateur
            
        Returns:
            List[Dict]: Liste des ventes de l'utilisateur
        """
        sales = self.load_sales()
        return [sale for sale in sales if sale.get("created_by") == username]
    
    def get_total_revenue(self) -> float:
        """
        Calculer le chiffre d'affaires total
        
        Returns:
            float: Chiffre d'affaires total
        """
        sales = self.load_sales()
        return sum(sale.get("total_price", 0) for sale in sales)
    
    def get_sales_count(self) -> int:
        """
        Obtenir le nombre total de ventes
        
        Returns:
            int: Nombre de ventes
        """
        return len(self.load_sales())
    
    def delete_sale(self, sale_id: str) -> bool:
        """
        Supprimer une vente
        
        Args:
            sale_id: ID de la vente
            
        Returns:
            bool: True si la vente a été supprimée
        """
        sales = self.load_sales()
        initial_count = len(sales)
        sales = [sale for sale in sales if sale.get("id") != sale_id]
        
        if len(sales) < initial_count:
            self.save_sales(sales)
            return True
        return False


# Instance singleton du service
sales_service = SalesService()

