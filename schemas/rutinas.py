from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RutinaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    duracion: Optional[float] = None
    frecuencia: Optional[int] = None
    tipo: Optional[str] = None
    intensidad: Optional[int] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

class RutinaCreate(RutinaBase):
    pass

class RutinaUpdate(RutinaBase):
    pass

class RutinaResponse(RutinaBase):
    id: int

    class Config:
        from_attributes = True 
