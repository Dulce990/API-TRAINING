from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.objetivo_programa import get_objetivos, get_objetivo_by_id, create_objetivo, update_objetivo, delete_objetivo
from schemas.objetivo_programa import ObjetivoProgramaCreate, ObjetivoProgramaUpdate, ObjetivoProgramaResponse
from typing import List

router = APIRouter(prefix="/objetivos_programa", tags=["Objetivos del Programa"])

@router.get("/", response_model=List[ObjetivoProgramaResponse])
def read_objetivos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_objetivos(db, skip, limit)

@router.get("/{objetivo_id}", response_model=ObjetivoProgramaResponse)
def read_objetivo(objetivo_id: int, db: Session = Depends(get_db)):
    objetivo = get_objetivo_by_id(db, objetivo_id)
    if not objetivo:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return objetivo

@router.post("/", response_model=ObjetivoProgramaResponse)
def create_new_objetivo(objetivo: ObjetivoProgramaCreate, db: Session = Depends(get_db)):
    return create_objetivo(db, objetivo)

@router.put("/{objetivo_id}", response_model=ObjetivoProgramaResponse)
def update_existing_objetivo(objetivo_id: int, objetivo: ObjetivoProgramaUpdate, db: Session = Depends(get_db)):
    updated_objetivo = update_objetivo(db, objetivo_id, objetivo)
    if not updated_objetivo:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return updated_objetivo

@router.delete("/{objetivo_id}")
def delete_existing_objetivo(objetivo_id: int, db: Session = Depends(get_db)):
    success = delete_objetivo(db, objetivo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Objetivo del programa no encontrado")
    return {"message": "Objetivo del programa eliminado exitosamente"}
