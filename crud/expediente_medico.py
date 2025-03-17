from sqlalchemy.orm import Session
from models.expediente_medico import ExpedienteMedico  # Asegúrate de que la importación del modelo sea correcta
from schemas.expediente_medico import ExpedienteMedicoCreate, ExpedienteMedicoUpdate

# Función para obtener expedientes médicos
def get_expediente_medico(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ExpedienteMedico).offset(skip).limit(limit).all()

# Función para obtener un expediente médico por su ID
def get_expediente_medico_by_id(db: Session, expediente_id: int):
    return db.query(ExpedienteMedico).filter(ExpedienteMedico.id == expediente_id).first()

# Función para crear un expediente médico
def create_expediente_medico(db: Session, expediente: ExpedienteMedicoCreate):
    nuevo_expediente = ExpedienteMedico(**expediente.dict())  # Asegúrate de pasar correctamente los datos
    db.add(nuevo_expediente)
    db.commit()
    db.refresh(nuevo_expediente)
    return nuevo_expediente

# Función para actualizar un expediente médico
def update_expediente_medico(db: Session, expediente_id: int, expediente: ExpedienteMedicoUpdate):
    db_expediente = db.query(ExpedienteMedico).filter(ExpedienteMedico.id == expediente_id).first()
    if not db_expediente:
        return None
    for key, value in expediente.dict(exclude_unset=True).items():
        setattr(db_expediente, key, value)
    db.commit()
    db.refresh(db_expediente)
    return db_expediente

# Función para eliminar un expediente médico
def delete_expediente_medico(db: Session, expediente_id: int):
    db_expediente = db.query(ExpedienteMedico).filter(ExpedienteMedico.id == expediente_id).first()
    if not db_expediente:
        return False
    db.delete(db_expediente)
    db.commit()
    return True
