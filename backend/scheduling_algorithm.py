# =============================================================================
# ALGORITHME DE PLANIFICATION - Logique de génération des cours
# =============================================================================

class SchedulingAlgorithm:
    """Algorithme de planification des cours"""
    
    def __init__(self, professeurs, classes, salles):
        """
        Initialise l'algorithme avec les ressources disponibles
        
        Args:
            professeurs (list): Liste des professeurs
            classes (list): Liste des classes
            salles (list): Liste des salles
        """
        if not professeurs or not classes or not salles:
            raise ValueError("Il faut au moins un professeur, une classe et une salle")
            
        self.professeurs = professeurs
        self.classes = classes
        self.salles = salles
        self.planning = []
    
    def find_suitable_salle(self, classe, salles_occupees):
        """
        Trouve une salle adaptée pour une classe
        
        Args:
            classe: La classe à placer
            salles_occupees (set): Salles déjà occupées
            
        Returns:
            Salle: Salle disponible ou None
        """
        # Priorité aux salles avec capacité adaptée
        for salle in self.salles:
            if salle.nom not in salles_occupees and salle.peut_accueillir(classe):
                return salle
        
        # Sinon, première salle disponible
        for salle in self.salles:
            if salle.nom not in salles_occupees:
                return salle
                
        return None
    
    def find_available_professor(self, profs_occupes):
        """
        Trouve un professeur disponible
        
        Args:
            profs_occupes (set): Professeurs déjà occupés
            
        Returns:
            Professeur: Professeur disponible ou None
        """
        for prof in self.professeurs:
            if prof.nom not in profs_occupes:
                return prof
        return None
    
    def generate_courses_to_schedule(self):
        """
        Génère la liste des cours à programmer
        
        Returns:
            list: Liste des cours à programmer
        """
        cours_a_programmer = []
        for classe in self.classes:
            for _ in range(classe.nb_heures_semaine):
                cours_a_programmer.append(classe)
        return cours_a_programmer
    
    def schedule_slot(self, slot, cours_a_programmer):
        """
        Programme les cours pour un créneau donné
        
        Args:
            slot (dict): Le créneau horaire
            cours_a_programmer (list): Liste des cours restants à programmer
            
        Returns:
            list: Liste des cours non programmés
        """
        profs_occupes = set()
        classes_occupees = set()
        salles_occupees = set()
        cours_restants = []
        
        for classe in cours_a_programmer:
            # Éviter les doublons de classes dans le même créneau
            if classe.nom in classes_occupees:
                cours_restants.append(classe)
                continue
            
            # Trouver les ressources disponibles
            prof_disponible = self.find_available_professor(profs_occupes)
            salle_disponible = self.find_suitable_salle(classe, salles_occupees)
            
            # Si toutes les ressources sont disponibles, programmer le cours
            if prof_disponible and salle_disponible:
                cours = {
                    "jour": slot["day"],
                    "heure": slot["formatted"],
                    "professeur": prof_disponible,
                    "classe": classe,
                    "salle": salle_disponible
                }
                
                self.planning.append(cours)
                
                # Marquer les ressources comme occupées
                profs_occupes.add(prof_disponible.nom)
                classes_occupees.add(classe.nom)
                salles_occupees.add(salle_disponible.nom)
            else:
                cours_restants.append(classe)
        
        return cours_restants
    
    def generate_planning(self, slots):
        """
        Génère le planning complet
        
        Args:
            slots (list): Liste des créneaux disponibles
            
        Returns:
            list: Planning généré
        """
        self.planning = []
        cours_a_programmer = self.generate_courses_to_schedule()
        
        for slot in slots:
            cours_a_programmer = self.schedule_slot(slot, cours_a_programmer)
            
            # Arrêter si tous les cours sont programmés
            if not cours_a_programmer:
                break
        
        return self.planning
    
    def get_planning(self):
        """Retourne le planning actuel"""
        return self.planning
