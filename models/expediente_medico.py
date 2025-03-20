from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum

class SexoEnum(str, Enum):
    Masculino = "Masculino"
    Femenino = "Femenino"
    Otro = "Otro"

class ExpedienteMedicoModel(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    sexo: SexoEnum
    curp: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_arterial: Optional[str] = None
    estatura: Optional[float] = None
    peso: Optional[float] = None
    fecha_registro: Optional[datetime] = datetime.utcnow()
