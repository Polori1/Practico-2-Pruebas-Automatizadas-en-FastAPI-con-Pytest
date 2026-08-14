from pydantic import BaseModel, Field
from typing import Annotated


class UsuarioCreate(BaseModel):
    username: Annotated[str, Field(min_length=5)]
    edad: Annotated[int, Field(ge=18)]