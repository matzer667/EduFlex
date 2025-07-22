days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


start_hour = int(input("Entrez l'heure de début de journée (0-23): "))
end_hour = int(input("Entrez l'heure de fin de journée (0-23): "))
if not (0 <= start_hour < 24 and 0 < end_hour <= 24 and start_hour < end_hour):
    raise ValueError("Heures invalides. Assure-toi que 0 <= début < fin <= 24.")


nb_profs = int(input("Entrez le nombre de professeurs: "))
profs = [f"Prof_{i+1}" for i in range(nb_profs)]


nb_classes = int(input("Entrez le nombre de classes: "))
classes = []
for i in range(nb_classes):
    classes.append({"name": f"Classe_{i+1}", "size": -1})




slots = []
for day in days:
    for hour in range(start_hour, end_hour):
        slots.append({
            "day": day,
            "hour_start": hour,
            "hour_end": hour + 1
        })


print("\n--- RÉSUMÉ ---")
per_day = end_hour - start_hour
print(f"Journée : {start_hour}h-{end_hour}h ({per_day} créneaux/jour)")
print(f"Semaine : {len(slots)} créneaux au total")
print(f"Profs ({len(profs)}): {profs}")
print(f"Classes ({len(classes)}): {[c['name'] for c in classes]}")


salles = [f"Salle_{i+1}" for i in range(len(classes))]

print("\n--- PLANNING AUTOMATIQUE ---")
planning = []
slot_index = 0


for i in range(len(classes)):
    if slot_index < len(slots):
        slot = slots[slot_index]
        prof = profs[i % len(profs)] 
        classe = classes[i]['name']
        salle = salles[i]
        
        cours = {
            "jour": slot["day"],
            "heure": f"{slot['hour_start']}h-{slot['hour_end']}h",
            "professeur": prof,
            "classe": classe,
            "salle": salle
        }
        
        planning.append(cours)
        print(f"{cours['jour']} {cours['heure']} : {cours['professeur']} enseigne à {cours['classe']} en {cours['salle']}")
        
        slot_index += 1

print(f"\nTotal : {len(planning)} cours programmés")


print("\n--- HEURES PAR PROFESSEUR ---")
heures_prof = {}


for prof in profs:
    heures_prof[prof] = 0


for cours in planning:
    prof = cours["professeur"]
    heures_prof[prof] += 1  


for prof, heures in heures_prof.items():
    print(f"{prof} : {heures}h de cours cette semaine")

print(f"\nTotal général : {sum(heures_prof.values())}h de cours programmées")

