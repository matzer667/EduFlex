from config import JOURS_SEMAINE, DUREE_CRENEAU
from utils import format_heure_decimale, validate_time_range

# =============================================================================
# GÉNÉRATEUR DE CRÉNEAUX - Logique de génération des slots temporels
# =============================================================================



class SlotGenerator:
    """Générateur de créneaux horaires pour le planning"""
    def __init__(self, start_hour, end_hour):
        validate_time_range(start_hour, end_hour)
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.days = JOURS_SEMAINE
        self.slots = []
        self._generate_slots()
    
    def _generate_slots(self):
        """Génère tous les créneaux horaires pour la semaine"""
        for day in self.days:
            current_hour = self.start_hour
            while current_hour < self.end_hour:
                slot_end = min(current_hour + DUREE_CRENEAU, self.end_hour)
                
                if slot_end > current_hour:
                    self.slots.append({
                        "day": day,
                        "hour_start": current_hour,
                        "hour_end": slot_end,
                        "formatted": f"{format_heure_decimale(current_hour)}-{format_heure_decimale(slot_end)}"
                    })
                current_hour += DUREE_CRENEAU
    
    def get_slots(self):
        """Retourne la liste des créneaux générés"""
        return self.slots
    
    def get_slots_for_day(self, day):
        """Retourne les créneaux pour un jour spécifique"""
        return [slot for slot in self.slots if slot["day"] == day]
    
    def get_total_slots_count(self):
        """Retourne le nombre total de créneaux"""
        return len(self.slots)
    
    def get_daily_slots_count(self):
        """Retourne le nombre de créneaux par jour"""
        return len([slot for slot in self.slots if slot["day"] == self.days[0]])
