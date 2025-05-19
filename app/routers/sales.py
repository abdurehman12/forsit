from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.database import get_db_connection

router = APIRouter()

@router.get("/", summary="List all sales")
def list_sales():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, product_id, quantity, total_amount, sale_date FROM sales")
                rows = cur.fetchall()
                sales = [
                    {
                        "id": row[0],
                        "product_id": row[1],
                        "quantity": row[2],
                        "total_amount": float(row[3]),
                        "sale_date": row[4].isoformat()
                    }
                    for row in rows
                ]
                return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", summary="Total sales within a date range")
def sales_summary(start_date: str = Query(...), end_date: str = Query(...)):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*), SUM(total_amount)
                    FROM sales
                    WHERE sale_date BETWEEN %s AND %s
                    """,
                    (start_date, end_date)
                )
                result = cur.fetchone()
                return {"total_sales": result[0], "total_revenue": float(result[1] or 0)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_product/{product_id}", summary="Get sales for a specific product")
def get_sales_by_product(product_id: int):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, product_id, quantity, total_amount, sale_date
                    FROM sales
                    WHERE product_id = %s
                """, (product_id,))
                rows = cur.fetchall()
                sales = [
                    {
                        "id": row[0],
                        "product_id": row[1],
                        "quantity": row[2],
                        "total_amount": float(row[3]),
                        "sale_date": row[4].isoformat()
                    }
                    for row in rows
                ]
                return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

