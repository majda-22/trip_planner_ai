from crewai.tools import tool  # <-- 1. Import 'tool' (lowercase)
from typing import Dict, List
import json

# 2. We removed the 'class CalculatorTools:' line and un-indented everything

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
        
        if total == 0:
             return "Impossible de calculer le budget. Aucun item valide fourni."

        result = f"Budget Total: €{total:.2f}\n\nDétail:\n"
        for category, amount in breakdown.items():
            percentage = (amount / total * 100)
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
        # Assurer que les jours sont un entier positif
        if num_days <= 0:
            return "Erreur: Le nombre de jours doit être supérieur à 0."
        
        daily = total_budget / num_days
        return f"Budget quotidien: €{daily:.2f}/jour pour {num_days} jours"
    
    except ZeroDivisionError:
        return "Erreur: Le nombre de jours ne peut pas être zéro."
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
        from_curr_upper = from_curr.upper()
        to_curr_upper = to_curr.upper()

        if from_curr_upper not in rates:
            return f"Erreur: Devise de départ '{from_curr}' non supportée."
        if to_curr_upper not in rates:
            return f"Erreur: Devise d'arrivée '{to_curr}' non supportée."

        from_rate = rates[from_curr_upper]
        to_rate = rates[to_curr_upper]
        
        converted = amount * (to_rate / from_rate)
        return f"{amount} {from_curr_upper} = {converted:.2f} {to_curr_upper}"
    
    except Exception as e:
        return f"Erreur de conversion: {str(e)}"