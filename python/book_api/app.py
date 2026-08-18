from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "books.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            year INTEGER
        )
    """)

    connection.commit()
    connection.close()


# --------------------------------
# Get All Books
# --------------------------------

@app.route("/api/books", methods=["GET"])
def get_books():

    connection = get_db_connection()

    books = connection.execute("""
        SELECT *
        FROM books
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(book)
        for book in books
    ]), 200


# --------------------------------
# Get Book by ID
# --------------------------------

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    connection = get_db_connection()

    book = connection.execute("""
        SELECT *
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    connection.close()

    if book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    return jsonify(dict(book)), 200


# --------------------------------
# Create Book
# --------------------------------

@app.route("/api/books", methods=["POST"])
def create_book():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    author = data.get("author")
    category = data.get("category")
    year = data.get("year")

    if not title or not author or not category:
        return jsonify({
            "error": "title, author and category are required"
        }), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO books (title, author, category, year)
        VALUES (?, ?, ?, ?)
    """, (title, author, category, year))

    connection.commit()

    book_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Book created successfully",
        "book_id": book_id,
        "book": {
            "title": title,
            "author": author,
            "category": category,
            "year": year
        }
    }), 201


# --------------------------------
# Update Book
# --------------------------------

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    connection = get_db_connection()

    book = connection.execute("""
        SELECT *
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    if book is None:
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    title = data.get("title", book["title"])
    author = data.get("author", book["author"])
    category = data.get("category", book["category"])
    year = data.get("year", book["year"])

    if not title or not author or not category:
        connection.close()

        return jsonify({
            "error": "title, author and category cannot be empty"
        }), 400

    connection.execute("""
        UPDATE books
        SET title = ?,
            author = ?,
            category = ?,
            year = ?
        WHERE id = ?
    """, (
        title,
        author,
        category,
        year,
        book_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book updated successfully"
    }), 200


# --------------------------------
# Delete Book
# --------------------------------

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    connection = get_db_connection()

    book = connection.execute("""
        SELECT id
        FROM books
        WHERE id = ?
    """, (book_id,)).fetchone()

    if book is None:
        connection.close()

        return jsonify({
            "error": "Book not found"
        }), 404

    connection.execute("""
        DELETE FROM books
        WHERE id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Book deleted successfully"
    }), 200


# --------------------------------
# Search Books
# --------------------------------

@app.route("/api/books/search", methods=["GET"])
def search_books():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    connection = get_db_connection()

    books = connection.execute("""
        SELECT *
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
    """, (
        f"%{query}%",
        f"%{query}%"
    )).fetchall()

    connection.close()

    return jsonify([
        dict(book)
        for book in books
    ]), 200


# --------------------------------
# Filter by Category
# --------------------------------

@app.route("/api/books/category/<string:category>", methods=["GET"])
def books_by_category(category):

    connection = get_db_connection()

    books = connection.execute("""
        SELECT *
        FROM books
        WHERE LOWER(category) = LOWER(?)
    """, (category,)).fetchall()

    connection.close()

    return jsonify([
        dict(book)
        for book in books
    ]), 200


# --------------------------------
# Start Application
# --------------------------------

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True
    )