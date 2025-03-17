from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IndicadorNutricionalBase(BaseModel):
    nombre: str
    descripcion: str
    unidad: str
    valor_referencia: float

class IndicadorNutricionalCreate(IndicadorNutricionalBase):
    pass

class IndicadorNutricionalUpdate(IndicadorNutricionalBase):
    pass

class IndicadorNutricionalResponse(IndicadorNutricionalBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
