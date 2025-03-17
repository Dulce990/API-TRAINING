from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.programas_saludables import (
    get_programas_saludables, get_programa_saludable_by_id, create_programa_saludable, update_programa_saludable, delete_programa_saludable
)
from schemas.programas_saludables import ProgramaSaludableCreate, ProgramaSaludableUpdate, ProgramaSaludableResponse

router = APIRouter()

@router.get("/programas_saludables", response_model=list[ProgramaSaludableResponse])
def read_programas_saludables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_programas_saludables(db, skip=skip, limit=limit)

@router.get("/programas_saludables/{programa_id}", response_model=ProgramaSaludableResponse)
def read_programa_saludable(programa_id: int, db: Session = Depends(get_db)):
    programa = get_programa_saludable_by_id(db, programa_id)
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa

@router.post("/programas_saludables", response_model=ProgramaSaludableResponse)
def create_programa(programa: ProgramaSaludableCreate, db: Session = Depends(get_db)):
    return create_programa_saludable(db, programa)

@router.put("/programas_saludables/{programa_id}", response_model=ProgramaSaludableResponse)
def update_programa(programa_id: int, programa: ProgramaSaludableUpdate, db: Session = Depends(get_db)):
    updated_programa = update_programa_saludable(db, programa_id, programa)
    if not updated_programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return updated_programa

@router.delete("/programas_saludables/{programa_id}")
def delete_programa(programa_id: int, db: Session = Depends(get_db)):
    success = delete_programa_saludable(db, programa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return {"message": "Programa eliminado correctamente"}
