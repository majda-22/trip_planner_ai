from crewai import Crew, Process
from agents.trip_agents import TripAgents
from tasks.trip_tasks import TripTasks
from datetime import datetime
import os

class TripCrew:
    """Classe principale pour orchestrer le Trip Planner"""
    
    def __init__(self, origin: str, cities: str, date_range: str,
                 duration: int, interests: str, budget: str):
        """
        Initialise le crew avec les paramètres du voyage
        
        Args:
            origin: Ville de départ
            cities: Liste des villes à considérer (séparées par des virgules)
            date_range: Période du voyage (ex: "1-8 septembre 2025")
            duration: Durée en jours
            interests: Centres d'intérêt (ex: "histoire, gastronomie, art")
            budget: Budget total (ex: "2000 EUR")
        """
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.duration = duration
        self.interests = interests
        self.budget = budget
        
        # Créer le dossier outputs s'il n'existe pas
        os.makedirs('outputs', exist_ok=True)
        
        # Initialiser les agents et tâches
        self.agents_factory = TripAgents()
        self.tasks_factory = TripTasks()
        
        # Variable pour stocker la ville sélectionnée
        self.selected_city = None
    
    def run(self):
        """Exécute le workflow complet de planification"""
        
        print("\n" + "="*60)
        print("🌍 DÉMARRAGE DU TRIP PLANNER AI")
        print("="*60)
        print(f"📍 Origine: {self.origin}")
        print(f"🎯 Destinations: {self.cities}")
        print(f"📅 Dates: {self.date_range}")
        print(f"⏱️  Durée: {self.duration} jours")
        print(f"💰 Budget: {self.budget}")
        print(f"❤️  Intérêts: {self.interests}")
        print("="*60 + "\n")
        
        # PHASE 1: Sélection de la ville
        print("\n🔍 PHASE 1: Analyse et Sélection de la Destination...")
        print("-" * 60)
        
        city_agent = self.agents_factory.city_selection_expert(
            cities=self.cities,
            origin=self.origin,
            date_range=self.date_range,
            interests=self.interests
        )
        
        city_task = self.tasks_factory.city_selection_task(
            agent=city_agent,
            cities=self.cities,
            origin=self.origin,
            date_range=self.date_range,
            interests=self.interests
        )
        
        city_crew = Crew(
            agents=[city_agent],
            tasks=[city_task],
            process=Process.sequential,
            verbose=True
        )
        
        city_result = city_crew.kickoff()
        
        # Extraire la ville recommandée du résultat
        # (simplifié: prendre la première ville mentionnée)
        self.selected_city = self.cities.split(',')[0].strip()
        print(f"\n✅ Ville sélectionnée: {self.selected_city}\n")
        
        # PHASE 2: Expertise locale
        print("\n🏛️ PHASE 2: Collecte d'Informations Locales...")
        print("-" * 60)
        
        local_agent = self.agents_factory.local_expert(
            city=self.selected_city,
            interests=self.interests
        )
        
        local_task = self.tasks_factory.local_insights_task(
            agent=local_agent,
            city=self.selected_city,
            interests=self.interests,
            date_range=self.date_range,
            context=[city_task]
        )
        
        local_crew = Crew(
            agents=[local_agent],
            tasks=[local_task],
            process=Process.sequential,
            verbose=True
        )
        
        local_result = local_crew.kickoff()
        print("\n✅ Informations locales collectées\n")
        
        # PHASE 3: Planification d'itinéraire
        print("\n📋 PHASE 3: Création de l'Itinéraire Détaillé...")
        print("-" * 60)
        
        concierge_agent = self.agents_factory.travel_concierge(
            city=self.selected_city,
            duration=self.duration,
            budget=self.budget
        )
        
        itinerary_task = self.tasks_factory.itinerary_planning_task(
            agent=concierge_agent,
            city=self.selected_city,
            duration=self.duration,
            budget=self.budget,
            context=[city_task, local_task]
        )
        
        itinerary_crew = Crew(
            agents=[concierge_agent],
            tasks=[itinerary_task],
            process=Process.sequential,
            verbose=True
        )
        
        itinerary_result = itinerary_crew.kickoff()
        print("\n✅ Itinéraire créé\n")
        
        # PHASE 4: Génération du rapport final
        print("\n📄 PHASE 4: Génération du Rapport Final...")
        print("-" * 60)
        
        reporter_agent = self.agents_factory.reporter()
        
        report_task = self.tasks_factory.report_generation_task(
            agent=reporter_agent,
            context=[city_task, local_task, itinerary_task]
        )
        
        report_crew = Crew(
            agents=[reporter_agent],
            tasks=[report_task],
            process=Process.sequential,
            verbose=True
        )
        
        final_report = report_crew.kickoff()
        
        print("\n" + "="*60)
        print("✅ PLANIFICATION TERMINÉE!")
        print("="*60)
        print(f"\n📁 Les rapports ont été sauvegardés dans le dossier 'outputs/'")
        print(f"📄 Rapport final: outputs/trip_report.md\n")
        
        return final_report

# Test de base
if __name__ == "__main__":
    crew = TripCrew(
        origin="Casablanca",
        cities="Madrid, Barcelona, Valencia",
        date_range="1-8 septembre 2025",
        duration=7,
        interests="histoire, gastronomie, art",
        budget="2000 EUR"
    )
    
    result = crew.run()
    print("\n" + "="*60)
    print("RÉSULTAT FINAL")
    print("="*60)
    print(result)