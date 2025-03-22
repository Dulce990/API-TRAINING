from typing import List
from config.db import mongo_db
from datetime import date, datetime
from models.expediente_medico import ExpedienteMedicoModel

async def get_expedientes(skip: int = 0, limit: int = 10) -> List[ExpedienteMedicoModel]:
    expedientes = await mongo_db["expedientes_medicos"].find().skip(skip).limit(limit).to_list(length=limit)
    
    for expediente in expedientes:
        # Mantiene el valor original de 'curp'
        expediente["curp"] = expediente.get("curp", "")
        del expediente["_id"]
    
    return expedientes

async def create_expediente(expediente: ExpedienteMedicoModel):
    expediente_dict = expediente.dict()
    # Convertir fechas a ISO
    for key, value in expediente_dict.items():
        if isinstance(value, (date, datetime)):
            expediente_dict[key] = value.isoformat()
    
    # Inserta el expediente sin modificar 'curp'
    await mongo_db["expedientes_medicos"].insert_one(expediente_dict)
    
    # Retorna el expediente con el curp original
    return expediente_dict

# Obtener expediente médico por CURP
async def get_expediente_by_id(curp: str):
    expediente = await mongo_db["expedientes_medicos"].find_one({"curp": curp})
    if expediente:
        expediente["curp"] = expediente["curp"]
        del expediente["_id"]  # Eliminar _id para evitar conflictos
    return expediente

async def update_expediente(curp: str, expediente: dict):
    result = await mongo_db["expedientes_medicos"].update_one(
        {"curp": curp}, {"$set": expediente}
    )
    if result.modified_count > 0:
        # Retornamos el documento actualizado para cumplir con el response_model
        updated_expediente = await mongo_db["expedientes_medicos"].find_one({"curp": curp})
        if updated_expediente:
            updated_expediente["curp"] = updated_expediente.get("curp", "")
            del updated_expediente["_id"]
        return updated_expediente
    return None

# Eliminar expediente médico por CURP
async def delete_expediente(curp: str):
    result = await mongo_db["expedientes_medicos"].delete_one({"curp": curp})
    return result.deleted_count > 0
