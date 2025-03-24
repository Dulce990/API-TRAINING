from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.db import get_db
from crud.programas_saludables import (
    get_programas_saludables, get_programa_saludable_by_id, create_programa_saludable, update_programa_saludable, delete_programa_saludable
)
from schemas.programas_saludables import ProgramaSaludableCreate, ProgramaSaludableUpdate, ProgramaSaludableResponse

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

@router.get("/programas_saludables", response_model=list[ProgramaSaludableResponse])
def read_programas_saludables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return get_programas_saludables(db, skip=skip, limit=limit)

@router.get("/programas_saludables/{programa_id}", response_model=ProgramaSaludableResponse)
def read_programa_saludable(programa_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    programa = get_programa_saludable_by_id(db, programa_id)
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa

@router.post("/programas_saludables", response_model=ProgramaSaludableResponse)
def create_programa(programa: ProgramaSaludableCreate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    return create_programa_saludable(db, programa)

@router.put("/programas_saludables/{programa_id}", response_model=ProgramaSaludableResponse)
def update_programa(programa_id: int, programa: ProgramaSaludableUpdate, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    updated_programa = update_programa_saludable(db, programa_id, programa)
    if not updated_programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return updated_programa

@router.delete("/programas_saludables/{programa_id}")
def delete_programa(programa_id: int, db: Session = Depends(get_db), user_id: str = Depends(verify_token)):
    success = delete_programa_saludable(db, programa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return {"message": "Programa eliminado correctamente"}
