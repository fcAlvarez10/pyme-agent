import sqlite3
import os

def setup_db():
    db_path = "pyme.db"
    
    # Remove existing db if needed
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            sales_last_month INTEGER NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # Insert sample data with more storytelling potential
    products = [
        (1, "Botas Industriales con Punta de Acero", 150, 180000.0, 500, "Calzado de Trabajo"),
        (2, "Zapatos Formales Oxford de Cuero", 300, 150000.0, 400, "Calzado Formal"),
        (3, "Botines Chelsea para Mujer", 120, 175000.0, 200, "Calzado Casual"),
        (4, "Zapatos Escolares Negros", 450, 95000.0, 1000, "Calzado Escolar"),
        (5, "Botas de Cuero para Senderismo", 80, 210000.0, 150, "Calzado Deportivo")
    ]
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", products)
    
    conn.commit()
    conn.close()
    print("Base de datos pyme.db creada exitosamente con datos de ventas detallados.")

if __name__ == "__main__":
    setup_db()
