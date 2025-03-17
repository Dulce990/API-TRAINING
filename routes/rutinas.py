from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.rutinas import (
    get_rutinas, get_rutina_by_id, create_rutina, update_rutina, delete_rutina
)
from schemas.rutinas import RutinaCreate, RutinaUpdate, RutinaResponse

router = APIRouter()

@router.get("/rutinas", response_model=list[RutinaResponse])
def read_rutinas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_rutinas(db, skip=skip, limit=limit)

@router.get("/rutinas/{rutina_id}", response_model=RutinaResponse)
def read_rutina(rutina_id: int, db: Session = Depends(get_db)):
    rutina = get_rutina_by_id(db, rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return rutina

@router.post("/rutinas", response_model=RutinaResponse)
def create_rutina_endpoint(rutina: RutinaCreate, db: Session = Depends(get_db)):
    return create_rutina(db, rutina)

@router.put("/rutinas/{rutina_id}", response_model=RutinaResponse)
def update_rutina_endpoint(rutina_id: int, rutina: RutinaUpdate, db: Session = Depends(get_db)):
    updated_rutina = update_rutina(db, rutina_id, rutina)
    if not updated_rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return updated_rutina

@router.delete("/rutinas/{rutina_id}")
def delete_rutina_endpoint(rutina_id: int, db: Session = Depends(get_db)):
    success = delete_rutina(db, rutina_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return {"message": "Rutina eliminada correctamente"}
