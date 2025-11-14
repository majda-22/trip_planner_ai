from crewai_tools import tool
import requests
from bs4 import BeautifulSoup

class BrowserTools:
    """Outils pour extraire du contenu web"""
    
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
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Retirer les scripts et styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extraire le texte
            text = soup.get_text()
            
            # Nettoyer
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limiter la longueur
            return text[:3000] + "..." if len(text) > 3000 else text
        
        except Exception as e:
            return f"Erreur lors du scraping: {str(e)}"