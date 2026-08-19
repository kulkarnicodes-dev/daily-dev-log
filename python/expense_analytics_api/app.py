from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "expenses.db"


# -----------------------------------
# Database Connection
# -----------------------------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------------
# Initialize Database
# -----------------------------------

def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------------
# Validate Date
# -----------------------------------

def validate_date(date_value):
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# -----------------------------------
# Home
# -----------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Expense Analytics REST API",
        "version": "1.0"
    })


# -----------------------------------
# Add Expense
# -----------------------------------

@app.route("/api/expenses", methods=["POST"])
def add_expense():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date")

    if not title or amount is None or not category or not date:
        return jsonify({
            "error": "title, amount, category and date are required"
        }), 400

    try:
        amount = float(amount)

        if amount <= 0:
            return jsonify({
                "error": "Amount must be greater than zero"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "error": "Amount must be a valid number"
        }), 400

    if not validate_date(date):
        return jsonify({
            "error": "Date must be in YYYY-MM-DD format"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO expenses
        (title, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (
        title,
        amount,
        category,
        date
    ))

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Expense added successfully",
        "id": expense_id
    }), 201


# -----------------------------------
# Get All Expenses
# -----------------------------------

@app.route("/api/expenses", methods=["GET"])
def get_expenses():

    connection = get_db_connection()

    expenses = connection.execute("""
        SELECT *
        FROM expenses
        ORDER BY date DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(expense)
        for expense in expenses
    ]), 200


# -----------------------------------
# Get Expense by ID
# -----------------------------------

@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):

    connection = get_db_connection()

    expense = connection.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
    """, (expense_id,)).fetchone()

    connection.close()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    return jsonify(dict(expense)), 200


# -----------------------------------
# Delete Expense
# -----------------------------------

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    connection = get_db_connection()

    expense = connection.execute("""
        SELECT id
        FROM expenses
        WHERE id = ?
    """, (expense_id,)).fetchone()

    if expense is None:
        connection.close()

        return jsonify({
            "error": "Expense not found"
        }), 404

    connection.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Expense deleted successfully"
    }), 200


# -----------------------------------
# Overall Summary
# -----------------------------------

@app.route("/api/analytics/summary", methods=["GET"])
def summary():

    connection = get_db_connection()

    result = connection.execute("""
        SELECT
            COUNT(*) AS total_transactions,
            COALESCE(SUM(amount), 0) AS total_spending,
            COALESCE(AVG(amount), 0) AS average_expense,
            COALESCE(MAX(amount), 0) AS highest_expense,
            COALESCE(MIN(amount), 0) AS lowest_expense
        FROM expenses
    """).fetchone()

    connection.close()

    return jsonify({
        "total_transactions": result["total_transactions"],
        "total_spending": round(result["total_spending"], 2),
        "average_expense": round(result["average_expense"], 2),
        "highest_expense": round(result["highest_expense"], 2),
        "lowest_expense": round(result["lowest_expense"], 2)
    }), 200


# -----------------------------------
# Category Analytics
# -----------------------------------

@app.route("/api/analytics/categories", methods=["GET"])
def category_analytics():

    connection = get_db_connection()

    results = connection.execute("""
        SELECT
            category,
            COUNT(*) AS transactions,
            SUM(amount) AS total_spending,
            AVG(amount) AS average_expense
        FROM expenses
        GROUP BY category
        ORDER BY total_spending DESC
    """).fetchall()

    connection.close()

    return jsonify([
        {
            "category": row["category"],
            "transactions": row["transactions"],
            "total_spending": round(row["total_spending"], 2),
            "average_expense": round(row["average_expense"], 2)
        }
        for row in results
    ]), 200


# -----------------------------------
# Monthly Analytics
# -----------------------------------

@app.route("/api/analytics/monthly", methods=["GET"])
def monthly_analytics():

    connection = get_db_connection()

    results = connection.execute("""
        SELECT
            substr(date, 1, 7) AS month,
            COUNT(*) AS transactions,
            SUM(amount) AS total_spending
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
    """).fetchall()

    connection.close()

    return jsonify([
        {
            "month": row["month"],
            "transactions": row["transactions"],
            "total_spending": round(row["total_spending"], 2)
        }
        for row in results
    ]), 200


# -----------------------------------
# Filter by Category
# -----------------------------------

@app.route("/api/expenses/category/<category>", methods=["GET"])
def expenses_by_category(category):

    connection = get_db_connection()

    expenses = connection.execute("""
        SELECT *
        FROM expenses
        WHERE LOWER(category) = LOWER(?)
        ORDER BY date DESC
    """, (category,)).fetchall()

    connection.close()

    return jsonify([
        dict(expense)
        for expense in expenses
    ]), 200


# -----------------------------------
# Start Application
# -----------------------------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)