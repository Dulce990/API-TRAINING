from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.indicadores_nutricionales import get_indicadores, get_indicador_by_id, create_indicador, update_indicador, delete_indicador
from schemas.indicadores_nutricionales import IndicadorNutricionalCreate, IndicadorNutricionalUpdate, IndicadorNutricionalResponse
from typing import List

router = APIRouter(prefix="/indicadores_nutricionales", tags=["Indicadores Nutricionales"])

@router.get("/", response_model=List[IndicadorNutricionalResponse])
def read_indicadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_indicadores(db, skip, limit)

@router.get("/{indicador_id}", response_model=IndicadorNutricionalResponse)
def read_indicador(indicador_id: int, db: Session = Depends(get_db)):
    indicador = get_indicador_by_id(db, indicador_id)
    if not indicador:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    return indicador

@router.post("/", response_model=IndicadorNutricionalResponse)
def create_new_indicador(indicador: IndicadorNutricionalCreate, db: Session = Depends(get_db)):
    return create_indicador(db, indicador)

@router.put("/{indicador_id}", response_model=IndicadorNutricionalResponse)
def update_existing_indicador(indicador_id: int, indicador: IndicadorNutricionalUpdate, db: Session = Depends(get_db)):
    updated_indicador = update_indicador(db, indicador_id, indicador)
    if not updated_indicador:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    return updated_indicador

@router.delete("/{indicador_id}")
def delete_existing_indicador(indicador_id: int, db: Session = Depends(get_db)):
    success = delete_indicador(db, indicador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Indicador nutricional no encontrado")
    return {"message": "Indicador nutricional eliminado exitosamente"}
