from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from models.dietas import Dieta  # Asegúrate de que la importación es correcta
from schemas.dietas import DietaCreate, DietaUpdate, DietaInDB  # Importa también el modelo de respuesta correcto
from crud.dietas import get_dietas
router = APIRouter(prefix="/dietas", tags=["Dietas"])
from crud.dietas import get_dietas

# Configuración del token
SECRET_KEY = "mysecretkey"  # Cámbialo por algo más seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bearer_scheme = HTTPBearer()

# Crear token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

# Obtener todas las dietas
@router.get("/", response_model=list[DietaInDB])
def get_dietas_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    dietas = get_dietas(db, skip=skip, limit=limit)
    return dietas

# Obtener una dieta por ID
@router.get("/{dieta_id}", response_model=DietaInDB)
def get_dieta(dieta_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    return dieta

# Crear una nueva dieta
@router.post("/", response_model=DietaInDB)
def create_dieta(dieta: DietaCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    nueva_dieta = Dieta(**dieta.dict())
    db.add(nueva_dieta)
    db.commit()
    db.refresh(nueva_dieta)
    return nueva_dieta

# Actualizar una dieta por ID
@router.put("/{dieta_id}", response_model=DietaInDB)
def update_dieta(dieta_id: int, dieta: DietaUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
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
def delete_dieta(dieta_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    db_dieta = db.query(Dieta).filter(Dieta.id == dieta_id).first()
    if not db_dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")

    db.delete(db_dieta)
    db.commit()
    return {"message": "Dieta eliminada correctamente"}

# Obtener dietas por usuario
@router.get("/usuario/{usuario_id}", response_model=list[DietaInDB])
def get_dietas_by_usuario(usuario_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return db.query(Dieta).filter(Dieta.user_id == usuario_id).offset(skip).limit(limit).all()
