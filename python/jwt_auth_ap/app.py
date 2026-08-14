from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3


app = Flask(__name__)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

DATABASE = "users.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


# -------------------------
# Register
# -------------------------

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
        SELECT id
        FROM users
        WHERE username = ? OR email = ?
        """,
        (username, email),
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
        (username, email, hashed_password),
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "User registered successfully",
        "user_id": user_id,
        "username": username,
        "email": email,
    }), 201


# -------------------------
# Login
# -------------------------

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
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,),
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

    access_token = create_access_token(
        identity=str(user["id"])
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        },
    }), 200


# -------------------------
# Protected Profile
# -------------------------

@app.route("/api/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "message": "Protected profile accessed successfully",
        "user": dict(user),
    }), 200


# -------------------------
# Get All Users
# -------------------------

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

    return jsonify([
        dict(user)
        for user in users
    ]), 200


# -------------------------
# Get User by ID
# -------------------------

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(dict(user)), 200


# -------------------------
# Delete User
# -------------------------

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        """,
        (user_id,),
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
        (user_id,),
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "User deleted successfully"
    }), 200


# -------------------------
# JWT Error Handlers
# -------------------------

@jwt.unauthorized_loader
def missing_token(error):
    return jsonify({
        "error": "Authorization token is required"
    }), 401


@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({
        "error": "Invalid authorization token"
    }), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({
        "error": "Authorization token has expired"
    }), 401


# -------------------------
# Start Application
# -------------------------

if __name__ == "__main__":
    init_database()

    app.run(
        debug=True
    )