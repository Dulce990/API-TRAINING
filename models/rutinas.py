from sqlalchemy import Column, Integer, String, DateTime, Float, SmallInteger
from config.db import Base

class Rutina(Base):
    __tablename__ = "tbc_rutinas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    duracion = Column(Float, nullable=True)
    frecuencia = Column(SmallInteger, nullable=True)
    tipo = Column(String(50), nullable=True)
    intensidad = Column(SmallInteger, nullable=True)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_actualizacion = Column(DateTime, nullable=True)
