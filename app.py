#!/usr/bin/env python3
# Simple aggregation API on port 8050.
# Endpoints:
#   GET /report/customer-orders?customer_id=1&format=json|csv|excel
#
# Returns columns: product_id, order_date, product_description, quantity, price, total_amount
#
# Dependencies: fastapi, uvicorn, pandas, openpyxl
#   pip install fastapi uvicorn pandas openpyxl

import io, sqlite3
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.responses import JSONResponse, StreamingResponse, PlainTextResponse
import pandas as pd
import uvicorn

DBS = {
    "cust": "customer.db",
    "prod": "product.db",
    "ord":  "order.db",
    "ol":   "order_line.db",
}

app = FastAPI(title="Demo Aggregation API")

def fetch_customer_orders(customer_id: int) -> pd.DataFrame:
    # Use an in-memory SQLite connection and ATTACH the 4 DBs so we can JOIN across files.
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    for alias, path in DBS.items():
        cur.execute(f"ATTACH DATABASE '{path}' AS {alias};")

    sql = """
    SELECT
        p.product_id                                      AS product_id,
        o.order_date                                      AS order_date,
        p.product_name                                    AS product_description,
        ol.quantity                                       AS quantity,
        p.price                                           AS price,
        ROUND(ol.quantity * p.price, 2)                   AS total_amount
    FROM cust.customers c
    JOIN ord.orders o       ON o.customer_id = c.customer_id
    JOIN ol.order_lines ol  ON ol.order_id   = o.order_id
    JOIN prod.products p    ON p.product_id  = ol.product_id
    WHERE c.customer_id = ?
    ORDER BY o.order_date, p.product_id;
    """
    df = pd.read_sql_query(sql, conn, params=(customer_id,))
    conn.close()
    return df

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/report/customer-orders")
def customer_orders_report(
    customer_id: int = Query(..., description="Customer number"),
    format: str = Query("json", pattern="^(json|csv|excel)$", description="json|csv|excel")
):
    df = fetch_customer_orders(customer_id)

    if format == "json":
        # Return empty list if no rows
        return JSONResponse(df.to_dict(orient="records"))

    if format == "csv":
        # Return CSV with headers even if empty
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        return StreamingResponse(io.BytesIO(csv_bytes),
                                 media_type="text/csv",
                                 headers={"Content-Disposition": f'attachment; filename="customer_{customer_id}_orders.csv"'})

    if format == "excel":
        # Return Excel with headers even if empty
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as xw:
            df.to_excel(xw, index=False, sheet_name="orders")
        buf.seek(0)
        return StreamingResponse(buf,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="customer_{customer_id}_orders.xlsx"'})

    # Shouldn’t get here because of the Query pattern
    raise HTTPException(status_code=400, detail="Unsupported format")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)
