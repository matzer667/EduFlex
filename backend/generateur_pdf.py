from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

# =============================================================================
# GÉNÉRATEUR DE PDF - Planning par classe
# =============================================================================

class PlanningPDFGenerator:
    def __init__(self, planning_data, start_hour, end_hour, jours_actifs=None):
        """
        Initialise le générateur de PDF
        
        Args:
            planning_data (list): Liste des cours du planning
            start_hour (float): Heure de début (ex: 8.0 pour 8h00)
            end_hour (float): Heure de fin (ex: 17.0 pour 17h00)
            jours_actifs (list): Jours de travail sélectionnés
        """
        self.planning_data = planning_data
        self.start_hour = start_hour
        self.end_hour = end_hour
        
        # Utiliser les jours actifs ou les jours par défaut
        if jours_actifs is None:
            self.jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        else:
            self.jours = jours_actifs
            
        self.styles = getSampleStyleSheet()
        
    def format_heure_decimale(self, heure_decimale):
        """Convertit une heure décimale en format HH:MM"""
        heures = int(heure_decimale)
        minutes = int((heure_decimale - heures) * 60)
        return f"{heures:02d}:{minutes:02d}"
    
    def generer_creneaux_horaires(self):
        """Génère la liste des créneaux horaires"""
        creneaux = []
        current_hour = self.start_hour
        
        while current_hour < self.end_hour:
            slot_end = min(current_hour + 1.0, self.end_hour)
            if slot_end > current_hour:
                creneau = f"{self.format_heure_decimale(current_hour)}-{self.format_heure_decimale(slot_end)}"
                creneaux.append(creneau)
            current_hour += 1.0
            
        return creneaux
    
    def extraire_classes(self):
        """Extrait la liste unique des classes du planning"""
        classes = set()
        for cours in self.planning_data:
            classes.add(cours.get('classe', 'Classe inconnue'))
        return sorted(list(classes))
    
    def creer_tableau_classe(self, nom_classe):
        """
        Crée le tableau de planning pour une classe donnée
        
        Args:
            nom_classe (str): Nom de la classe
            
        Returns:
            Table: Tableau de planning pour la classe
        """
        creneaux = self.generer_creneaux_horaires()
        
        # Tous les jours de la semaine (pour affichage complet)
        tous_les_jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        
        # En-tête du tableau : Horaires + Tous les jours
        header = ["Horaires"] + tous_les_jours
        
        # Données du tableau
        table_data = [header]
        
        # Pour chaque créneau horaire
        for creneau in creneaux:
            row = [creneau]  # Première colonne = horaire
            
            # Pour chaque jour de la semaine
            for jour in tous_les_jours:
                # Vérifier si ce jour est dans les jours actifs
                if jour in self.jours:
                    # Jour actif : chercher s'il y a un cours
                    cours_trouve = None
                    for cours in self.planning_data:
                        if (cours.get('classe') == nom_classe and 
                            cours.get('jour') == jour and 
                            cours.get('heure') == creneau):
                            cours_trouve = cours
                            break
                    
                    # Contenu de la cellule
                    if cours_trouve:
                        prof = cours_trouve.get('professeur', 'Prof ?')
                        salle = cours_trouve.get('salle', 'Salle ?')
                        cellule_content = f"{prof}\n{salle}"
                    else:
                        cellule_content = ""
                else:
                    # Jour non actif : cellule vide (sera grisée)
                    cellule_content = ""
                
                row.append(cellule_content)
            
            table_data.append(row)
        
        # Créer le tableau
        table = Table(table_data)
        
        # Style de base du tableau
        style_commands = [
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            
            # Colonne des horaires
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 9),
            
            # Contenu
            ('FONTNAME', (1, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordures
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
            ('LINEAFTER', (0, 0), (0, -1), 2, colors.black),
        ]
        
        # Ajouter le grisage pour les jours non actifs
        for i, jour in enumerate(tous_les_jours, 1):  # i+1 car première colonne = horaires
            if jour not in self.jours:
                # Griser l'en-tête du jour non actif
                style_commands.append(('BACKGROUND', (i, 0), (i, 0), colors.darkgrey))
                style_commands.append(('TEXTCOLOR', (i, 0), (i, 0), colors.white))
                
                # Griser toute la colonne du jour non actif
                style_commands.append(('BACKGROUND', (i, 1), (i, -1), colors.lightgrey))
                style_commands.append(('TEXTCOLOR', (i, 1), (i, -1), colors.grey))
        
        table.setStyle(TableStyle(style_commands))
        
        return table
    
    def generer_pdf(self):
        """
        Génère le PDF complet avec un tableau par classe
        
        Returns:
            BytesIO: Buffer contenant le PDF généré
        """
        buffer = BytesIO()
        
        # Document en format paysage pour avoir plus d'espace
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        story = []
        
        classes = self.extraire_classes()
        
        for i, nom_classe in enumerate(classes):
            # Titre de la classe
            titre = Paragraph(f"<b>Planning - {nom_classe}</b>", self.styles['Title'])
            story.append(titre)
            story.append(Spacer(1, 0.2*inch))
            
            # Tableau de planning pour cette classe
            table = self.creer_tableau_classe(nom_classe)
            story.append(table)
            
            # Saut de page sauf pour la dernière classe
            if i < len(classes) - 1:
                story.append(PageBreak())
        
        # Construction du PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer

# =============================================================================
# FONCTION UTILITAIRE
# =============================================================================

def generer_planning_pdf(planning_data, start_hour=8.0, end_hour=17.0, jours_actifs=None):
    """
    Fonction utilitaire pour générer un PDF de planning
    
    Args:
        planning_data (list): Liste des cours
        start_hour (float): Heure de début
        end_hour (float): Heure de fin
        jours_actifs (list): Jours de travail sélectionnés
        
    Returns:
        BytesIO: Buffer du PDF généré
    """
    generator = PlanningPDFGenerator(planning_data, start_hour, end_hour, jours_actifs)
    return generator.generer_pdf()

# =============================================================================
# TEST DE LA FONCTION
# =============================================================================

if __name__ == "__main__":
    # Données de test
    planning_test = [
        {
            "jour": "Lundi",
            "heure": "08:00-09:00",
            "professeur": "Prof_1",
            "classe": "Classe_1",
            "salle": "Salle_1"
        },
        {
            "jour": "Lundi",
            "heure": "09:00-10:00",
            "professeur": "Prof_2",
            "classe": "Classe_1",
            "salle": "Salle_2"
        },
        {
            "jour": "Mercredi",
            "heure": "08:00-09:00",
            "professeur": "Prof_1",
            "classe": "Classe_2",
            "salle": "Salle_1"
        },
        {
            "jour": "Vendredi",
            "heure": "10:00-11:00",
            "professeur": "Prof_3",
            "classe": "Classe_1",
            "salle": "Salle_3"
        }
    ]
    
    # Test avec seulement Lundi, Mercredi, Vendredi actifs (Mardi, Jeudi, Samedi, Dimanche grisés)
    jours_test = ["Lundi", "Mercredi", "Vendredi"]
    
    # Générer le PDF de test
    pdf_buffer = generer_planning_pdf(planning_test, 8.0, 17.0, jours_test)
    
    # Sauvegarder pour test
    with open("planning_test.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())
    
    print("✅ PDF de test généré : planning_test.pdf")
    print("🎨 Jours actifs:", jours_test)
    print("🔘 Jours grisés: Mardi, Jeudi, Samedi, Dimanche")
