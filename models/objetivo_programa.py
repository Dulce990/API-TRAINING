from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from config.db import Base

class ObjetivoPrograma(Base):
    __tablename__ = "tbc_objetivo_programa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(Integer, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Nueva relación para rutinas
    rutinas = relationship("Rutina", back_populates="objetivo")