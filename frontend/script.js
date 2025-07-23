// =============================================================================
// EDUFLEX - SCRIPT MODERNE AVEC GESTION MODULAIRE
// =============================================================================

// Configuration globale
const CONFIG = {
    API_URL: "http://127.0.0.1:8001/planning/pdf",
    MATIERES_DISPONIBLES: [
        "Mathématiques", "Français", "Histoire", "Géographie", "Sciences",
        "Physique", "Chimie", "Biologie", "Anglais", "Espagnol", "Allemand",
        "Sport", "Arts Plastiques", "Musique", "Technologie", "Informatique"
    ]
};

// État de l'application
let appState = {
    etablissementConfigured: false,
    professeurs: [],
    classes: [],
    salles: []
};

// =============================================================================
// INITIALISATION
// =============================================================================

document.addEventListener("DOMContentLoaded", function() {
    initializeTimeSelectors();
    initializeEventListeners();
});

function initializeTimeSelectors() {
    populateTimeSelectors();
    document.getElementById("startHourSelect").addEventListener("change", updateHiddenTimeFields);
    document.getElementById("startMinuteSelect").addEventListener("change", updateHiddenTimeFields);
    document.getElementById("endHourSelect").addEventListener("change", updateHiddenTimeFields);
    document.getElementById("endMinuteSelect").addEventListener("change", updateHiddenTimeFields);
}

function populateTimeSelectors() {
    const startHourSelect = document.getElementById("startHourSelect");
    const endHourSelect = document.getElementById("endHourSelect");
    
    for (let i = 6; i <= 22; i++) {
        const startOption = document.createElement("option");
        startOption.value = i;
        startOption.textContent = i.toString().padStart(2, '0');
        if (i === 8) startOption.selected = true;
        startHourSelect.appendChild(startOption);
        
        const endOption = document.createElement("option");
        endOption.value = i;
        endOption.textContent = i.toString().padStart(2, '0');
        if (i === 17) endOption.selected = true;
        endHourSelect.appendChild(endOption);
    }
}

function updateHiddenTimeFields() {
    const startHour = parseInt(document.getElementById("startHourSelect").value);
    const startMinute = parseInt(document.getElementById("startMinuteSelect").value);
    const endHour = parseInt(document.getElementById("endHourSelect").value);
    const endMinute = parseInt(document.getElementById("endMinuteSelect").value);
    
    const startDecimal = startHour + (startMinute / 60);
    const endDecimal = endHour + (endMinute / 60);
    
    document.getElementById("startHour").value = startDecimal.toFixed(2);
    document.getElementById("endHour").value = endDecimal.toFixed(2);
}

function initializeEventListeners() {
    document.getElementById("planningForm").addEventListener("submit", handleFormSubmit);
}

// =============================================================================
// GESTION DE L'ÉTABLISSEMENT
// =============================================================================

function toggleEtablissementConfig() {
    const config = document.getElementById("etablissement-config");
    const button = document.querySelector("#etablissement-card .add-button");
    
    if (config.style.display === "none") {
        config.style.display = "block";
        button.innerHTML = '<span class="plus-icon">-</span><span class="add-text">Masquer la configuration</span>';
        appState.etablissementConfigured = true;
        
        config.style.opacity = "0";
        config.style.transform = "translateY(-20px)";
        setTimeout(() => {
            config.style.transition = "all 0.3s ease";
            config.style.opacity = "1";
            config.style.transform = "translateY(0)";
        }, 10);
    } else {
        config.style.display = "none";
        button.innerHTML = '<span class="plus-icon">+</span><span class="add-text">Configurer l\'établissement</span>';
    }
}

// =============================================================================
// GESTION DES PROFESSEURS
// =============================================================================

function ajouterProfesseur() {
    const container = document.getElementById("professeurs-container");
    
    // Trouver le prochain numéro disponible (le plus petit non utilisé)
    const existingCards = container.querySelectorAll('[id^="prof-card-"]');
    const usedNumbers = Array.from(existingCards).map(card => 
        parseInt(card.id.split('-')[2])
    ).sort((a, b) => a - b);
    
    let profId = 1;
    for (let i = 0; i < usedNumbers.length; i++) {
        if (usedNumbers[i] !== profId) {
            break;
        }
        profId++;
    }
    
    const profCard = createProfesseurCard(profId);
    container.appendChild(profCard);
    
    // Mettre à jour le compteur caché
    document.getElementById("nbProfs").value = container.children.length;
    
    // Animation d'apparition
    profCard.style.opacity = "0";
    profCard.style.transform = "translateY(-20px)";
    setTimeout(() => {
        profCard.style.transition = "all 0.3s ease";
        profCard.style.opacity = "1";
        profCard.style.transform = "translateY(0)";
    }, 10);
}

function supprimerProfesseur(profId) {
    const profCard = document.getElementById(`prof-card-${profId}`);
    if (profCard) {
        profCard.style.transition = "all 0.3s ease";
        profCard.style.opacity = "0";
        profCard.style.transform = "translateY(-20px)";
        setTimeout(() => {
            profCard.remove();
            // Mettre à jour le compteur basé sur le nombre réel d'éléments
            const container = document.getElementById("professeurs-container");
            document.getElementById("nbProfs").value = container.children.length;
        }, 300);
    }
}

function createProfesseurCard(profNumber) {
    const card = document.createElement("div");
    card.className = "item-card hoverable";
    card.id = `prof-card-${profNumber}`;
    card.innerHTML = `
        <div class="item-header">
            <div class="item-title">👨‍🏫 Professeur ${profNumber}</div>
            <div class="item-controls">
                <div class="item-number">${profNumber}</div>
                <button type="button" class="delete-button" onclick="supprimerProfesseur(${profNumber})">×</button>
            </div>
        </div>
        
        <div class="form-group">
            <label class="form-label">Matières enseignées</label>
            <div class="checkbox-group">
                ${CONFIG.MATIERES_DISPONIBLES.map(matiere => `
                    <label class="checkbox-item">
                        <input type="checkbox" name="prof${profNumber}Matieres" value="${matiere}">
                        <div class="checkbox-custom"></div>
                        <span class="checkbox-label">${matiere}</span>
                    </label>
                `).join('')}
            </div>
        </div>
    `;
    
    return card;
}

// =============================================================================
// GESTION DES CLASSES
// =============================================================================

function ajouterClasse() {
    const container = document.getElementById("classes-container");
    
    // Trouver le prochain numéro disponible (le plus petit non utilisé)
    const existingCards = container.querySelectorAll('[id^="classe-card-"]');
    const usedNumbers = Array.from(existingCards).map(card => 
        parseInt(card.id.split('-')[2])
    ).sort((a, b) => a - b);
    
    let classeId = 1;
    for (let i = 0; i < usedNumbers.length; i++) {
        if (usedNumbers[i] !== classeId) {
            break;
        }
        classeId++;
    }
    
    const classeCard = createClasseCard(classeId);
    container.appendChild(classeCard);
    
    document.getElementById("nbClasses").value = container.children.length;
    
    classeCard.style.opacity = "0";
    classeCard.style.transform = "translateY(-20px)";
    setTimeout(() => {
        classeCard.style.transition = "all 0.3s ease";
        classeCard.style.opacity = "1";
        classeCard.style.transform = "translateY(0)";
    }, 10);
}

function supprimerClasse(classeId) {
    const classeCard = document.getElementById(`classe-card-${classeId}`);
    if (classeCard) {
        classeCard.style.transition = "all 0.3s ease";
        classeCard.style.opacity = "0";
        classeCard.style.transform = "translateY(-20px)";
        setTimeout(() => {
            classeCard.remove();
            const container = document.getElementById("classes-container");
            document.getElementById("nbClasses").value = container.children.length;
        }, 300);
    }
}

function createClasseCard(classeNumber) {
    const card = document.createElement("div");
    card.className = "item-card hoverable";
    card.id = `classe-card-${classeNumber}`;
    card.innerHTML = `
        <div class="item-header">
            <div class="item-title">🎓 Classe ${classeNumber}</div>
            <div class="item-controls">
                <div class="item-number">${classeNumber}</div>
                <button type="button" class="delete-button" onclick="supprimerClasse(${classeNumber})">×</button>
            </div>
        </div>
        
        <div class="form-group">
            <label class="form-label">Effectif de la classe</label>
            <input type="number" name="classe${classeNumber}Effectif" class="form-input" 
                   min="1" max="50" value="25" placeholder="Nombre d'élèves">
        </div>
        
        <div class="form-group">
            <label class="form-label">Heures par semaine</label>
            <input type="number" name="classe${classeNumber}Heures" class="form-input" 
                   min="1" max="35" value="25" placeholder="Nombre de cours par semaine">
        </div>
    `;
    
    return card;
}

// =============================================================================
// GESTION DES SALLES
// =============================================================================

function ajouterSalle() {
    const container = document.getElementById("salles-container");
    
    // Trouver le prochain numéro disponible (le plus petit non utilisé)
    const existingCards = container.querySelectorAll('[id^="salle-card-"]');
    const usedNumbers = Array.from(existingCards).map(card => 
        parseInt(card.id.split('-')[2])
    ).sort((a, b) => a - b);
    
    let salleId = 1;
    for (let i = 0; i < usedNumbers.length; i++) {
        if (usedNumbers[i] !== salleId) {
            break;
        }
        salleId++;
    }
    
    const salleCard = createSalleCard(salleId);
    container.appendChild(salleCard);
    
    document.getElementById("nbSalles").value = container.children.length;
    
    salleCard.style.opacity = "0";
    salleCard.style.transform = "translateY(-20px)";
    setTimeout(() => {
        salleCard.style.transition = "all 0.3s ease";
        salleCard.style.opacity = "1";
        salleCard.style.transform = "translateY(0)";
    }, 10);
}

function supprimerSalle(salleId) {
    const salleCard = document.getElementById(`salle-card-${salleId}`);
    if (salleCard) {
        salleCard.style.transition = "all 0.3s ease";
        salleCard.style.opacity = "0";
        salleCard.style.transform = "translateY(-20px)";
        setTimeout(() => {
            salleCard.remove();
            const container = document.getElementById("salles-container");
            document.getElementById("nbSalles").value = container.children.length;
        }, 300);
    }
}

function createSalleCard(salleNumber) {
    const card = document.createElement("div");
    card.className = "item-card hoverable";
    card.id = `salle-card-${salleNumber}`;
    card.innerHTML = `
        <div class="item-header">
            <div class="item-title">🏢 Salle ${salleNumber}</div>
            <div class="item-controls">
                <div class="item-number">${salleNumber}</div>
                <button type="button" class="delete-button" onclick="supprimerSalle(${salleNumber})">×</button>
            </div>
        </div>
        
        <div class="form-group">
            <label class="form-label">Capacité d'accueil</label>
            <input type="number" name="salle${salleNumber}Capacite" class="form-input" 
                   min="1" max="100" value="30" placeholder="Nombre de places">
        </div>
    `;
    
    return card;
}

// =============================================================================
// COLLECTE ET ENVOI DES DONNÉES
// =============================================================================

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const button = document.querySelector(".generate-button");
    const buttonText = document.getElementById("button-text");
    const buttonLoading = document.getElementById("button-loading");
    
    button.disabled = true;
    buttonText.style.display = "none";
    buttonLoading.style.display = "inline-flex";
    
    try {
        const formData = collectFormData();
        await downloadPlanningPDF(formData);
        showSuccessMessage();
    } catch (error) {
        displayError(error.message);
    } finally {
        button.disabled = false;
        buttonText.style.display = "inline";
        buttonLoading.style.display = "none";
    }
}

function collectFormData() {
    const nbProfs = parseInt(document.getElementById("nbProfs").value);
    const nbClasses = parseInt(document.getElementById("nbClasses").value);
    const nbSalles = parseInt(document.getElementById("nbSalles").value);
    
    if (nbProfs === 0 || nbClasses === 0 || nbSalles === 0) {
        throw new Error("Veuillez ajouter au moins un professeur, une classe et une salle.");
    }
    
    // Collecter les jours de travail sélectionnés
    const joursCheckboxes = document.querySelectorAll('input[name="joursActifs"]:checked');
    const joursActifs = Array.from(joursCheckboxes).map(cb => cb.value);
    
    if (joursActifs.length === 0) {
        throw new Error("Veuillez sélectionner au moins un jour de travail.");
    }
    
    // Collecter les matières des professeurs
    const matieresProfs = [];
    const profCards = document.querySelectorAll('[id^="prof-card-"]');
    profCards.forEach((card, index) => {
        const profNumber = card.id.split('-')[2];
        const checkboxes = card.querySelectorAll(`input[name="prof${profNumber}Matieres"]:checked`);
        const matieres = Array.from(checkboxes).map(cb => cb.value);
        matieresProfs.push(matieres.length > 0 ? matieres : ["Matière générale"]);
    });
    
    // Collecter les effectifs des classes
    const effectifsClasses = [];
    const classeCards = document.querySelectorAll('[id^="classe-card-"]');
    classeCards.forEach((card, index) => {
        const classeNumber = card.id.split('-')[2];
        const effectif = parseInt(card.querySelector(`input[name="classe${classeNumber}Effectif"]`).value) || 25;
        const heures = parseInt(card.querySelector(`input[name="classe${classeNumber}Heures"]`).value) || 25;
        effectifsClasses.push({ 
            effectif: effectif,
            heures_semaine: heures 
        });
    });
    
    // Collecter les capacités des salles
    const capacitesSalles = [];
    const salleCards = document.querySelectorAll('[id^="salle-card-"]');
    salleCards.forEach((card, index) => {
        const salleNumber = card.id.split('-')[2];
        const capacite = parseInt(card.querySelector(`input[name="salle${salleNumber}Capacite"]`).value) || 30;
        capacitesSalles.push({ capacite: capacite });
    });
    
    return {
        startHour: parseFloat(document.getElementById("startHour").value),
        endHour: parseFloat(document.getElementById("endHour").value),
        joursActifs: joursActifs,
        nbProfs: nbProfs,
        nbClasses: nbClasses,
        nbSalles: nbSalles,
        matieresProfs: matieresProfs,
        effectifsClasses: effectifsClasses,
        capacitesSalles: capacitesSalles
    };
}

async function downloadPlanningPDF(data) {
    console.log("Données envoyées:", data);
    
    const response = await fetch(CONFIG.API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        throw new Error(`Erreur HTTP ${response.status}`);
    }
    
    // Vérifier si c'est une erreur JSON ou un PDF
    const contentType = response.headers.get("content-type");
    
    if (contentType && contentType.includes("application/json")) {
        // C'est une erreur JSON
        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }
    } else {
        // C'est un PDF, le télécharger
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'planning.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}

function showSuccessMessage() {
    const container = document.getElementById("results-container");
    const content = document.getElementById("result-content");
    
    content.innerHTML = `
        <div class="success-message">
            ✅ <strong>Planning généré avec succès !</strong><br>
            📥 Le fichier PDF a été téléchargé automatiquement.
        </div>
    `;
    
    container.classList.add("show");
    container.scrollIntoView({ behavior: "smooth" });
}

// =============================================================================
// AFFICHAGE DES MESSAGES
// =============================================================================

function showSuccessMessage() {
    const container = document.getElementById("results-container");
    const content = document.getElementById("result-content");
    
    content.innerHTML = `
        <div class="success-message">
            ✅ <strong>Planning généré avec succès !</strong><br>
            📥 Le fichier PDF a été téléchargé automatiquement.
        </div>
    `;
    
    container.classList.add("show");
    container.scrollIntoView({ behavior: "smooth" });
}

function displayError(message) {
    const container = document.getElementById("results-container");
    const content = document.getElementById("result-content");
    
    content.innerHTML = `
        <div class="error-message">
            ❌ <strong>Erreur lors de la génération :</strong><br>
            ${message}
        </div>
    `;
    
    container.classList.add("show");
    container.scrollIntoView({ behavior: "smooth" });
}

// Debug
window.debugAppState = () => {
    console.log("État de l'application:", appState);
};
