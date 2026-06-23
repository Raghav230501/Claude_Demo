from flask import Flask, request, jsonify
from tasks import TaskStore

app = Flask(__name__)
store = TaskStore()


@app.route("/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    tasks = store.get_all(status_filter=status)
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: title"}), 400
    try:
        task = store.create(data["title"], data.get("priority", "medium"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = store.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        task = store.update(task_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    success = store.delete(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=False)
