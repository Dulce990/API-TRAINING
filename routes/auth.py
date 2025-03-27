from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config import db
from models.usuarios import Usuario  # Importamos 'Usuario'
from werkzeug.security import check_password_hash, generate_password_hash
from config.db import get_db  # Asegúrate de importar bien tu conexión a la BD

auth_router = APIRouter()

# Tu ruta de login# Esquema para la solicitud de login
class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

# Esquema para la solicitud de registro
class RegisterRequest(BaseModel):
    nombreUsuario: str
    correo: str
    telefono: str
    password: str

# Tu ruta de login
@auth_router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):  
    # Usamos 'db' directamente para realizar la consulta
    user = db.query(Usuario).filter_by(nombre_usuario=data.usuario).first()

    if user and check_password_hash(user.Password, data.contrasena):
        return {"success": True, "message": "Login exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

# Ruta de registro
@auth_router.post("/register")
async def register(data: RegisterRequest, db: Session = Depends(get_db)):  
    hashed_password = generate_password_hash(data.password, method="pbkdf2:sha256")

    # Crear un nuevo usuario
    nuevo_usuario = Usuario(
        Username=data.nombreUsuario,
        Email=data.correo,
        Apellido=data.telefono,
        Password=hashed_password,
        Estatus="ACTIVO"
    )

    # Usamos la sesión 'db' correctamente
    db.add(nuevo_usuario)
    db.commit()

    return {"success": True, "message": "Usuario registrado correctamente"}