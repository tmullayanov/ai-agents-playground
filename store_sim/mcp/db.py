"""
Simulation of DB
"""

CUSTOMERS_TABLE = {
    "cust#1": {
        "name": "Alice Alisson",
        "email": "alice@alice.com",
        "phone": "11-911",
    },
    "cust#2": {
        "name": "Bob Bobster",
        "email": "bob@bob.com",
        "phone": "11-922",
    },
}

ORDERS_TABLE = {
    "ORD1001": {
        "customer_id": "cust#1",
        "date": "2024-04-01",
        "status": "Shipped",
        "total": 89.99,
        "items": ["SKU100", "SKU200"],
    },
    "ORD1015": {
        "customer_id": "cust#1",
        "date": "2024-05-17",
        "status": "Processing",
        "total": 45.50,
        "items": ["SKU300"],
    },
    "ORD1022": {
        "customer_id": "cust#2",
        "date": "2024-06-04",
        "status": "Delivered",
        "total": 120.00,
        "items": ["SKU100", "SKU100"],
    },
}

PRODUCTS_TABLE = {
    "SKU100": {"name": "Wireless Mouse", "price": 29.99, "stock": 42},
    "SKU200": {"name": "Keyboard", "price": 59.99, "stock": 18},
    "SKU300": {"name": "USB-C Cable", "price": 15.50, "stock": 77},
}