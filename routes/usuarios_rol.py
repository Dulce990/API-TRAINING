# routes/usuarios_roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from crud.usuarios_rol import get_usuarios_by_rol

router = APIRouter()

@router.get("/usuarios/rol/{rol_name}")
def usuarios_por_rol(rol_name: str, db: Session = Depends(get_db)):
    usuarios = get_usuarios_by_rol(db, rol_name)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese rol")
    return usuarios

@router.get("/{rol_name}")
def usuarios_por_rol_l(rol_name: str, db: Session = Depends(get_db)):
    usuarios = get_usuarios_by_rol(db, rol_name)
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con el rol especificado")
    return usuarios