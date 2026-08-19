from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "notes.db"


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
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            pinned INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------------
# Home
# -----------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Notes Management REST API",
        "version": "1.0",
        "status": "running"
    })


# -----------------------------------
# Create Note
# -----------------------------------

@app.route("/api/notes", methods=["POST"])
def create_note():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    content = data.get("content")
    category = data.get("category", "General")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    if not content:
        return jsonify({
            "error": "Content is required"
        }), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO notes
        (title, content, category, pinned, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        content,
        category,
        0,
        now,
        now
    ))

    connection.commit()

    note_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Note created successfully",
        "id": note_id
    }), 201


# -----------------------------------
# Get All Notes
# -----------------------------------

@app.route("/api/notes", methods=["GET"])
def get_notes():

    connection = get_db_connection()

    notes = connection.execute("""
        SELECT *
        FROM notes
        ORDER BY pinned DESC, updated_at DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(note)
        for note in notes
    ]), 200


# -----------------------------------
# Get Note by ID
# -----------------------------------

@app.route("/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):

    connection = get_db_connection()

    note = connection.execute("""
        SELECT *
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    connection.close()

    if note is None:
        return jsonify({
            "error": "Note not found"
        }), 404

    return jsonify(dict(note)), 200


# -----------------------------------
# Update Note
# -----------------------------------

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    connection = get_db_connection()

    note = connection.execute("""
        SELECT *
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    if note is None:
        connection.close()

        return jsonify({
            "error": "Note not found"
        }), 404

    title = data.get("title", note["title"])
    content = data.get("content", note["content"])
    category = data.get("category", note["category"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection.execute("""
        UPDATE notes
        SET title = ?,
            content = ?,
            category = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        title,
        content,
        category,
        now,
        note_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Note updated successfully"
    }), 200


# -----------------------------------
# Delete Note
# -----------------------------------

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):

    connection = get_db_connection()

    note = connection.execute("""
        SELECT id
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    if note is None:
        connection.close()

        return jsonify({
            "error": "Note not found"
        }), 404

    connection.execute("""
        DELETE FROM notes
        WHERE id = ?
    """, (note_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Note deleted successfully"
    }), 200


# -----------------------------------
# Search Notes
# -----------------------------------

@app.route("/api/notes/search", methods=["GET"])
def search_notes():

    query = request.args.get("q")

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    connection = get_db_connection()

    notes = connection.execute("""
        SELECT *
        FROM notes
        WHERE title LIKE ?
           OR content LIKE ?
           OR category LIKE ?
        ORDER BY updated_at DESC
    """, (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"
    )).fetchall()

    connection.close()

    return jsonify([
        dict(note)
        for note in notes
    ]), 200


# -----------------------------------
# Filter by Category
# -----------------------------------

@app.route("/api/notes/category/<category>", methods=["GET"])
def notes_by_category(category):

    connection = get_db_connection()

    notes = connection.execute("""
        SELECT *
        FROM notes
        WHERE LOWER(category) = LOWER(?)
        ORDER BY updated_at DESC
    """, (category,)).fetchall()

    connection.close()

    return jsonify([
        dict(note)
        for note in notes
    ]), 200


# -----------------------------------
# Pin / Unpin Note
# -----------------------------------

@app.route("/api/notes/<int:note_id>/pin", methods=["PATCH"])
def toggle_pin(note_id):

    connection = get_db_connection()

    note = connection.execute("""
        SELECT pinned
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    if note is None:
        connection.close()

        return jsonify({
            "error": "Note not found"
        }), 404

    new_status = 0 if note["pinned"] else 1

    connection.execute("""
        UPDATE notes
        SET pinned = ?
        WHERE id = ?
    """, (
        new_status,
        note_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Note pinned successfully"
        if new_status
        else "Note unpinned successfully",
        "pinned": bool(new_status)
    }), 200


# -----------------------------------
# Start Application
# -----------------------------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)