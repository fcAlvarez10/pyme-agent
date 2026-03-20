import sqlite3
import json
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("PymeBackend")

def get_db_connection():
    # Attempt to resolve the database path regardless of where the script is called from
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "pyme.db")
    return sqlite3.connect(db_path)

def get_memory_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "memory.json")

@mcp.tool()
def get_sales_data() -> str:
    """Get sales data for products from the database. Use this to determine which product to promote."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, sales_last_month, price, stock, category FROM products ORDER BY sales_last_month DESC")
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            result.append({
                "product": row[0],
                "sales_last_month": row[1],
                "price": row[2],
                "stock": row[3],
                "category": row[4]
            })
        return json.dumps(result)
    except Exception as e:
        return f"Error accediendo a la base de datos de ventas: {e}"

@mcp.tool()
def get_manager_preferences() -> str:
    """Get the manager's preferences and business rules for the campaign."""
    try:
        memory_path = get_memory_path()
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data)
    except Exception as e:
        return f"Error leyendo la memoria episódica: {e}"

@mcp.tool()
def calculate_budget(product_name: str, discount_percentage: float) -> str:
    """
    Calculate the projected campaign budget based on the product and discount.
    If the discount violates the company policy (e.g. > 20%), it will return an error.
    """
    if discount_percentage > 20:
        return (
            "Error de política corporativa: El descuento máximo permitido es del 20%. "
            f"Un descuento del {discount_percentage}% genera un margen negativo inaceptable para '{product_name}'. "
            "Reflexiona sobre tu estrategia y vuelve a llamar a la herramienta con un descuento válido."
        )
    
    # Simple simulated logic for budget
    base_budget = 500.0
    # Additional budget if discount is lower, saving margin
    savings = 20 - discount_percentage
    final_budget = base_budget + (savings * 10)
    
    return json.dumps({
        "status": "success",
        "product": product_name,
        "discount_applied": discount_percentage,
        "approved_budget": final_budget,
        "message": "Presupuesto calculado y aprobado correctamente."
    })

if __name__ == "__main__":
    # Run the server over SSE on internal port 8001
    mcp.settings.host = "127.0.0.1"
    mcp.settings.port = 8001
    mcp.run(transport="sse")
