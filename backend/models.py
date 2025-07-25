class Salle:
    
    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite
    
    def peut_accueillir(self, classe):
        return self.capacite >= classe.effectif
    
    def __str__(self):
        return f"{self.nom} (capacité: {self.capacite})"


class Professeur:
    
    def __init__(self, nom, matieres=None):
        self.nom = nom
        self.matieres = matieres if matieres else ["Matière générale"]
    
    def __str__(self):
        return f"{self.nom} - {', '.join(self.matieres)}"


class Classe:
    
    def __init__(self, nom, effectif, nb_heures_semaine):
        self.nom = nom
        self.effectif = effectif
        self.nb_heures_semaine = nb_heures_semaine
    
    def __str__(self):
        return f"{self.nom} ({self.effectif} élèves, {self.nb_heures_semaine}h/sem)"
