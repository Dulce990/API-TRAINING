from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from config.db import get_db
from schemas.usuarios import Token, UsuarioLogin, UsuarioCreate, UsuarioUpdate, UsuarioR
from models.usuarios import Usuario
from crud.usuarios import get_usuario_by_email, get_usuarios
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

# ✅ Crear token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ Verificar token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

# ✅ Ruta para login
@router.post("/login", response_model=Token, tags=["Usuarios"])
def login(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    user = get_usuario_by_email(db, email=user_data.correo_electronico)
    if not user or not bcrypt.checkpw(user_data.contrasena.encode('utf-8'), user.contrasena.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": user.correo_electronico})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/", response_model=List[UsuarioR], tags=["Usuarios"])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db, skip, limit)

# ✅ Crear usuario
@router.post("/", response_model=UsuarioR, tags=["Usuarios"])
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        correo_electronico=usuario.correo_electronico,
        contrasena=hashed_password.decode('utf-8'),
        numero_telefonico_movil=usuario.numero_telefonico_movil,
        estatus=usuario.estatus
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# ✅ Obtener usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioR, tags=["Usuarios"])
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db), email: str = Depends(verify_token)):
    usuario = db.query(Usuario).filter(Usuario.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ✅ Actualizar usuario
@router.put("/{usuario_id}", response_model=UsuarioR, tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db), email: str = Depends(verify_token)):
    usuario = db.query(Usuario).filter(Usuario.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in usuario_data.dict(exclude_unset=True).items():
        setattr(usuario, key, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

# ✅ Eliminar usuario
@router.delete("/{usuario_id}", tags=["Usuarios"])
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), email: str = Depends(verify_token)):
    usuario = db.query(Usuario).filter(Usuario.ID == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}