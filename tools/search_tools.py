from crewai_tools import tool
from duckduckgo_search import DDGS
import json

class SearchTools:
    """Outils de recherche pour les agents"""
    
    @tool("Search Internet")
    def search_internet(query: str) -> str:
        """
        Recherche des informations sur internet.
        Utile pour trouver des informations actuelles sur les destinations,
        la météo, les événements, etc.
        """
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=5)
            
            if not results:
                return "Aucun résultat trouvé."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['body']}\n"
                    f"   Source: {result['href']}\n"
                )
            
            return "\n".join(formatted_results)
        
        except Exception as e:
            return f"Erreur lors de la recherche: {str(e)}"
    
    @tool("Search Weather")
    def search_weather(location: str, dates: str) -> str:
        """
        Recherche les prévisions météo pour une destination.
        Args:
            location: Nom de la ville
            dates: Période du voyage (ex: "1-8 septembre 2025")
        """
        query = f"weather forecast {location} {dates}"
        return SearchTools.search_internet(query)
    
    @tool("Search Flights")
    def search_flights(origin: str, destination: str, dates: str) -> str:
        """
        Recherche des informations sur les vols.
        Args:
            origin: Ville de départ
            destination: Ville d'arrivée
            dates: Dates du voyage
        """
        query = f"flights from {origin} to {destination} {dates} prices"
        return SearchTools.search_internet(query)
    
    @tool("Search Attractions")
    def search_attractions(city: str, interests: str) -> str:
        """
        Recherche les attractions touristiques.
        Args:
            city: Nom de la ville
            interests: Centres d'intérêt (ex: "histoire, gastronomie")
        """
        query = f"best attractions in {city} for {interests} tourism"
        return SearchTools.search_internet(query)