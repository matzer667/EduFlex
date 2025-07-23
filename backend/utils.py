# =============================================================================
# FONCTIONS UTILITAIRES - Helpers et outils de formatting
# =============================================================================

def format_heure_decimale(heure_decimale):
    """
    Convertit une heure décimale en format HH:MM
    
    Args:
        heure_decimale (float): Heure au format décimal (ex: 8.5 = 8h30)
        
    Returns:
        str: Heure formatée au format HH:MM (ex: "08:30")
        
    Examples:
        >>> format_heure_decimale(8.5)
        "08:30"
        >>> format_heure_decimale(17.75)
        "17:45"
    """
    heures = int(heure_decimale)
    minutes = int((heure_decimale - heures) * 60)
    return f"{heures:02d}:{minutes:02d}"

def validate_time_range(start_hour, end_hour, min_hour=0, max_hour=24):
    """
    Valide que les heures sont dans une plage correcte
    
    Args:
        start_hour (float): Heure de début
        end_hour (float): Heure de fin
        min_hour (int): Heure minimum autorisée
        max_hour (int): Heure maximum autorisée
        
    Returns:
        bool: True si valide, False sinon
        
    Raises:
        ValueError: Si les heures sont invalides
    """
    if not (min_hour <= start_hour < max_hour and min_hour < end_hour <= max_hour and start_hour < end_hour):
        raise ValueError(f"Heures invalides. Reçu: début={start_hour}, fin={end_hour}. "
                        f"Assure-toi que {min_hour} <= début < fin <= {max_hour}.")
    return True

def calculate_time_slots_count(start_hour, end_hour, slot_duration=1.0):
    """
    Calcule le nombre de créneaux possibles dans une plage horaire
    
    Args:
        start_hour (float): Heure de début
        end_hour (float): Heure de fin
        slot_duration (float): Durée d'un créneau en heures
        
    Returns:
        int: Nombre de créneaux possibles
    """
    return int((end_hour - start_hour) / slot_duration)
