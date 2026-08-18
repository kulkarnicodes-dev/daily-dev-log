from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "inventory.db"
LOW_STOCK_LIMIT = 5


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# Get All Products
# --------------------------------

@app.route("/api/products", methods=["GET"])
def get_products():

    connection = get_db_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(product)
        for product in products
    ]), 200


# --------------------------------
# Get Product by ID
# --------------------------------

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    connection = get_db_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE id = ?
    """, (product_id,)).fetchone()

    connection.close()

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(dict(product)), 200


# --------------------------------
# Create Product
# --------------------------------

@app.route("/api/products", methods=["POST"])
def create_product():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    price = data.get("price")
    category = data.get("category")
    stock = data.get("stock")

    if not name or price is None or not category or stock is None:
        return jsonify({
            "error": "name, price, category and stock are required"
        }), 400

    try:
        price = float(price)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({
            "error": "price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if stock < 0:
        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO products (name, price, category, stock)
        VALUES (?, ?, ?, ?)
    """, (name, price, category, stock))

    connection.commit()

    product_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Product created successfully",
        "product_id": product_id,
        "product": {
            "name": name,
            "price": price,
            "category": category,
            "stock": stock
        }
    }), 201


# --------------------------------
# Update Product
# --------------------------------

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    connection = get_db_connection()

    product = connection.execute("""
        SELECT *
        FROM products
        WHERE id = ?
    """, (product_id,)).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    name = data.get("name", product["name"])
    price = data.get("price", product["price"])
    category = data.get("category", product["category"])
    stock = data.get("stock", product["stock"])

    if not name or not category:
        connection.close()

        return jsonify({
            "error": "name and category cannot be empty"
        }), 400

    try:
        price = float(price)
        stock = int(stock)
    except (ValueError, TypeError):
        connection.close()

        return jsonify({
            "error": "price must be a number and stock must be an integer"
        }), 400

    if price < 0:
        connection.close()

        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if stock < 0:
        connection.close()

        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    connection.execute("""
        UPDATE products
        SET name = ?,
            price = ?,
            category = ?,
            stock = ?
        WHERE id = ?
    """, (
        name,
        price,
        category,
        stock,
        product_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product updated successfully"
    }), 200


# --------------------------------
# Delete Product
# --------------------------------

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    connection = get_db_connection()

    product = connection.execute("""
        SELECT id
        FROM products
        WHERE id = ?
    """, (product_id,)).fetchone()

    if product is None:
        connection.close()

        return jsonify({
            "error": "Product not found"
        }), 404

    connection.execute("""
        DELETE FROM products
        WHERE id = ?
    """, (product_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


# --------------------------------
# Search Products
# --------------------------------

@app.route("/api/products/search", methods=["GET"])
def search_products():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    connection = get_db_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        WHERE name LIKE ?
           OR category LIKE ?
    """, (
        f"%{query}%",
        f"%{query}%"
    )).fetchall()

    connection.close()

    return jsonify([
        dict(product)
        for product in products
    ]), 200


# --------------------------------
# Filter by Category
# --------------------------------

@app.route("/api/products/category/<string:category>", methods=["GET"])
def products_by_category(category):

    connection = get_db_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        WHERE LOWER(category) = LOWER(?)
    """, (category,)).fetchall()

    connection.close()

    return jsonify([
        dict(product)
        for product in products
    ]), 200


# --------------------------------
# Low Stock Products
# --------------------------------

@app.route("/api/products/low-stock", methods=["GET"])
def low_stock_products():

    connection = get_db_connection()

    products = connection.execute("""
        SELECT *
        FROM products
        WHERE stock < ?
        ORDER BY stock ASC
    """, (LOW_STOCK_LIMIT,)).fetchall()

    connection.close()

    return jsonify({
        "low_stock_limit": LOW_STOCK_LIMIT,
        "count": len(products),
        "products": [
            dict(product)
            for product in products
        ]
    }), 200


# --------------------------------
# Inventory Summary
# --------------------------------

@app.route("/api/products/summary", methods=["GET"])
def inventory_summary():

    connection = get_db_connection()

    summary = connection.execute("""
        SELECT
            COUNT(*) AS total_products,
            COALESCE(SUM(stock), 0) AS total_stock,
            COALESCE(SUM(price * stock), 0) AS inventory_value
        FROM products
    """).fetchone()

    low_stock = connection.execute("""
        SELECT COUNT(*) AS count
        FROM products
        WHERE stock < ?
    """, (LOW_STOCK_LIMIT,)).fetchone()

    connection.close()

    return jsonify({
        "total_products": summary["total_products"],
        "total_stock": summary["total_stock"],
        "inventory_value": round(summary["inventory_value"], 2),
        "low_stock_products": low_stock["count"]
    }), 200


# --------------------------------
# Start Application
# --------------------------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)