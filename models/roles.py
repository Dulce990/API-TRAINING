from sqlalchemy import Column, Integer, String, DateTime
from config.db import Base
from datetime import datetime

class Rol(Base):
    __tablename__ = "tbc_roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)
    estatus = Column(String(10), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True)
