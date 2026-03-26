from pydantic import BaseModel, Field
from typing import Optional

class crear_Usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

class actualizar_usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

class actualizar_usuario_patch(BaseModel):
    nombre: Optional[str] = Field(None, min_length = 3, max_length = 50, example = "John Doe")
    edad: Optional[int] = Field(None, ge = 1, le = 125, description = "Edad válida entre 1 y 125")