from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.ejercicios import get_ejercicios, get_ejercicio_by_id, create_ejercicio, update_ejercicio, delete_ejercicio, get_progreso_usuario
from schemas.ejercicios import EjercicioCreate, EjercicioUpdate, EjercicioResponse
from typing import List
from models.ejercicios import Ejercicio


router = APIRouter(prefix="/ejercicios", tags=["Ejercicios"])

@router.get("/", response_model=List[EjercicioResponse])
def read_ejercicios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ejercicios = get_ejercicios(db, skip, limit)
    return ejercicios
@router.get("/{ejercicio_id}", response_model=EjercicioResponse)
def read_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
    ejercicio = get_ejercicio_by_id(db, ejercicio_id)
    if not ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return ejercicio

@router.post("/", response_model=EjercicioResponse)
def create_new_ejercicio(ejercicio: EjercicioCreate, db: Session = Depends(get_db)):
    return create_ejercicio(db, ejercicio)

@router.put("/{ejercicio_id}", response_model=EjercicioResponse)
def update_existing_ejercicio(ejercicio_id: int, ejercicio: EjercicioUpdate, db: Session = Depends(get_db)):
    updated_ejercicio = update_ejercicio(db, ejercicio_id, ejercicio)
    if not updated_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return updated_ejercicio

@router.delete("/{ejercicio_id}")
def delete_existing_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
    success = delete_ejercicio(db, ejercicio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": "Ejercicio eliminado exitosamente"}

@router.get("/usuario/{usuario_id}", response_model=List[EjercicioResponse])
def get_ejercicios_by_usuario(usuario_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Ejercicio).filter(Ejercicio.user_id == usuario_id).offset(skip).limit(limit).all()

# Crear un endpoint para obtener ejercicios completados por usuario y fecha
@router.get("/progreso/{usuario_id}", response_model=dict)
def progreso_usuario(usuario_id: int, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    ejercicios_usuario = db.query(Ejercicio).filter(Ejercicio.user_id == usuario_id).all()
    if not ejercicios_usuario:
        return {"message": "No hay ejercicios para este usuario", "data": []}

    # Filtrar ejercicios completados
    ejercicios_completados = [
        ejercicio for ejercicio in ejercicios_usuario if ejercicio.completado
    ]

    # Procesar los datos para agruparlos por día del mes
    conteo_por_dia = [0] * 31
    for ejercicio in ejercicios_completados:
        dia = ejercicio.fecha_registro.day - 1  # Obtener el día del mes (0-indexado)
        conteo_por_dia[dia] += 1

    return {"message": "Progreso obtenido correctamente", "data": conteo_por_dia}


@router.put("/{ejercicio_id}/completar", response_model=EjercicioResponse)
def marcar_como_completado(ejercicio_id: int, db: Session = Depends(get_db)):
    db_ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    if not db_ejercicio:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    db_ejercicio.completado = True  # Marcar como completado
    db.commit()
    db.refresh(db_ejercicio)
    return db_ejercicio