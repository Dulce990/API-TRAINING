from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObjetivoProgramaBase(BaseModel):
    nombre: str
    descripcion: str
    estado: bool
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime]

class ObjetivoProgramaCreate(ObjetivoProgramaBase):
    pass

class ObjetivoProgramaUpdate(ObjetivoProgramaBase):
    pass

class ObjetivoProgramaResponse(ObjetivoProgramaBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime]  # ✅ Acepta NULL

    class Config:
        from_attributes = True
