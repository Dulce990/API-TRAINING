from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, Boolean
import enum
from datetime import datetime
from sqlalchemy.orm import relationship
from config.db import Base
from sqlalchemy import Date

class TipoEjercicio(str, enum.Enum):
    Aerobico = "Aerobico"
    Resistencia = "Resistencia"
    Flexibilidad = "Flexibilidad"
    Fuerza = "Fuerza"

class DificultadEjercicio(str, enum.Enum):
    Basico = "Basico"
    Intermedio = "Intermedio"
    Avanzado = "Avanzado"

class Ejercicio(Base):
    __tablename__ = "tbc_ejercicios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255))
    video = Column(String(255))
    tipo = Column(Enum(TipoEjercicio), nullable=False)
    estatus = Column(Boolean, nullable=False, default=True)
    dificultad = Column(Enum(DificultadEjercicio), nullable=False) # valor numerico para que desde el front, se mida la dificultad
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    recomendaciones = Column(String(255)) # Por ejemplo: Tener la espalda recta.
    restricciones = Column(String(255))# No apto para personas con problemas cardi
    
    # Nueva relación para rutinas
    rutinas = relationship("Rutina", back_populates="ejercicio")