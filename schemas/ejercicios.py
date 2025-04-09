from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoEjercicio(str, Enum):
    Aerobico = "Aerobico"
    Resistencia = "Resistencia"
    Flexibilidad = "Flexibilidad"
    Fuerza = "Fuerza"

class DificultadEjercicio(str, Enum):
    Basico = "Basico"
    Intermedio = "Intermedio"
    Avanzado = "Avanzado"

class EjercicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    video: Optional[str] = None
    tipo: TipoEjercicio
    estatus: bool
    dificultad: DificultadEjercicio
    recomendaciones: Optional[str] = None
    restricciones: Optional[str] = None

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioUpdate(EjercicioBase):
    pass

class EjercicioResponse(EjercicioBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True
