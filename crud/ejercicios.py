from sqlalchemy.orm import Session, joinedload
from models.ejercicios import Ejercicio
from schemas.ejercicios import EjercicioCreate, EjercicioUpdate

def get_ejercicios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ejercicio).options(joinedload(Ejercicio.usuario)).offset(skip).limit(limit).all()

def get_ejercicio_by_id(db: Session, ejercicio_id: int):
    return db.query(Ejercicio).options(joinedload(Ejercicio.usuario)).filter(Ejercicio.id == ejercicio_id).first()

def create_ejercicio(db: Session, ejercicio: EjercicioCreate):
    nuevo_ejercicio = Ejercicio(**ejercicio.dict())
    db.add(nuevo_ejercicio)
    db.commit()
    db.refresh(nuevo_ejercicio)
    return nuevo_ejercicio


def update_ejercicio(db: Session, ejercicio_id: int, ejercicio: EjercicioUpdate):
    db_ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    if not db_ejercicio:
        return None
    for key, value in ejercicio.dict(exclude_unset=True).items():
        setattr(db_ejercicio, key, value)
    db.commit()
    db.refresh(db_ejercicio)
    return db_ejercicio

def delete_ejercicio(db: Session, ejercicio_id: int):
    db_ejercicio = db.query(Ejercicio).filter(Ejercicio.id == ejercicio_id).first()
    if not db_ejercicio:
        return False
    db.delete(db_ejercicio)
    db.commit()
    return True
