from sqlalchemy.orm import Session
from models.rutinas import Rutina
from schemas.rutinas import RutinaCreate, RutinaUpdate

def get_rutinas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Rutina).offset(skip).limit(limit).all()

def get_rutina_by_id(db: Session, rutina_id: int):
    return db.query(Rutina).filter(Rutina.id == rutina_id).first()

def create_rutina(db: Session, rutina: RutinaCreate):
    db_rutina = Rutina(**rutina.dict())
    db.add(db_rutina)
    db.commit()
    db.refresh(db_rutina)
    return db_rutina

def update_rutina(db: Session, rutina_id: int, rutina: RutinaUpdate):
    db_rutina = get_rutina_by_id(db, rutina_id)
    if not db_rutina:
        return None
    for key, value in rutina.dict(exclude_unset=True).items():
        setattr(db_rutina, key, value)
    db.commit()
    db.refresh(db_rutina)
    return db_rutina

def delete_rutina(db: Session, rutina_id: int):
    db_rutina = get_rutina_by_id(db, rutina_id)
    if not db_rutina:
        return False
    db.delete(db_rutina)
    db.commit()
    return True
