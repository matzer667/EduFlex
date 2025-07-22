from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


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

@app.post("/planning")
async def planning(data: PlanningRequest):
    print(data.startHour)
    print(data.endHour)
    print(data.nbProfs)
    print(data.nbClasses)
    return {"message": "Planning reçu !", "start": data.startHour, "end": data.endHour, "profs": data.nbProfs, "classes": data.nbClasses}