from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "TAI204-miApiJWT-clave-super-secreta-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

usuarios_db = {
    "diegogarcia": {
        "username": "diegogarcia",
        "hashed_password": pwd_context.hash("123456"),
        "rol": "admin"
    },
    "coral": {
        "username": "coral",
        "hashed_password": pwd_context.hash("abcdef"),
        "rol": "usuario"
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Mi API JWT",
    description="García García Diego Antonio — OAuth2 + JWT",
    version="2.0"
)

usuarios = [
    {"id": 1, "nombre": "Diego",   "edad": 20},
    {"id": 2, "nombre": "Coral",   "edad": 19},
    {"id": 3, "nombre": "Ricardo", "edad": 21}
]

class crear_Usuario(BaseModel):
    id:     int = Field(..., gt=0,         description="Identificador de Usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="John Doe")
    edad:   int = Field(..., ge=1, le=125, description="Edad válida entre 1 y 125")

class actualizar_usuario(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="John Doe")
    edad:   int = Field(..., ge=1, le=125, description="Edad válida entre 1 y 125")

class Token(BaseModel):
    access_token: str
    token_type:   str

class TokenData(BaseModel):
    username: Optional[str] = None

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

def autenticar_usuario(username: str, password: str):
    usuario = usuarios_db.get(username)
    if not usuario:
        return False
    if not verificar_password(password, usuario["hashed_password"]):
        return False
    return usuario

def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    if expires_delta:
        expiracion = datetime.now(timezone.utc) + expires_delta
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> str:
    credencial_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credencial_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credencial_exception

    usuario = usuarios_db.get(token_data.username)
    if usuario is None:
        raise credencial_exception
    return token_data.username

@app.post("/token", response_model=Token, tags=["Autenticación OAuth2"])
async def login_para_obtener_token(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tiempo_expiracion = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = crear_token_acceso(
        data={"sub": usuario["username"]},
        expires_delta=tiempo_expiracion
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/", tags=["Inicio"])
async def bienvenido():
    return {"mensaje": "Bienvenido a FastAPI con JWT"}

@app.get("/holaMundo", tags=["Asyncronía"])
async def hola():
    await asyncio.sleep(5)
    return {"mensaje": "Hola Mundo FastAPI", "status": "200"}

@app.get("/v1/ParametroOb/{id}", tags=["Parámetro Obligatorio"])
async def consultauno(id: int):
    return {"mensaje": "Bienvenido a FastAPI", "Usuario": id, "status": "200"}

@app.get("/v1/ParametroOp/", tags=["Parámetro Opcional"])
async def consultatodos(id: Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return {"mensaje": "Usuario Encontrado!", "usuario": usuarioK}
        return {"mensaje": "Usuario no Encontrado!", "status": "200"}
    return {"mensaje": "No se proporcionó ningún id !", "status": "200"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def consultaT():
    return {"status": "200", "total": len(usuarios), "Usuarios": usuarios}

@app.post("/v1/usuarios", tags=["CRUD HTTP"])
async def agregar_usuario(usuario: crear_Usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe !")
    usuarios.append(usuario)
    return {"mensaje": "usuario agregado correctamente !", "Usuario": usuario, "status": "200"}

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario_endpoint(
    id: int,
    usuario: actualizar_usuario,
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.nombre
            usr["edad"]   = usuario.edad
            return {"mensaje": f"Usuario actualizado por {usuario_actual}", "Usuario": usr, "status": "200"}
    raise HTTPException(status_code=400, detail="El id no existe !")

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"], status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int,
    usuario_actual: str = Depends(obtener_usuario_actual)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"mensaje": f"Usuario eliminado correctamente por {usuario_actual}", "usuario": usr, "status": 200}
    raise HTTPException(status_code=400, detail="El id no existe!")
