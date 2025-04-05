from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, SmallInteger, Time
from sqlalchemy.orm import relationship
from config.db import Base

class Rutina(Base):
    __tablename__ = "tbc_rutinas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("tbb_usuarios.id"), nullable=False)
    ejercicios_id = Column(Integer, ForeignKey("tbc_ejercicios.id"), nullable=False)
    objetivo_id = Column(Integer, ForeignKey("tbc_objetivo_programa.id"), nullable=True)
    descripcion = Column(String(500), nullable=True)
    duracion = Column(Float, nullable=True)
    frecuencia = Column(DateTime, nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_finalizacion = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_actualizacion = Column(DateTime, nullable=True) 
    
# Opcionalmente, puedes definir relaciones para facilitar el acceso a los objetos relacionados:
    usuario = relationship("Usuario", back_populates="rutinas")
    ejercicio = relationship("Ejercicio", back_populates="rutinas")
    objetivo = relationship("ObjetivoPrograma", back_populates="rutinas")
    
    