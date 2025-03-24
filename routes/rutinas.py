from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.rutinas import (
    get_rutinas, get_rutina_by_id, create_rutina, update_rutina, delete_rutina
)
from schemas.rutinas import RutinaCreate, RutinaUpdate, RutinaResponse

router = APIRouter()

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


@router.get("/rutinas", response_model=list[RutinaResponse])
def read_rutinas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return get_rutinas(db, skip=skip, limit=limit)

@router.get("/rutinas/{rutina_id}", response_model=RutinaResponse)
def read_rutina(rutina_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    rutina = get_rutina_by_id(db, rutina_id)
    if not rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return rutina

@router.post("/rutinas", response_model=RutinaResponse)
def create_rutina_endpoint(rutina: RutinaCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return create_rutina(db, rutina)

@router.put("/rutinas/{rutina_id}", response_model=RutinaResponse)
def update_rutina_endpoint(rutina_id: int, rutina: RutinaUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    updated_rutina = update_rutina(db, rutina_id, rutina)
    if not updated_rutina:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return updated_rutina

@router.delete("/rutinas/{rutina_id}")
def delete_rutina_endpoint(rutina_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    success = delete_rutina(db, rutina_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return {"message": "Rutina eliminada correctamente"}
