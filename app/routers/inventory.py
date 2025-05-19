from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter()

LOW_STOCK_THRESHOLD = 5

@router.get("/", summary="View all inventory")
def get_inventory():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, product_id, stock_level FROM inventory")
                rows = cur.fetchall()
                inventory = [
                    {"id": row[0], "product_id": row[1], "stock_level": row[2]}
                    for row in rows
                ]
                return inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/low_stock", summary="List low stock items")
def low_stock():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, product_id, stock_level FROM inventory WHERE stock_level <= %s", (LOW_STOCK_THRESHOLD,))
                rows = cur.fetchall()
                inventory = [
                    {"id": row[0], "product_id": row[1], "stock_level": row[2]}
                    for row in rows
                ]
                return inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{product_id}", summary="Update stock level for a product")
def update_stock(product_id: int, new_stock: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE inventory SET stock_level = %s, updated_at = NOW() WHERE product_id = %s RETURNING id, stock_level", (new_stock, product_id))
                row = cur.fetchone()
                if row:
                    conn.commit()
                    return {"message": "Stock updated", "inventory": {"id": row[0], "product_id": product_id, "stock_level": row[1]}}
                raise HTTPException(status_code=404, detail="Product not found in inventory")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
