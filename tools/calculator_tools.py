from crewai_tools import tool
from typing import Dict, List
import json

class CalculatorTools:
    """Outils de calcul pour les budgets et distances"""
    
    @tool("Calculate Budget")
    def calculate_budget(items: str) -> str:
        """
        Calcule le budget total à partir d'une liste d'items.
        Format attendu: "hotel:100, food:50, transport:30"
        """
        try:
            total = 0
            breakdown = {}
            
            # Parse les items
            for item in items.split(','):
                if ':' in item:
                    category, amount = item.strip().split(':')
                    amount = float(amount)
                    breakdown[category] = amount
                    total += amount
            
            result = f"Budget Total: €{total:.2f}\n\nDétail:\n"
            for category, amount in breakdown.items():
                percentage = (amount / total * 100) if total > 0 else 0
                result += f"- {category}: €{amount:.2f} ({percentage:.1f}%)\n"
            
            return result
        
        except Exception as e:
            return f"Erreur de calcul: {str(e)}"
    
    @tool("Calculate Daily Budget")
    def calculate_daily_budget(total_budget: float, num_days: int) -> str:
        """
        Calcule le budget quotidien moyen.
        """
        try:
            daily = total_budget / num_days
            return f"Budget quotidien: €{daily:.2f}/jour pour {num_days} jours"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    @tool("Convert Currency")
    def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
        """
        Convertit une devise (taux approximatifs pour démo).
        """
        # Taux de change approximatifs (EUR base)
        rates = {
            'EUR': 1.0,
            'USD': 1.10,
            'GBP': 0.86,
            'MAD': 10.80
        }
        
        try:
            from_rate = rates.get(from_curr.upper(), 1.0)
            to_rate = rates.get(to_curr.upper(), 1.0)
            
            converted = amount * (to_rate / from_rate)
            return f"{amount} {from_curr} = {converted:.2f} {to_curr}"
        
        except Exception as e:
            return f"Erreur de conversion: {str(e)}"