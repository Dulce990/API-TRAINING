from sqlalchemy import Column, Integer, ForeignKey, DateTime
from config.db import Base
from datetime import datetime

class RolUsuario(Base):
    __tablename__ = "tbd_usuarios_roles"
    usuario_id = Column(Integer, ForeignKey("tbb_usuarios.id"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("tbc_roles.id"), primary_key=True)
    estatus = Column(Integer, nullable=False, default=1)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True)
