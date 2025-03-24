from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.objetivo_programa import get_objetivos, get_objetivo_by_id, create_objetivo, update_objetivo, delete_objetivo
from schemas.objetivo_programa import ObjetivoProgramaCreate, ObjetivoProgramaUpdate, ObjetivoProgramaResponse
from typing import List

router = APIRouter(prefix="/objetivos_programa", tags=["Objetivos del Programa"])

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


@router.get("/", response_model=List[ObjetivoProgramaResponse])
def read_objetivos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return get_objetivos(db, skip, limit)

@router.get("/{objetivo_id}", response_model=ObjetivoProgramaResponse)
def read_objetivo(objetivo_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    objetivo = get_objetivo_by_id(db, objetivo_id)
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return objetivo

@router.post("/", response_model=ObjetivoProgramaResponse)
def create_new_objetivo(objetivo: ObjetivoProgramaCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return create_objetivo(db, objetivo)

@router.put("/{objetivo_id}", response_model=ObjetivoProgramaResponse)
def update_existing_objetivo(objetivo_id: int, objetivo: ObjetivoProgramaUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    updated_objetivo = update_objetivo(db, objetivo_id, objetivo)
    if not updated_objetivo:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return updated_objetivo

@router.delete("/{objetivo_id}")
def delete_existing_objetivo(objetivo_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    success = delete_objetivo(db, objetivo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return {"message": "Objetivo del programa eliminado exitosamente"}
