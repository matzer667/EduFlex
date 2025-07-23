from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api_service import generate_planning
from config import API_TITLE, API_DESCRIPTION, API_VERSION, API_HOST, API_PORT
import uvicorn

# =============================================================================
# CONFIGURATION DE L'APPLICATION
# =============================================================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# MODÈLES PYDANTIC
# =============================================================================

class EffectifClasse(BaseModel):
    """Modèle pour l'effectif d'une classe"""
    effectif: int
    heures_semaine: int = 25  # Nombre de cours par semaine

class CapaciteSalle(BaseModel):
    """Modèle pour la capacité d'une salle"""
    capacite: int

class PlanningRequest(BaseModel):
    """Modèle de requête pour générer un planning"""
    startHour: float
    endHour: float
    joursActifs: list[str] = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    nbProfs: int
    nbClasses: int
    nbSalles: int
    matieresProfs: list[list[str]]
    effectifsClasses: list[EffectifClasse]
    capacitesSalles: list[CapaciteSalle]

# =============================================================================
# ROUTES API
# =============================================================================

@app.get("/")
def read_root():
    """Route racine - Information sur l'API"""
    return {
        "message": "Bienvenue dans EduFlex - Générateur de planning scolaire",
        "version": API_VERSION,
        "architecture": "Modulaire et optimisée",
        "endpoints": {
            "planning": "/planning (POST) - Génère un planning automatique",
            "docs": "/docs - Documentation interactive"
        }
    }

@app.post("/planning")
async def create_planning(data: PlanningRequest):
    """
    Génère un planning scolaire automatique basé sur les paramètres fournis.
    
    Args:
        data: Paramètres de configuration du planning
        
    Returns:
        dict: Planning généré avec statistiques
    """
    try:
        result = generate_planning(
            data.startHour, 
            data.endHour, 
            data.joursActifs,
            data.nbProfs, 
            data.nbClasses,
            data.nbSalles,
            data.matieresProfs,
            data.effectifsClasses,
            data.capacitesSalles
        )
        return result
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}

@app.post("/planning/pdf")
async def create_planning_pdf(data: PlanningRequest):
    """
    Génère un planning scolaire et retourne un PDF téléchargeable.
    
    Args:
        data: Paramètres de configuration du planning
        
    Returns:
        StreamingResponse: PDF du planning
    """
    try:
        from fastapi.responses import StreamingResponse
        from generateur_pdf import generer_planning_pdf
        import io
        
        # Générer le planning d'abord
        result = generate_planning(
            data.startHour, 
            data.endHour, 
            data.joursActifs,
            data.nbProfs, 
            data.nbClasses,
            data.nbSalles,
            data.matieresProfs,
            data.effectifsClasses,
            data.capacitesSalles
        )
        
        # Vérifier qu'il n'y a pas d'erreur
        if "error" in result:
            return {"error": result["error"]}
        
        # Générer le PDF
        pdf_buffer = generer_planning_pdf(
            result["planning"], 
            data.startHour, 
            data.endHour,
            data.joursActifs
        )
        
        # Retourner le PDF en tant que fichier téléchargeable
        return StreamingResponse(
            io.BytesIO(pdf_buffer.getvalue()),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=planning.pdf"}
        )
        
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Erreur inattendue: {str(e)}"}

# =============================================================================
# LANCEMENT DU SERVEUR
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host=API_HOST, 
        port=API_PORT, 
        reload=True,
        log_level="info"
    )
