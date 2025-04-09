from sqlalchemy.orm import Session
from models.dietas import Dieta
from schemas.dietas import DietaCreate, DietaUpdate

def get_dietas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Dieta).offset(skip).limit(limit).all()

def get_dieta_by_id(db: Session, dieta_id: int):
    return db.query(Dieta).filter(Dieta.id == dieta_id).first()

def create_dieta(db: Session, dieta: DietaCreate):
    nueva_dieta = Dieta(**dieta.dict())
    db.add(nueva_dieta)
    db.commit()
    db.refresh(nueva_dieta)
    return nueva_dieta

def update_dieta(db: Session, dieta_id: int, dieta: DietaUpdate):
    db_dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not db_dieta:
        return None
    for key, value in dieta.dict(exclude_unset=True).items():
        setattr(db_dieta, key, value)
    db.commit()
    db.refresh(db_dieta)
    return db_dieta

def delete_dieta(db: Session, dieta_id: int):
    db_dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not db_dieta:
        return False
    db.delete(db_dieta)
    db.commit()
    return True
