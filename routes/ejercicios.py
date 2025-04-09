from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import timedelta, datetime
from config.db import get_db
from crud.ejercicios import get_ejercicios, get_ejercicio_by_id, create_ejercicio, update_ejercicio, delete_ejercicio
from schemas.ejercicios import EjercicioCreate, EjercicioUpdate, EjercicioResponse

router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])
bearer_scheme = HTTPBearer()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@router.get("/", response_model=List[EjercicioResponse])
def read_ejercicios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    return get_ejercicios(db, skip, limit)

@router.get("/{ejercicio_id}", response_model=EjercicioResponse)
def read_ejercicio(ejercicio_id: int, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    ejercicio = get_ejercicio_by_id(db, ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.post("/", response_model=EjercicioResponse)
def create_new_ejercicio(ejercicio: EjercicioCreate, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    return create_ejercicio(db, ejercicio)

@router.put("/{ejercicio_id}", response_model=EjercicioResponse)
def update_existing_ejercicio(ejercicio_id: int, ejercicio: EjercicioUpdate, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    updated_ejercicio = update_ejercicio(db, ejercicio_id, ejercicio)
    if not updated_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return updated_ejercicio

@router.delete("/{ejercicio_id}")
def delete_existing_ejercicio(ejercicio_id: int, db: Session = Depends(get_db), _: str = Depends(verify_token)):
    if not delete_ejercicio(db, ejercicio_id):
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": "Ejercicio eliminado exitosamente"}
