document.getElementById("planningForm").addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const data = {
        startHour: parseInt(document.getElementById("startHour").value),
        endHour: parseInt(document.getElementById("endHour").value),
        nbProfs: parseInt(document.getElementById("nbProfs").value),
        nbClasses: parseInt(document.getElementById("nbClasses").value)
    };

    
    const jsonData = JSON.stringify(data);

    
    const res = await fetch("http://127.0.0.1:8000/planning", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: jsonData
    });

    const result = await res.json();
    document.getElementById("result").textContent = JSON.stringify(result, null, 2);
});
