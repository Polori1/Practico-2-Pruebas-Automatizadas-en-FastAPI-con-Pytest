from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from app.database import FAKE_DB
from app.items.schemas import ItemCreate
from app.items.dependencies import get_admin_token


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/")
def read_items():
    return FAKE_DB


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    token: Annotated[str, Depends(get_admin_token)]
):
    new_item = {
        "id": len(FAKE_DB) + 1,
        **item.model_dump()
    }

    FAKE_DB.append(new_item)

    return new_item


@router.get("/{item_id}")
def get_item(item_id: int):
    for item in FAKE_DB:
        if item["id"] == item_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Item no encontrado"
    )