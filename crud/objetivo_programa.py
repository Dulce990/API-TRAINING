from sqlalchemy.orm import Session
from models.objetivo_programa import ObjetivoPrograma
from schemas.objetivo_programa import ObjetivoProgramaCreate, ObjetivoProgramaUpdate

def get_objetivos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ObjetivoPrograma).offset(skip).limit(limit).all()

def get_objetivo_by_id(db: Session, objetivo_id: int):
    return db.query(ObjetivoPrograma).filter(ObjetivoPrograma.id == objetivo_id).first()

def create_objetivo(db: Session, objetivo: ObjetivoProgramaCreate):
    nuevo_objetivo = ObjetivoPrograma(**objetivo.dict())
    db.add(nuevo_objetivo)
    db.commit()
    db.refresh(nuevo_objetivo)
    return nuevo_objetivo

def update_objetivo(db: Session, objetivo_id: int, objetivo: ObjetivoProgramaUpdate):
    db_objetivo = db.query(ObjetivoPrograma).filter(ObjetivoPrograma.id == objetivo_id).first()
    if not db_objetivo:
        return None
    for key, value in objetivo.dict(exclude_unset=True).items():
        setattr(db_objetivo, key, value)
    db.commit()
    db.refresh(db_objetivo)
    return db_objetivo

def delete_objetivo(db: Session, objetivo_id: int):
    db_objetivo = db.query(ObjetivoPrograma).filter(ObjetivoPrograma.id == objetivo_id).first()
    if not db_objetivo:
        return False
    db.delete(db_objetivo)
    db.commit()
    return True
