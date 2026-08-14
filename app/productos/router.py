from fastapi import APIRouter

from app.database import db_productos


router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)


@router.get("/")
def listar_productos():
    return db_productos