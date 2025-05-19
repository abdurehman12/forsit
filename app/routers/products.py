from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter()

@router.get("/", summary="List all products")
def get_products():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, category, price FROM products")
                rows = cur.fetchall()
                products = [
                    {"id": row[0], "name": row[1], "category": row[2], "price": float(row[3])}
                    for row in rows
                ]
                return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", summary="Get a product by ID")
def get_product(product_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, category, price FROM products WHERE id = %s", (product_id,))
                row = cur.fetchone()
                if row:
                    return {"id": row[0], "name": row[1], "category": row[2], "price": float(row[3])}
                raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", summary="Create a new product")
def create_product(product: dict):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO products (name, category, price) VALUES (%s, %s, %s) RETURNING id",
                    (product["name"], product["category"], product["price"])
                )
                new_id = cur.fetchone()[0]
                conn.commit()
                return {"id": new_id, **product}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
