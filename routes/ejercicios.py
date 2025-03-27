from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.ejercicios import get_ejercicios, get_ejercicio_by_id, create_ejercicio, update_ejercicio, delete_ejercicio, get_progreso_usuario
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
    ejercicios = get_ejercicios(db, skip, limit)
    return ejercicios
  
@router.get("/{ejercicio_id}", response_model=EjercicioResponse)
def read_ejercicio(ejercicio_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    ejercicio = get_ejercicio_by_id(db, ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.post("/", response_model=EjercicioResponse)
def create_new_ejercicio(ejercicio: EjercicioCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    print(ejercicio.dict())  # Imprime los datos recibidos
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

# Crear un endpoint para obtener ejercicios completados por usuario y fecha
from sqlalchemy.sql import extract  # Importa extract para trabajar con fechas

@router.get("/progreso/{usuario_id}", response_model=dict)
def progreso_usuario(usuario_id: int, mes: int = None, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    if mes is None:
        raise HTTPException(status_code=400, detail="El parámetro 'mes' es obligatorio.")
    # Filtrar ejercicios por usuario y mes usando fecha_personalizada
    ejercicios_usuario = db.query(Ejercicio).filter(
        Ejercicio.user_id == usuario_id,
        extract('month', Ejercicio.fecha_personalizada) == mes  # Extraer el mes de fecha_personalizada
    ).all()

    if not ejercicios_usuario:
        return {"message": "No hay ejercicios para este usuario en este mes", "data": [], "objetivo": None}

    ejercicios_completados = [ej for ej in ejercicios_usuario if ej.completado]
    conteo_por_dia = [0] * 31
    for ejercicio in ejercicios_completados:
        if ejercicio.fecha_personalizada:
            dia = ejercicio.fecha_personalizada.day - 1
            conteo_por_dia[dia] += 1

    total_completados = sum(conteo_por_dia)
    porcentaje = (total_completados / 31) * 100

    # Obtener el objetivo del usuario (asumiendo que todos los ejercicios tienen el mismo objetivo)
    objetivo = ejercicios_usuario[0].objetivo if ejercicios_usuario else None

    return {"message": "Progreso obtenido correctamente", "data": conteo_por_dia, "porcentaje": porcentaje, "objetivo": objetivo}

@router.put("/{ejercicio_id}/completar", response_model=EjercicioResponse)
def marcar_como_completado(ejercicio_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    db_ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    if not db_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    db_ejercicio.completado = True  # Marcar como completado
    db.commit()
    db.refresh(db_ejercicio)
    return db_ejercicio