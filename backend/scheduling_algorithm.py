# =============================================================================
# ALGORITHME DE PLANIFICATION - Logique de génération des cours
# =============================================================================

class SchedulingAlgorithm:
    """Algorithme de planification des cours"""
    
    def __init__(self, professeurs, classes, salles):
        if not professeurs or not classes or not salles:
            raise ValueError("Il faut au moins un professeur, une classe et une salle")
            
        self.professeurs = professeurs
        self.classes = classes
        self.salles = salles
        self.planning = []
    
    def find_suitable_salle(self, classe, salles_occupees):
        # Chercher une salle libre qui peut accueillir la classe
        for salle in self.salles:
            if salle.nom not in salles_occupees and salle.peut_accueillir(classe):
                return salle
        
        # Si aucune salle appropriée n'est trouvée, retourner None
        return None
    
    def find_available_professor(self, profs_occupes):
        for prof in self.professeurs:
            if prof.nom not in profs_occupes:
                return prof
        return None
    
    def generate_courses_to_schedule(self):
        cours_a_programmer = []
        # Chaque classe a un nombre d'heures défini par son attribut nb_heures_semaine
        for classe in self.classes:
            for _ in range(classe.nb_heures_semaine):
                cours_a_programmer.append(classe)
        return cours_a_programmer
    
    def schedule_slot(self, slot, cours_a_programmer):
        profs_occupes = set()
        classes_occupees = set()
        salles_occupees = set()
        cours_restants = []
        
        for classe in cours_a_programmer:

            if classe.nom in classes_occupees:
                cours_restants.append(classe)
                continue
            
            prof_disponible = self.find_available_professor(profs_occupes)
            salle_disponible = self.find_suitable_salle(classe, salles_occupees)

            if prof_disponible and salle_disponible:
                cours = {
                    "jour": slot["day"],
                    "heure": slot["formatted"],
                    "professeur": prof_disponible,
                    "classe": classe,
                    "salle": salle_disponible
                }
                
                self.planning.append(cours)
               
                profs_occupes.add(prof_disponible.nom)
                classes_occupees.add(classe.nom)
                salles_occupees.add(salle_disponible.nom)
            else:
                cours_restants.append(classe)
        
        return cours_restants
    
    def generate_planning(self, slots):
        self.planning = []
        cours_a_programmer = self.generate_courses_to_schedule()
        
        for slot in slots:
            cours_a_programmer = self.schedule_slot(slot, cours_a_programmer)
            
            if not cours_a_programmer:
                break
        
        # Diagnostic des cours non programmés
        if cours_a_programmer:
            print(f"⚠️  {len(cours_a_programmer)} cours n'ont pas pu être programmés")
            self._diagnose_capacity_issues(cours_a_programmer)
        
        return self.planning
    
    def _diagnose_capacity_issues(self, cours_non_programmes):
        """Diagnostique les problèmes de capacité entre classes et salles"""
        classes_problematiques = set()
        
        for classe in cours_non_programmes:
            salles_compatibles = [s for s in self.salles if s.peut_accueillir(classe)]
            if not salles_compatibles:
                classes_problematiques.add(classe)
        
        if classes_problematiques:
            print("❌ Classes avec effectif trop important pour toutes les salles disponibles :")
            for classe in classes_problematiques:
                max_capacite = max(s.capacite for s in self.salles) if self.salles else 0
                print(f"   • {classe.nom} (effectif: {classe.effectif}) - Capacité max des salles: {max_capacite}")
    
    def get_planning(self):
        return self.planning
