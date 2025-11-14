from crewai import Task
import yaml

class TripTasks:
    """Classe pour créer et gérer les tâches du Trip Planner"""
    
    def __init__(self):
        with open('config/tasks.yaml', 'r', encoding='utf-8') as f:
            self.tasks_config = yaml.safe_load(f)
    
    def city_selection_task(self, agent, cities: str, origin: str,
                           date_range: str, interests: str) -> Task:
        """Crée la tâche de sélection de ville"""
        config = self.tasks_config['city_selection_task']
        
        return Task(
            description=config['description'].format(
                cities=cities,
                origin=origin,
                date_range=date_range,
                interests=interests
            ),
            expected_output=config['expected_output'],
            agent=agent,
            output_file='outputs/city_selection.md'
        )
    
    def local_insights_task(self, agent, city: str, interests: str,
                           date_range: str, context: list = None) -> Task:
        """Crée la tâche d'expertise locale"""
        config = self.tasks_config['local_insights_task']
        
        return Task(
            description=config['description'].format(
                city=city,
                interests=interests,
                date_range=date_range
            ),
            expected_output=config['expected_output'],
            agent=agent,
            context=context if context else [],
            output_file='outputs/local_insights.md'
        )
    
    def itinerary_planning_task(self, agent, city: str, duration: int,
                               budget: str, context: list = None) -> Task:
        """Crée la tâche de planification d'itinéraire"""
        config = self.tasks_config['itinerary_planning_task']
        
        return Task(
            description=config['description'].format(
                duration=duration,
                city=city,
                budget=budget
            ),
            expected_output=config['expected_output'],
            agent=agent,
            context=context if context else [],
            output_file='outputs/itinerary.md'
        )
    
    def report_generation_task(self, agent, context: list = None) -> Task:
        """Crée la tâche de génération de rapport"""
        config = self.tasks_config['report_generation_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=agent,
            context=context if context else [],
            output_file='outputs/trip_report.md'
        )