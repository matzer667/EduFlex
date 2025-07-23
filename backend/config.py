# =============================================================================
# CONFIGURATION GLOBALE - Variables et constantes de l'application
# =============================================================================

# Jours de la semaine par défaut
JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Matières disponibles par défaut
MATIERES_DISPONIBLES = [
    "Mathématiques", "Français", "Histoire", "Géographie", "Sciences",
    "Physique", "Chimie", "Biologie", "Anglais", "Espagnol", "Allemand",
    "Sport", "Arts Plastiques", "Musique", "Technologie", "Informatique"
]

# Limites de validation
HEURE_MIN = 0
HEURE_MAX = 24
DUREE_CRENEAU = 1.0  # Durée d'un créneau en heures

# Configuration API
API_TITLE = "EduFlex API"
API_DESCRIPTION = "API de génération automatique de planning scolaire"
API_VERSION = "1.0.0"
API_HOST = "127.0.0.1"
API_PORT = 8000
