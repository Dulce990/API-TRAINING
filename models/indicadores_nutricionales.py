# models/indicadores_nutricionales.py
from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy.sql import func
from config.db import Base  # Asegúrate de que tu objeto Base esté correctamente importado

class NivelActividad(enum.Enum):
    Sedentario = "Sedentario"
    Ligero = "Ligero"
    Moderado = "Moderado"
    Activo = "Activo"
    Muy_Activo = "Muy_Activo"

class IndicadorNutricional(Base):
    __tablename__ = "tbd_indicadores_nutricionales"  # Coincide con tu tabla en MySQL
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)
    porcentaje_grasa = Column(Float, nullable=False)
    nivel_actividad = Column(Enum(NivelActividad), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    usuario_id = Column(Integer, ForeignKey("tbb_usuarios.id"), nullable=True)  # Relación con la tabla de usuarios

    # Relación: permite acceder al objeto Usuario asociado
    usuario = relationship("Usuario", back_populates="indicadores_nutricionales")
