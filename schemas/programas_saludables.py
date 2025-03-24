from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgramaSaludableBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_finalizacion: Optional[datetime] = None
    estado: int
    progreso: Optional[float] = None
    responsable: Optional[str] = None
    prioridad: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

class ProgramaSaludableCreate(ProgramaSaludableBase):
    pass

class ProgramaSaludableUpdate(ProgramaSaludableBase):
    pass

class ProgramaSaludableResponse(ProgramaSaludableBase):
    id: int

    class Config:
       from_attributes = True 
