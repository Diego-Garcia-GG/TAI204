from fastapi import APIRouter
import asyncio
from typing import Optional # Para parámetros opcionales

routerV = APIRouter(tags=["Inicio"])

# Endpoints
@routerV.get("/")
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # Izquierdo clave o index y Derecho el mensaje

@routerV.get("/")
async def hola():
    await asyncio.sleep(5) # Peticion, consultaBD, archivo
    return{
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }

# Endpoint con parámetro obligatorio
@routerV.get("/{id}")
async def consultauno(id:int):

    return {"mensaje":"Bienvenido a FastAPI",
            "Usuario":id,
            "status":"200"}

# Endpoint con parámetro opcional
@routerV.get("/")
async def consultatodos(id:Optional[int] = None):

    if(id != None):
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje":"Usuario Encontrado!",
                        "usuario":usuarioK}
            
        return {"mensaje":"Usuario no Encontrado!",
                "status":"200"}
    
    return {"mensaje":"No se proporcionó ningún id !",
            "status":"200"}