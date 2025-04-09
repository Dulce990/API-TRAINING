from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

from sqlalchemy import Time

class RutinaBase(BaseModel):
    nombre: str
    user_id: Optional[int] = None
    ejercicio_id: Optional[int] = None
    objetivo_id: Optional[int] = None
    descripcion: Optional[str] = None
    duracion: Optional[float] = None
    frecuencia: Optional[time] = None
    fecha_inicio: Optional[datetime] = None
    fecha_finalizacion: Optional[datetime] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

class RutinaCreate(RutinaBase):
    pass

class RutinaUpdate(RutinaBase):
    pass

class RutinaResponse(RutinaBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True 
        
