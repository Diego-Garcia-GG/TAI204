# importaciones
from fastapi import FastAPI, APIRouter # Depends (Condicional para entrar al endpoint) para protección de endpoints
from app.routers import usuarios, varios

# Instancia del servidor
app = FastAPI(
    title = "Mi Primer API",
    description = "García García Diego Antonio",
    version = "1.0"
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)