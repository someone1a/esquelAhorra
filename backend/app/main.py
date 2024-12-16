from fastapi import FastAPI
from app.api.v1 import products, prices, users

app = FastAPI()

# Include routes
app.include_router(products.router, prefix="/api/v1/products")
app.include_router(prices.router, prefix="/api/v1/prices")
app.include_router(users.router, prefix="/api/v1/users")
