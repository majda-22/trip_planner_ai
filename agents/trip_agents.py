from crewai import Agent
from langchain_community.llms import Ollama
from tools.search_tools import SearchInternetTool, SearchWeatherTool, SearchFlightsTool, SearchAttractionsTool
from tools.calculator_tools import CalculatorTools
from tools.browser_tools import BrowserTools
import yaml
import os

class TripAgents:
    """Classe pour créer et gérer les agents du Trip Planner avec Ollama"""
    
    def __init__(self, model_name: str = "gemma3:4b"):
        """
        Initialise les agents avec Ollama
        
        Args:
            model_name: Nom du modèle Ollama à utiliser
                       Options recommandées:
                       - "gemma2:2b" (rapide, léger, recommandé)
                       - "llama3.2" (plus puissant)
                       - "mistral" (bon équilibre)
        """
        # Charger la configuration
        config_path = os.path.join('config', 'agents.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.agents_config = yaml.safe_load(f)
        
        # Initialiser le LLM avec Ollama
        self.llm = Ollama(
            model=model_name,
            base_url="http://localhost:11434",  # URL par défaut d'Ollama
            temperature=0.7,
            num_predict=2048,  # Limite de tokens pour la génération
            top_k=40,
            top_p=0.9,
            repeat_penalty=1.1
        )
        
        print(f"✅ LLM initialisé: Ollama avec {model_name}")
        
        # Initialiser les outils
        self.search_internet_tool = SearchInternetTool()
        self.search_weather_tool = SearchWeatherTool()
        self.search_flights_tool = SearchFlightsTool()
        self.search_attractions_tool = SearchAttractionsTool()
        self.calculator_tools = CalculatorTools()
        self.browser_tools = BrowserTools()
    
    def city_selection_expert(self, cities: str, origin: str, 
                              date_range: str, interests: str) -> Agent:
        """Crée l'agent expert en sélection de villes"""
        config = self.agents_config['city_selection_expert']
        
        return Agent(
            role=config['role'],
            goal=config['goal'].format(
                cities=cities,
                origin=origin,
                date_range=date_range
            ),
            backstory=config['backstory'],
            tools=[
                self.search_internet_tool,
                self.search_weather_tool,
                self.search_flights_tool,
                self.calculator_tools.calculate_budget
            ],
            llm=self.llm,
            verbose=True,
            max_iter=5,
            allow_delegation=False  # Important pour Ollama
        )
    
    def local_expert(self, city: str, interests: str) -> Agent:
        """Crée l'agent expert local"""
        config = self.agents_config['local_expert']
        
        return Agent(
            role=config['role'],
            goal=config['goal'].format(
                city=city,
                interests=interests
            ),
            backstory=config['backstory'].format(city=city),
            tools=[
                self.search_internet_tool,
                self.search_attractions_tool,
                self.browser_tools.scrape_website
            ],
            llm=self.llm,
            verbose=True,
            max_iter=5,
            allow_delegation=False
        )
    
    def travel_concierge(self, city: str, duration: int, budget: str) -> Agent:
        """Crée l'agent concierge de voyage"""
        config = self.agents_config['travel_concierge']
        
        return Agent(
            role=config['role'],
            goal=config['goal'].format(
                duration=duration,
                city=city,
                budget=budget
            ),
            backstory=config['backstory'],
            tools=[
                self.search_internet_tool,
                self.calculator_tools.calculate_budget,
                self.calculator_tools.calculate_daily_budget,
                self.calculator_tools.convert_currency
            ],
            llm=self.llm,
            verbose=True,
            max_iter=5,
            allow_delegation=False
        )
    
    def reporter(self) -> Agent:
        """Crée l'agent rédacteur de rapport"""
        config = self.agents_config['reporter']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[],  # Pas besoin d'outils, juste de la rédaction
            llm=self.llm,
            verbose=True,
            max_iter=3,
            allow_delegation=False
        )