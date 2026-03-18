from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_Usuario, actualizar_usuario
from app.security.auth import verificar_peticion

router=APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

@router.get("/")
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios), # len = lenght
        "Usuarios":usuarios # usuarios = tabla de usuarios DB ficticia
    }

# Método POST
@router.post("/")
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
@router.put("/{id}")
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
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, usuarioAut:str=Depends(verificar_peticion)):
    for usr in usuarios:
        if(usr["id"] == id):
            usuarios.remove(usr)
            return{
                "mensaje": f"Usuario eliminado correctamente por {usuarioAut}",
                "usuario": usr,
                "status": 200
            }

    raise HTTPException(status_code=400, detail="El id no existe!")

# Para encender el servidor de FastAPI, se utiliza el comando "uvicorn [Nombre del archivo main]:[Nombre del objeto instanciado con FastAPI] --reload"