from fastapi import FastAPI
from app.routers import products, sales, inventory
from app.startup import run_all_migrations

app = FastAPI()

run_all_migrations()

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

@app.get("/")
def root():
    return {"message": "E-commerce Admin API is up!"}
