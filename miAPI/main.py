# importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional # Para parámetros opcionales

# Instancia del servidor
app = FastAPI(
    title = "Mi Primer API",
    description = "García García Diego Antonio",
    version = "1.0"
)

usuarios = [
    {"id":1, "nombre":"Diego", "edad":20},
    {"id":2, "nombre":"Coral", "edad":19},
    {"id":3, "nombre":"Ricardo", "edad":21}
]

# Endpoints
@app.get("/", tags = ["Inicio"])
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # Izquierdo clave o index y Derecho el mensaje

@app.get("/holaMundo", tags = ["Asyncronía"])
async def hola():
    await asyncio.sleep(5) # Peticion, consultaBD, archivo
    return{
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }

# Endpoint con parámetro obligatorio
@app.get("/v1/usuario/{id}", tags = ["Parámetro Obligatorio"])
async def consultauno(id:int):

    return {"mensaje":"Bienvenido a FastAPI",
            "Usuario":id,
            "status":"200"}

# Endpoint con parámetro opcional
@app.get("/v1/usuarios/", tags = ["Parámetro Opcional"])
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

# Para encender el servidor de FastAPI, se utiliza el comando "uvicorn [Nombre del archivo main]:[Nombre del objeto instanciado con FastAPI] --reload"