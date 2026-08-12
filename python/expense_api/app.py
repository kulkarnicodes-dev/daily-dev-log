from flask import Flask, request, jsonify

app = Flask(__name__)

expenses = [
    {
        "id": 1,
        "title": "Lunch",
        "amount": 150,
        "category": "Food"
    },
    {
        "id": 2,
        "title": "Bus Ticket",
        "amount": 50,
        "category": "Transport"
    }
]


@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses)


@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = next(
        (expense for expense in expenses if expense["id"] == expense_id),
        None
    )

    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    return jsonify(expense)


@app.route("/api/expenses", methods=["POST"])
def add_expense():
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
    except (TypeError, ValueError):
        return jsonify({"error": "amount must be a number"}), 400

    new_expense = {
        "id": len(expenses) + 1,
        "title": title,
        "amount": amount,
        "category": category
    }

    expenses.append(new_expense)

    return jsonify(new_expense), 201


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = next(
        (expense for expense in expenses if expense["id"] == expense_id),
        None
    )

    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    expenses.remove(expense)

    return jsonify({
        "message": "Expense deleted successfully"
    })


@app.route("/api/expenses/summary", methods=["GET"])
def expense_summary():
    total = sum(expense["amount"] for expense in expenses)

    return jsonify({
        "total_expenses": total,
        "number_of_expenses": len(expenses)
    })


@app.route("/api/expenses/category/<string:category>", methods=["GET"])
def expenses_by_category(category):
    filtered_expenses = [
        expense
        for expense in expenses
        if expense["category"].lower() == category.lower()
    ]

    return jsonify(filtered_expenses)


if __name__ == "__main__":
    app.run(debug=True)