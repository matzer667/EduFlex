from slot_generator import SlotGenerator
from scheduling_algorithm import SchedulingAlgorithm
from stats import PlanningStats

# =============================================================================
# GÉNÉRATEUR DE PLANNING PRINCIPAL - Orchestrateur de la génération
# =============================================================================


class PlanningGenerator:
    """Générateur principal de planning - Orchestrateur"""
    
    def __init__(self, start_hour, end_hour):
        """
        Initialise le générateur de planning
        
        Args:
            start_hour (float): Heure de début de journée
            end_hour (float): Heure de fin de journée
        """
        self.start_hour = start_hour
        self.end_hour = end_hour

        self.slot_generator = SlotGenerator(start_hour, end_hour)
        
        self.professeurs = []
        self.classes = []
        self.salles = []
        
        self.planning = []
        self.algorithm = None
        self.stats = None
    
    def add_professeur(self, professeur):
        """Ajoute un professeur"""
        self.professeurs.append(professeur)
    
    def add_classe(self, classe):
        """Ajoute une classe"""
        self.classes.append(classe)
    
    def add_salle(self, salle):
        """Ajoute une salle"""
        self.salles.append(salle)
    
    def generate_planning(self):
        """
        Génère le planning complet
        
        Returns:
            list: Planning généré
        """

        self.algorithm = SchedulingAlgorithm(self.professeurs, self.classes, self.salles)

        slots = self.slot_generator.get_slots()
        self.planning = self.algorithm.generate_planning(slots)
    
        self.stats = PlanningStats(
            self.planning, 
            self.professeurs, 
            self.classes, 
            self.start_hour, 
            self.end_hour
        )
        
        return self.planning
    
    def get_planning(self):
        """Retourne le planning actuel"""
        return self.planning
    
    def get_heures_par_prof(self):
        """Retourne les heures par professeur"""
        if not self.stats:
            return {}
        return self.stats.get_heures_par_prof()
    
    def get_heures_par_classe(self):
        """Retourne les heures par classe"""
        if not self.stats:
            return {}
        return self.stats.get_heures_par_classe()
    
    def get_resume(self):
        """Retourne le résumé du planning"""
        if not self.stats:
            return {}
        return self.stats.get_resume(self.slot_generator.get_total_slots_count())
    
    def afficher_planning(self):
        """Affiche le planning"""
        if self.stats:
            self.stats.afficher_planning(self.slot_generator.get_total_slots_count())
        else:
            print("Aucun planning généré")
