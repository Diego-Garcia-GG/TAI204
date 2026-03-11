from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Literal
from pydantic import BaseModel, Field, EmailStr
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date, time, datetime

app = FastAPI(
    title="Examen 2doP"
)

clientes = [
    {"id":1, "Nombre":"Iván Isay"},
    {"id":2, "Nombre":"Ricardo Méndez"}
]

turnos = []

class crear_cliente(BaseModel):
    id:int = Field(..., gt=0, example=1, description="Identificador único de usuario")
    cliente:str = Field(..., min_length=8, example="Nombre del Cliente", description="Nombre del Cliente")

class crear_turno(BaseModel):
    id:int = Field(..., gt=0, example=1, description="Identificador único de turno")
    id_cliente:int = Field(..., gt=0, example=1, description="Identificador único de cliente")
    estatus:Literal["Pendiente", "Atendido"] = Field(..., example="Estatus del turno", description="estatus del turno")
    tramite:Literal["Depósito", "Retiro", "Consulta"] = Field(..., example="Tipo de trámite", description="Tipo de trámimte")
    fecha:time

class marcar_atendido(BaseModel):
    estatus:Literal["Pendiente", "Atendido"] = Field(..., example="Estatus del turno", description="estatus del turno")

security = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuarioAuth = secrets.compare_digest(credenciales.username,"banco")
    contraAuth = secrets.compare_digest(credenciales.password,"2468")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales No Autorizadas"
        )
    return credenciales.username

@app.post("/v1/turnos", tags=["TURNOS"])
async def crear_turno(turno:crear_turno):
    for tur in turnos:
        if(tur["id"] == turno.id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Ya existe un turno con ese id !")
        
        if(tur["id_cliente"] == turno.id_cliente >= 5):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El mismo cliente no puede tener 5 consultas en el mismo día !")
        
        if(turno.fecha > time(9,0) and turno.fecha < time(15,0)):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No se pueden crear turnos antes de las 09:00 a.m y 3:00 p.m")
    turnos.append(turno.model_dump())
    return{
        "status":"200 OK",
        "mensaje":"El turno ha sido creado exitosamente !"
    }

@app.get("/v1/turnos", tags=["TURNOS"])
async def listar_turnos():
    return{
        "status":"200 OK",
        "total":len(turnos),
        "turno":turnos
    }

@app.get("/v1/turnos/{id}", tags=["TURNOS"])
async def consultar_turno(id:int):
    for tur in turnos:
        if(tur["id"] == id):
            return{
                "status":"200 OK",
                "datos del turno":tur
            }

@app.put("/v1/turnos/{id}", tags=["TURNOS"])
async def marcar_turno_atendido(id:int, marcar:marcar_atendido, usuarioAuth:str=Depends(verificar_peticion)):
    for tur in turnos:
        if(tur["id"] == id):
            if(tur["estatus"] == "Atendido"):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El turno ya se encuentra atendido !")
            if(marcar.estatus == "Pendiente"):
                raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Solo se acepta el cambio de estatus de un turno a 'Atendido' !")
        tur["estatus"] == marcar.estatus
        return{
            "status":"200 OK",
            "mensaje":"El turno ha sido marcado como atendido !",
            "Datos del turno":tur
        }
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No existe ningun turno con ese id !")

@app.delete("/v1/turnos/{id}", tags=["TURNOS"])
async def eliminar_turno(id:int, usuarioAuth:str=Depends(verificar_peticion)):
    for tur in turnos:
        if(tur["id"] == id):
            turnos.remove(tur)
            return{
                "status":"200 OK",
                "mensaje":"El turno ha sido eliminado exitosamente !",
                "datos del turno":tur
            }
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="No existe ningún turno con ese id !")