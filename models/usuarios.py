from sqlalchemy import Column, Integer, String, DateTime, Enum
from config.db import Base
import enum
from datetime import datetime
from sqlalchemy.orm import relationship

class EstatusUsuario(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    
class RolUsuario(str, enum.Enum):
    Usuario = "Usuario"
    Administrador = "Administrador"

class Usuario(Base):
    __tablename__ = "tbb_usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(60), nullable=False)
    correo_electronico = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)  # Contraseñas encriptadas
    numero_telefonico_movil = Column(String(20))
    estatus = Column(Enum(EstatusUsuario), default=EstatusUsuario.Activo)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = None
    rol = Column(Enum(RolUsuario), default=RolUsuario.Usuario)  # ✅ Nuevo campo
    fecha_actualizacion = Column(DateTime, nullable=True)
    

    # Relación con Dieta
    dietas = relationship("Dieta", back_populates="usuario")
