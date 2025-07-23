import random
from models import Salle, Professeur, Classe


# =============================================================================
# SECTION 1: LOGIQUE DE PLANIFICATION
# =============================================================================


class PlanningGenerator:
    def __init__(self, start_hour, end_hour):
        if not (0 <= start_hour < 24 and 0 < end_hour <= 24 and start_hour < end_hour):
            raise ValueError("Heures invalides. Assure-toi que 0 <= début < fin <= 24.")
        
        self.days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.professeurs = []
        self.classes = []
        self.salles = []
        self.slots = []
        self.planning = []
        
        self._generate_slots()
    
    def _generate_slots(self):
        for day in self.days:
            for hour in range(self.start_hour, self.end_hour):
                self.slots.append({
                    "day": day,
                    "hour_start": hour,
                    "hour_end": hour + 1
                })
    
    def add_professeur(self, professeur):
        self.professeurs.append(professeur)
    
    def add_classe(self, classe):
        self.classes.append(classe)
    
    def add_salle(self, salle):
        self.salles.append(salle)
    
    def _find_suitable_salle(self, classe):
        for salle in self.salles:
            if salle.peut_accueillir(classe):
                return salle
        return self.salles[0] if self.salles else None
    
    def generate_planning(self):
        if not self.professeurs or not self.classes or not self.salles:
            raise ValueError("Il faut au moins un professeur, une classe et une salle")
        
        self.planning = []
        
        cours_a_programmer = []
        for classe in self.classes:
            for h in range(classe.nb_heures_semaine):
                cours_a_programmer.append(classe)
        
        for slot in self.slots:
            profs_occupes = set()
            classes_occupees = set()
            salles_occupees = set()
            
            cours_restants = []
            
            for classe in cours_a_programmer:
                if classe.nom in classes_occupees:
                    cours_restants.append(classe)
                    continue
                
                prof_disponible = None
                for prof in self.professeurs:
                    if prof.nom not in profs_occupes:
                        prof_disponible = prof
                        break
                
                salle_disponible = None
                for salle in self.salles:
                    if salle.nom not in salles_occupees and salle.peut_accueillir(classe):
                        salle_disponible = salle
                        break
                
                if not salle_disponible:
                    for salle in self.salles:
                        if salle.nom not in salles_occupees:
                            salle_disponible = salle
                            break
                
                if prof_disponible and salle_disponible:
                    cours = {
                        "jour": slot["day"],
                        "heure": f"{slot['hour_start']}h-{slot['hour_end']}h",
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
            
            cours_a_programmer = cours_restants
            
            if not cours_a_programmer:
                break
        
        return self.planning
    
    def get_heures_par_prof(self):
        heures_prof = {prof.nom: 0 for prof in self.professeurs}
        
        for cours in self.planning:
            prof_nom = cours["professeur"].nom
            heures_prof[prof_nom] += 1
        
        return heures_prof
    
    def get_heures_par_classe(self):
        heures_classe = {classe.nom: 0 for classe in self.classes}
        
        for cours in self.planning:
            classe_nom = cours["classe"].nom
            heures_classe[classe_nom] += 1
        
        return heures_classe
    
    def get_resume(self):
        per_day = self.end_hour - self.start_hour
        return {
            "journee": f"{self.start_hour}h-{self.end_hour}h ({per_day} créneaux/jour)",
            "semaine": f"{len(self.slots)} créneaux au total",
            "profs": f"({len(self.professeurs)}): {[prof.nom for prof in self.professeurs]}",
            "classes": f"({len(self.classes)}): {[classe.nom for classe in self.classes]}"
        }
    
    def afficher_planning(self):
        resume = self.get_resume()
        heures_prof = self.get_heures_par_prof()
        heures_classe = self.get_heures_par_classe()
        
        print("\n--- RÉSUMÉ ---")
        print(resume["journee"])
        print(resume["semaine"])
        print(resume["profs"])
        print(resume["classes"])
        
        print(f"\n--- SALLES DISPONIBLES ---")
        for salle in self.salles:
            print(f"- {salle}")
        
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


# =============================================================================
# SECTION 2: FONCTION API 
# =============================================================================

def generate_planning(start_hour, end_hour, nb_profs, nb_classes, heures_par_semaine, nb_salles, effectif_min, effectif_max, capacite_min, capacite_max, matieres_str):
    try:
        generator = PlanningGenerator(start_hour, end_hour)
        
        matieres_list = [m.strip() for m in matieres_str.split(',') if m.strip()]
        if not matieres_list:
            matieres_list = ["Matière générale"]
        
        for i in range(nb_profs):
            if len(matieres_list) > 1:
                nb_matieres = min(random.randint(1, 3), len(matieres_list))
                matieres_prof = random.sample(matieres_list, nb_matieres)
            else:
                matieres_prof = matieres_list
            prof = Professeur(f"Prof_{i+1}", matieres_prof)
            generator.add_professeur(prof)
        
        for i in range(nb_classes):
            effectif = random.randint(effectif_min, effectif_max)
            classe = Classe(f"Classe_{i+1}", effectif, heures_par_semaine)
            generator.add_classe(classe)
        
        for i in range(nb_salles):
            capacite = random.randint(capacite_min, capacite_max)
            salle = Salle(f"Salle_{i+1}", capacite)
            generator.add_salle(salle)
        
        planning = generator.generate_planning()
        resume = generator.get_resume()
        heures_prof = generator.get_heures_par_prof()
        heures_classe = generator.get_heures_par_classe()
        
        return {
            "resume": resume,
            "planning": [
                {
                    "jour": cours["jour"],
                    "heure": cours["heure"],
                    "professeur": cours["professeur"].nom,
                    "classe": cours["classe"].nom,
                    "salle": cours["salle"].nom
                } for cours in planning
            ],
            "heures_par_prof": heures_prof,
            "heures_par_classe": heures_classe,
            "total_cours": len(planning),
            "total_heures": sum(heures_prof.values())
        }
    
    except Exception as e:
        raise ValueError(str(e))


# =============================================================================
# SECTION 3: SCRIPT PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    start_hour = int(input("Entrez l'heure de début de journée (0-23): "))
    end_hour = int(input("Entrez l'heure de fin de journée (0-23): "))
    nb_profs = int(input("Entrez le nombre de professeurs: "))
    nb_classes = int(input("Entrez le nombre de classes: "))
    
    generator = PlanningGenerator(start_hour, end_hour)
    
    matieres_possibles = ["Mathématiques", "Français", "Histoire", "Sciences", "Anglais", "Sport"]
    
    for i in range(nb_profs):
        matieres = random.sample(matieres_possibles, random.randint(1, 3))
        prof = Professeur(f"Prof_{i+1}", matieres)
        generator.add_professeur(prof)
    
    for i in range(nb_classes):
        effectif = int(input(f"Effectif pour Classe_{i+1} (ENTER = aléatoire): ") or random.randint(20, 35))
        heures_semaine = int(input(f"Heures par semaine pour Classe_{i+1} (ENTER = 25): ") or 25)
        classe = Classe(f"Classe_{i+1}", effectif, heures_semaine)
        generator.add_classe(classe)
    
    for i in range(nb_classes):
        capacite = int(input(f"Capacité pour Salle_{i+1} (ENTER = aléatoire): ") or random.randint(25, 40))
        salle = Salle(f"Salle_{i+1}", capacite)
        generator.add_salle(salle)
    
    generator.generate_planning()
    generator.afficher_planning()