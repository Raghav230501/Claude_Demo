from datetime import datetime

VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUSES = {"todo", "in_progress", "done"}


class TaskStore:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def get_all(self, status_filter=None):
        tasks = list(self._tasks.values())
        if status_filter:
            tasks = [t for t in tasks if t["status"] == status_filter]
        return tasks

    def get(self, task_id):
        return self._tasks.get(task_id)

    def create(self, title, priority="medium"):
        if not title or not isinstance(title, str):
            raise ValueError("title must be a non-empty string")
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
        task = {
            "id": self._next_id,
            "title": title,
            "priority": priority,
            "status": "todo",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def update(self, task_id, data):
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if "title" in data:
            task["title"] = data["title"]
        if "priority" in data:
            if data["priority"] not in VALID_PRIORITIES:
                raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
            task["priority"] = data["priority"]
        if "status" in data:
            if data["status"] not in VALID_STATUSES:
                raise ValueError(f"status must be one of {VALID_STATUSES}")
            task["status"] = data["status"]

        task["updated_at"] = datetime.utcnow().isoformat()
        return task

    def delete(self, task_id):
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def stats(self):
        tasks = list(self._tasks.values())
        done = sum(1 for t in tasks if t["status"] == "done")
        completion_rate = (done / len(tasks) * 100) if tasks else 0.0
        return {"total": len(tasks), "done": done, "completion_rate": completion_rate}
