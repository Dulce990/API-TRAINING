from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UsuarioRolBase(BaseModel):
    usuario_id: int
    rol_id: int
    estatus: int

class UsuarioRolResponse(UsuarioRolBase):
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True
