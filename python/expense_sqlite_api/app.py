from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "expenses.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Get all expenses
@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    connection = get_db_connection()

    expenses = connection.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return jsonify([dict(expense) for expense in expenses])


# Get expense by ID
@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    connection = get_db_connection()

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    connection.close()

    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify(dict(expense))


# Create expense
@app.route("/api/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    amount = data.get("amount")
    category = data.get("category")

    if not title or amount is None or not category:
        return jsonify({
            "error": "title, amount and category are required"
        }), 400

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({
            "error": "amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "amount must be greater than zero"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO expenses (title, amount, category)
        VALUES (?, ?, ?)
        """,
        (title, amount, category)
    )

    connection.commit()

    expense_id = cursor.lastrowid

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(expense)), 201


# Update expense
@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    amount = data.get("amount")
    category = data.get("category")

    if not title or amount is None or not category:
        return jsonify({
            "error": "title, amount and category are required"
        }), 400

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({
            "error": "amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "amount must be greater than zero"
        }), 400

    connection = get_db_connection()

    existing_expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    if existing_expense is None:
        connection.close()
        return jsonify({"error": "Expense not found"}), 404

    connection.execute(
        """
        UPDATE expenses
        SET title = ?, amount = ?, category = ?
        WHERE id = ?
        """,
        (title, amount, category, expense_id)
    )

    connection.commit()

    updated_expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(updated_expense))


# Delete expense
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    connection = get_db_connection()

    expense = connection.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    if expense is None:
        connection.close()
        return jsonify({"error": "Expense not found"}), 404

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Expense deleted successfully"
    })


# Filter expenses by category
@app.route("/api/expenses/category/<string:category>", methods=["GET"])
def get_expenses_by_category(category):
    connection = get_db_connection()

    expenses = connection.execute(
        """
        SELECT * FROM expenses
        WHERE LOWER(category) = LOWER(?)
        ORDER BY id DESC
        """,
        (category,)
    ).fetchall()

    connection.close()

    return jsonify([dict(expense) for expense in expenses])


# Expense summary
@app.route("/api/expenses/summary", methods=["GET"])
def get_summary():
    connection = get_db_connection()

    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS number_of_expenses,
            COALESCE(SUM(amount), 0) AS total_expenses
        FROM expenses
        """
    ).fetchone()

    connection.close()

    return jsonify({
        "total_expenses": summary["total_expenses"],
        "number_of_expenses": summary["number_of_expenses"]
    })


if __name__ == "__main__":
    init_database()
    app.run(debug=True)