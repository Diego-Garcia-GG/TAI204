from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Literal
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="Biblioteca Digital API",
    description="García García Diego Antonio",
    version="1.0"
)

usuarios = [
    {"id":1, "nombre":"Diego", "correo":"diego@gmail.com"},
    {"id":2, "nombre":"Erik", "correo":"erik@gmail.com"},
    {"id":3, "nombre":"Santiago", "correo":"santy@gmail.com"}
]

libros = [
    {"id":1, "nombre":"El innombrable", "autor":"Samuel Beckett", "año":1953, "paginas":179, "estatus":"Disponible"},
    {"id":2, "nombre":"La subasta del lote 49", "autor":"Thomas Pynchon", "año":1966, "paginas":152, "estatus":"Prestado"},
    {"id":3, "nombre":"El libro del desasociego", "autor":"Fernando Pessoa", "año":1983, "paginas":544, "estatus":"Disponible"}
]

prestamos = [
    {"id":1, "id_usuario":2, "id_libro":3},
    {"id":2, "id_usuario":1, "id_libro":2},
    {"id":3, "id_usuario":3, "id_libro":1}
]

class registrar_libro(BaseModel):
    id: int = Field(..., gt = 0, description = "Identificador único del libro")
    nombre: str = Field(..., min_length = 2, max_length = 100, example = "Nombre del libro")
    autor: str = Field(..., min_length = 2, max_length = 100, example = "Autor del libro")
    año: int = Field(..., gt = 1450, le = 2026, example = "Año del libro")
    paginas:int = Field(..., gt = 1, example = "Número de páginas del libro")
    estatus:Literal["Disponible", "Prestado"] = Field(..., example = "Estatus de préstamo del libro")

class actualizar_estatus_libro(BaseModel):
    estatus:Literal["Disponible", "Prestado"] = Field(..., example = "Estatus de préstamo del libro")

class registrar_usuario(BaseModel):
    id: int = Field(..., gt = 0, example = "Identificador único de usuario")
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "Nombre del usuario")
    correo: EmailStr = Field(..., example = "Correo electrónico del usuario") # Falta validar correo del usuario

class registrar_prestamo(BaseModel):
    id: int = Field(..., gt=0, description="ID del préstamo")
    id_usuario: int = Field(..., gt=0)
    id_libro: int = Field(..., gt=0)

@app.get("/v1/usuarios/", tags = ["USUARIOS"])
async def mostrar_usuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "Usuarios":usuarios
    }

@app.post("/v1/usuarios/", tags = ["USUARIOS"])
async def agregar_usuario(usuario:registrar_usuario):
    for us in usuarios:
        if(us["id"] == usuario.id):
            raise HTTPException(status_code=400, detail="El id ya existe !")
    usuarios.append(usuario.model_dump())
    return{
        "status":"200",
        "mensaje":"el usuario ha sido agregado correctamente !",
        "usuario":usuario
    }

@app.post("/v1/libros/", tags = ["LIBROS"])
async def agregar_libro(libro:registrar_libro):
    for lib in libros:
        if lib["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El id ya existe !")
    libros.append(libro.model_dump())
    return{
        "status":"200",
        "mensaje":"Libro agregado correctamente !",
        "libro":libro
    }

@app.get("/v1/libros/", tags = ["LIBROS"])
async def consultar_todos_libros():
    return{
        "status":"200",
        "total":len(libros),
        "Libros":libros
    }

@app.get("/v1/libros/{nombre}", tags = ["LIBROS"])
async def consultar_libro(nombre:str):
    for lib in libros:
        if lib["nombre"].lower() == nombre.lower():
            return{
                "status":"200",
                "Datos del libro":lib
            }
    raise HTTPException(status_code=400, detail="No existe ningún libro con ese nombre !")

@app.post("/v1/prestamos/", tags=["PRÉSTAMOS"])
async def registrar_prestamo(prestamo:registrar_prestamo):
    usuario_encontrado = None
    for us in usuarios:
        if us["id"] == prestamo.id_usuario:
            usuario_encontrado = us
            break
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    libro_encontrado = None
    for lib in libros:
        if lib["id"] == prestamo.id_libro:
            libro_encontrado = lib
            break
    if not libro_encontrado:
        raise HTTPException(status_code=404, detail="El libro no existe")

    if libro_encontrado["estatus"] == "Prestado":
        raise HTTPException(status_code=409, detail="El libro ya se encuentra prestado")

    prestamos.append(prestamo.model_dump())

    libro_encontrado["estatus"] = "Prestado"
    return {
        "status": "200",
        "mensaje": "Préstamo registrado correctamente",
        "prestamo": prestamo,
        "libro": libro_encontrado,
        "usuario": usuario_encontrado
    }

@app.patch("/v1/libros/{id}", tags = ["PRÉSTAMOS"])
async def marcar_devuelto(id:int, estatus:actualizar_estatus_libro):
    for lib in libros:
        if(lib["id"] == id):
            if(lib["estatus"] == "Disponible"):
                raise HTTPException(status_code=409, detail="El libro se encuentra ya devuelto (Disponible) !")
            if(estatus.estatus == "Prestado"):
                raise HTTPException(status_code=409, detail="Solo se acepta el estado de devolución 'Disponible'")
            lib["estatus"] = estatus.estatus
            return{
                "status":"200",
                "mensaje":"El libro se ha devuelto correctamente (Prestado -> Disponible) !",
                "Datos del libro":lib
            }
    raise HTTPException(status_code=400, detail="No existe nignun libro con ese id !")

@app.delete("/v1/prestamos/{id}", tags = ["PRÉSTAMOS"])
async def eliminar_prestamo(id:int):
    for pres in prestamos:
        if pres["id"] == id:
            prestamos.remove(pres)
            return{
                "status":"200",
                "mensaje":"El prestamo ha sido eliminado exitosamente !",
                "id":pres
            }
    raise HTTPException(status_code=400, detail="El préstamo ya no existe !")

# from typing import Literal = Para especificar solo QUE valores son aceptados, un ejemplo, el estatus de un libro: Literal["Disponible", "Prestado"].

# main.py:
# from pydantic import EmailStr

# requirements.txt:
# email-validator = Para validar correos válidos de usuarios

# .model_dump() = Para guardar un objeto de clase mediante Pydantic por un diccionario.