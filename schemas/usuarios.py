from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class EstatusUsuario(str, Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    
class RolUsuario(str, Enum):
    Usuario = "Usuario"
    Administrador = "Administrador"

class UsuarioBase(BaseModel):
    nombre_usuario: str
    correo_electronico: str
    contrasena: str
    numero_telefonico_movil: Optional[str] = None
    estatus: EstatusUsuario = EstatusUsuario.Activo
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    rol: RolUsuario = RolUsuario.Usuario  # ✅ Nuevo campo

    class Config:
        from_attributes = True

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    correo_electronico: Optional[str] = None
    contrasena: Optional[str] = None
    numero_telefonico_movil: Optional[str] = None
    estatus: Optional[EstatusUsuario] = None
    fecha_actualizacion: Optional[datetime] = None  # Se actualiza en la BD automáticamente
    rol: Optional[RolUsuario] = None  # ✅ Nuevo campo

    class Config:
        from_attributes = True

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    correo_electronico: str
    contrasena: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioR(BaseModel):
    id: int
    nombre_usuario: str
    correo_electronico: str

class RolUsuario(str, Enum):
    Usuario = "Usuario"
    Administrador = "Administrador"
