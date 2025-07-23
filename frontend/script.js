document.getElementById("planningForm").addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const data = {
        startHour: parseInt(document.getElementById("startHour").value),
        endHour: parseInt(document.getElementById("endHour").value),
        nbProfs: parseInt(document.getElementById("nbProfs").value),
        nbClasses: parseInt(document.getElementById("nbClasses").value),
        heuresParSemaine: parseInt(document.getElementById("heuresParSemaine").value),
        nbSalles: parseInt(document.getElementById("nbSalles").value),
        effectifMin: parseInt(document.getElementById("effectifMin").value),
        effectifMax: parseInt(document.getElementById("effectifMax").value),
        capaciteMin: parseInt(document.getElementById("capaciteMin").value),
        capaciteMax: parseInt(document.getElementById("capaciteMax").value),
        matieres: document.getElementById("matieres").value
    };

    
    const jsonData = JSON.stringify(data);

    
    const res = await fetch("http://127.0.0.1:8000/planning", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonData
    });

    const result = await res.json();
    
    const resultDiv = document.getElementById("result");
    
    if (result.error) {
        resultDiv.textContent = `Erreur: ${result.error}`;
        return;
    }
    
    let output = "";
    
    output += "--- RÉSUMÉ ---\n";
    output += `${result.resume.journee}\n`;
    output += `${result.resume.semaine}\n`;
    output += `${result.resume.profs}\n`;
    output += `${result.resume.classes}\n\n`;
    
    output += "--- PLANNING AUTOMATIQUE ---\n";
    result.planning.forEach(cours => {
        output += `${cours.jour} ${cours.heure} : ${cours.professeur} enseigne à ${cours.classe} en ${cours.salle}\n`;
    });
    output += `\nTotal : ${result.total_cours} cours programmés\n\n`;
    
    output += "--- HEURES PAR PROFESSEUR ---\n";
    Object.entries(result.heures_par_prof).forEach(([prof, heures]) => {
        output += `${prof} : ${heures}h de cours cette semaine\n`;
    });
    
    output += "\n--- HEURES PAR CLASSE ---\n";
    Object.entries(result.heures_par_classe).forEach(([classe, heures]) => {
        output += `${classe} : ${heures}h programmées\n`;
    });
    
    output += `\nTotal général : ${result.total_heures}h de cours programmées`;
    
    resultDiv.style.whiteSpace = "pre-line";
    resultDiv.style.fontFamily = "monospace";
    resultDiv.style.backgroundColor = "#f5f5f5";
    resultDiv.style.padding = "15px";
    resultDiv.style.borderRadius = "5px";
    resultDiv.textContent = output;
});
