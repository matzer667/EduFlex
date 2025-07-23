# =============================================================================
# STATISTIQUES ET RAPPORTS - Calculs et affichage des métriques
# =============================================================================

from utils import format_heure_decimale

class PlanningStats:
    """Calculateur de statistiques pour le planning"""
    
    def __init__(self, planning, professeurs, classes, start_hour, end_hour):
        """
        Initialise le calculateur de statistiques
        
        Args:
            planning (list): Liste des cours programmés
            professeurs (list): Liste des professeurs
            classes (list): Liste des classes
            start_hour (float): Heure de début
            end_hour (float): Heure de fin
        """
        self.planning = planning
        self.professeurs = professeurs
        self.classes = classes
        self.start_hour = start_hour
        self.end_hour = end_hour
    
    def get_heures_par_prof(self):
        """
        Calcule les heures de cours par professeur
        
        Returns:
            dict: Heures par professeur
        """
        heures_prof = {prof.nom: 0 for prof in self.professeurs}
        
        for cours in self.planning:
            prof_nom = cours["professeur"].nom
            heures_prof[prof_nom] += 1
        
        return heures_prof
    
    def get_heures_par_classe(self):
        """
        Calcule les heures de cours par classe
        
        Returns:
            dict: Heures par classe
        """
        heures_classe = {classe.nom: 0 for classe in self.classes}
        
        for cours in self.planning:
            classe_nom = cours["classe"].nom
            heures_classe[classe_nom] += 1
        
        return heures_classe
    
    def get_resume(self, slots_count):
        """
        Génère un résumé du planning
        
        Args:
            slots_count (int): Nombre total de créneaux
            
        Returns:
            dict: Résumé du planning
        """
        per_day = self.end_hour - self.start_hour
        start_formatted = format_heure_decimale(self.start_hour)
        end_formatted = format_heure_decimale(self.end_hour)
        
        return {
            "journee": f"{start_formatted}-{end_formatted} ({per_day:.1f}h/jour)",
            "semaine": f"{slots_count} créneaux au total",
            "profs": f"({len(self.professeurs)}): {[prof.nom for prof in self.professeurs]}",
            "classes": f"({len(self.classes)}): {[classe.nom for classe in self.classes]}"
        }
    
    def get_total_heures(self):
        """
        Calcule le nombre total d'heures programmées
        
        Returns:
            int: Total des heures
        """
        return sum(self.get_heures_par_prof().values())
    
    def get_taux_occupation_profs(self):
        """
        Calcule le taux d'occupation des professeurs
        
        Returns:
            dict: Taux d'occupation par professeur
        """
        heures_prof = self.get_heures_par_prof()
        total_possible = len(self.planning) // len(self.professeurs) if self.professeurs else 0
        
        return {
            prof: (heures / total_possible * 100) if total_possible > 0 else 0
            for prof, heures in heures_prof.items()
        }
    
    def afficher_planning(self, slots_count):
        """
        Affiche le planning de manière formatée
        
        Args:
            slots_count (int): Nombre total de créneaux
        """
        resume = self.get_resume(slots_count)
        heures_prof = self.get_heures_par_prof()
        heures_classe = self.get_heures_par_classe()
        
        print("\n--- RÉSUMÉ ---")
        print(resume["journee"])
        print(resume["semaine"])
        print(resume["profs"])
        print(resume["classes"])
        
        print(f"\n--- SALLES DISPONIBLES ---")
        # Note: Nous n'avons pas accès aux salles ici, mais on pourrait les passer en paramètre
        
        print("\n--- PLANNING AUTOMATIQUE ---")
        for cours in self.planning:
            prof = cours["professeur"]
            classe = cours["classe"]
            salle = cours["salle"]
            print(f"{cours['jour']} {cours['heure']} : {prof.nom} enseigne à {classe.nom} en {salle.nom}")
            
            if not salle.peut_accueillir(classe):
                print(f"   ⚠️  ATTENTION: {salle.nom} (cap.{salle.capacite}) trop petite pour {classe.nom} ({classe.effectif} élèves)")
        
        print(f"\nTotal : {len(self.planning)} cours programmés")
        
        print("\n--- HEURES PAR PROFESSEUR ---")
        for prof_nom, heures in heures_prof.items():
            print(f"{prof_nom} : {heures}h de cours cette semaine")
        
        print("\n--- HEURES PAR CLASSE ---")
        for classe_nom, heures in heures_classe.items():
            classe = next(c for c in self.classes if c.nom == classe_nom)
            print(f"{classe_nom} : {heures}h programmées / {classe.nb_heures_semaine}h demandées")
        
        print(f"\nTotal général : {sum(heures_prof.values())}h de cours programmées")
