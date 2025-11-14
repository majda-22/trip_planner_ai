from crewai.tools import tool  # <-- 1. Import 'tool' (lowercase)
import requests
from bs4 import BeautifulSoup

# 2. We removed the 'class BrowserTools:' line and un-indented the function

@tool("Scrape Website")
def scrape_website(url: str) -> str:
    """
    Extrait le contenu textuel d'une page web.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Retirer les scripts et styles
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        # Extraire le texte
        text = soup.get_text()
        
        # Nettoyer
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limiter la longueur
        return text[:4000] + "..." if len(text) > 4000 else text
    
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion lors du scraping ({url}): {str(e)}"
    except Exception as e:
        return f"Erreur lors du scraping ({url}): {str(e)}"