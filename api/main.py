from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_assistencia import consultar_asistencia, registrar_asistencia
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Origen permitido (puedes agregar más en una lista)
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

class AsistenciaAlumnoRequest(BaseModel):
    fecha: str
    id_alumno: int

class AsistenciaProfesorRequest(BaseModel):
    fecha: str
    grupo: str
    asignatura: str
    alumnos: list[int]
    hora_inicio: str
    hora_final: str


@app.post("/asistencia/alumno")
def obtener_asistencia(data: AsistenciaAlumnoRequest):
    asistencia = consultar_asistencia(data.id_alumno, data.fecha)
    if asistencia is None:
        raise HTTPException(status_code=404, detail="No se encontraron asistencias para el alumno en esa fecha.")
    return asistencia

@app.post("/asistencia/profesor")
def pasar_lista(data: AsistenciaProfesorRequest):
    registrar_asistencia(data.fecha, data.grupo, data.asignatura, data.alumnos, data.hora_inicio, data.hora_final)
    return {"message": "Lista pasada correctamente"}
