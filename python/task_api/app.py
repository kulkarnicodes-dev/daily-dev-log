from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Python", "completed": True},
    {"id": 2, "title": "Build REST API", "completed": False},
]


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False,
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks

    task = next((task for task in tasks if task["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks = [task for task in tasks if task["id"] != task_id]

    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)