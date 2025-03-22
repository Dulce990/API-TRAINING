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
    
class ExpedienteUpdateModel(BaseModel):
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
    estatura: Optional[float] = None
    peso: Optional[float] = None

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data['sexo'] = self.sexo.value  # Convertir el Enum a su valor
        return data
    
    @classmethod
    def parse_obj(cls, obj):
        if isinstance(obj.get('fecha_nacimiento'), datetime.date):
            obj['fecha_nacimiento'] = datetime.combine(obj['fecha_nacimiento'], datetime.min.time())
        if isinstance(obj.get('fecha_ultima_de_evaluacion'), datetime.date):
            obj['fecha_ultima_de_evaluacion'] = datetime.combine(obj['fecha_ultima_de_evaluacion'], datetime.min.time())
        return super().parse_obj(obj)


