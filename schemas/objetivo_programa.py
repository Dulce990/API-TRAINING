from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObjetivoProgramaBase(BaseModel):
    nombre: str
    descripcion: str
    estado: int
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

class ObjetivoProgramaCreate(ObjetivoProgramaBase):
    pass

class ObjetivoProgramaUpdate(ObjetivoProgramaBase):
    pass

class ObjetivoProgramaResponse(ObjetivoProgramaBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
