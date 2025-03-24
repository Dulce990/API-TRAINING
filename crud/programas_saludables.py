from sqlalchemy.orm import Session
from models.programas_saludables import ProgramaSaludable
from schemas.programas_saludables import ProgramaSaludableCreate, ProgramaSaludableUpdate

def get_programas_saludables(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProgramaSaludable).offset(skip).limit(limit).all()

def get_programa_saludable_by_id(db: Session, programa_id: int):
    return db.query(ProgramaSaludable).filter(ProgramaSaludable.id == programa_id).first()

def create_programa_saludable(db: Session, programa: ProgramaSaludableCreate):
    db_programa = ProgramaSaludable(**programa.dict())
    db.add(db_programa)
    db.commit()
    db.refresh(db_programa)
    return db_programa

def update_programa_saludable(db: Session, programa_id: int, programa: ProgramaSaludableUpdate):
    db_programa = get_programa_saludable_by_id(db, programa_id)
    if not db_programa:
        return None
    for key, value in programa.dict(exclude_unset=True).items():
        setattr(db_programa, key, value)
    db.commit()
    db.refresh(db_programa)
    return db_programa

def delete_programa_saludable(db: Session, programa_id: int):
    db_programa = get_programa_saludable_by_id(db, programa_id)
    if not db_programa:
        return False
    db.delete(db_programa)
    db.commit()
    return True
