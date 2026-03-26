from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuarios import crear_Usuario, actualizar_usuario, actualizar_usuario_patch
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router=APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

@router.get("/")
async def consultaT(db:Session= Depends(get_db)):
    queryUsuario= db.query(usuarioDB).all()
    return{
        "status":"200",
        "total":len(queryUsuario), # len = lenght
        "Usuarios":queryUsuario # usuarios = tabla de usuarios DB ficticia
    }

# Método GET (por id)
@router.get("/{id}")
async def consulta_por_id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="el id no existe !")
    return {
        "status":"200",
        "Usuario": usuario
    }

# Método POST
@router.post("/")
async def agregar_usuario(usuarioP:crear_Usuario, db:Session= Depends(get_db)): # dict = Cuando un parámetro es obligatorio, debe ser de tipo "int", cuando se declara como dict, se traspasa al formato JSON.
    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad=usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return{
        "mensaje":"usuario agregado correctamente !",
        "Usuario":usuarioP,
        "status":"200"
    }

# Método PUT
@router.put("/{id}")
async def actualizar_usuario_endpoint(id: int, usuario: actualizar_usuario, db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=400, detail="el id no existe !")
    
    usuario_db.nombre = usuario.nombre
    usuario_db.edad = usuario.edad
    
    db.commit()
    db.refresh(usuario_db)
    return {
        "mensaje": "usuario actualizado correctamente !",
        "Usuario": usuario_db,
        "status": "200"
    }

# Método PATCH
@router.patch("/{id}")
async def actualizar_usuario_parcial(id: int, usuario: actualizar_usuario_patch, db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=400, detail="el id no existe !")
    
    if usuario.nombre is not None:
        usuario_db.nombre = usuario.nombre
    if usuario.edad is not None:
        usuario_db.edad = usuario.edad
        
    db.commit()
    db.refresh(usuario_db)
    return {
        "mensaje": "usuario actualizado parcialmente !",
        "Usuario": usuario_db,
        "status": "200"
    }

# Método DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAut: str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    usuario_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    if not usuario_db:
        raise HTTPException(status_code=400, detail="El id no existe!")
    
    db.delete(usuario_db)
    db.commit()
    return {
        "mensaje": f"Usuario eliminado correctamente por {usuarioAut}",
        "usuario": usuario_db,
        "status": 200
    }

# Para encender el servidor de FastAPI, se utiliza el comando "uvicorn [Nombre del archivo main]:[Nombre del objeto instanciado con FastAPI] --reload"