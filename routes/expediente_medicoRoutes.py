from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, date, time
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from crud.expediente_medico import (
    get_expedientes,
    get_expediente_by_id,
    create_expediente,
    update_expediente,
    delete_expediente,
    get_expediente_by_id
)
from models.expediente_medico import ExpedienteMedicoModel, ExpedienteUpdateModel

router = APIRouter()

# Configuración del token
SECRET_KEY = "mysecretkey"  # Cámbialo por algo más seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bearer_scheme = HTTPBearer()

# Crear token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

def convert_dates(update_dict: dict) -> dict:
    for key, value in update_dict.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            update_dict[key] = datetime.combine(value, time.min)
    return update_dict

# Obtener lista de expedientes (con paginación)
@router.get("/expedientes", response_model=List[ExpedienteMedicoModel])
async def read_expedientes(skip: int = 0, limit: int = 10, user_id: str = Depends(verify_token)):
    return await get_expedientes(skip, limit)

# Obtener expediente por CURP
@router.get("/expedientes/{curp}", response_model=ExpedienteMedicoModel)
async def read_expediente(curp: str, user_id: str = Depends(verify_token)):
    expediente = await get_expediente_by_id(curp)
    if not expediente:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return expediente

# Crear un nuevo expediente
@router.post("/expedientes", response_model=ExpedienteMedicoModel)
async def create_new_expediente(expediente: ExpedienteMedicoModel, user_id: str = Depends(verify_token)):
    nuevo_expediente = await create_expediente(expediente)
    if not nuevo_expediente:
        raise HTTPException(status_code=400, detail="Error al crear el expediente")
    return nuevo_expediente

# Actualizar expediente existente por CURP
@router.put("/expedientes/{curp}", response_model=ExpedienteMedicoModel)
async def update_existing_expediente(curp: str, expediente: ExpedienteUpdateModel, user_id: str = Depends(verify_token)):
    update_data = expediente.dict(exclude_unset=True)
    update_data = convert_dates(update_data)
    expediente_actualizado = await update_expediente(curp, update_data)
    if not expediente_actualizado:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return expediente_actualizado

# Eliminar expediente existente por CURP
@router.delete("/expedientes/{curp}", response_model=dict)
async def delete_existing_expediente(curp: str, user_id: str = Depends(verify_token)):
    success = await delete_expediente(curp)
    if not success:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return {"message": "Expediente eliminado correctamente"}

# Obtener expediente por usuario_id (relación con MySQL)
@router.get("/expedientes/usuario/{usuario_id}", response_model=ExpedienteMedicoModel)
async def read_expediente_by_usuario_id(usuario_id: int, user_id: str = Depends(verify_token)):
    expediente = await get_expediente_by_id(usuario_id)
    if not expediente:
        raise HTTPException(status_code=404, detail="Expediente no encontrado")
    return expediente
