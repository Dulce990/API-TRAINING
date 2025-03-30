from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from enum import Enum

class ExpedienteMedicoBase(BaseModel):
    curp: Optional[str] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    estatura: Optional[float] = None   # Nuevo campo
    peso: Optional[float] = None       # Nuevo campo
    usuario_id: Optional[int] = None 

class ExpedienteMedicoCreate(ExpedienteMedicoBase):
    pass

class  ExpedienteUpdateModel(BaseModel):
    curp: Optional[str] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    estatura: Optional[float] = None   # Nuevo campo
    peso: Optional[float] = None       # Nuevo campo

class ExpedienteMedico(ExpedienteMedicoBase):
    id: str
