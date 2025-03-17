from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from models.dietas import Dieta  # Asegúrate de que la importación es correcta
from schemas.dietas import DietaCreate, DietaUpdate, DietaInDB  # Importa también el modelo de respuesta correcto

router = APIRouter(prefix="/dietas", tags=["Dietas"])

# Obtener todas las dietas
@router.get("/", response_model=list[DietaInDB])  # Asegúrate de usar DietaInDB para las respuestas
def get_dietas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Dieta).offset(skip).limit(limit).all()

# Obtener una dieta por ID
@router.get("/{dieta_id}", response_model=DietaInDB)  # También aquí usa DietaInDB
def get_dieta(dieta_id: int, db: Session = Depends(get_db)):
    dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    return dieta

# Crear una nueva dieta
@router.post("/", response_model=DietaInDB)
def create_dieta(dieta: DietaCreate, db: Session = Depends(get_db)):
    nueva_dieta = Dieta(**dieta.dict())
    db.add(nueva_dieta)
    db.commit()
    db.refresh(nueva_dieta)
    return nueva_dieta

# Actualizar una dieta por ID
@router.put("/{dieta_id}", response_model=DietaInDB)
def update_dieta(dieta_id: int, dieta: DietaUpdate, db: Session = Depends(get_db)):
    db_dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not db_dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    
    for key, value in dieta.dict(exclude_unset=True).items():
        setattr(db_dieta, key, value)

    db.commit()
    db.refresh(db_dieta)
    return db_dieta

# Eliminar una dieta por ID
@router.delete("/{dieta_id}")
def delete_dieta(dieta_id: int, db: Session = Depends(get_db)):
    db_dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not db_dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")

    db.delete(db_dieta)
    db.commit()
    return {"message": "Dieta eliminada correctamente"}
