from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

from schemas.usuarios import UsuarioR

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
    user_id: Optional[int] = None  # ✅ Añade user_id

class EjercicioUpdate(EjercicioBase):
    pass

class EjercicioResponse(EjercicioBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime
    usuario: Optional[UsuarioR] = None  # Agrega la relación usuario

    class Config:
        from_attributes = True
