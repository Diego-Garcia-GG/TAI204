from fastapi import status, HTTPException, Depends # Depends (Condicional para entrar al endpoint) para protección de endpoints
from fastapi.security import HTTPBasic, HTTPBasicCredentials # HTTPBasic, HTTPBasicCredentialss (Credenciales) Para protección de endpoints
import secrets # Secrets (Manipulación de contraseñas) para protección de endpoints

security = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    usuarioAut = secrets.compare_digest(credenciales.username,"diegogarcia")
    contraAut = secrets.compare_digest(credenciales.password, "123456")

    if not (usuarioAut and contraAut):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales no autorizadas"
        )
    return credenciales.username