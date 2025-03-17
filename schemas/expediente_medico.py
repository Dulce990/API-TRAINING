from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum

class SexoEnum(str, Enum):
    Masculino = "Masculino"
    Femenino = "Femenino"
    Otro = "Otro"

class ExpedienteMedicoBase(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    sexo: SexoEnum
    curp: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_arterial: Optional[str] = None
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

class ExpedienteMedicoCreate(ExpedienteMedicoBase):
    pass

class ExpedienteMedicoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[SexoEnum] = None
    curp: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_arterial: Optional[str] = None
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

class ExpedienteMedico(ExpedienteMedicoBase):
    id: int

    class Config:
        from_attributes = True
