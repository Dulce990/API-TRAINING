# crud/usuarios_roles.py
from sqlalchemy.orm import Session
from models.usuarios import Usuario
from models.roles_usuario import RolUsuario
from models.roles import Rol

def get_usuarios_by_rol(db: Session, rol_name: str):
    """
    Retorna la lista de usuarios que tengan asignado el rol indicado y estatus activo.
    """
    usuarios = (
        db.query(Usuario)
        .join(RolUsuario, Usuario.id == RolUsuario.usuario_id)
        .join(Rol, Rol.id == RolUsuario.rol_id)
        .filter(Rol.nombre == rol_name, RolUsuario.estatus == 1)
        .all()
    )
    return usuarios
