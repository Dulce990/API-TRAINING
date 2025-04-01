# routes/indicadores_nutricionales.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.indicadores_nutricionales import get_indicadores, get_indicador_by_id, create_indicador, update_indicador, delete_indicador
from schemas.indicadores_nutricionales import IndicadorNutricionalCreate, IndicadorNutricionalUpdate, IndicadorNutricionalResponse
from typing import List

router = APIRouter(prefix="/indicadores_nutricionales", tags=["Indicadores Nutricionales"])

SECRET_KEY = "mysecretkey"  # Cambia por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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

@router.get("/", response_model=List[IndicadorNutricionalResponse])
def read_indicadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    indicadores = get_indicadores(db, skip, limit)
    # Si deseas asignar el nombre del usuario en la respuesta, lo puedes hacer de la siguiente manera:
    for ind in indicadores:
        if ind.usuario:
            ind.usuario_nombre = ind.usuario.nombre_usuario
    return indicadores

@router.get("/{indicador_id}", response_model=IndicadorNutricionalResponse)
def read_indicador(indicador_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    indicador = get_indicador_by_id(db, indicador_id)
    if not indicador:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    if indicador.usuario:
        indicador.usuario_nombre = indicador.usuario.nombre_usuario
    return indicador

@router.post("/", response_model=IndicadorNutricionalResponse)
def create_new_indicador(indicador: IndicadorNutricionalCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    nuevo = create_indicador(db, indicador)
    if nuevo.usuario:
        nuevo.usuario_nombre = nuevo.usuario.nombre_usuario
    return nuevo

@router.put("/{indicador_id}", response_model=IndicadorNutricionalResponse)
def update_existing_indicador(indicador_id: int, indicador: IndicadorNutricionalUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    updated = update_indicador(db, indicador_id, indicador)
    if not updated:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    if updated.usuario:
        updated.usuario_nombre = updated.usuario.nombre_usuario
    return updated

@router.delete("/{indicador_id}")
def delete_existing_indicador(indicador_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    success = delete_indicador(db, indicador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    return {"message": "Indicador nutricional eliminado exitosamente"}
