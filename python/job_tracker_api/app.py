from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "job_tracker.db"


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
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            location TEXT DEFAULT 'Not specified',
            status TEXT DEFAULT 'Applied',
            job_type TEXT DEFAULT 'Full-time',
            applied_date TEXT NOT NULL,
            notes TEXT DEFAULT '',
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
        "message": "Job Application Tracker API",
        "version": "1.0",
        "status": "running"
    })


# -----------------------------------
# Create Application
# -----------------------------------

@app.route("/api/applications", methods=["POST"])
def create_application():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    company = data.get("company")
    position = data.get("position")
    location = data.get("location", "Not specified")
    status = data.get("status", "Applied")
    job_type = data.get("job_type", "Full-time")
    applied_date = data.get(
        "applied_date",
        datetime.now().strftime("%Y-%m-%d")
    )
    notes = data.get("notes", "")

    if not company:
        return jsonify({
            "error": "Company is required"
        }), 400

    if not position:
        return jsonify({
            "error": "Position is required"
        }), 400

    allowed_statuses = [
        "Applied",
        "Interview",
        "Selected",
        "Rejected",
        "Withdrawn"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO applications
        (
            company,
            position,
            location,
            status,
            job_type,
            applied_date,
            notes,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company,
        position,
        location,
        status,
        job_type,
        applied_date,
        notes,
        now,
        now
    ))

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Job application created successfully",
        "id": application_id
    }), 201


# -----------------------------------
# Get All Applications
# -----------------------------------

@app.route("/api/applications", methods=["GET"])
def get_applications():

    connection = get_db_connection()

    applications = connection.execute("""
        SELECT *
        FROM applications
        ORDER BY applied_date DESC
    """).fetchall()

    connection.close()

    return jsonify([
        dict(application)
        for application in applications
    ]), 200


# -----------------------------------
# Get Application by ID
# -----------------------------------

@app.route("/api/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):

    connection = get_db_connection()

    application = connection.execute("""
        SELECT *
        FROM applications
        WHERE id = ?
    """, (application_id,)).fetchone()

    connection.close()

    if application is None:
        return jsonify({
            "error": "Application not found"
        }), 404

    return jsonify(dict(application)), 200


# -----------------------------------
# Update Application
# -----------------------------------

@app.route("/api/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    connection = get_db_connection()

    application = connection.execute("""
        SELECT *
        FROM applications
        WHERE id = ?
    """, (application_id,)).fetchone()

    if application is None:
        connection.close()

        return jsonify({
            "error": "Application not found"
        }), 404

    company = data.get("company", application["company"])
    position = data.get("position", application["position"])
    location = data.get("location", application["location"])
    status = data.get("status", application["status"])
    job_type = data.get("job_type", application["job_type"])
    applied_date = data.get(
        "applied_date",
        application["applied_date"]
    )
    notes = data.get("notes", application["notes"])

    allowed_statuses = [
        "Applied",
        "Interview",
        "Selected",
        "Rejected",
        "Withdrawn"
    ]

    if status not in allowed_statuses:
        connection.close()

        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection.execute("""
        UPDATE applications
        SET company = ?,
            position = ?,
            location = ?,
            status = ?,
            job_type = ?,
            applied_date = ?,
            notes = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        company,
        position,
        location,
        status,
        job_type,
        applied_date,
        notes,
        now,
        application_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Job application updated successfully"
    }), 200


# -----------------------------------
# Delete Application
# -----------------------------------

@app.route("/api/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):

    connection = get_db_connection()

    application = connection.execute("""
        SELECT id
        FROM applications
        WHERE id = ?
    """, (application_id,)).fetchone()

    if application is None:
        connection.close()

        return jsonify({
            "error": "Application not found"
        }), 404

    connection.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Job application deleted successfully"
    }), 200


# -----------------------------------
# Filter by Status
# -----------------------------------

@app.route("/api/applications/status/<status>", methods=["GET"])
def filter_by_status(status):

    connection = get_db_connection()

    applications = connection.execute("""
        SELECT *
        FROM applications
        WHERE LOWER(status) = LOWER(?)
        ORDER BY applied_date DESC
    """, (status,)).fetchall()

    connection.close()

    return jsonify([
        dict(application)
        for application in applications
    ]), 200


# -----------------------------------
# Filter by Company
# -----------------------------------

@app.route("/api/applications/company/<company>", methods=["GET"])
def filter_by_company(company):

    connection = get_db_connection()

    applications = connection.execute("""
        SELECT *
        FROM applications
        WHERE LOWER(company) LIKE LOWER(?)
        ORDER BY applied_date DESC
    """, (f"%{company}%",)).fetchall()

    connection.close()

    return jsonify([
        dict(application)
        for application in applications
    ]), 200


# -----------------------------------
# Search Applications
# -----------------------------------

@app.route("/api/applications/search", methods=["GET"])
def search_applications():

    query = request.args.get("q")

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    connection = get_db_connection()

    applications = connection.execute("""
        SELECT *
        FROM applications
        WHERE company LIKE ?
           OR position LIKE ?
           OR location LIKE ?
           OR notes LIKE ?
        ORDER BY applied_date DESC
    """, (
        f"%{query}%",
        f"%{query}%",
        f"%{query}%",
        f"%{query}%"
    )).fetchall()

    connection.close()

    return jsonify([
        dict(application)
        for application in applications
    ]), 200


# -----------------------------------
# Application Statistics
# -----------------------------------

@app.route("/api/applications/summary", methods=["GET"])
def application_summary():

    connection = get_db_connection()

    total = connection.execute("""
        SELECT COUNT(*) AS count
        FROM applications
    """).fetchone()["count"]

    applied = connection.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Applied'
    """).fetchone()["count"]

    interviews = connection.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Interview'
    """).fetchone()["count"]

    selected = connection.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Selected'
    """).fetchone()["count"]

    rejected = connection.execute("""
        SELECT COUNT(*) AS count
        FROM applications
        WHERE status = 'Rejected'
    """).fetchone()["count"]

    connection.close()

    return jsonify({
        "total_applications": total,
        "applied": applied,
        "interviews": interviews,
        "selected": selected,
        "rejected": rejected
    }), 200


# -----------------------------------
# Start Application
# -----------------------------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)