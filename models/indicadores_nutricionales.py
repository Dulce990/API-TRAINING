from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class IndicadorNutricional(Base):
    __tablename__ = "tbc_indicadores_nutricionales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)
    unidad = Column(String(50), nullable=False)
    valor_referencia = Column(Float, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
