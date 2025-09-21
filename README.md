# Demo Aggregation API (Customer–Orders)

This project demonstrates a small **Python REST API** that aggregates across
four separate SQLite databases (`customer.db`, `product.db`, `order.db`, `order_line.db`)
to provide customer order reports in **JSON**, **CSV**, or **Excel**.

---

## 1. Setup

Clone the repo and install dependencies (Python 3.10+ recommended):

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Create Demo Databases

Run the setup script once to generate sample data:

python setup_db.py


This will create:

customer.db (customers)

product.db (products)

order.db (orders)

order_line.db (order lines)

## 3. Start the API
python app.py


The API runs on http://127.0.0.1:8050

## 4. Try it Out

## JSON output
http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=json

## CSV download
http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=csv

## Excel download
http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=excel

No orders? You’ll get an empty dataset with headers.

## 5. Diagrams
## Database Schema
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_LINE : contains
    PRODUCT ||--o{ ORDER_LINE : "is referenced by"

    CUSTOMER {
      INTEGER customer_id PK
      TEXT    name
      TEXT    address
    }

    ORDER {
      INTEGER order_id PK
      INTEGER customer_id FK
      TEXT    order_date
      REAL    order_total
    }

    ORDER_LINE {
      INTEGER order_line_id PK
      INTEGER order_id   FK
      INTEGER product_id FK
      INTEGER quantity
      REAL    line_total
    }

    PRODUCT {
      INTEGER product_id PK
      TEXT    product_name
      INTEGER quantity
      REAL    price
    }
```

## 6. API & Data Flow

```mermaid
flowchart LR
  subgraph Client["Client"]
    req["curl / browser / app\n→ GET /report/customer-orders?..."]
  end

  req --> apiSvc["FastAPI Aggregation Service\n127.0.0.1:8050\n• Joins across 4 DBs\n• Exports JSON / CSV / Excel"]

  subgraph DBs["SQLite Databases"]
    dbCust[/"customer.db"/]
    dbOrd[/"order.db"/]
    dbOL[/"order_line.db"/]
    dbProd[/"product.db"/]
  end

  apiSvc --> dbCust
  apiSvc --> dbOrd
  apiSvc --> dbOL
  apiSvc --> dbProd

  apiSvc --> respJSON[(JSON)]
  apiSvc --> respCSV[(CSV)]
  apiSvc --> respXLSX[(Excel)]
```

## 7. 🚀 Live Demo (render.com)

The API is deployed on **Render (free tier)**:  
👉 https://python-api-demo-with-database.onrender.com

⚠️ **Note:** On the free tier, the instance “sleeps” after ~15 minutes of inactivity.  
When you visit a link, it may take **30–60 seconds** to spin back up before the response appears.

### Interactive Documentation
- **Swagger UI:** [https://python-api-demo-with-database.onrender.com/docs](https://python-api-demo-with-database.onrender.com/docs)  
    #### Swagger UI - Landing Screen
    ![Swagger UI Screenshot](sample-output/Swagger%20UI%20Screenshot%201.png)
    #### Swagger UI - Endpoint #1 - Health
    ![Swagger UI Endpoint 1 - Health](sample-output/Swagger%20UI%20Endpoint%201%20-%20Health.png)
    #### Swagger UI - Endpoint #2 - Report Customer Orders
    ![Swagger UI Endpoint 2 - Report Customer Orders Part 1](sample-output/Swagger%20UI%20Endpoint%202%20-%20Report%20Customer%20Orders%20Part%201.png)
    ![Swagger UI Endpoint 2 - Report Customer Orders Part 2](sample-output/Swagger%20UI%20Endpoint%202%20-%20Report%20Customer%20Orders%20Part%202.png)

- **ReDoc:** [https://python-api-demo-with-database.onrender.com/redoc](https://python-api-demo-with-database.onrender.com/redoc)
    ![API Redoc](sample-output/API%20Redoc.png)
  
- **OpenAPI JSON:** [https://python-api-demo-with-database.onrender.com/openapi.json](https://python-api-demo-with-database.onrender.com/openapi.json)
    Expected Result: Output JSON [should look like this.](sample-output/openapi_spec.json)

- **Health check:** [https://python-api-demo-with-database.onrender.com/health](https://python-api-demo-with-database.onrender.com/health)
    For the health check you should see: `{"status":"ok"}` as a response. This means the API is working as intended. If not, then there is an issue. 

### Example Endpoints
- JSON (customer 1):  
  [https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=json](https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=json)

    Response (Pretty Print) should yield these results:
    ```json
    [
      {
        "product_id": 10,
        "order_date": "2025-09-14",
        "product_description": "Widget A",
        "quantity": 2,
        "price": 9.99,
        "total_amount": 19.98
      },
      {
        "product_id": 11,
        "order_date": "2025-09-14",
        "product_description": "Widget B",
        "quantity": 1,
        "price": 19.5,
        "total_amount": 19.5
      },
      {
        "product_id": 12,
        "order_date": "2025-09-14",
        "product_description": "Gadget C",
        "quantity": 1,
        "price": 49,
        "total_amount": 49
      }
    ]
    ```

- CSV (customer 1):  
  [https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=csv](https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=csv)

    Output CSV should look like [this example CSV file](sample-output/customer_1_orders.csv).

- Excel (customer 1):  
  [https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=excel](https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=1&format=excel)

    Output Excel file should look like [this example XLSX file](sample-output/customer_1_orders.xlsx).

- No orders (customer 999):  
  [https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=999&format=json](https://python-api-demo-with-database.onrender.com/report/customer-orders?customer_id=999&format=json)

    Output JSON should be empty, i.e., you should see `[]` as the response.

## 8. 📦 Local Development

```bash
# Clone repo and install dependencies
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create demo databases
python setup_db.py

# Run API (localhost:8050 by default)
python app.py
```
