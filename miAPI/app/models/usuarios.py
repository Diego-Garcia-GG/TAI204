from pydantic import BaseModel, Field

class crear_Usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

class actualizar_usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")