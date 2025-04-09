from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from models.dietas import Dieta
from schemas.dietas import DietaCreate, DietaUpdate, DietaInDB
from crud.dietas import get_dietas, get_dieta_by_id, create_dieta, update_dieta, delete_dieta

# Configuración del token
SECRET_KEY = "mysecretkey"  # Cámbialo por una clave más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bearer_scheme = HTTPBearer()

# Función para generar un token de acceso
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función que verifica que el token sea válido
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

# Se inyecta la verificación del token a nivel de router
router = APIRouter(
    prefix="/dietas",
    tags=["Dietas"],
    dependencies=[Depends(verify_token)]
)

# Obtener todas las dietas
@router.get("/", response_model=list[DietaInDB])
def get_dietas_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    dietas = get_dietas(db, skip=skip, limit=limit)
    return dietas

# Obtener una dieta por ID
@router.get("/{dieta_id}", response_model=DietaInDB)
def get_dieta(dieta_id: int, db: Session = Depends(get_db)):
    dieta = get_dieta_by_id(db, dieta_id)
    if not dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    return dieta

# Crear una nueva dieta
@router.post("/", response_model=DietaInDB, status_code=status.HTTP_201_CREATED)
def create_dieta_endpoint(dieta: DietaCreate, db: Session = Depends(get_db)):
    nueva_dieta = create_dieta(db, dieta)
    return nueva_dieta

# Actualizar una dieta por ID
@router.put("/{dieta_id}", response_model=DietaInDB)
def update_dieta_endpoint(dieta_id: int, dieta: DietaUpdate, db: Session = Depends(get_db)):
    db_dieta = update_dieta(db, dieta_id, dieta)
    if not db_dieta:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    return db_dieta

# Eliminar una dieta por ID
@router.delete("/{dieta_id}")
def delete_dieta_endpoint(dieta_id: int, db: Session = Depends(get_db)):
    result = delete_dieta(db, dieta_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dieta no encontrada")
    return {"message": "Dieta eliminada correctamente"}
