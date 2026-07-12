# app/main.py
from fastapi import FastAPI
from api.routes import product

app = FastAPI(title="Shop API")
app.include_router(product.router)