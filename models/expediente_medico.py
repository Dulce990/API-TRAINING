from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class ExpedienteMedicoModel(BaseModel):
    curp: Optional[str] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_arterial: Optional[str] = None
    estatura: Optional[float] = None
    peso: Optional[float] = None
    fecha_registro: Optional[datetime] = datetime.utcnow()
    usuario_id: Optional[int] = None 
    
class ExpedienteUpdateModel(BaseModel):
    curp: Optional[str] = None
    fecha_ultima_de_evaluacion: Optional[date] = None
    antecedentes_medicos: Optional[str] = None
    lesiones_previas: Optional[str] = None
    presion_arterial: Optional[str] = None
    estatura: Optional[float] = None
    peso: Optional[float] = None
    
    @classmethod
    def parse_obj(cls, obj):
        if isinstance(obj.get('fecha_ultima_de_evaluacion'), datetime.date):
            obj['fecha_ultima_de_evaluacion'] = datetime.combine(obj['fecha_ultima_de_evaluacion'], datetime.min.time())
        return super().parse_obj(obj)


