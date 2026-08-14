from pydantic import BaseModel, Field
from typing import Annotated


class ProductoCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    price: Annotated[float, Field(gt=0)]