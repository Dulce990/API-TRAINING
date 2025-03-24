from sqlalchemy.orm import Session
from models.indicadores_nutricionales import IndicadorNutricional
from schemas.indicadores_nutricionales import IndicadorNutricionalCreate, IndicadorNutricionalUpdate

def get_indicadores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(IndicadorNutricional).offset(skip).limit(limit).all()

def get_indicador_by_id(db: Session, indicador_id: int):
    return db.query(IndicadorNutricional).filter(IndicadorNutricional.id == indicador_id).first()

def create_indicador(db: Session, indicador: IndicadorNutricionalCreate):
    nuevo_indicador = IndicadorNutricional(**indicador.dict())
    db.add(nuevo_indicador)
    db.commit()
    db.refresh(nuevo_indicador)
    return nuevo_indicador

def update_indicador(db: Session, indicador_id: int, indicador: IndicadorNutricionalUpdate):
    db_indicador = db.query(IndicadorNutricional).filter(IndicadorNutricional.id == indicador_id).first()
    if not db_indicador:
        return None
    for key, value in indicador.dict(exclude_unset=True).items():
        setattr(db_indicador, key, value)
    db.commit()
    db.refresh(db_indicador)
    return db_indicador

def delete_indicador(db: Session, indicador_id: int):
    db_indicador = db.query(IndicadorNutricional).filter(IndicadorNutricional.id == indicador_id).first()
    if not db_indicador:
        return False
    db.delete(db_indicador)
    db.commit()
    return True
