from fastapi import APIRouter, HTTPException
from typing import List
from crud.expediente_medico import (
    get_expedientes,
    get_expediente_by_id,
    create_expediente,
    update_expediente,
    delete_expediente
)
from models.expediente_medico import ExpedienteMedicoModel

router = APIRouter()

@router.get("/expediente_medico", response_model=List[ExpedienteMedicoModel])
async def read_expedientes(skip: int = 0, limit: int = 10):
    return await get_expedientes(skip, limit)

@router.get("/expediente_medico//{expediente_id}", response_model=ExpedienteMedicoModel)
async def read_expediente(expediente_id: str):
    expediente = await get_expediente_by_id(expediente_id)
    if not expediente:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return expediente

@router.post("/expediente_medico", response_model=str)
async def create_new_expediente(expediente: ExpedienteMedicoModel):
    return await create_expediente(expediente)

@router.put("/expediente_medico/{expediente_id}")
async def update_existing_expediente(expediente_id: str, expediente: dict):
    success = await update_expediente(expediente_id, expediente)
    if not success:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return {"message": "Expediente actualizado"}

@router.delete("/expediente_medico/{expediente_id}")
async def delete_existing_expediente(expediente_id: str):
    success = await delete_expediente(expediente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return {"message": "Expediente eliminado"}
