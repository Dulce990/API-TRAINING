from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObjetivoProgramaBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: Optional[datetime] = None
    fecha_finalizacion: Optional[datetime] = None
    estado: int
    progreso: float
    responsable: str
    prioridad: int

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
