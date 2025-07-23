# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def format_heure_decimale(heure_decimale):
    heures = int(heure_decimale)
    minutes = int((heure_decimale - heures) * 60)
    return f"{heures:02d}:{minutes:02d}"

def validate_time_range(start_hour, end_hour, min_hour=0, max_hour=24):
    if not (min_hour <= start_hour < max_hour and min_hour < end_hour <= max_hour and start_hour < end_hour):
        raise ValueError(f"Heures invalides. Reçu: début={start_hour}, fin={end_hour}. "
                        f"Assure-toi que {min_hour} <= début < fin <= {max_hour}.")
    return True

def calculate_time_slots_count(start_hour, end_hour, slot_duration=1.0):
    return int((end_hour - start_hour) / slot_duration)
