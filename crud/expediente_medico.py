from typing import List
from config.db import mongo_db
from models.expediente_medico import ExpedienteMedicoModel

# Obtener todos los expedientes médicos
async def get_expedientes(skip: int = 0, limit: int = 10) -> List[ExpedienteMedicoModel]:
    expedientes = await mongo_db["expedientes_medicos"].find().skip(skip).limit(limit).to_list(length=limit)
    return expedientes

# Obtener expediente médico por ID
async def get_expediente_by_id(expediente_id: str):
    expediente = await mongo_db["expedientes_medicos"].find_one({"_id": expediente_id})
    return expediente

# Crear expediente médico
async def create_expediente(expediente: ExpedienteMedicoModel):
    result = await mongo_db["expedientes_medicos"].insert_one(expediente.dict())
    return result.inserted_id

# Actualizar expediente médico
async def update_expediente(expediente_id: str, expediente: dict):
    result = await mongo_db["expedientes_medicos"].update_one(
        {"_id": expediente_id}, {"$set": expediente}
    )
    return result.modified_count > 0

# Eliminar expediente médico
async def delete_expediente(expediente_id: str):
    result = await mongo_db["expedientes_medicos"].delete_one({"_id": expediente_id})
    return result.deleted_count > 0
