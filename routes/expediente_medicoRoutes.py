from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db  # Asegúrate de que la importación de get_db sea correcta
from crud.expediente_medico import (
    get_expediente_medico,
    get_expediente_medico_by_id,
    create_expediente_medico,
    update_expediente_medico,
    delete_expediente_medico
)
from schemas.expediente_medico import ExpedienteMedico, ExpedienteMedicoCreate, ExpedienteMedicoUpdate

router = APIRouter()

@router.get("/expediente_medico/", response_model=list[ExpedienteMedico])
def read_expedientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_expediente_medico(db, skip=skip, limit=limit)

@router.get("/expediente_medico/{expediente_id}", response_model=ExpedienteMedico)
def read_expediente(expediente_id: int, db: Session = Depends(get_db)):
    expediente = get_expediente_medico_by_id(db, expediente_id)
    if expediente is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return expediente

@router.post("/expediente_medico/", response_model=ExpedienteMedico)
def create_new_expediente(expediente: ExpedienteMedicoCreate, db: Session = Depends(get_db)):
    return create_expediente_medico(db, expediente)

@router.put("/expediente_medico/{expediente_id}", response_model=ExpedienteMedico)
def update_existing_expediente(expediente_id: int, expediente: ExpedienteMedicoUpdate, db: Session = Depends(get_db)):
    db_expediente = update_expediente_medico(db, expediente_id, expediente)
    if db_expediente is None:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return db_expediente

@router.delete("/expediente_medico/{expediente_id}")
def delete_existing_expediente(expediente_id: int, db: Session = Depends(get_db)):
    success = delete_expediente_medico(db, expediente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return {"message": "Expediente eliminado exitosamente"}
