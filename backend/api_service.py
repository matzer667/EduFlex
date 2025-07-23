import random
from models import Salle, Professeur, Classe
from planning_generator import PlanningGenerator


# =============================================================================
# API SERVICE - Interface pour l'API FastAPI
# =============================================================================


def generate_planning(start_hour, end_hour, nb_profs, nb_classes, 
                     nb_salles, matieres_profs, effectifs_classes, capacites_salles):
    """
    Service principal pour générer un planning automatique
    
    Args:
        start_hour (float): Heure de début des cours (ex: 8.5 pour 8h30)
        end_hour (float): Heure de fin des cours (ex: 17.75 pour 17h45)
        nb_profs (int): Nombre de professeurs
        nb_classes (int): Nombre de classes
        nb_salles (int): Nombre de salles disponibles
        matieres_profs (list): Liste de listes des matières par professeur
        effectifs_classes (list): Liste des effectifs par classe
        capacites_salles (list): Liste des capacités par salle
        
    Returns:
        dict: Contenant le planning et les statistiques
        
    Raises:
        ValueError: En cas d'erreur lors de la génération
    """
    try:
        generator = PlanningGenerator(start_hour, end_hour)
        
        for i in range(nb_profs):
            matieres = matieres_profs[i] if i < len(matieres_profs) else ["Matière générale"]
            prof = Professeur(f"Prof_{i+1}", matieres)
            generator.add_professeur(prof)
        
        # Ajouter les classes avec effectifs individuels
        for i in range(nb_classes):
            if i < len(effectifs_classes):
                effectif = effectifs_classes[i].effectif
                heures_semaine = effectifs_classes[i].heures_semaine
            else:
                # Valeurs par défaut si pas assez d'effectifs spécifiés
                effectif = 25
                heures_semaine = 25
            
            classe = Classe(f"Classe_{i+1}", effectif, heures_semaine)
            generator.add_classe(classe)
        
        for i in range(nb_salles):
            if i < len(capacites_salles):
                # Utiliser la capacité spécifiée pour cette salle
                capacite = capacites_salles[i].capacite
            else:
                # Valeur par défaut si pas assez de capacités spécifiées
                capacite = 30
            
            salle = Salle(f"Salle_{i+1}", capacite)
            generator.add_salle(salle)
        planning = generator.generate_planning()
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
