const MATIERES_DISPONIBLES = [
    "Mathématiques",
    "Français", 
    "Histoire",
    "Géographie",
    "Sciences",
    "Physique",
    "Chimie",
    "Biologie",
    "Anglais",
    "Espagnol",
    "Allemand",
    "Sport",
    "Arts Plastiques",
    "Musique",
    "Technologie",
    "Informatique"
];

function toggleSection(sectionId) {
    const content = document.getElementById(sectionId);
    const arrow = document.getElementById(`arrow-${sectionId}`);
    
    if (content.classList.contains('collapsed')) {
        content.classList.remove('collapsed');
        arrow.classList.remove('rotated');
    } else {
        content.classList.add('collapsed');
        arrow.classList.add('rotated');
    }
}

function formatHeure(heureDecimale) {
    const heures = Math.floor(heureDecimale);
    const minutes = Math.round((heureDecimale - heures) * 60);
    return `${heures.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

function initializeTimeSelectors() {
    const startHourSelect = document.getElementById('startHourSelect');
    const endHourSelect = document.getElementById('endHourSelect');

    for (let hour = 6; hour <= 23; hour++) {
        const startOption = document.createElement('option');
        startOption.value = hour.toString().padStart(2, '0');
        startOption.textContent = hour.toString().padStart(2, '0');
        if (hour === 8) startOption.selected = true;
        startHourSelect.appendChild(startOption);
        
        const endOption = document.createElement('option');
        endOption.value = hour.toString().padStart(2, '0');
        endOption.textContent = hour.toString().padStart(2, '0');
        if (hour === 17) endOption.selected = true;
        endHourSelect.appendChild(endOption);
    }
    
    // Écouter les changements et mettre à jour les inputs cachés
    function updateHiddenInputs() {
        const startHourValue = parseInt(document.getElementById('startHourSelect').value);
        const startMinuteValue = parseInt(document.getElementById('startMinuteSelect').value);
        const endHourValue = parseInt(document.getElementById('endHourSelect').value);
        const endMinuteValue = parseInt(document.getElementById('endMinuteSelect').value);
        
        // Convertir en format décimal
        const startDecimal = startHourValue + (startMinuteValue / 60);
        const endDecimal = endHourValue + (endMinuteValue / 60);
        
        document.getElementById('startHour').value = startDecimal.toFixed(2);
        document.getElementById('endHour').value = endDecimal.toFixed(2);
    }
    
    // Attacher les événements
    document.getElementById('startHourSelect').addEventListener('change', updateHiddenInputs);
    document.getElementById('startMinuteSelect').addEventListener('change', updateHiddenInputs);
    document.getElementById('endHourSelect').addEventListener('change', updateHiddenInputs);
    document.getElementById('endMinuteSelect').addEventListener('change', updateHiddenInputs);
    
    // Initialiser les valeurs
    updateHiddenInputs();
}

function generatePlanningHTML(result) {
    // Extraire les heures de début et fin des paramètres (format décimal)
    const startHour = parseFloat(document.getElementById("startHour").value) || 8.0;
    const endHour = parseFloat(document.getElementById("endHour").value) || 17.0;
    
    // Créer la grille complète des créneaux avec pas de 1 heure
    const jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];
    const heuresCompletes = [];
    
    // Générer les créneaux d'1 heure à partir des heures décimales (comme le backend)
    let currentHour = startHour;
    
    while (currentHour < endHour) {
        const slotEnd = Math.min(currentHour + 1.0, endHour);
        
        if (slotEnd > currentHour) {
            const startFormatted = formatHeure(currentHour);
            const endFormatted = formatHeure(slotEnd);
            heuresCompletes.push(`${startFormatted}-${endFormatted}`);
        }
        
        currentHour += 1.0;
    }
    
    const planningGrid = {};
    jours.forEach(jour => {
        planningGrid[jour] = {};
        heuresCompletes.forEach(heure => {
            planningGrid[jour][heure] = []; 
        });
    });
    
    result.planning.forEach(cours => {
        if (planningGrid[cours.jour] && planningGrid[cours.jour][cours.heure]) {
            planningGrid[cours.jour][cours.heure].push(cours);
        }
    });
    
    const joursAvecCours = jours.filter(jour => {
        return heuresCompletes.some(heure => planningGrid[jour][heure].length > 0);
    });
    
    let html = `
        <div class="planning-container">
            <div class="planning-header">
                <h2>📅 Planning Généré</h2>
                <div class="planning-stats">
                    <span class="stat">📚 ${result.total_cours} cours</span>
                    <span class="stat">⏰ ${result.total_heures}h totales</span>
                    <span class="stat">👨‍🏫 ${Object.keys(result.heures_par_prof).length} professeurs</span>
                    <span class="stat">🕐 ${formatHeure(startHour)}-${formatHeure(endHour)}</span>
                </div>
            </div>
            
            <div class="planning-table-container">
                <table class="planning-table">
                    <thead>
                        <tr>
                            <th class="time-header">Heures</th>`;
    
    joursAvecCours.forEach(jour => {
        html += `<th class="day-header">${jour}</th>`;
    });
    
    html += `</tr></thead><tbody>`;
    
    heuresCompletes.forEach(heure => {
        html += `<tr><td class="time-cell">${heure}</td>`;
        
        joursAvecCours.forEach(jour => {
            const coursListe = planningGrid[jour][heure];
            if (coursListe.length > 0) {
                html += `<td class="course-cell">`;
                coursListe.forEach((cours, index) => {
                    html += `
                        <div class="course-info ${index > 0 ? 'course-separator' : ''}">
                            <div class="prof-name">👨‍🏫 ${cours.professeur}</div>
                            <div class="class-name">🎓 ${cours.classe}</div>
                            <div class="room-name">🏫 ${cours.salle}</div>
                        </div>`;
                });
                html += `</td>`;
            } else {
                html += `<td class="empty-cell">-</td>`;
            }
        });
        
        html += `</tr>`;
    });
    
    html += `</tbody></table></div>`;
    
    html += `
        <div class="stats-section">
            <div class="stat-block">
                <h3>👨‍🏫 Heures par Professeur</h3>
                <div class="stat-grid">`;
    
    Object.entries(result.heures_par_prof).forEach(([prof, heures]) => {
        html += `<div class="stat-item"><span class="stat-label">${prof}</span><span class="stat-value">${heures}h</span></div>`;
    });
    
    html += `</div></div><div class="stat-block">
                <h3>🎓 Heures par Classe</h3>
                <div class="stat-grid">`;
    
    Object.entries(result.heures_par_classe).forEach(([classe, heures]) => {
        html += `<div class="stat-item"><span class="stat-label">${classe}</span><span class="stat-value">${heures}h</span></div>`;
    });
    
    html += `</div></div></div></div>`;
    
    return html;
}

function generateProfMatieresFields(nbProfs) {
    const container = document.getElementById("profMatieresContainer");
    container.innerHTML = "";
    container.style.display = "grid";
    container.style.gridTemplateColumns = "1fr 1fr";
    container.style.gap = "20px";
    
    for (let i = 1; i <= nbProfs; i++) {
        const profDiv = document.createElement("div");
        profDiv.style.border = "1px solid #ddd";
        profDiv.style.padding = "15px";
        profDiv.style.borderRadius = "8px";
        profDiv.style.backgroundColor = "#f9f9f9";
        
        let html = `<h4 style="margin: 0 0 10px 0; color: #2c3e50;">Professeur ${i}</h4>`;
        html += `<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;">`;
        
        MATIERES_DISPONIBLES.forEach(matiere => {
            html += `
                <label style="display: flex; align-items: center; font-size: 14px; cursor: pointer;">
                    <input type="checkbox" name="prof${i}Matieres" value="${matiere}" style="margin-right: 8px;">
                    ${matiere}
                </label>
            `;
        });
        
        html += `</div>`;
        profDiv.innerHTML = html;
        container.appendChild(profDiv);
    }
}


document.getElementById("nbProfs").addEventListener("input", function() {
    const nbProfs = parseInt(this.value) || 0;
    if (nbProfs > 0) {
        generateProfMatieresFields(nbProfs);
    } else {
        document.getElementById("profMatieresContainer").innerHTML = "";
    }
});


document.addEventListener("DOMContentLoaded", function() {
    // Initialiser les sélecteurs d'heures
    initializeTimeSelectors();
    
    const nbProfsDefault = parseInt(document.getElementById("nbProfs").value) || 0;
    if (nbProfsDefault > 0) {
        generateProfMatieresFields(nbProfsDefault);
    }
    
    // Initialisation des sections - toutes ouvertes par défaut
    const sections = ['horaires', 'classes', 'professeurs', 'salles'];
    sections.forEach(sectionId => {
        const content = document.getElementById(sectionId);
        const arrow = document.getElementById(`arrow-${sectionId}`);
        content.classList.remove('collapsed');
        arrow.classList.remove('rotated');
    });
});

document.getElementById("planningForm").addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const nbProfs = parseInt(document.getElementById("nbProfs").value);
    
    const matieresProfs = [];
    for (let i = 1; i <= nbProfs; i++) {
        const checkboxes = document.querySelectorAll(`input[name="prof${i}Matieres"]:checked`);
        const matieresSelectionnees = Array.from(checkboxes).map(cb => cb.value);
        
        if (matieresSelectionnees.length === 0) {
            matieresSelectionnees.push("Matière générale");
        }
        
        matieresProfs.push(matieresSelectionnees);
    }

    const data = {
        startHour: parseFloat(document.getElementById("startHour").value),
        endHour: parseFloat(document.getElementById("endHour").value),
        nbProfs: nbProfs,
        nbClasses: parseInt(document.getElementById("nbClasses").value),
        heuresParSemaine: parseInt(document.getElementById("heuresParSemaine").value),
        nbSalles: parseInt(document.getElementById("nbSalles").value),
        effectifMin: parseInt(document.getElementById("effectifMin").value),
        effectifMax: parseInt(document.getElementById("effectifMax").value),
        capaciteMin: parseInt(document.getElementById("capaciteMin").value),
        capaciteMax: parseInt(document.getElementById("capaciteMax").value),
        matieresProfs: matieresProfs
    };

    // Debug log pour vérifier les heures
    console.log("Données envoyées:", {
        startHour: data.startHour,
        endHour: data.endHour,
        type_start: typeof data.startHour,
        type_end: typeof data.endHour
    });

    
    const jsonData = JSON.stringify(data);

    
    const res = await fetch("http://127.0.0.1:8000/planning", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonData
    });

    const result = await res.json();
    
    const resultDiv = document.getElementById("result");
    
    if (result.error) {
        resultDiv.innerHTML = `<div class="error">❌ Erreur: ${result.error}</div>`;
        return;
    }
    
    resultDiv.innerHTML = generatePlanningHTML(result);
});
