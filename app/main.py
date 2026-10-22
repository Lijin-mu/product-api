
from fastapi import FastAPI

from app.routers.products import router as products_router
from app.routers.auth import router as auth_router

app = FastAPI(
    title="Product API",
    version="1.0.0",
)

app.include_router(products_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Product API is running"}
