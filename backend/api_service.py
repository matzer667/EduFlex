# =============================================================================
# API SERVICE - Interface pour l'API FastAPI
# =============================================================================

import random
from models import Salle, Professeur, Classe
from planning_generator import PlanningGenerator

def generate_planning(start_hour, end_hour, nb_profs, nb_classes, heures_par_semaine, 
                     nb_salles, effectif_min, effectif_max, capacite_min, capacite_max, 
                     matieres_profs):
    """
    Service principal pour générer un planning automatique
    
    Args:
        start_hour (float): Heure de début des cours (ex: 8.5 pour 8h30)
        end_hour (float): Heure de fin des cours (ex: 17.75 pour 17h45)
        nb_profs (int): Nombre de professeurs
        nb_classes (int): Nombre de classes
        heures_par_semaine (int): Heures de cours par semaine par classe
        nb_salles (int): Nombre de salles disponibles
        effectif_min (int): Effectif minimum d'une classe
        effectif_max (int): Effectif maximum d'une classe
        capacite_min (int): Capacité minimum d'une salle
        capacite_max (int): Capacité maximum d'une salle
        matieres_profs (list): Liste de listes des matières par professeur
        
    Returns:
        dict: Contenant le planning et les statistiques
        
    Raises:
        ValueError: En cas d'erreur lors de la génération
    """
    try:
        # Créer le générateur principal
        generator = PlanningGenerator(start_hour, end_hour)
        
        # Ajouter les professeurs
        for i in range(nb_profs):
            matieres = matieres_profs[i] if i < len(matieres_profs) else ["Matière générale"]
            prof = Professeur(f"Prof_{i+1}", matieres)
            generator.add_professeur(prof)
        
        # Ajouter les classes
        for i in range(nb_classes):
            effectif = random.randint(effectif_min, effectif_max)
            classe = Classe(f"Classe_{i+1}", effectif, heures_par_semaine)
            generator.add_classe(classe)
        
        # Ajouter les salles
        for i in range(nb_salles):
            capacite = random.randint(capacite_min, capacite_max)
            salle = Salle(f"Salle_{i+1}", capacite)
            generator.add_salle(salle)
        
        # Générer le planning
        planning = generator.generate_planning()
        
        # Retourner le résultat formaté pour l'API
        return {
            "resume": generator.get_resume(),
            "planning": [
                {
                    "jour": cours["jour"],
                    "heure": cours["heure"],
                    "professeur": cours["professeur"].nom,
                    "classe": cours["classe"].nom,
                    "salle": cours["salle"].nom
                } for cours in planning
            ],
            "heures_par_prof": generator.get_heures_par_prof(),
            "heures_par_classe": generator.get_heures_par_classe(),
            "total_cours": len(planning),
            "total_heures": sum(generator.get_heures_par_prof().values())
        }
    
    except Exception as e:
        raise ValueError(str(e))
