
import asyncio
from fastmcp import FastMCP

from store_sim_mcp.db import CUSTOMERS_TABLE, ORDERS_TABLE, PRODUCTS_TABLE


mcp = FastMCP("ecom")

@mcp.tool
async def get_customer_info(customer_id: str) -> str:
    """
    Search for a customer by their ID and return their information.
    """

    customer = CUSTOMERS_TABLE.get(customer_id)
    if customer is None:
        return f"Customer with ID '{customer_id}' not found."
    return str(customer)

@mcp.tool
async def get_order_info(order_id: str) -> str:
    """
    Search for an order by its ID and return its information.
    """
    await asyncio.sleep(1)  # Simulate a delay for fetching order info

    order = ORDERS_TABLE.get(order_id)
    if order is None:
        return f"Order with ID '{order_id}' not found."
    
    items = [PRODUCTS_TABLE[item_id]["name"] for item_id in order["items"] if item_id in PRODUCTS_TABLE]

    return (
        f"Order ID: {order_id}\n"
        f"Customer ID: {order['customer_id']}\n"
        f"Date: {order['date']}\n"
        f"Status: {order['status']}\n"
        f"Total: ${order['total']:.2f}\n"
        f"Items: {', '.join(items)}"
    )

@mcp.tool()
async def check_inventory(product_name: str) -> str:
    """Search inventory for a product by product name."""
    await asyncio.sleep(1)
    matches = []
    for sku, product in PRODUCTS_TABLE.items():
        if product_name.lower() in product["name"].lower():
            matches.append(
                f"{product['name']} (SKU: {sku}) — Stock: {product['stock']}"
            )
    return "\n".join(matches) if matches else "No matching products found."

@mcp.tool()
async def get_customer_ids_by_name(customer_name: str) -> list[str]:
    """Get customer IDs by using a customer's full name"""
    await asyncio.sleep(1)
    return [
        cust_id
        for cust_id, info in CUSTOMERS_TABLE.items()
        if info.get("name") == customer_name
    ]

@mcp.tool()
async def get_orders_by_customer_id(
    customer_id: str,
) -> dict[str, dict[str, str]]:
    """Get orders by customer ID"""
    await asyncio.sleep(1)
    return {
        order_id: order
        for order_id, order in ORDERS_TABLE.items()
        if order.get("customer_id") == customer_id
    }


def run(port: int = 8000):
    mcp.run("streamable-http", port=port)

if __name__ == "__main__":
    run()