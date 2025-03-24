from sqlalchemy import Column, Integer, String, DateTime, Float
from config.db import Base

class ProgramaSaludable(Base):
    __tablename__ = "tbc_programas_saludables"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(500), nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_finalizacion = Column(DateTime, nullable=True)
    estado = Column(Integer, nullable=False)
    progreso = Column(Float, nullable=True)
    responsable = Column(String(255), nullable=True)
    prioridad = Column(Integer, nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    fecha_actualizacion = Column(DateTime, nullable=True)
