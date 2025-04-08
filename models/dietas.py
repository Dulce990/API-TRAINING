from sqlalchemy import Boolean, Column, Enum, Float, Integer, Text, DateTime, String
from sqlalchemy.orm import declarative_base
import datetime
from config.db import Base

class Dieta(Base):
    __tablename__ = "tbc_dietas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(55), nullable=False)
    objetivo = Column(Enum('Perdida de Peso', 'Aumento de masa muscular', 'Mantenimiento'), nullable=False)
    tipo_ejercicios_recomendados = Column(Enum('Cardio', 'Levantamiento de pesas', 'Ejercicios Tecnicos'), nullable=False)
    dias_ejercicio = Column(Enum('1 dia a la semana', '2 dias a la semana', '3 dias a la semana', '4 dias a la semana', '5 dias a la semana'), nullable=False)
    calorias_diarias = Column(Float, nullable=False)
    observaciones = Column(Text, nullable=True)
    estatus = Column(Boolean, default=True, nullable=False)  # Manejar como bit(1)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=True)
