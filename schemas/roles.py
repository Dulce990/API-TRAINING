from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estatus: str

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True
