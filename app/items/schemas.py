from pydantic import BaseModel, Field
from typing import Annotated


class ItemCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    price: Annotated[float, Field(gt=0)]
    sku: Annotated[str, Field(min_length=5, max_length=5)]