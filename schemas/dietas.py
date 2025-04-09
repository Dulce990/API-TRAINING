from pydantic import BaseModel
from typing import Optional
import datetime

class DietaBase(BaseModel):
    nombre: str
    objetivo: str
    tipo_ejercicios_recomendados: str
    dias_ejercicio: str
    calorias_diarias: float
    observaciones: Optional[str] = None
    estatus: bool

class DietaCreate(DietaBase):
    # Se elimina la relación con usuario.
    pass

class DietaUpdate(BaseModel):
    # Para la actualización se hace cada campo opcional
    nombre: Optional[str] = None
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

    class Config:
        from_attributes = True
