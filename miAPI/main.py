# importaciones
from fastapi import FastAPI
import asyncio

# Instancia del servidor
app = FastAPI()

# Endpoints
@app.get("/")
async def bienvenido():
    return {"mensaje":"Bienvenido a FastAPI"} # Izquierdo clave o index y Derecho el mensaje

@app.get("/holaMundo")
async def hola():
    await asyncio.sleep(5) # Peticion, consultaBD, archivo
    return{
        "mensaje":"Hola Mundo FastAPI",
        "status":"200"
        }

# Para encender el servidor de FastAPI, se utiliza el comando "uvicorn [Nombre del archivo main]:[Nombre del objeto instanciado con FastAPI] --reload"