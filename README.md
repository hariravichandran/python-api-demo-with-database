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

2. Create Demo Databases

Run the setup script once to generate sample data:

python setup_db.py


This will create:

customer.db (customers)

product.db (products)

order.db (orders)

order_line.db (order lines)

3. Start the API
python app.py


The API runs on http://127.0.0.1:8050

4. Try it Out

JSON output

http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=json


CSV download

http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=csv


Excel download

http://127.0.0.1:8050/report/customer-orders?customer_id=1&format=excel


No orders? You’ll get an empty dataset with headers.

5. Diagrams

GitHub natively renders Mermaid diagrams:

Database Schema
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

API & Data Flow
```mermaid
flowchart LR
    subgraph Client["Client"]
      C1["GET /report/customer-orders?customer_id=...&format=json|csv|excel"]
    end

    C1 --> API

    subgraph API["FastAPI Aggregation Service"]
      API["/report/customer-orders
      • Joins across 4 DBs via ATTACH
      • Exports: JSON / CSV / Excel"]
    end

    subgraph DBS["4 SQLite Databases"]
      D1[/"customer.db"/]
      D2[/"order.db"/]
      D3[/"order_line.db"/]
      D4[/"product.db"/]
    end

    API --> D1
    API --> D2
    API --> D3
    API --> D4
```


---

