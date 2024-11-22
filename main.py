from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_assistencia import alumnes_assistir, marcar_assistencia
from datetime import date

app = FastAPI()

# Request models
class AsistenciaRequest(BaseModel):
    IdAssignatura: int
    Grup: int 
    Dia: date

class MarcarAsistenciaRequest(BaseModel):
    IdAlumne: int
    IdAssignatura: int
    Dia: date
    Estat: str

@app.post("/assistencia/lista")
def obtener_lista_asistentes(request: AsistenciaRequest):
    try:
        alumnes = alumnes_assistir(request.IdAssignatura, request.Dia, request.Grup)
        if not alumnes:
            raise HTTPException(status_code=404, detail="no existeix grup")
        return {"alumnes": alumnes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error {e}")

@app.post("/assistencia/marcar")
def marcar_asistencia(request: MarcarAsistenciaRequest):
    try:
        if request.Estat not in ['Present', 'Falta', 'Retard']:
            raise HTTPException(status_code=400, detail="error")
        
        marcar_assistencia(request.IdAlumne, request.IdAssignatura, request.Dia, request.Estat)
        return {"message": "Asistencia marcada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {e}")
    

from fastapi import FastAPI, HTTPException
from db_assistencia import obtenir_grups
from pydantic import BaseModel

app = FastAPI()

# Request models
class GrupResponse(BaseModel):
    grup_id: int
    nom_grup: str

@app.get("/grupos", response_model=list[GrupResponse])
def obtener_grupos():
    try:
        grups = obtenir_grups()
        if not grups:
            raise HTTPException(status_code=404, detail="error")
        return [{"grup_id": grup[0], "nom_grup": grup[1]} for grup in grups]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {e}")

