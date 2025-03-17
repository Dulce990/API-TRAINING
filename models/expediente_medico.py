from sqlalchemy import Column, Integer, String, Date, Text, Enum, TIMESTAMP
from config.db import Base
from datetime import datetime
import enum

class SexoEnum(str, enum.Enum):
    Masculino = "Masculino"
    Femenino = "Femenino"
    Otro = "Otro"

class ExpedienteMedico(Base):
    __tablename__ = "tbb_expediente_medico"  # Verifica que la tabla exista en tu base de datos
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(Enum(SexoEnum), nullable=False)
    curp = Column(String(18), nullable=False, unique=True)
    fecha_registro = Column(TIMESTAMP, default=datetime.utcnow)
    direccion = Column(String(255))
    telefono = Column(String(15))
    correo_electronico = Column(String(100))
    fecha_ultima_de_evaluacion = Column(Date)
    antecedentes_medicos = Column(Text)
    lesiones_previas = Column(Text)
    presion_arterial = Column(String(20))
