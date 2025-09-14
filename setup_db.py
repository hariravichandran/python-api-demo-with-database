#!/usr/bin/env python3
# Creates 4 separate SQLite DBs with minimal demo data.
import sqlite3, os, datetime as dt

SCHEMAS = {
    "customer.db": """
        CREATE TABLE IF NOT EXISTS customers(
          customer_id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          address TEXT NOT NULL
        );
    """,
    "product.db": """
        CREATE TABLE IF NOT EXISTS products(
          product_id INTEGER PRIMARY KEY,
          product_name TEXT NOT NULL,
          quantity INTEGER NOT NULL,
          price REAL NOT NULL
        );
    """,
    "order.db": """
        CREATE TABLE IF NOT EXISTS orders(
          order_id INTEGER PRIMARY KEY,
          customer_id INTEGER NOT NULL,
          order_date TEXT NOT NULL,
          order_total REAL NOT NULL
        );
    """,
    "order_line.db": """
        CREATE TABLE IF NOT EXISTS order_lines(
          order_line_id INTEGER PRIMARY KEY,
          order_id INTEGER NOT NULL,
          product_id INTEGER NOT NULL,
          quantity INTEGER NOT NULL,
          line_total REAL NOT NULL
        );
    """
}

def init_db(path, ddl):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(ddl)
    conn.commit()
    conn.close()

def seed():
    # Customers
    conn = sqlite3.connect("customer.db")
    c = conn.cursor()
    c.execute("DELETE FROM customers;")
    c.executemany("INSERT INTO customers VALUES(?,?,?)", [
        (1, "Alice Adams", "101 Main St, Springfield"),
        (2, "Bob Brown",  "202 Oak Ave, Shelbyville"),
    ])
    conn.commit(); conn.close()

    # Products
    conn = sqlite3.connect("product.db")
    p = conn.cursor()
    p.execute("DELETE FROM products;")
    p.executemany("INSERT INTO products VALUES(?,?,?,?)", [
        (10, "Widget A", 100, 9.99),
        (11, "Widget B",  50, 19.5),
        (12, "Gadget C",  20, 49.0),
    ])
    conn.commit(); conn.close()

    # Orders
    today = dt.date.today().isoformat()
    conn = sqlite3.connect("order.db")
    o = conn.cursor()
    o.execute("DELETE FROM orders;")
    o.executemany("INSERT INTO orders VALUES(?,?,?,?)", [
        (1001, 1, today,  9.99*2 + 19.5),   # Alice
        (1002, 1, today,  49.0),           # Alice
        (1003, 2, today,  19.5*2),         # Bob
    ])
    conn.commit(); conn.close()

    # Order lines
    conn = sqlite3.connect("order_line.db")
    ol = conn.cursor()
    ol.execute("DELETE FROM order_lines;")
    ol.executemany("INSERT INTO order_lines VALUES(?,?,?,?,?)", [
        (1, 1001, 10, 2,  9.99*2),  # 2 x Widget A
        (2, 1001, 11, 1,  19.5),    # 1 x Widget B
        (3, 1002, 12, 1,  49.0),    # 1 x Gadget C
        (4, 1003, 11, 2,  19.5*2),  # 2 x Widget B
    ])
    conn.commit(); conn.close()

if __name__ == "__main__":
    for path, ddl in SCHEMAS.items():
        # re-create files for a clean demo
        if not os.path.exists(path):
            open(path, "w").close()
        init_db(path, ddl)
    seed()
    print("✅ Created customer.db, product.db, order.db, order_line.db with sample data.")
