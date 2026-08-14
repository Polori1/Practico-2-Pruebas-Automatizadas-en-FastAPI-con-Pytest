from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import Annotated

from app.database import db_usuarios
from app.usuarios.schemas import UsuarioCreate


router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    for usuario_existente in db_usuarios:
        if usuario_existente["username"] == usuario.username:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )

    nuevo_usuario = {
        "id": len(db_usuarios) + 1,
        "username": usuario.username,
        "edad": usuario.edad
    }

    db_usuarios.append(nuevo_usuario)

    return nuevo_usuario


@router.get("/{user_id}")
def obtener_usuario(
    user_id: Annotated[int, Path(gt=0)],
    search: Annotated[str, Query()] = "general"
):
    for usuario in db_usuarios:
        if usuario["id"] == user_id:
            return {
                **usuario,
                "search": search
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )