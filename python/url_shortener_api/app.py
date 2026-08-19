from flask import Flask, jsonify, request, redirect
import sqlite3
import secrets
import string
from urllib.parse import urlparse

app = Flask(__name__)

DATABASE = "urls.db"


# -------------------------------
# Database Connection
# -------------------------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# -------------------------------
# Initialize Database
# -------------------------------

def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -------------------------------
# URL Validation
# -------------------------------

def is_valid_url(url):
    try:
        parsed = urlparse(url)

        return parsed.scheme in ["http", "https"] and bool(parsed.netloc)

    except Exception:
        return False


# -------------------------------
# Generate Short Code
# -------------------------------

def generate_short_code(length=6):

    characters = string.ascii_letters + string.digits

    while True:
        code = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        connection = get_db_connection()

        existing = connection.execute("""
            SELECT id
            FROM urls
            WHERE short_code = ?
        """, (code,)).fetchone()

        connection.close()

        if existing is None:
            return code


# -------------------------------
# Get All URLs
# -------------------------------

@app.route("/api/urls", methods=["GET"])
def get_urls():

    connection = get_db_connection()

    urls = connection.execute("""
        SELECT *
        FROM urls
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(url)
        for url in urls
    ]), 200


# -------------------------------
# Create Short URL
# -------------------------------

@app.route("/api/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    original_url = data.get("url")

    if not original_url:
        return jsonify({
            "error": "URL is required"
        }), 400

    if not is_valid_url(original_url):
        return jsonify({
            "error": "Invalid URL. Use http:// or https://"
        }), 400

    short_code = generate_short_code()

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO urls (original_url, short_code)
        VALUES (?, ?)
    """, (
        original_url,
        short_code
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "URL shortened successfully",
        "original_url": original_url,
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:5000/{short_code}"
    }), 201


# -------------------------------
# Get URL by ID
# -------------------------------

@app.route("/api/urls/<int:url_id>", methods=["GET"])
def get_url(url_id):

    connection = get_db_connection()

    url = connection.execute("""
        SELECT *
        FROM urls
        WHERE id = ?
    """, (url_id,)).fetchone()

    connection.close()

    if url is None:
        return jsonify({
            "error": "URL not found"
        }), 404

    return jsonify(dict(url)), 200


# -------------------------------
# Redirect Short URL
# -------------------------------

@app.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code):

    connection = get_db_connection()

    url = connection.execute("""
        SELECT original_url
        FROM urls
        WHERE short_code = ?
    """, (short_code,)).fetchone()

    connection.close()

    if url is None:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    return redirect(url["original_url"])


# -------------------------------
# Delete URL
# -------------------------------

@app.route("/api/urls/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):

    connection = get_db_connection()

    url = connection.execute("""
        SELECT id
        FROM urls
        WHERE id = ?
    """, (url_id,)).fetchone()

    if url is None:
        connection.close()

        return jsonify({
            "error": "URL not found"
        }), 404

    connection.execute("""
        DELETE FROM urls
        WHERE id = ?
    """, (url_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "URL deleted successfully"
    }), 200


# -------------------------------
# Start Application
# -------------------------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)