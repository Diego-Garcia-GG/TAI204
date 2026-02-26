# importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional # Para parámetros opcionales
from pydantic import BaseModel, Field

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

# Modelos Pydantic de validación
class crear_Usuario(BaseModel):
    id: int = Field(..., gt = 0, description = "Identificador de Usuario")
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

class actualizar_usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

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
@app.get("/v1/ParametroOb/{id}", tags = ["Parámetro Obligatorio"])
async def consultauno(id:int):

    return {"mensaje":"Bienvenido a FastAPI",
            "Usuario":id,
            "status":"200"}

# Endpoint con parámetro opcional
@app.get("/v1/ParametroOp/", tags = ["Parámetro Opcional"])
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

# Método GET
@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios), # len = lenght
        "Usuarios":usuarios # usuarios = tabla de usuarios DB ficticia
    }

# Método POST
@app.post("/v1/usuarios", tags=["CRUD HTTP"])
async def agregar_usuario(usuario:crear_Usuario): # dict = Cuando un parámetro es obligatorio, debe ser de tipo "int", cuando se declara como dict, se traspasa al formato JSON.
    for usr in usuarios:
        if(usr["id"] == usuario.id):
            raise HTTPException(status_code=400, detail="El id ya existe !")
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente !",
        "Usuario":usuario,
        "status":"200"
    }

# Método PUT
@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id:int, usuario:actualizar_usuario):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.nombre
            usr["edad"] = usuario.edad
            return{
                "mensaje":"usuario actualizado correctamente !",
                "Usuario":usr,
                "status":"200"
            }
    raise HTTPException(status_code=400, detail="el id no existe !")

# Método DELETE
@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id:int):
    for usr in usuarios:
        if(usr["id"] == usuario.id):
            usuarios.remove(usr)
            return{
                "mensaje":"usuario eliminado correctamente !",
                "Usuario":usuario,
                "status":"200"
            }
    raise HTTPException(status_code=400, detail="el id no existe !")


# Para encender el servidor de FastAPI, se utiliza el comando "uvicorn [Nombre del archivo main]:[Nombre del objeto instanciado con FastAPI] --reload"