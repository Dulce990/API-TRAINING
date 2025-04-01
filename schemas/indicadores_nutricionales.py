# schemas/indicadores_nutricionales.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class NivelActividadEnum(str, Enum):
    Sedentario = "Sedentario"
    Ligero = "Ligero"
    Moderado = "Moderado"
    Activo = "Activo"
    Muy_Activo = "Muy_Activo"

class IndicadorNutricionalBase(BaseModel):
    altura: float
    peso: float
    imc: float
    porcentaje_grasa: float
    nivel_actividad: NivelActividadEnum
    usuario_id: Optional[int] = None  # Se recibe el id del usuario en creación

class IndicadorNutricionalCreate(IndicadorNutricionalBase):
    pass

class IndicadorNutricionalUpdate(IndicadorNutricionalBase):
    pass

class IndicadorNutricionalResponse(BaseModel):
    id: int
    altura: float
    peso: float
    imc: float
    porcentaje_grasa: float
    nivel_actividad: NivelActividadEnum
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    usuario_nombre: Optional[str] = None  # Se mostrará el nombre del usuario en vez de solo el id

    class Config:
        orm_mode = True
