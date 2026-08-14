from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "users.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Register a new user
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "error": "username, email and password are required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": "Password must contain at least 6 characters"
        }), 400

    connection = get_db_connection()

    existing_user = connection.execute(
        """
        SELECT id FROM users
        WHERE username = ? OR email = ?
        """,
        (username, email)
    ).fetchone()

    if existing_user:
        connection.close()

        return jsonify({
            "error": "Username or email already exists"
        }), 409

    hashed_password = generate_password_hash(password)

    cursor = connection.execute(
        """
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """,
        (username, email, hashed_password)
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id,
        "username": username,
        "email": email
    }), 201


# Login user
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "email and password are required"
        }), 400

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not check_password_hash(user["password"], password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    })


# Get all users
@app.route("/api/users", methods=["GET"])
def get_users():
    connection = get_db_connection()

    users = connection.execute(
        """
        SELECT id, username, email
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return jsonify([dict(user) for user in users])


# Get user by ID
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(dict(user))


# Delete user
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    if user is None:
        connection.close()

        return jsonify({
            "error": "User not found"
        }), 404

    connection.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "User deleted successfully"
    })


if __name__ == "__main__":
    init_database()
    app.run(debug=True)