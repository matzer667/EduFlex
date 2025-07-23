from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sheduler import generate_planning


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans EduFlex avec FastAPI !"}




class PlanningRequest(BaseModel):
    startHour: int
    endHour: int
    nbProfs: int
    nbClasses: int
    heuresParSemaine: int
    nbSalles: int
    effectifMin: int
    effectifMax: int
    capaciteMin: int
    capaciteMax: int
    matieres: str

@app.post("/planning")
async def planning(data: PlanningRequest):
    try:
        result = generate_planning(
            data.startHour, 
            data.endHour, 
            data.nbProfs, 
            data.nbClasses,
            data.heuresParSemaine,
            data.nbSalles,
            data.effectifMin,
            data.effectifMax,
            data.capaciteMin,
            data.capaciteMax,
            data.matieres
        )
        return result
    except ValueError as e:
        return {"error": str(e)}