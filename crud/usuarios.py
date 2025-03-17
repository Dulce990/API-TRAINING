from sqlalchemy.orm import Session
import bcrypt
from models.usuarios import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioUpdate

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.correo_electronico == email).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
    
    # Crear el nuevo usuario con la contraseña hasheada
    nuevo_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        correo_electronico=usuario.correo_electronico,
        contrasena=hashed_password.decode('utf-8'),  # Convertir bytes a string
        numero_telefonico_movil=usuario.numero_telefonico_movil,
        estatus=usuario.estatus
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        return None
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        return False
    db.delete(db_usuario)
    db.commit()
    return True
