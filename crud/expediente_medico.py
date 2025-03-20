from typing import List
from config.db import mongo_db
from datetime import date, datetime
from models.expediente_medico import ExpedienteMedicoModel

# Obtener todos los expedientes médicos
async def get_expedientes(skip: int = 0, limit: int = 10) -> List[ExpedienteMedicoModel]:
    expedientes = await mongo_db["expedientes_medicos"].find().skip(skip).limit(limit).to_list(length=limit)
    return expedientes

# Obtener expediente médico por ID
async def get_expediente_by_id(expediente_id: str):
    expediente = await mongo_db["expedientes_medicos"].find_one({"_id": expediente_id})
    return expediente

async def create_expediente(expediente: ExpedienteMedicoModel):
    # Convertir fechas a strings antes de insertarlas en MongoDB
    expediente_dict = expediente.dict()

    # Convertir datetime.date y datetime.datetime a ISO format
    for key, value in expediente_dict.items():
        if isinstance(value, (date, datetime)):
            expediente_dict[key] = value.isoformat()
    
    result = await mongo_db["expedientes_medicos"].insert_one(expediente_dict)
    
    # Retornar el ID insertado como string
    return str(result.inserted_id)
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
