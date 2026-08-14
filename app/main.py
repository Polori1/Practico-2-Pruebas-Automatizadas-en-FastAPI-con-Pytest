from fastapi import FastAPI, Depends

from app.items.router import router as items_router
from app.items.dependencies import get_admin_token as items_token

from app.usuarios.router import router as usuarios_router

from app.productos.router import router as productos_router
from app.productos.dependencies import get_admin_token as productos_token


app = FastAPI()


app.include_router(
    items_router,
    dependencies=[Depends(items_token)]
)

app.include_router(usuarios_router)

app.include_router(
    productos_router,
    dependencies=[Depends(productos_token)]
)