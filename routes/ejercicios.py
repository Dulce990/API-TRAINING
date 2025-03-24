from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.ejercicios import get_ejercicios, get_ejercicio_by_id, create_ejercicio, update_ejercicio, delete_ejercicio
from schemas.ejercicios import EjercicioCreate, EjercicioUpdate, EjercicioResponse
from typing import List
from models.ejercicios import Ejercicio

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])

# Configuración del token
SECRET_KEY = "mysecretkey"  # Cámbialo por algo más seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bearer_scheme = HTTPBearer()

# Crear token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

@router.get("/", response_model=List[EjercicioResponse])
def read_ejercicios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return get_ejercicios(db, skip, limit)

@router.get("/{ejercicio_id}", response_model=EjercicioResponse)
def read_ejercicio(ejercicio_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    ejercicio = get_ejercicio_by_id(db, ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.post("/", response_model=EjercicioResponse)
def create_new_ejercicio(ejercicio: EjercicioCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return create_ejercicio(db, ejercicio)

@router.put("/{ejercicio_id}", response_model=EjercicioResponse)
def update_existing_ejercicio(ejercicio_id: int, ejercicio: EjercicioUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    updated_ejercicio = update_ejercicio(db, ejercicio_id, ejercicio)
    if not updated_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return updated_ejercicio

@router.delete("/{ejercicio_id}")
def delete_existing_ejercicio(ejercicio_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    success = delete_ejercicio(db, ejercicio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": "Ejercicio eliminado exitosamente"}

@router.get("/usuario/{usuario_id}", response_model=List[EjercicioResponse])
def get_ejercicios_by_usuario(usuario_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return db.query(Ejercicio).filter(Ejercicio.user_id == usuario_id).offset(skip).limit(limit).all()