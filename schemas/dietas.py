from pydantic import BaseModel
from typing import Optional
import datetime
from schemas.usuarios import UsuarioR  # Importa el esquema de salid

class DietaBase(BaseModel):
    nombre: str
    genero: str
    altura: float
    peso: float
    objetivo: str
    tipo_ejercicios_recomendados: str
    dias_ejercicio: str
    calorias_diarias: float
    observaciones: Optional[str] = None
    estatus: bool


class DietaCreate(DietaBase):
       user_id: int  # ID del usuario a


class DietaUpdate(DietaBase):
    nombre: Optional[str] = None
    genero: Optional[str] = None
    altura: Optional[float] = None
    peso: Optional[float] = None
    objetivo: Optional[str] = None
    tipo_ejercicios_recomendados: Optional[str] = None
    dias_ejercicio: Optional[str] = None
    calorias_diarias: Optional[float] = None
    observaciones: Optional[str] = None
    estatus: Optional[bool] = None

class DietaInDB(DietaBase):
    id: int
    fecha_registro: datetime.datetime
    fecha_actualizacion: Optional[datetime.datetime] = None
    usuario: Optional[UsuarioR] = None  # Incluye la relación usuario

    class Config:
        from_attributes = True
