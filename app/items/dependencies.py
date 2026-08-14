from fastapi import Query, HTTPException
from typing import Annotated


def get_admin_token(
    token: Annotated[str | None, Query()] = None
):
    if token != "nivel-intermedio-2026":
        raise HTTPException(
            status_code=401,
            detail="No autorizado"
        )

    return token